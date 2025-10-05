import polars as pl
from pathlib import Path
import tempfile
import zipfile
import gzip
import urllib.request
import shutil
import os
from processor import Processor

class RedfinProcessor(Processor):
    def __init__(self, cache_path="redfin_cached_city_year.csv"):
        super().__init__()
        self.temp_dir = None
        self.zipmap = None
        self.redfin_df = None
        self.cache_path = Path(cache_path)

    def grab_data(self):
        """Downloads and loads both Redfin ZIP-level and SimpleMaps ZIP mapping data."""
        self.temp_dir = Path(tempfile.mkdtemp())

        # === 1. Download Redfin ZIP Market Tracker ===
        redfin_url = "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/zip_code_market_tracker.tsv000.gz"
        redfin_gz_path = self.temp_dir / "zip_code_market_tracker.tsv000.gz"
        redfin_tsv_path = self.temp_dir / "zip_code_market_tracker.tsv000"

        print("⬇️ Downloading Redfin ZIP Market Tracker...")
        req = urllib.request.Request(
            redfin_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/119.0.0.0 Safari/537.36"
                )
            },
        )
        with urllib.request.urlopen(req) as response, open(redfin_gz_path, "wb") as out_file:
            out_file.write(response.read())
        print(f"✅ Downloaded → {redfin_gz_path}")

        print("🧩 Decompressing Redfin TSV...")
        with gzip.open(redfin_gz_path, "rb") as f_in, open(redfin_tsv_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"✅ Decompressed → {redfin_tsv_path}")

        # === 2. Load Redfin data ===
        print("📖 Reading Redfin TSV (lazy mode)...")
        self.redfin_df = (
            pl.scan_csv(
                redfin_tsv_path,
                separator="\t",
                null_values=["", "NA", "NaN"],
                ignore_errors=True,
                infer_schema_length=10000,
            )
            .select(["REGION", "STATE", "REGION_TYPE", "PERIOD_END", "MEDIAN_SALE_PRICE"])
            .filter(pl.col("REGION_TYPE").str.to_lowercase() == "zip code")
            .with_columns([
                pl.col("REGION")
                .cast(pl.Utf8)
                .str.replace_all(r"(?i)zip code:\s*", "")
                .str.replace_all(r"\.0$", "")
                .str.strip_chars()
                .str.zfill(5)
                .alias("ZIP"),
                pl.col("PERIOD_END").str.slice(0, 4).alias("YEAR"),
                pl.col("MEDIAN_SALE_PRICE").cast(pl.Float64),
            ])
            .collect()
        )
        print(f"✅ Loaded Redfin data with {self.redfin_df.shape[0]:,} rows.")

        # === 3. Download SimpleMaps ZIP dataset ===
        print("⬇️ Downloading SimpleMaps ZIP dataset...")
        simplemaps_url = "https://simplemaps.com/static/data/us-zips/1.911/basic/simplemaps_uszips_basicv1.911.zip"
        zip_path = self.temp_dir / "uszips.zip"

        req = urllib.request.Request(
            simplemaps_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/119.0.0.0 Safari/537.36"
                )
            },
        )
        with urllib.request.urlopen(req) as response, open(zip_path, "wb") as out_file:
            out_file.write(response.read())

        print("🧩 Extracting SimpleMaps ZIP...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.temp_dir)

        zipmap_path = next(self.temp_dir.glob("**/uszips.csv"), None)
        if not zipmap_path:
            raise FileNotFoundError("Could not find 'uszips.csv' inside extracted ZIP directory.")
        print(f"✅ Found ZIP mapping → {zipmap_path}")

        # === 4. Load SimpleMaps Data ===
        self.zipmap = (
            pl.read_csv(
                zipmap_path,
                columns=["zip", "city", "state_name", "state_id", "county_name"],
            )
            .with_columns(
                pl.col("zip").cast(pl.Utf8).str.strip_chars().str.zfill(5),
                pl.col("city").str.to_titlecase(),
            )
        )
        print(f"✅ Loaded SimpleMaps ZIP mapping ({self.zipmap.shape[0]:,} rows).")

    def process(self):
        """Merges Redfin and ZIP mapping data, aggregates to city-level."""
        print("🔗 Merging Redfin ZIPs with SimpleMaps cities...")
        merged = self.redfin_df.join(self.zipmap, left_on="ZIP", right_on="zip", how="left")

        merged = merged.select([
            "ZIP",
            pl.col("city").alias("CITY"),
            pl.col("state_name").alias("STATE"),
            pl.col("state_id").alias("STATE_CODE"),
            pl.col("county_name").alias("COUNTY"),
            "YEAR",
            "MEDIAN_SALE_PRICE",
        ])

        merged = merged.filter(
            pl.col("CITY").is_not_null() &
            (pl.col("CITY") != "") &
            pl.col("STATE").is_not_null() &
            (pl.col("STATE") != "")
        )

        print(f"✅ Cleaned merged dataset: {merged.shape[0]:,} rows.")
        print("📊 Aggregating by CITY, STATE, YEAR...")
        city_agg = (
            merged.group_by(["CITY", "STATE", "YEAR"])
            .agg([
                pl.col("MEDIAN_SALE_PRICE").mean().alias("avg_price"),
                pl.count("ZIP").alias("zip_count"),
            ])
            .sort(["STATE", "CITY", "YEAR"])
        )

        self.data = city_agg
        print(f"✅ Created city-level aggregated DataFrame ({self.data.shape[0]:,} rows).")

        # Cache for reuse
        print(f"💾 Saving cached copy → {self.cache_path}")
        self.data.write_csv(self.cache_path)

        # Cleanup
        print("🧹 Cleaning up temporary files...")
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        print("✅ Temp files cleaned up.")
        return self.data

    def create_data(self):
        """Use cached data if available."""
        if self.cache_path.exists():
            print(f"⚡ Using cached Redfin data from {self.cache_path}")
            self.data = pl.read_csv(self.cache_path)
            print(f"✅ Loaded cached Redfin data ({self.data.shape[0]:,} rows).")
            return self.data

        print("🚀 Cache not found — generating new Redfin dataset...")
        self.grab_data()
        self.process()
        return self.data
