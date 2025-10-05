import requests
import pandas as pd
from io import StringIO

FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"

def fetch_fred_series(series_id: str):
    """Fetch a FRED time series as a DataFrame(year, value)."""
    url = FRED_CSV_URL.format(series_id=series_id)
    resp = requests.get(url, allow_redirects=True)

    if not resp.ok:
        raise ValueError(f"❌ Request failed for {series_id}: {resp.status_code}")
    text = resp.text.strip()

    # Detect if FRED returned HTML instead of CSV
    if text.startswith("<") or "DOCTYPE html" in text:
        raise ValueError(f"❌ FRED returned HTML for {series_id} (likely invalid ID or redirect)")

    df = pd.read_csv(StringIO(text))
    if df.empty:
        raise ValueError(f"❌ Empty CSV for {series_id}")

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Detect date column
    date_col = None
    for possible in ["date", "observation_date", "time"]:
        if possible in df.columns:
            date_col = possible
            break

    if not date_col:
        raise ValueError(f"❌ No date column found in CSV for {series_id}. Columns: {df.columns}")

    # Identify the value column (the other one)
    value_col = [c for c in df.columns if c != date_col][0]

    # Parse year and rename columns
    df["year"] = pd.to_datetime(df[date_col]).dt.year
    df = df.rename(columns={value_col: "value"})[["year", "value"]]
    df = df.dropna(subset=["value"])
    print(f"✅ Loaded {len(df)} rows for {series_id}")
    return df


def main():
    # Choose FRED series
    # PCEC96 = Real Personal Consumption Expenditures (chained 2017 dollars)
    # PCE = Nominal Personal Consumption Expenditures
    series_ids = {
        "real_consumer_spending": "PCEC96",
        "nominal_consumer_spending": "PCE"
    }

    combined = None
    for col_name, sid in series_ids.items():
        try:
            df = fetch_fred_series(sid)
            # Aggregate monthly to yearly average
            df = df.groupby("year", as_index=False).mean()
            df.rename(columns={"value": col_name}, inplace=True)

            if combined is None:
                combined = df
            else:
                combined = pd.merge(combined, df, on="year", how="outer")

        except ValueError as e:
            print(e)

    if combined is not None and not combined.empty:
        combined.to_csv("us_consumer_spending.csv", index=False)
        print("✅ Saved us_consumer_spending.csv")
        print(combined.head(10))
    else:
        print("❌ No valid data saved")


if __name__ == "__main__":
    main()
