import pandas as pd

df = pd.read_csv("data/master_dataset_final.csv")

print("=== ORGANIZATION: total unique values ===")
print(df["organization"].nunique())

print("\n=== ORGANIZATION: checking for near-duplicate/variant names ===")
orgs = sorted(df["organization"].unique())
for org in orgs:
    if "(" in org or org.upper() == org or org.lower() == org:
        print(org)

print("\n=== TITLE: sample of raw titles (checking formatting) ===")
print(df["title"].head(20).tolist())

print("\n=== TITLE: checking for casing inconsistencies (ALL CAPS titles) ===")
all_caps_titles = df[df["title"].astype(str).str.isupper()]["title"]
print(all_caps_titles.head(10).tolist())
print(f"Count of ALL CAPS titles: {len(all_caps_titles)}")

print("\n=== DATE: raw sample of date_posted ===")
print(df["date_posted"].dropna().head(5).tolist())

print("\n=== DATE: raw sample of deadline ===")
print(df["deadline"].dropna().head(5).tolist())

print(f"\n=== DATE: current dtypes ===")
print(df[["date_posted", "deadline"]].dtypes)