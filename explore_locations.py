import pandas as pd

df = pd.read_csv("data/master_dataset.csv")

unique_locations = df["location"].dropna().unique()
print(f"Total unique location values: {len(unique_locations)}")

print("\nValues 40–100:")
print(unique_locations[40:100])

print("\nValues 100–160:")
print(unique_locations[100:160])

print("\nTop 20 most frequent location values:")
print(df["location"].value_counts().head(20))