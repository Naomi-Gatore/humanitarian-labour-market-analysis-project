import pandas as pd

df = pd.read_csv("data/master_dataset_final.csv")

print(f"Starting rows: {len(df)}")

org_fixes = {
    "The International Council on Clean Transportation (ICCT)": "International Council on Clean Transportation (ICCT)",
}
df["organization"] = df["organization"].replace(org_fixes)

df.loc[df["title"] == "001-07-2026_EMERGENCY COMMUNITY ENGAGEMENT ASSOCIATE", "title"] = "Emergency Community Engagement Associate"

df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")

df["deadline"] = df["deadline"].str.replace("Apply by: ", "", regex=False)
df["deadline"] = pd.to_datetime(df["deadline"], format="%d %b %Y", errors="coerce")

print(f"\nUnique organizations after fix: {df['organization'].nunique()}")
print(f"\nSample cleaned dates:")
print(df[["date_posted", "deadline"]].dropna(how="all").head(10))

print(f"\nDate dtypes now:")
print(df[["date_posted", "deadline"]].dtypes)

df.to_csv("data/master_dataset_v2.csv", index=False)
print("\nSaved to data/master_dataset_v2.csv")