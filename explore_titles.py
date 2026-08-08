import pandas as pd

df = pd.read_csv("data/master_dataset_v3.csv")
pd.set_option('display.max_rows', None)
print(df["title"].value_counts())
import pandas as pd
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # makes results consistent/reproducible across runs

df = pd.read_csv("data/master_dataset_v3.csv")

def detect_language(title):
    try:
        return detect(title)
    except:
        return "unknown"

df["detected_language"] = df["title"].apply(detect_language)

print("=== Language breakdown ===")
print(df["detected_language"].value_counts())

print("\n=== Non-English titles (sample) ===")
non_english = df[df["detected_language"] != "en"]
print(f"Total non-English: {len(non_english)}")
print(non_english[["title", "detected_language"]].to_string())
language_names = {
    "en": "English", "fr": "French", "ro": "Romanian", "it": "Italian",
    "de": "German", "nl": "Dutch", "es": "Spanish", "ca": "Catalan",
    "pt": "Portuguese", "id": "Indonesian", "hr": "Croatian", "tl": "Tagalog",
    "af": "Afrikaans", "lt": "Lithuanian", "no": "Norwegian", "et": "Estonian",
    "sl": "Slovenian", "pl": "Polish", "sv": "Swedish", "da": "Danish"
}

non_english["language_full_name"] = non_english["detected_language"].map(language_names)

non_english[["title", "detected_language", "language_full_name"]].to_csv(
    "data/titles_to_review.csv", index=False
)
print("\nSaved to data/titles_to_review.csv")
pd.set_option('display.max_colwidth', None)

partial_matches = [
    "Consultor (a) Individual",
    "Recrutement D'un (E) Chef",
    "Consultant Individuel Pour L'audit",
    "Spécialiste De La Gestion Financière",
    "Recrutement D'un (01) Spécialiste",
    "Termes De Référence Pour Des Services",
    "Consultoria Individual Especializada",
    "Recrutement D'un Consultant Chargé",
]

for partial in partial_matches:
    matches = df[df["title"].str.contains(partial, case=False, na=False, regex=False)]
    for title in matches["title"]:
        print(repr(title))
        print("---")
