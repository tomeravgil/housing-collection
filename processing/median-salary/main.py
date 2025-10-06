import pandas as pd
import requests
import os
from tqdm import tqdm

# Directory to save results
data_dir = "/Users/elizabeth/Downloads/data_salary/housing-collection/processed-data/median-salary"
os.makedirs(data_dir, exist_ok=True)

# Years to download
years = range(2010, 2024)

# Variable for median household income
var = "S1901_C01_012E"

# Base URL pattern (ACS 1-Year Subject Tables)
base_url = "https://api.census.gov/data/{year}/acs/acs1/subject"

all_dfs = []

for year in tqdm(years, desc="Downloading ACS data"):
    params = {
        "get": f"NAME,{var}",
        "for": "place:*"  # use 'state:*' for state-level instead
    }

    url = base_url.format(year=year)
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        data = r.json()

        # First row is headers
        cols = data[0]
        df = pd.DataFrame(data[1:], columns=cols)
        df[var] = pd.to_numeric(df[var], errors="coerce")
        df["Year"] = year

        all_dfs.append(df)

    except Exception as e:
        print(f"Error downloading {year}: {e}")

# Combine all years
combined_df = pd.concat(all_dfs, ignore_index=True)

# Split NAME into City and State
city_state = combined_df["NAME"].str.split(",", n=1, expand=True)
combined_df["City"] = city_state[0].str.strip()
combined_df["State"] = city_state[1].str.strip()

# Clean up and reorder
combined_df = combined_df[["City", "State", "Year", var]]
combined_df = combined_df.rename(columns={var: "Median_Income"})

# Save combined data
out_path = os.path.join(data_dir, "acs1y_s1901_median_income_2010_2023.csv")
combined_df.to_csv(out_path, index=False)

