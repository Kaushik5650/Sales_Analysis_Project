# ==============================
# Sales Data Analysis Project
# ==============================

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile

# ------------------------------
# Step 0: Load CSV from ZIP
# ------------------------------
zip_path = "data/raw/train.csv.zip"

with zipfile.ZipFile(zip_path) as z:
    csv_name = z.namelist()[0]  # assumes only one CSV inside
    df = pd.read_csv(z.open(csv_name))

print("First 5 rows:")
print(df.head())
print("\nColumns in the dataset:")
print(df.columns)

# ------------------------------
# Step 1: Data Cleaning
# ------------------------------
df = df.drop_duplicates()

# Fill missing numeric values
numeric_cols = df.select_dtypes(include='number').columns
for col in numeric_cols:
    df[col] = df[col].fillna(0)

# Convert 'Order Date' to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

print("\nData after cleaning:")
print(df.info())

# ------------------------------
# Step 2: Save to SQLite
# ------------------------------
engine = create_engine("sqlite:///sales_db.sqlite")
df.to_sql("sales", engine, if_exists="replace", index=False)
print("\nCleaned data saved to SQLite: sales_db.sqlite")

# ------------------------------
# Step 3: SQL Analysis
# ------------------------------

# 3.1 Total sales per Category
query_category_sales = """
SELECT Category, SUM(Sales) AS total_sales
FROM sales
GROUP BY Category
ORDER BY total_sales DESC
"""
df_category_sales = pd.read_sql(query_category_sales, engine)
print("\nTotal sales per Category:")
print(df_category_sales)

# 3.2 Total sales per Sub-Category
query_subcat_sales = """
SELECT "Sub-Category", SUM(Sales) AS total_sales
FROM sales
GROUP BY "Sub-Category"
ORDER BY total_sales DESC
"""
df_subcat_sales = pd.read_sql(query_subcat_sales, engine)
print("\nTotal sales per Sub-Category:")
print(df_subcat_sales)

# 3.3 Monthly sales trend
df['Month'] = df['Order Date'].dt.to_period('M')
query_monthly_sales = """
SELECT strftime('%Y-%m', "Order Date") AS Month, SUM(Sales) AS total_sales
FROM sales
GROUP BY Month
ORDER BY Month
"""
df_monthly_sales = pd.read_sql(query_monthly_sales, engine)
print("\nMonthly sales trend:")
print(df_monthly_sales)

# ------------------------------
# Step 4: Insights
# ------------------------------
top_category = df_category_sales.iloc[0]
top_subcategory = df_subcat_sales.iloc[0]
top_month = df_monthly_sales.iloc[df_monthly_sales['total_sales'].idxmax()]

print(f"\nTop-selling Category: {top_category['Category']} with sales = {top_category['total_sales']}")
print(f"Top-selling Sub-Category: {top_subcategory['Sub-Category']} with sales = {top_subcategory['total_sales']}")
print(f"Month with highest sales: {top_month['Month']} with sales = {top_month['total_sales']}")

# ------------------------------
# Step 5: Visualizations
# ------------------------------
sns.set(style="whitegrid")

# Total sales per Category
plt.figure(figsize=(8,5))
sns.barplot(data=df_category_sales, x='Category', y='total_sales', palette='Blues_d')
plt.title("Total Sales per Category")
plt.ylabel("Total Sales")
plt.show()

# Total sales per Sub-Category
plt.figure(figsize=(10,5))
sns.barplot(data=df_subcat_sales, x='Sub-Category', y='total_sales', palette='Greens_d')
plt.xticks(rotation=45)
plt.title("Total Sales per Sub-Category")
plt.ylabel("Total Sales")
plt.show()

# Monthly sales trend
plt.figure(figsize=(10,5))
sns.lineplot(data=df_monthly_sales, x='Month', y='total_sales', marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.ylabel("Total Sales")
plt.show()

# Sales distribution
plt.figure(figsize=(8,5))
sns.histplot(df['Sales'], bins=30, kde=True, color='orange')
plt.title("Sales Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.show()

print("\nProject completed! Dataset cleaned, SQL queries executed, visualizations generated, and insights ready.")
