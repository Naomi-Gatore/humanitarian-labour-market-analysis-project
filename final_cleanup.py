import pandas as pd

df = pd.read_csv("data/master_dataset_cleaned.csv")

print(f"Starting rows: {len(df)}")

df = df[df["organization"] != "(Value Members only)"]
print(f"After removing placeholder orgs: {len(df)}")

df = df.dropna(subset=["organization", "title", "location"])
print(f"After removing blank rows: {len(df)}")

df = df.drop_duplicates()
print(f"After removing exact duplicates: {len(df)}")

df.to_csv("data/master_dataset_final.csv", index=False)
print("\nSaved to data/master_dataset_final.csv")