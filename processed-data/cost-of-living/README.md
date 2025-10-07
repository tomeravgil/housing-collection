# 📈 U.S. Consumer Spending Dataset

This dataset provides aggregated U.S. consumer spending data compiled from the Federal Reserve Economic Data (FRED) system.  
It includes both **real** (inflation-adjusted) and **nominal** personal consumption expenditures at the **yearly** level for economic analysis.

---

## 📘 Dataset Overview

- **File name:** `us_consumer_spending.csv`
- **Format:** CSV (comma-separated values)
- **Records:** One record per year
- **Columns:**
  - `year` – Year of the record (YYYY)
  - `real_consumer_spending` – Real Personal Consumption Expenditures in billions of chained 2017 dollars
  - `nominal_consumer_spending` – Nominal Personal Consumption Expenditures in billions of current dollars

---

## 🧩 Source Information

- **Data Source:** [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)
- **Series Used:**
  - **PCEC96** - Real Personal Consumption Expenditures (chained 2017 dollars)
    - URL: https://fred.stlouisfed.org/series/PCEC96
  - **PCE** - Nominal Personal Consumption Expenditures
    - URL: https://fred.stlouisfed.org/series/PCE

- **Data Provider:** Federal Reserve Bank of St. Louis
- **Original Frequency:** Monthly
- **Aggregation:** Monthly values are averaged to produce yearly estimates
- **Coverage:** 1959-present (varies by series)

All derived datasets are publicly reproducible.

---

## 🎯 Purpose & Use Cases

This dataset is designed for:

1. **Economic Analysis:** Track consumer spending trends over time
2. **Cost of Living Studies:** Compare spending patterns with housing prices and income levels
3. **Inflation Analysis:** Compare real vs. nominal spending to understand inflation impact
4. **Macroeconomic Research:** Analyze consumer behavior and economic cycles
5. **Policy Research:** Support evidence-based economic policy decisions
6. **Data Visualization:** Create time-series charts and economic dashboards

---

## 📊 Understanding the Data

### Real vs. Nominal Consumer Spending

- **Real Consumer Spending (PCEC96):**
  - Adjusted for inflation using 2017 as the base year
  - Shows actual changes in consumption volume
  - Better for comparing purchasing power across years
  - Measured in "chained 2017 dollars"

- **Nominal Consumer Spending (PCE):**
  - Not adjusted for inflation
  - Shows spending in current dollar values
  - Reflects both price changes and volume changes
  - Measured in current dollars

### Why Both Metrics Matter

Using both real and nominal values allows researchers to:
- Calculate implicit price deflators
- Understand inflation's impact on consumer behavior
- Compare economic growth in real terms
- Analyze nominal spending patterns for budgeting purposes

---

## 🗃️ Data Management & Preservation

1. **Physical Storage:**
   - Raw data is fetched programmatically from FRED API (not stored locally)
   - Processed and aggregated datasets are stored in `/processed-data/cost-of-living/`
   - Backups are maintained in both local storage and GitHub repository

2. **Version Control:**
   - All scripts and datasets are tracked using Git/GitHub
   - Changes to processing scripts or derived data are versioned with commit history for reproducibility

3. **Formats & Standards:**
   - CSV and JSON formats are used to ensure long-term accessibility
   - Date fields use ISO 8601 standard (`YYYY`)
   - Numeric values are in billions of dollars
   - Character encoding: UTF-8

4. **Interoperability:**
   - Fully compatible with Python (`pandas`, `polars`), R (`tidyverse`), and SQL
   - Designed for integration into data visualization tools like Tableau, Power BI, or Observable

5. **Security:**
   - All data is public and non-sensitive
   - No API key required for FRED data access

6. **Persistence:**
   - Final CSV files and accompanying metadata JSONs are stored in GitHub repository
   - Persistent identifiers (e.g., DOI) may be assigned upon publication

---

## 🔐 Data Ownership

- **Raw Data Ownership:**  
  FRED data is provided by the Federal Reserve Bank of St. Louis and is publicly available.
  
- **Derived Dataset Ownership:**  
  The cleaned and aggregated dataset is owned by the researcher (Tomer Avgil) and can be shared or cited with attribution.

---

## 📊 Data Quality Notes

- **Temporal Coverage:** Real spending data (PCEC96) starts in 1959; nominal data (PCE) has broader coverage
- **Aggregation Method:** Monthly values are averaged (not summed) to produce yearly estimates
- **Units:** All values are in billions of dollars
- **Revisions:** FRED data may be revised by the Federal Reserve; re-run the processing script for the latest values
- **Missing Data:** Some years may have null values if one series has data but the other doesn't

---

## 🔄 Processing Pipeline

1. **Data Collection:** Fetch CSV data from FRED for each series (PCEC96, PCE)
2. **Parsing:** Extract date and value columns from CSV responses
3. **Date Processing:** Convert dates to years
4. **Aggregation:** Group by year and calculate mean values
5. **Merging:** Combine both series into a single dataset
6. **Export:** Save as CSV with UTF-8 encoding

---

## 📚 Citation

If you use this dataset, please cite:

```
Avgil, T. (2025). U.S. Consumer Spending Dataset (Real and Nominal Personal 
Consumption Expenditures). Derived from Federal Reserve Economic Data (FRED), 
Federal Reserve Bank of St. Louis.

Original Data Sources:
- U.S. Bureau of Economic Analysis, Real Personal Consumption Expenditures [PCEC96], 
  retrieved from FRED, Federal Reserve Bank of St. Louis
- U.S. Bureau of Economic Analysis, Personal Consumption Expenditures [PCE], 
  retrieved from FRED, Federal Reserve Bank of St. Louis
```

---

## 📞 Contact

For questions or issues with this dataset:
- **Maintainer:** Tomer Avgil
- **Email:** tomeravgil@gmail.com
- **Institution:** Rensselaer Polytechnic Institute
