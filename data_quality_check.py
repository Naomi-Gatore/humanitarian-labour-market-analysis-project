import pandas as pd

df = pd.read_csv("data/master_dataset_cleaned.csv")

print("=== SHAPE ===")
print(df.shape)

print("\n=== MISSING VALUES PER COLUMN ===")
print(df.isna().sum())

print("\n=== DUPLICATE ROWS (exact duplicates) ===")
print(df.duplicated().sum())

print("\n=== DUPLICATE JOB TITLES (same org + title, possible re-scrape duplicates) ===")
print(df.duplicated(subset=["organization", "title"]).sum())

print("\n=== ORGANIZATION column - suspicious/placeholder values ===")
print(df["organization"].value_counts().head(20))

print("\n=== TITLE column - sample of unusual/short values ===")
short_titles = df[df["title"].astype(str).str.len() < 5]
print(short_titles[["organization", "title"]])

print("\n=== source_url - checking for placeholder/non-job URLs ===")
print(df["source_url"].value_counts().head(10))
print("\n=== Sample of duplicate org+title pairs ===")
dupes = df[df.duplicated(subset=["organization", "title"], keep=False)]
print(dupes[["organization", "title", "location"]].sort_values("organization").head(30))