# 📊 Data Visualization & Curation

This folder contains scripts for visualizing and curating the processed housing, income, and consumer spending datasets.

---

## 🎯 Purpose

The visualization script generates comprehensive charts and analyses to:
- Present key trends in housing prices, income, and consumer spending
- Identify regional patterns and disparities
- Analyze housing affordability through price-to-income ratios
- Explore correlations between economic indicators
- Provide data-driven insights for research and policy analysis

---

## 📁 Files

- **`main.py`** - Main visualization script that generates all charts and statistics
- **`README.md`** - This file

---

## 🖼️ Generated Visualizations

Running `main.py` creates the following outputs in `processed-data/visualizations/`:

1. **`00_summary_statistics.txt`**
   - Comprehensive summary statistics for all datasets
   - Record counts, date ranges, averages, and medians

2. **`01_consumer_spending_trends.png`**
   - Real vs. nominal consumer spending over time
   - Inflation impact visualization

3. **`02_housing_price_trends.png`**
   - National average housing prices by year
   - Data coverage (number of cities) by year

4. **`03_top_10_expensive_cities.png`**
   - Most expensive cities in the most recent year
   - Filtered for data quality (≥10 ZIP codes)

5. **`04_income_trends_top_states.png`**
   - Median income trends for top 10 highest-income states
   - Multi-line time series comparison

6. **`05_housing_affordability.png`**
   - Most and least affordable cities (2020+)
   - Based on price-to-income ratios

7. **`06_price_income_correlation.png`**
   - Scatter plot of housing prices vs. median income
   - Trend line and correlation coefficient
   - Color-coded by year

---

## 🚀 Usage

### Prerequisites

Install required packages:
```bash
pip install -r ../requirements.txt
```

Required packages:
- pandas
- matplotlib
- seaborn
- numpy

### Running the Script

From the `visualization/` directory:
```bash
cd visualization
python3 main.py
```

The script will:
1. Load all processed datasets
2. Generate 7 visualizations
3. Save outputs to `processed-data/visualizations/`
4. Display progress messages

Expected runtime: ~10-30 seconds depending on system performance.

---

## 📊 Key Insights

### Housing Affordability Analysis
The price-to-income ratio is a critical metric for understanding housing affordability:
- **Ratio < 3**: Generally considered affordable
- **Ratio 3-5**: Moderately affordable
- **Ratio > 5**: Severely unaffordable

### Correlation Analysis
The correlation between housing prices and median income reveals:
- How income levels influence housing markets
- Regional economic disparities
- Temporal trends in housing affordability

### Consumer Spending Trends
Comparing real vs. nominal spending shows:
- Impact of inflation on purchasing power
- Long-term economic growth patterns
- Consumer behavior changes over time

---

## 🎨 Customization

### Modifying Visualizations

To customize the visualizations, edit `main.py`:

**Change color schemes:**
```python
sns.set_palette("husl")  # or "Set2", "pastel", etc.
```

**Adjust figure sizes:**
```python
plt.rcParams['figure.figsize'] = (14, 8)  # width, height in inches
```

**Filter data differently:**
```python
# Example: Focus on specific states
states_of_interest = ['California', 'New York', 'Texas']
filtered_df = df[df['State'].isin(states_of_interest)]
```

**Add more visualizations:**
Follow the existing pattern:
1. Load/filter data
2. Create figure and axes
3. Plot data
4. Add labels and formatting
5. Save to OUTPUT_DIR

---

## 📈 Data Sources

All visualizations use data from:
- **Housing Data**: `processed-data/housing-data/housing_prices_city_aggregated.csv`
- **Income Data**: `processed-data/median-salary/acs1y_s1901_median_income_2010_2023.csv`
- **Spending Data**: `processed-data/cost-of-living/us_consumer_spending.csv`

See individual dataset READMEs for source information and methodology.

---

## 🔧 Troubleshooting

### Common Issues

**Import errors:**
```bash
# Ensure all packages are installed
pip install matplotlib seaborn pandas numpy
```

**File not found errors:**
- Verify you're running from the `visualization/` directory
- Check that processed data files exist in `processed-data/`

**Memory issues with large datasets:**
- The script filters data appropriately for visualization
- If issues persist, increase filtering thresholds in the code

**Display issues on headless systems:**
```python
# Add at the top of main.py
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

---

## 📝 Notes

- All visualizations are saved as high-resolution PNG files (300 DPI)
- Charts use colorblind-friendly color schemes where possible
- Data is filtered for quality (e.g., minimum ZIP code counts)
- Missing data (like 2020 income data) is handled gracefully

---

## 🔮 Future Enhancements

Potential additions:
- Interactive visualizations using Plotly or Bokeh
- Geographic maps using GeoPandas
- Time-series forecasting models
- Statistical significance testing
- Export to HTML dashboard format
- Automated report generation (PDF)

---

## 📞 Contact

For questions about the visualizations:
- **Maintainer:** Tomer Avgil
- **Email:** tomeravgil@gmail.com
- **Institution:** Rensselaer Polytechnic Institute
