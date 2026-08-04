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