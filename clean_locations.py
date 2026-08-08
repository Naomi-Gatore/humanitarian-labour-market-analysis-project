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
    "Africa", "Multiple Locations Considered","Remote Africa",
]
# ============================================
# ADD THIS REGION MAPPING DICTIONARY HERE
# ============================================
region_mapping = {
    # East Africa
    "Kenya": "East Africa",
    "Uganda": "East Africa",
    "Tanzania": "East Africa",
    "Ethiopia": "East Africa",
    "Rwanda": "East Africa",
    "Burundi": "East Africa",
    "South Sudan": "East Africa",
    "Somalia": "East Africa",
    "Djibouti": "East Africa",
    "Eritrea": "East Africa",
    
    # West Africa
    "Nigeria": "West Africa",
    "Ghana": "West Africa",
    "Senegal": "West Africa",
    "Ivory Coast": "West Africa",
    "Côte d'Ivoire": "West Africa",
    "Mali": "West Africa",
    "Burkina Faso": "West Africa",
    "Guinea": "West Africa",
    "Benin": "West Africa",
    "Togo": "West Africa",
    "Liberia": "West Africa",
    "Sierra Leone": "West Africa",
    "Gambia": "West Africa",
    "Niger": "West Africa",
    
    # Central Africa
    "Democratic Republic of Congo": "Central Africa",
    "DRC": "Central Africa",
    "Congo": "Central Africa",
    "Central African Republic": "Central Africa",
    "CAR": "Central Africa",
    "Chad": "Central Africa",
    "Cameroon": "Central Africa",
    "Gabon": "Central Africa",
    
    # Southern Africa
    "South Africa": "Southern Africa",
    "Zimbabwe": "Southern Africa",
    "Zambia": "Southern Africa",
    "Malawi": "Southern Africa",
    "Mozambique": "Southern Africa",
    "Angola": "Southern Africa",
    "Namibia": "Southern Africa",
    "Botswana": "Southern Africa",
    "Lesotho": "Southern Africa",
    "Eswatini": "Southern Africa",
    
    # North Africa
    "Egypt": "North Africa",
    "Morocco": "North Africa",
    "Algeria": "North Africa",
    "Tunisia": "North Africa",
    "Libya": "North Africa",
    "Sudan": "North Africa",
    
    # Europe
    "UK": "Europe",
    "United Kingdom": "Europe",
    "Switzerland": "Europe",
    "Netherlands": "Europe",
    "France": "Europe",
    "Germany": "Europe",
    "Italy": "Europe",
    "Spain": "Europe",
    "Belgium": "Europe",
    "Denmark": "Europe",
    "Sweden": "Europe",
    "Norway": "Europe",
    "Finland": "Europe",
    "Ireland": "Europe",
    "Austria": "Europe",
    "Portugal": "Europe",
    "Greece": "Europe",
    "Poland": "Europe",
    "Romania": "Europe",
    "Ukraine": "Europe",
    
    # North America
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    
    # South America
    "Brazil": "South America",
    "Argentina": "South America",
    "Colombia": "South America",
    "Peru": "South America",
    "Chile": "South America",
    "Ecuador": "South America",
    "Bolivia": "South America",
    "Paraguay": "South America",
    "Uruguay": "South America",
    "Venezuela": "South America",
    
    # Asia
    "India": "Asia",
    "China": "Asia",
    "Japan": "Asia",
    "South Korea": "Asia",
    "Indonesia": "Asia",
    "Philippines": "Asia",
    "Vietnam": "Asia",
    "Thailand": "Asia",
    "Malaysia": "Asia",
    "Singapore": "Asia",
    "Pakistan": "Asia",
    "Bangladesh": "Asia",
    "Nepal": "Asia",
    "Sri Lanka": "Asia",
    "Cambodia": "Asia",
    "Laos": "Asia",
    "Myanmar": "Asia",
    
    # Middle East
    "UAE": "Middle East",
    "United Arab Emirates": "Middle East",
    "Lebanon": "Middle East",
    "Jordan": "Middle East",
    "Israel": "Middle East",
    "Palestine": "Middle East",
    "Syria": "Middle East",
    "Iraq": "Middle East",
    "Yemen": "Middle East",
    "Saudi Arabia": "Middle East",
    "Qatar": "Middle East",
    "Kuwait": "Middle East",
    "Oman": "Middle East",
    "Bahrain": "Middle East",
    
    # Oceania
    "Australia": "Oceania",
    "New Zealand": "Oceania",
    "Fiji": "Oceania",
    "Papua New Guinea": "Oceania",
    
    # Special
    "Not specified": "Not specified"
}
additional_region_mapping = {
    "Palestinian Territory": "Middle East",
    "Turkey": "Europe",
    "Madagascar": "Southern Africa",
    "Syrian Arab Republic": "Middle East",
    "Afghanistan": "Asia",
    "Albania": "Europe",
    "New Caledonia": "Oceania",
    "Costa Rica": "Central America",
    "Hungary": "Europe",
    "Bulgaria": "Europe",
    "Grenada": "Caribbean",
    "Macau": "Asia",
    "Barbados": "Caribbean",
    "Netherlands Antilles": "Caribbean",
    "Equatorial Guinea": "Central Africa",
    "Guatemala": "Central America",
    "Uzbekistan": "Asia",
    "Palau": "Oceania",
    "Guyana": "South America",
    "Cape Verde": "West Africa",
}

region_mapping.update(additional_region_mapping)
def clean_location(raw_location):
    if pd.isna(raw_location):
        return "Not specified", "Not specified"

    text = raw_location.replace("Location: ", "").strip()

    if text in non_country_values:
        return "Not specified", "Not specified"

    work_arrangement = "Onsite"
    if "Hybrid" in text:
        work_arrangement = "Hybrid"
    elif "Remote" in text:
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
# ============================================
# ADD THE 2 LINES RIGHT HERE (between 206 and 208)
# ============================================
df["country_region"] = df["country"].map(region_mapping)
df["country_region"] = df["country_region"].fillna("Other")

# ============================================
# PRINT RESULTS
# ============================================
print(f"Unique countries found: {df['country'].nunique()}")
print(f"\nTop 15 countries by job count:")
print(df["country"].value_counts().head(15))

print("\n Work Arrangement Distribution:")
print(df["work_arrangement"].value_counts())

print("\n Region Distribution:")
print(df["country_region"].value_counts())

print("\nSample of 'Not specified' rows (original location values):")
print(df[df["country"] == "Not specified"]["location"].value_counts().head(15))

print("\nAll unique country values found (sorted):")
for c in sorted(df["country"].unique()):
    print(c)



print("\n--- Rows where country = 'Remote Africa' ---")
print(df[df["country"] == "Remote Africa"]["location"].unique())

print("\n--- Checking for any other suspicious short/odd values ---")
suspicious = [c for c in df["country"].unique() if len(c) <= 3 or "Remote" in c or "(" in c]
print(suspicious)
df.to_csv("data/master_dataset_cleaned.csv", index=False)
print("\nSaved to data/master_dataset_cleaned.csv")