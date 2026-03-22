import pandas as pd
import glob

# Load all CSV files
files = glob.glob("dataset/*.csv")

df_list = []
for file in files:
    print("Loading:", file)
    df = pd.read_csv(file)
    df_list.append(df)

data = pd.concat(df_list, ignore_index=True)

print("\nTotal Records:", len(data))
print("Total Columns:", len(data.columns))

# Correct label column
label_col = " Label"

# Check label distribution
print("\nAttack Distribution:")
print(data[label_col].value_counts())

# Drop useless columns (like Flow ID, IPs if present)
drop_cols = []
for col in data.columns:
    if "IP" in col or "Flow ID" in col or "Timestamp" in col:
        drop_cols.append(col)

if drop_cols:
    print("\nDropping columns:", drop_cols)
    data = data.drop(columns=drop_cols)

# Handle missing values
data = data.replace([float('inf'), float('-inf')], 0)
data = data.fillna(0)

print("\nAfter Cleaning:")
print("Total Records:", len(data))
print("Total Columns:", len(data.columns))

# Save cleaned dataset
data.to_csv("dataset/cleaned_dataset.csv", index=False)

print("\n✅ Cleaned dataset saved as dataset/cleaned_dataset.csv")
