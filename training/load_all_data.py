import pandas as pd
import glob
import os

print("Current Working Directory:")
print(os.getcwd())

files = glob.glob("dataset/*.csv")

print("\nFound CSV files:")
for f in files:
    print(" -", f)

if len(files) == 0:
    print("\n❌ No CSV files found.")
    exit()

df_list = []

for file in files:
    print("\nLoading:", file)
    df = pd.read_csv(file)
    df_list.append(df)

# Merge all files
data = pd.concat(df_list, ignore_index=True)

print("\n✅ Total Records:", len(data))
print("✅ Total Features:", len(data.columns))

print("\n📌 Column Names:\n")
for col in data.columns:
    print(col)
