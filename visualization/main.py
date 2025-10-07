"""
Data Visualization and Curation Script
=======================================
This script creates visualizations from the processed housing, income, and consumer spending data.
Generates charts showing trends, correlations, and regional comparisons.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from pathlib import Path

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Create output directory for visualizations
OUTPUT_DIR = Path("../processed-data/visualizations")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("📊 Loading datasets...")

# Load datasets
housing_df = pd.read_csv("../processed-data/housing-data/housing_prices_city_aggregated.csv")
income_df = pd.read_csv("../processed-data/median-salary/acs1y_s1901_median_income_2010_2023.csv")
spending_df = pd.read_csv("../processed-data/cost-of-living/us_consumer_spending.csv")

print(f"✅ Housing data: {len(housing_df):,} records")
print(f"✅ Income data: {len(income_df):,} records")
print(f"✅ Consumer spending data: {len(spending_df):,} records")

# ============================================================================
# 1. NATIONAL CONSUMER SPENDING TRENDS
# ============================================================================
print("\n📈 Creating consumer spending visualization...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Real vs Nominal Consumer Spending
spending_clean = spending_df.dropna()
ax1.plot(spending_clean['year'], spending_clean['nominal_consumer_spending'], 
         label='Nominal Spending', linewidth=2, marker='o', markersize=4)
ax1.plot(spending_clean['year'], spending_clean['real_consumer_spending'], 
         label='Real Spending (2017 dollars)', linewidth=2, marker='s', markersize=4)
ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Billions of Dollars', fontsize=12, fontweight='bold')
ax1.set_title('U.S. Personal Consumption Expenditures Over Time', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Plot 2: Inflation Impact (Nominal/Real ratio)
spending_clean = spending_clean.copy()
spending_clean['inflation_factor'] = (spending_clean['nominal_consumer_spending'] / 
                                       spending_clean['real_consumer_spending'])
ax2.plot(spending_clean['year'], spending_clean['inflation_factor'], 
         linewidth=2, marker='o', markersize=4, color='coral')
ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Nominal/Real Ratio', fontsize=12, fontweight='bold')
ax2.set_title('Inflation Impact on Consumer Spending', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='Baseline (2017)')
ax2.legend(fontsize=11)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_consumer_spending_trends.png", dpi=300, bbox_inches='tight')
print(f"✅ Saved: {OUTPUT_DIR / '01_consumer_spending_trends.png'}")
plt.close()

# ============================================================================
# 2. HOUSING PRICE TRENDS BY YEAR
# ============================================================================
print("\n🏠 Creating housing price trends visualization...")

# Calculate national average housing prices by year
housing_yearly = housing_df.groupby('YEAR').agg({
    'avg_price': 'mean',
    'City': 'count'
}).reset_index()
housing_yearly.columns = ['Year', 'Avg_Price', 'City_Count']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Average housing price over time
ax1.plot(housing_yearly['Year'], housing_yearly['Avg_Price'], 
         linewidth=2.5, marker='o', markersize=6, color='steelblue')
ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Average Price ($)', fontsize=12, fontweight='bold')
ax1.set_title('National Average Housing Prices Over Time', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

# Plot 2: Number of cities with data by year
ax2.bar(housing_yearly['Year'], housing_yearly['City_Count'], color='lightcoral', alpha=0.7)
ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Cities', fontsize=12, fontweight='bold')
ax2.set_title('Data Coverage: Cities with Housing Data by Year', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_housing_price_trends.png", dpi=300, bbox_inches='tight')
print(f"✅ Saved: {OUTPUT_DIR / '02_housing_price_trends.png'}")
plt.close()

# ============================================================================
# 3. TOP 10 MOST EXPENSIVE CITIES (2024)
# ============================================================================
print("\n💰 Creating most expensive cities visualization...")

# Get 2024 data (or most recent year)
recent_year = housing_df['YEAR'].max()
recent_housing = housing_df[housing_df['YEAR'] == recent_year].copy()

# Filter for cities with reasonable data (at least 10 zip codes)
recent_housing_filtered = recent_housing[recent_housing['zip_count'] >= 10]

# Get top 10 most expensive
top_10_expensive = recent_housing_filtered.nlargest(10, 'avg_price')

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(range(len(top_10_expensive)), top_10_expensive['avg_price'], color='darkgreen', alpha=0.7)
ax.set_yticks(range(len(top_10_expensive)))
ax.set_yticklabels([f"{row['City']}, {row['State']}" for _, row in top_10_expensive.iterrows()])
ax.set_xlabel('Average Price ($)', fontsize=12, fontweight='bold')
ax.set_title(f'Top 10 Most Expensive Cities ({recent_year})', fontsize=14, fontweight='bold')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
ax.grid(True, alpha=0.3, axis='x')

# Add value labels on bars
for i, (idx, row) in enumerate(top_10_expensive.iterrows()):
    ax.text(row['avg_price'], i, f" ${row['avg_price']/1000:.0f}K", 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_top_10_expensive_cities.png", dpi=300, bbox_inches='tight')
print(f"✅ Saved: {OUTPUT_DIR / '03_top_10_expensive_cities.png'}")
plt.close()

# ============================================================================
# 4. MEDIAN INCOME TRENDS BY STATE (Top 10 States)
# ============================================================================
print("\n💵 Creating median income trends visualization...")

# Calculate average income by state and year
income_state_year = income_df.groupby(['State', 'Year'])['Median_Income'].mean().reset_index()

# Get top 10 states by most recent average income
recent_income_year = income_df['Year'].max()
top_states = (income_df[income_df['Year'] == recent_income_year]
              .groupby('State')['Median_Income'].mean()
              .nlargest(10).index.tolist())

fig, ax = plt.subplots(figsize=(14, 8))

for state in top_states:
    state_data = income_state_year[income_state_year['State'] == state]
    ax.plot(state_data['Year'], state_data['Median_Income'], 
            marker='o', linewidth=2, label=state, markersize=5)

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Median Household Income ($)', fontsize=12, fontweight='bold')
ax.set_title('Median Income Trends: Top 10 Highest-Income States', fontsize=14, fontweight='bold')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_income_trends_top_states.png", dpi=300, bbox_inches='tight')
print(f"✅ Saved: {OUTPUT_DIR / '04_income_trends_top_states.png'}")
plt.close()

# ============================================================================
# 5. HOUSING AFFORDABILITY: PRICE-TO-INCOME RATIO
# ============================================================================
print("\n🏘️  Creating housing affordability analysis...")

# Clean city names in income data (remove "city", "town", etc.)
income_df['City_Clean'] = income_df['City'].str.replace(r'\s+(city|town|CDP|municipality)$', '', regex=True)

# Merge housing and income data
merged_df = pd.merge(
    housing_df,
    income_df,
    left_on=['City', 'State', 'YEAR'],
    right_on=['City_Clean', 'State', 'Year'],
    how='inner'
)

# Calculate price-to-income ratio
merged_df['price_to_income_ratio'] = merged_df['avg_price'] / merged_df['Median_Income']

# Get recent data for analysis
recent_merged = merged_df[merged_df['YEAR'] >= 2020].copy()

# Get cities with highest and lowest affordability (filter for data quality)
recent_merged_filtered = recent_merged[recent_merged['zip_count'] >= 5]

# Top 10 least affordable (highest ratio)
least_affordable = recent_merged_filtered.nlargest(15, 'price_to_income_ratio')

# Top 10 most affordable (lowest ratio)
most_affordable = recent_merged_filtered.nsmallest(15, 'price_to_income_ratio')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Least affordable cities
bars1 = ax1.barh(range(len(least_affordable)), least_affordable['price_to_income_ratio'], 
                 color='darkred', alpha=0.7)
ax1.set_yticks(range(len(least_affordable)))
ax1.set_yticklabels([f"{row['City']}, {row['State']} ({row['YEAR']})" 
                      for _, row in least_affordable.iterrows()], fontsize=9)
ax1.set_xlabel('Price-to-Income Ratio', fontsize=11, fontweight='bold')
ax1.set_title('Least Affordable Cities (2020+)', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3, axis='x')

# Most affordable cities
bars2 = ax2.barh(range(len(most_affordable)), most_affordable['price_to_income_ratio'], 
                 color='darkgreen', alpha=0.7)
ax2.set_yticks(range(len(most_affordable)))
ax2.set_yticklabels([f"{row['City']}, {row['State']} ({row['YEAR']})" 
                      for _, row in most_affordable.iterrows()], fontsize=9)
ax2.set_xlabel('Price-to-Income Ratio', fontsize=11, fontweight='bold')
ax2.set_title('Most Affordable Cities (2020+)', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_housing_affordability.png", dpi=300, bbox_inches='tight')
print(f"✅ Saved: {OUTPUT_DIR / '05_housing_affordability.png'}")
plt.close()

# ============================================================================
# 6. CORRELATION: HOUSING PRICES vs MEDIAN INCOME
# ============================================================================
print("\n📊 Creating correlation analysis...")

# Use recent data for correlation
correlation_data = merged_df[merged_df['YEAR'] >= 2015].copy()

# Remove any rows with null values
correlation_data = correlation_data.dropna(subset=['Median_Income', 'avg_price'])

if len(correlation_data) > 0:
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create scatter plot
    scatter = ax.scatter(correlation_data['Median_Income'], 
                         correlation_data['avg_price'],
                         c=correlation_data['YEAR'], 
                         cmap='viridis',
                         alpha=0.5, 
                         s=30)
    
    # Add trend line
    z = np.polyfit(correlation_data['Median_Income'], correlation_data['avg_price'], 1)
    p = np.poly1d(z)
    ax.plot(correlation_data['Median_Income'].sort_values(), 
            p(correlation_data['Median_Income'].sort_values()), 
            "r--", linewidth=2, label=f'Trend line: y={z[0]:.2f}x+{z[1]:.0f}')
    
    ax.set_xlabel('Median Household Income ($)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Housing Price ($)', fontsize=12, fontweight='bold')
    ax.set_title('Housing Prices vs. Median Income (2015-2024)', fontsize=14, fontweight='bold')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Year', fontsize=11, fontweight='bold')
    
    # Calculate and display correlation coefficient
    corr = correlation_data[['Median_Income', 'avg_price']].corr().iloc[0, 1]
    ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', 
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "06_price_income_correlation.png", dpi=300, bbox_inches='tight')
    print(f"✅ Saved: {OUTPUT_DIR / '06_price_income_correlation.png'}")
    plt.close()
else:
    print("⚠️  Skipping correlation plot - insufficient matching data between housing and income datasets")

# ============================================================================
# 7. GENERATE SUMMARY STATISTICS
# ============================================================================
print("\n📋 Generating summary statistics...")

summary_stats = {
    "Housing Data": {
        "Total Records": len(housing_df),
        "Year Range": f"{housing_df['YEAR'].min()}-{housing_df['YEAR'].max()}",
        "Unique Cities": housing_df['City'].nunique(),
        "Unique States": housing_df['State'].nunique(),
        "Avg Price (Overall)": f"${housing_df['avg_price'].mean():,.2f}",
        "Median Price (Overall)": f"${housing_df['avg_price'].median():,.2f}",
    },
    "Income Data": {
        "Total Records": len(income_df),
        "Year Range": f"{income_df['Year'].min()}-{income_df['Year'].max()}",
        "Unique Cities": income_df['City'].nunique(),
        "Unique States": income_df['State'].nunique(),
        "Avg Income (Overall)": f"${income_df['Median_Income'].mean():,.2f}",
        "Median Income (Overall)": f"${income_df['Median_Income'].median():,.2f}",
    },
    "Consumer Spending Data": {
        "Total Records": len(spending_df),
        "Year Range": f"{spending_df['year'].min()}-{spending_df['year'].max()}",
        "Latest Real Spending": f"${spending_clean['real_consumer_spending'].iloc[-1]:,.2f}B",
        "Latest Nominal Spending": f"${spending_clean['nominal_consumer_spending'].iloc[-1]:,.2f}B",
    }
}

# Save summary to text file
with open(OUTPUT_DIR / "00_summary_statistics.txt", 'w') as f:
    f.write("=" * 70 + "\n")
    f.write("DATA SUMMARY STATISTICS\n")
    f.write("=" * 70 + "\n\n")
    
    for dataset_name, stats in summary_stats.items():
        f.write(f"\n{dataset_name}\n")
        f.write("-" * 70 + "\n")
        for key, value in stats.items():
            f.write(f"{key:.<40} {value}\n")
        f.write("\n")

print(f"✅ Saved: {OUTPUT_DIR / '00_summary_statistics.txt'}")

# ============================================================================
# COMPLETION
# ============================================================================
print("\n" + "=" * 70)
print("✅ ALL VISUALIZATIONS COMPLETED!")
print("=" * 70)
print(f"\nOutput directory: {OUTPUT_DIR.absolute()}")
print("\nGenerated files:")
print("  1. 00_summary_statistics.txt - Dataset summary statistics")
print("  2. 01_consumer_spending_trends.png - National spending trends")
print("  3. 02_housing_price_trends.png - Housing price evolution")
print("  4. 03_top_10_expensive_cities.png - Most expensive cities")
print("  5. 04_income_trends_top_states.png - Income trends by state")
print("  6. 05_housing_affordability.png - Price-to-income ratios")
print("  7. 06_price_income_correlation.png - Correlation analysis")
print("\n" + "=" * 70)
