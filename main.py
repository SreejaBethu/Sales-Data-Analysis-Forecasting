import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import textwrap

# load data frame
df = pd.read_csv(r'C:\Users\bethu\PycharmProjects\Sales Data Analysis & Forecasting\amazon.csv')

def wrap_labels(labels, width=10):
    return [textwrap.fill(label, width) for label in labels]

# Cleaning and converting relevant columns
df['discount_percentage'] = df['discount_percentage'].str.replace('%', '', regex=True)
df['discount_percentage'] = pd.to_numeric(df['discount_percentage'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating_count'] = df['rating_count'].str.replace(',', '', regex=True)
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

# Abbreviate and truncate category names
category_map = {
    'Electronics and Gadgets': 'Electronics',
    'Home and Kitchen Appliances': 'Home & Kitchen',
    'Fashion and Accessories': 'Fashion',
}

df['category'] = df['category'].replace(category_map).str[:15]

# Drop rows with NaN in critical columns
df = df.dropna(subset=['discount_percentage', 'rating', 'rating_count'])

# Filter for valid data
df = df[(df['discount_percentage'] > 0) & (df['rating'] > 0) & (df['rating_count'] > 0)]

if df.empty:
    print("The dataset is empty after cleaning. Please check the source data or cleaning criteria.")
else:
    print("Data available for visualization.")

# ---- Plot 1: Distribution of Product Ratings ----

# Check if data is empty
if not df['rating'].empty:
    plt.figure(figsize=(10, 6))
    sns.histplot(df['rating'].dropna(), bins=10, kde=True, color="green")
    plt.title("Distribution of Product Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.show()
else:
    print("No data available for rating distribution plot.")

# ---- Plot 2: Average Discount Percentage by Product Category ----
if 'category' in df.columns and not df.empty:
        avg_discount = df.groupby('category')['discount_percentage'].mean().sort_values(ascending=False).head(10)
        if not avg_discount.empty:
            plt.figure(figsize=(12, 6))
            avg_discount.plot(kind='bar', color='orange', edgecolor='black')
            plt.title("Top 10 Categories: Average Discount Percentage by Category", fontsize=14)
            plt.xlabel("Average Discount (%)", fontsize=12)
            plt.ylabel("Product Category", fontsize=8)
            plt.xticks(ticks=range(len(avg_discount)), labels=wrap_labels(avg_discount.index, 15), rotation=45,fontsize=10, ha='right')
            plt.tight_layout()
            plt.savefig('avg_discount_by_category.png')
            plt.show()
        else:
            print("No valid data available for average discount percentage by category plot.")
else:
        print("Category column is missing or has no valid data.")

# ---- Plot 3: Average Rating Count by Product Category ----
if 'category' in df.columns and not df.empty:
    avg_rating_count_by_category = df.groupby('category')['rating_count'].mean().sort_values(ascending=False).head(10)
    if not avg_rating_count_by_category.empty:
            plt.figure(figsize=(12, 8))
            avg_rating_count_by_category.plot(kind='bar', color='green', edgecolor='black')
            plt.title("Average Rating Count by Product Category", fontsize=14)
            plt.xlabel("Average Rating Count", fontsize=10)
            plt.ylabel("Product Category", fontsize=12)
            plt.tight_layout()
            plt.xticks(rotation=45, fontsize=10, ha='right')
            plt.savefig('avg_rating_count_by_category.png')
            plt.show()
    else:
        print("No data available for average rating count by category plot.")
else:
    print("Category column is missing or has no valid data.")