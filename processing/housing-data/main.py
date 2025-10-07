import polars as pl
from redfin import RedfinProcessor
from zillow import ZillowProcessor
import os
STATE_MAP = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}


print("Running Redfin Processor...")
redfin_df = RedfinProcessor().create_data()

print("Running Zillow Processor...")
zillow_df = ZillowProcessor().create_data()

# Inspect Zillow data before normalization
print("\n🔍 Inspecting Zillow raw data (before cleaning)...")
print(zillow_df.head(10))

# Find rows with missing City/State/YEAR but non-null avg_price
bad_rows = zillow_df.filter(
    (pl.col("City").is_null() | (pl.col("City") == "")) &
    (pl.col("State").is_null() | (pl.col("State") == "")) &
    pl.col("avg_price").is_not_null()
)
print(f"\n⚠️ Found {bad_rows.shape[0]} rows with empty City/State but avg_price present.")
print(bad_rows.head(20))


# === Normalize column names ===
redfin_df = redfin_df.rename({"CITY": "City", "STATE": "State"})


def normalize(df: pl.DataFrame, is_redfin: bool = False) -> pl.DataFrame:
    # Map full state names to abbreviations (for Redfin)
    state_expr = (
        pl.col("State")
        .map_elements(lambda s: STATE_MAP.get(s.strip().title(), s.strip().upper()) if s else None, return_dtype=pl.Utf8)
    ) if is_redfin else (
        pl.col("State").str.strip_chars().str.strip_chars(" ").str.to_uppercase()
    )

    return (
        df.with_columns([
            pl.col("City")
              .cast(pl.Utf8)
              .str.strip_chars()
              .str.strip_chars(" ")
              .str.to_titlecase()
              .alias("City"),
            state_expr.alias("State"),
            pl.col("YEAR").cast(pl.Int32),
            pl.col("avg_price").cast(pl.Float64),
            pl.col("zip_count").cast(pl.Int32),
        ])
        .filter(
            pl.col("City").is_not_null() & (pl.col("City") != "") &
            pl.col("State").is_not_null() & (pl.col("State") != "") &
            pl.col("YEAR").is_not_null()
        )
    )


redfin_df = normalize(redfin_df, is_redfin=True)
zillow_df = normalize(zillow_df, is_redfin=False)

print(f"✅ Redfin: {redfin_df.shape[0]:,} rows")
print(f"✅ Zillow: {zillow_df.shape[0]:,} rows")

print("\n🔍 Checking for blanks BEFORE join...")
for name, df in [("Redfin", redfin_df), ("Zillow", zillow_df)]:
    if df is not None:
        blanks = df.filter(
            (pl.col("City").is_null() | (pl.col("City") == "")) |
            (pl.col("State").is_null() | (pl.col("State") == "")) |
            (pl.col("YEAR").is_null())
        )
        print(f"⚠️ {name} blank rows: {blanks.shape[0]:,}")


# === Full outer join ===
print("Joining datasets on City, State, YEAR (full join)...")
merged = redfin_df.join(
    zillow_df,
    on=["City", "State", "YEAR"],
    how="full",
    suffix="_zillow",
)

print(f"✅ After join: {merged.shape[0]:,} rows")

# === Coalesce columns so nulls are filled from Zillow side ===
merged = merged.with_columns([
    pl.coalesce([pl.col("City"), pl.col("City_zillow")]).alias("City"),
    pl.coalesce([pl.col("State"), pl.col("State_zillow")]).alias("State"),
    pl.coalesce([pl.col("YEAR"), pl.col("YEAR_zillow")]).alias("YEAR"),
])

# === Drop duplicate columns now that coalesce filled them ===
merged = merged.drop(["City_zillow", "State_zillow", "YEAR_zillow"])

# === Check for blanks again ===
missing = merged.filter(
    (pl.col("City").is_null() | (pl.col("City") == "")) |
    (pl.col("State").is_null() | (pl.col("State") == "")) |
    (pl.col("YEAR").is_null())
)

print(f"⚠️ Empty City/State/YEAR rows after coalesce: {missing.shape[0]:,}")
if missing.shape[0] > 0:
    print(missing.head(10))



print(f"✅ After join: {merged.shape[0]:,} rows")


# === Resolve overlap ===
result = (
    merged
    .with_columns([
        # Pick final price based on zip_count
        pl.when(pl.col("avg_price").is_not_null() & pl.col("avg_price_zillow").is_not_null())
          .then(
              pl.when(pl.col("zip_count") > pl.col("zip_count_zillow"))
               .then(pl.col("avg_price"))
               .when(pl.col("zip_count") < pl.col("zip_count_zillow"))
               .then(pl.col("avg_price_zillow"))
               .otherwise((pl.col("avg_price") + pl.col("avg_price_zillow")) / 2)
          )
          .otherwise(pl.coalesce([pl.col("avg_price"), pl.col("avg_price_zillow")]))
          .alias("avg_price_final"),

        # Highest zip_count between both
        pl.when(pl.col("zip_count").is_not_null() & pl.col("zip_count_zillow").is_not_null())
          .then(pl.max_horizontal("zip_count", "zip_count_zillow"))
          .otherwise(pl.coalesce([pl.col("zip_count"), pl.col("zip_count_zillow")]))
          .alias("zip_count_final"),
    ])
    .select(["City", "State", "YEAR", "avg_price_final", "zip_count_final"])
    .rename({"avg_price_final": "avg_price", "zip_count_final": "zip_count"})
    .sort(["State", "City", "YEAR"])
)

# === Save ===
# Create processed-data directory if it doesn't exist
os.makedirs("../../processed-data/housing-data", exist_ok=True)

output_path = "../../processed-data/housing-data/housing_prices_city_aggregated.csv"
result = result.unique(["City", "State", "YEAR"])

result.write_csv(output_path)
print(f"✅ Saved combined dataset to {output_path}")
print(f"✅ Final row count: {result.shape[0]:,}")
print(result.head(10))

# Quick diagnostics
print("Unique City-State-Year combos:")
print(f"Redfin: {redfin_df.select(pl.count()).item()} rows")
print(f"Zillow: {zillow_df.select(pl.count()).item()} rows")
print(f"Merged: {merged.select(pl.count()).item()} rows")
