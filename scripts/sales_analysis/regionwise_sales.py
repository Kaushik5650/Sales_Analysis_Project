# ==============================
# Bonus Analysis: Region & Segment
# ==============================

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile

# Load CSV from ZIP (reuse the same dataset)
zip_path = "data/raw/train.csv.zip"

with zipfile.ZipFile(zip_path) as z:
    csv_name = z.namelist()[0]
    df = pd.read_csv(z.open(csv_name))

# Convert 'Order Date' to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Save to SQLite
engine = create_engine("sqlite:///sales_db.sqlite")
df.to_sql("sales", engine, if_exists="replace", index=False)

# ------------------------------
# Region-wise Sales
# ------------------------------
query_region_sales = """
SELECT Region, SUM(Sales) AS total_sales
FROM sales
GROUP BY Region
ORDER BY total_sales DESC
"""
df_region_sales = pd.read_sql(query_region_sales, engine)
print("\nRegion-wise Total Sales:")
print(df_region_sales)

# Visualization
plt.figure(figsize=(8,5))
sns.barplot(data=df_region_sales, x='Region', y='total_sales', palette='coolwarm')
plt.title("Total Sales by Region")
plt.ylabel("Total Sales")
plt.show()

# ------------------------------
# Customer Segment Analysis
# ------------------------------
query_segment_sales = """
SELECT Segment, SUM(Sales) AS total_sales
FROM sales
GROUP BY Segment
ORDER BY total_sales DESC
"""
df_segment_sales = pd.read_sql(query_segment_sales, engine)
print("\nSales by Customer Segment:")
print(df_segment_sales)

# Visualization
plt.figure(figsize=(6,4))
sns.barplot(data=df_segment_sales, x='Segment', y='total_sales', palette='Set2')
plt.title("Sales by Customer Segment")
plt.ylabel("Total Sales")
plt.show()

# Optional: Monthly sales per Segment
query_month_segment = """
SELECT strftime('%Y-%m', "Order Date") AS Month, Segment, SUM(Sales) AS total_sales
FROM sales
GROUP BY Month, Segment
ORDER BY Month
"""
df_month_segment = pd.read_sql(query_month_segment, engine)

plt.figure(figsize=(12,6))
sns.lineplot(data=df_month_segment, x='Month', y='total_sales', hue='Segment', marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend by Segment")
plt.ylabel("Total Sales")
plt.show()

print("\nBonus insights completed: region-wise and segment-wise analysis.")
