import pandas as pd

df = pd.read_csv("data/master_dataset_final.csv")

print(f"Total jobs: {len(df)}\n")

print("=== Jobs per organization (top 15) ===")
print(df["organization"].value_counts().head(15))

print("\n=== Jobs per country (top 15) ===")
print(df["country"].value_counts().head(15))

print("\n=== Work arrangement breakdown ===")
print(df["work_arrangement"].value_counts())
print("\n=== Verifying One Acre Fund source ===")
one_acre = df[df["organization"] == "One Acre Fund"]
print(one_acre[["organization", "title", "source_url"]].head())