# 💰 U.S. Median Household Income Dataset

This dataset provides aggregated U.S. median household income information compiled from the U.S. Census Bureau's American Community Survey (ACS) 1-Year Subject Tables.  
It summarizes median household income at the **city–state–year** level for analysis of economic trends and cost of living comparisons.

---

## 📘 Dataset Overview

- **File name:** `acs1y_s1901_median_income_2010_2023.csv`
- **Format:** CSV (comma-separated values)
- **Records:** One record per `{city, state, year}`
- **Columns:**
  - `City` – City name
  - `State` – State full name
  - `Year` – Year of the record (YYYY)
  - `Median_Income` – Estimated median household income in USD

---

## 🧩 Source Information

- **Raw Data:** [U.S. Census Bureau - American Community Survey](https://data.census.gov/)  
  (ACS 1-Year Subject Tables - S1901_C01_012E)
- **API Base URL:** `https://api.census.gov/data/{year}/acs/acs1/subject`
- **Variable Used:** `S1901_C01_012E` (Median household income in the past 12 months)
- **Geographic Level:** Place (city-level data)
- **Years Covered:** 2010-2023 (excluding 2020)

**Note:** 2020 data is unavailable because the Census Bureau did not release ACS 1-Year estimates for that year due to COVID-19 data collection disruptions.

All derived datasets are publicly reproducible.

---

## 🎯 Purpose & Use Cases

This dataset is designed for:

1. **Economic Analysis:** Track median household income trends across U.S. cities over time
2. **Cost of Living Studies:** Compare income levels with housing prices and consumer spending
3. **Regional Comparisons:** Analyze income disparities between cities and states
4. **Policy Research:** Support evidence-based policy decisions on economic development
5. **Data Visualization:** Create interactive dashboards and time-series visualizations

---

## 🗃️ Data Management & Preservation

1. **Physical Storage:**
   - Raw API responses are fetched programmatically and not stored locally
   - Processed and aggregated datasets are stored in `/processed-data/median-salary/`
   - Backups are maintained in both local storage and GitHub repository

2. **Version Control:**
   - All scripts and datasets are tracked using Git/GitHub
   - Changes to processing scripts or derived data are versioned with commit history for reproducibility

3. **Formats & Standards:**
   - CSV and JSON formats are used to ensure long-term accessibility
   - Date fields use ISO 8601 standard (`YYYY`)
   - States use full names (not abbreviations) for clarity
   - Character encoding: UTF-8

4. **Interoperability:**
   - Fully compatible with Python (`pandas`, `polars`), R (`tidyverse`), and SQL
   - Designed for integration into data visualization tools like Tableau, Power BI, or Observable

5. **Security:**
   - All data is public and non-sensitive
   - No API key required for Census Bureau API access

6. **Persistence:**
   - Final CSV files and accompanying metadata JSONs are stored in GitHub repository
   - Persistent identifiers (e.g., DOI) may be assigned upon publication

---

## 🔐 Data Ownership

- **Raw Data Ownership:**  
  U.S. Census Bureau data is in the public domain and freely available for use.
  
- **Derived Dataset Ownership:**  
  The cleaned and aggregated dataset is owned by the researcher (Tomer Avgil) and can be shared or cited with attribution.

---

## 📊 Data Quality Notes

- **Coverage:** Not all cities have data for all years (ACS 1-Year estimates are only available for areas with populations ≥65,000)
- **Missing Data:** 2020 is completely absent due to Census Bureau data collection issues
- **Currency:** All income values are in nominal USD (not adjusted for inflation)
- **Accuracy:** Income estimates are based on survey data and include margins of error (not included in this simplified dataset)

---

## 🔄 Processing Pipeline

1. **Data Collection:** Fetch data from Census API for each year (2010-2023, excluding 2020)
2. **Parsing:** Extract city name, state, and median income from API responses
3. **Cleaning:** Split location names into separate City and State fields
4. **Validation:** Remove null values and ensure data quality
5. **Export:** Save as CSV with UTF-8 encoding

---

## 📚 Citation

If you use this dataset, please cite:

```
Avgil, T. (2025). Aggregated U.S. Median Household Income by City-State-Year 
(ACS 1-Year Estimates). Derived from U.S. Census Bureau American Community Survey.
```

---

## 📞 Contact

For questions or issues with this dataset:
- **Maintainer:** Tomer Avgil
- **Email:** tomeravgil@gmail.com
- **Institution:** Rensselaer Polytechnic Institute
