import pandas as pd

# Load the dataset
file_path = "C:\\Users\\HP\\OneDrive\\Desktop\\cleant1\\clean45\\cleannew.xlsx"  # Update with your file path
df = pd.read_excel(file_path)

# Check for issues in the dataset
print("Checking dataset cleanliness...\n")

# Check for missing values
missing_values = df.isnull().sum()
print("Missing Values:\n", missing_values[missing_values > 0])

# Check for duplicate rows
duplicate_rows = df.duplicated().sum()
print("\nNumber of Duplicate Rows:", duplicate_rows)

# Check for inconsistent data types
print("\nColumn Data Types:")
print(df.dtypes)

# Check for outliers (basic check using summary statistics)
print("\nSummary Statistics:")
print(df.describe())

# Check for invalid values (like negative prices, incorrect categories, etc.)
if 'Price' in df.columns:
    print("\nNegative Prices:", (df['Price'] < 0).sum())

if 'Rating' in df.columns:
    print("\nInvalid Ratings (outside 0-5 range):", df[(df['Rating'] < 0) | (df['Rating'] > 5)].shape[0])

if 'Discount' in df.columns:
    print("\nNegative Discounts:", (df['Discount'] < 0).sum())

# Final conclusion
if missing_values.sum() == 0 and duplicate_rows == 0:
    print("\n✅ The dataset appears to be clean!")
else:
    print("\n⚠️ The dataset has issues that need cleaning.")
