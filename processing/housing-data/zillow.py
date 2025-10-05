import polars as pl
from pathlib import Path
import requests
import tempfile
import os
from processor import Processor

class ZillowProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.data = None
        self.temp_file = None

    def grab_data(self):
        url = "https://files.zillowstatic.com/research/public_csvs/zhvi/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
        temp_dir = tempfile.gettempdir()
        self.temp_file = Path(temp_dir) / "zillow_raw.csv"

        print("Downloading Zillow data...")
        response = requests.get(url)
        response.raise_for_status()
        with open(self.temp_file, "wb") as f:
            f.write(response.content)
        print(f"Download complete → {self.temp_file}")

        print("Reading CSV into Polars...")
        self.data = pl.read_csv(self.temp_file, ignore_errors=True)

    def process(self):
        print("Processing Zillow data...")

        # Identify date columns (those starting with 4 digits)
        date_cols = [c for c in self.data.columns if c[:4].isdigit()]
        if not date_cols:
            raise ValueError("❌ Could not identify date columns — check the Zillow CSV headers!")

        # Melt the dataframe (wide → long format)
        melted = (
            self.data.melt(
                id_vars=["RegionName", "City", "State"],
                value_vars=date_cols,
                variable_name="Date",
                value_name="ZHVI"
            )
            .with_columns([
                # Extract year from the first 4 characters of the column name
                pl.col("Date").str.extract(r"(\d{4})").cast(pl.Int32).alias("YEAR"),
                pl.col("ZHVI").cast(pl.Float64),
                # Normalize text fields (strip spaces, lowercase "nan")
                pl.col("City").cast(pl.Utf8).str.strip_chars().alias("City"),
                pl.col("State").cast(pl.Utf8).str.strip_chars().alias("State"),
            ])
            # Filter invalid entries (City, State, YEAR)
            .filter(
                (pl.col("City").is_not_null()) &
                (pl.col("City").str.strip_chars() != "") &
                (~pl.col("City").str.to_lowercase().is_in(["nan", "none"])) &
                (pl.col("State").is_not_null()) &
                (pl.col("State").str.strip_chars() != "") &
                (~pl.col("State").str.to_lowercase().is_in(["nan", "none"])) &
                (pl.col("YEAR").is_not_null()) &
                (pl.col("YEAR") > 1900)
            )
        )

        print(f"✅ Zillow valid rows after cleaning: {melted.shape[0]:,}")

        # Average across ZIPs within city per year
        city_year_avg = (
            melted
            .filter(pl.col("ZHVI").is_not_null())
            .group_by(["City", "State", "YEAR"])
            .agg([
                pl.col("ZHVI").mean().alias("avg_price"),
                pl.count("RegionName").alias("zip_count"),
            ])
            .filter(pl.col("avg_price").is_not_null())
            .sort(["State", "City", "YEAR"])
        )

        self.data = city_year_avg
        print(f"✅ Created Zillow DataFrame ({self.data.shape[0]:,} rows).")
        os.remove(self.temp_file)
        return self.data
