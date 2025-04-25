import pandas as pd
import re

# Load the dataset
file_path = "amazon_products.csv"  # Update if needed
df = pd.read_csv(file_path)

# Function to clean numeric columns safely
def clean_numeric(column):
    return pd.to_numeric(column.str.replace(r"[₹,]", "", regex=True), errors="coerce")

# Clean Price (handle 'N/A' by converting non-numeric values to NaN)
if "Price" in df.columns:
    df["Price"] = clean_numeric(df["Price"])

# Convert Reviews to numeric safely
if "Reviews" in df.columns:
    df["Reviews"] = clean_numeric(df["Reviews"])

# Clean Discount (remove parentheses and extract numbers safely)
if "Discount" in df.columns:
    df["Discount"] = df["Discount"].str.extract(r"(\d+)").astype(float)

# Clean Delivery Date (remove unnecessary text after 'Details')
if "Delivery Date" in df.columns:
    df["Delivery Date"] = df["Delivery Date"].str.split("Details").str[0].str.strip()

# Function to extract only the date from the "Delivery Date" column
def extract_date(text):
    if pd.isna(text) or text.strip() == "":
        return "Unknown"  # Replace missing or empty values with "Unknown"
    
    match = re.search(r"\b(?:\d{1,2} [A-Za-z]+|\d{1,2} [A-Za-z]+ - \d{1,2} [A-Za-z]+)\b", str(text))
    return match.group(0) if match else "Unknown"

# Apply the function to clean the "Delivery Date" column
if "Delivery Date" in df.columns:
    df["Delivery Date"] = df["Delivery Date"].apply(extract_date)

# Fill missing values appropriately (avoiding inplace warning)
if "Rating" in df.columns:
    df["Rating"] = df["Rating"].fillna(df["Rating"].median())  # Use median for ratings

if "Reviews" in df.columns:
    df["Reviews"] = df["Reviews"].fillna(0)  # Assume 0 reviews if missing

if "Discount" in df.columns:
    df["Discount"] = df["Discount"].fillna(0)  # Assume 0% discount if missing

if "Availability" in df.columns:
    df["Availability"] = df["Availability"].fillna("Unknown")  # Fill missing availability with "Unknown"

# Save the cleaned dataset
final_cleaned_file = "final_cleaned_amazon_products.csv"
df.to_csv(final_cleaned_file, index=False)

print(f"✅ Final cleaned data saved to {final_cleaned_file}")
