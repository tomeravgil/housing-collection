# 🏠 Housing Prices Aggregated Dataset

This dataset provides aggregated U.S. housing price information compiled from Redfin ZIP-level market tracker data and merged with ZIP–City mapping from the SimpleMaps `uszips.csv` database.  
It summarizes housing prices at the **city–state–year** level, showing the average home price and number of ZIP codes contributing to that average.

---

## 📘 Dataset Overview

- **File name:** `housing_prices_city_aggregated.csv`
- **Format:** CSV (comma-separated values)
- **Records:** One record per `{city, state, year}`
- **Columns:**
  - `CITY` – City name
  - `STATE` – State full name
  - `YEAR` – Year of the aggregated record
  - `avg_price` – Mean median sale price across ZIPs in that city
  - `zip_count` – Number of ZIP codes contributing to the average

---

## 🧩 Source Information

- **Raw Data:** [Redfin Data Center](https://www.redfin.com/news/data-center/)  
  (`zip_code_market_tracker.tsv`)
- **ZIP–City Crosswalk:** [SimpleMaps US ZIP Database (Free)](https://simplemaps.com/data/us-zips)

All derived datasets are publicly reproducible.

---

## 🗃️ Data Management & Preservation

1. **Physical Storage:**
   - Raw Redfin TSV files and intermediate datasets (`zip_city_year.csv`) are preserved in the `/data/raw/` folder.
   - Processed and aggregated datasets are stored in `/data/processed/`.
   - Backups are maintained in both local storage and an institutional repository (if available).

2. **Version Control:**
   - All scripts and datasets are tracked using Git/GitHub.
   - Changes to processing scripts or derived data are versioned with commit history for reproducibility.

3. **Formats & Standards:**
   - CSV and JSON formats are used to ensure long-term accessibility.
   - Date fields use ISO 8601 standard (`YYYY`).
   - States use USPS and FIPS-compliant abbreviations.
   - Character encoding: UTF-8.

4. **Interoperability:**
   - Fully compatible with Python (`pandas`, `polars`), R (`tidyverse`), and SQL.
   - Designed for integration into data visualization tools like Tableau, Power BI, or Observable.

5. **Security:**
   - All data is public and non-sensitive.
   - Authentication credentials (if used for APIs or scraping) are stored in `.env` files and excluded from version control.

6. **Persistence:**
   - Final CSV files and accompanying metadata JSONs will be deposited in a long-term repository (e.g., RPI Institutional Repository or Zenodo).
   - Persistent identifiers (e.g., DOI) will be assigned upon publication.

---

## 🔐 Data Ownership

- **Raw Data Ownership:**  
  Redfin and SimpleMaps retain ownership of the original datasets per their terms of use.
  
- **Derived Dataset Ownership:**  
  The cleaned and aggregated dataset is owned by the researcher (Tomer Avgil) and can be shared or cited with attribution: