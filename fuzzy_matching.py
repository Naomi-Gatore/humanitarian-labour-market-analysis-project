import pandas as pd

df = pd.read_csv("data/master_dataset_v2.csv")

print(f"Starting unique organizations: {df['organization'].nunique()}")

org_fixes = {
    "Care": "CARE",
    "Goal": "GOAL",
    "Searca": "SEARCA",
    "The Better Cotton Initiative": "Better Cotton Initiative",
    "Asian Development Bank (ADB)": "Asian Development Bank",
    "United Nations University (UNU)": "United Nations University",
}

df["organization"] = df["organization"].replace(org_fixes)

print(f"Unique organizations after merge: {df['organization'].nunique()}")

df.to_csv("data/master_dataset_v3.csv", index=False)
print("\nSaved to data/master_dataset_v3.csv")