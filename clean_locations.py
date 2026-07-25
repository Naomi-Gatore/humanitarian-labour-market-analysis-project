import pandas as pd

df = pd.read_csv("data/master_dataset.csv")

city_to_country = {
    "Nairobi": "Kenya",
    "Kampala": "Uganda",
    "GOMA-BENI & BUTEMBO": "Democratic Republic of Congo",
}

us_state_or_region_codes = ["CA", "NY", "TX", "OH", "VA", "NC", "IL", "MT", "IA", "AB", "BC"]

country_aliases = {
    "DRC": "Democratic Republic of Congo",
    "Congo": "Democratic Republic of Congo",
    "Cote Divoire": "Ivory Coast",
}

non_country_values = [
    "Medical", "Non-Medical", "Field Based", "Home-based",
    "Africa", "Multiple Locations Considered", "Regional / Global",
    "Remote Africa",
]

def clean_location(raw_location):
    if pd.isna(raw_location):
        return "Not specified", "Not specified"

    text = raw_location.replace("Location: ", "").strip()

    if text in non_country_values:
        return "Not specified", "Not specified"

    work_arrangement = "Onsite"
    if "Remote" in text:
        work_arrangement = "Remote"
    if "Regional" in text or "Global" in text or text == "Africa":
        work_arrangement = "Regional/Global"

    text_clean = text.replace(" or ", ", ").replace(" - ", ", ").replace("(Remote)", "")
    parts = [p.strip() for p in text_clean.split(",")]

    exclude_terms = ["Remote", "Regional / Global", "Regional", "Global"] + non_country_values
    country_candidates = [p for p in parts if p not in exclude_terms and p]

    if country_candidates:
        country = country_candidates[-1]
    else:
        country = "Not specified"

    if country in city_to_country:
        country = city_to_country[country]
    elif country in us_state_or_region_codes:
        country = "United States"
    elif country in country_aliases:
        country = country_aliases[country]

    return country, work_arrangement

df["country"] = df["location"].apply(lambda x: clean_location(x)[0])
df["work_arrangement"] = df["location"].apply(lambda x: clean_location(x)[1])

print(f"Unique countries found: {df['country'].nunique()}")
print(f"\nTop 15 countries by job count:")
print(df["country"].value_counts().head(15))

print("\nSample of 'Not specified' rows (original location values):")
print(df[df["country"] == "Not specified"]["location"].value_counts().head(15))

print("\nAll unique country values found (sorted):")
for c in sorted(df["country"].unique()):
    print(c)
print("\n--- Remaining countries (continued) ---")
for c in sorted(df["country"].unique()):
    print(c)

print("\n--- Rows where country = 'Remote Africa' ---")
print(df[df["country"] == "Remote Africa"]["location"].unique())

print("\n--- Checking for any other suspicious short/odd values ---")
suspicious = [c for c in df["country"].unique() if len(c) <= 3 or "Remote" in c or "(" in c]
print(suspicious)
df.to_csv("data/master_dataset_cleaned.csv", index=False)
print("\nSaved to data/master_dataset_cleaned.csv")