import pandas as pd

# Load the current final dataset
master_dataset_v3 = pd.read_csv("data/master_dataset_v3.csv")

# ============================================================
# STEP 1: Drop noise rows (not real job postings)
# ============================================================
noise_titles = [
    "General Interest Application",
    "General Interest",
    "General Application",
    "Application for General Consideration - Professionals",
    "Traineeship",
    "Board Members",
]

master_dataset_v4 = master_dataset_v3[~master_dataset_v3["title"].isin(noise_titles)].copy()

print(f"Rows before dropping noise: {len(master_dataset_v3)}")
print(f"Rows after dropping noise: {len(master_dataset_v4)}")

# ============================================================
# STEP 2: Flag genuinely non-English titles
# ============================================================
non_english_titles_with_language = {
    "Gestor De Campo - Auditoria Interna": "Spanish",
    "Spécialiste En Sauvegarde Sociales": "French",
    "Consultor (a) Individual - Elaboração": "Portuguese",
    "Recrutement D'un (E) Chef (Fe) Comptable": "French",
    "Assistant (E) Technique Au Volet Entrepreneuriat": "French",
    "Consultant Individuel Pour L'audit De La Performance": "French",
    "Consultor Em Comunicação E Imagem Institucional": "Portuguese",
    "Oficial Social Júnior": "Portuguese",
    "Un (E) Stagiaire Développement": "French",
    "Spécialiste De La Gestion Financière": "French",
    "Responsable De Recherche Pour La République Centrafricaine": "French",
    "Líder Brasil De Combustíveis": "Portuguese",
    "Recrutement D'un (01) Spécialiste En Passation": "French",
    "Termes De Référence Pour Des Services": "French",
    "Coordinador/A Nacional Y Especialista Social": "Spanish",
    "Consultoria Individual Especializada": "Portuguese",
    "Recrutement D'un Consultant Chargé De L'évaluation": "French",
    "Especialista Social De La Unidad": "Spanish",
    "Contrôleur De Gestion Junior": "French",
    "Formatrice/Tore E Focal Point Scuole": "Italian",
    "Medisch Secretariaat Antwerpen": "Dutch",
    "Referentieverpleegkundige in De Diabeteszorg": "Dutch",
    "Accueillant E Medibus Charleroi": "French",
    "Accueillant E Bruxelles": "French",
    "Psicologa E Operatrice Di Accoglienza": "Italian",
    "Contrôleur·euse De Gestion Junior": "French",
    "MEAL Officer RCCE": "French",
    "Seksjonssjef": "Norwegian",
    "Formatrice/Tore E Facilitatrice/Tore": "Italian",
    "Assistant.E Archiviste": "French",
    "Assistant.E Controle De Gestion Siege": "French",
    "Rwanda Recrutement Stagiaire": "French",
}

master_dataset_v4["title_language"] = "English"
master_dataset_v4["job_category"] = None
master_dataset_v4["seniority_level"] = None

for phrase, language in non_english_titles_with_language.items():
    mask = master_dataset_v4["title"].str.startswith(phrase, na=False)
    master_dataset_v4.loc[mask, "title_language"] = language
    master_dataset_v4.loc[mask, "job_category"] = "Non-English/Unclassified"
    master_dataset_v4.loc[mask, "seniority_level"] = "Non-English/Unclassified"

print(f"\nNon-English titles flagged: {(master_dataset_v4['title_language'] != 'English').sum()}")

# ============================================================
# STEP 3: Seniority level keyword mapping (English titles only)
# ============================================================
seniority_keywords = {
    "Leadership": ["chief", "director", "head of", "head,", "vice president",
                   "principal", "cluster director", "country director"],
    "Senior": ["senior", "sr.", "sr "],
    "Entry/Support": ["intern", "internship", "assistant", "trainee",
                      "fellowship", "junior", "entry"],
    "Consultant": ["consultant", "consultancy"],
}

def assign_seniority(title):
    if pd.isna(title):
        return "Not specified"
    title_lower = title.lower()
    for level, keywords in seniority_keywords.items():
        if any(keyword in title_lower for keyword in keywords):
            return level
    return "Mid/Standard"

is_unclassified = master_dataset_v4["seniority_level"] == "Non-English/Unclassified"
master_dataset_v4.loc[~is_unclassified, "seniority_level"] = (
    master_dataset_v4.loc[~is_unclassified, "title"].apply(assign_seniority)
)

# ============================================================
# STEP 4: Job category keyword mapping (English titles only)
# ============================================================
field_keywords = {
    "Health": ["health", "medical", "clinical", "nurse", "physician", "doctor",
               "psychiatr", "psycholog", "midwife", "pharmac", "epidemiolog",
               "surgeon", "obstetric", "gynecolog", "anesthesiolog"],
    "Finance": ["finance", "financial", "accountant", "accounting", "budget",
                "treasury", "controller", "audit"],
    "Legal": ["legal", "counsel", "paralegal", "litigation", "compliance"],
    "HR": ["human resource", "hr ", "hr&", "talent acquisition", "recruit",
           "people lead", "people operations"],
    "Logistics": ["logistic", "supply chain", "procurement", "warehouse"],
    "M&E": ["monitoring", "evaluation", "meal", "m&e", "mel "],
    "Communications": ["communications", "media", "press", "pr &", "journalist",
                        "editor", "content"],
    "Fundraising/Grants": ["fundraising", "grant", "donor", "philanthrop",
                            "resource mobilization", "resource mobilisation"],
    "Research": ["research", "scientist", "scientific"],
    "IT/Tech": ["it ", "ict", "software", "engineer", "developer", "data",
                "digital", "systems", "cloud", "ai "],
    "Program/Project Management": ["program", "programme", "project"],
    "Advocacy/Policy": ["advocacy", "policy", "policies"],
    "Operations/Admin": ["operations", "administrat", "office"],
}

def assign_job_category(title):
    if pd.isna(title):
        return "Not specified"
    title_lower = title.lower()
    for category, keywords in field_keywords.items():
        if any(keyword in title_lower for keyword in keywords):
            return category
    return "Other/Uncategorized"

master_dataset_v4.loc[~is_unclassified, "job_category"] = (
    master_dataset_v4.loc[~is_unclassified, "title"].apply(assign_job_category)
)

print("\n=== Job category breakdown (initial) ===")
print(master_dataset_v4["job_category"].value_counts())

# ============================================================
# STEP 4b: Additional keyword refinements for Other/Uncategorized
# ============================================================
additional_field_keywords = {
    "Health": ["laboratory", "lab "],
    "Fundraising/Grants": ["partnership"],
    "Program/Project Management": ["country director", "country representative", "country technical"],
    "Business Development/Sales": ["business development", "sales", "account manager", "investment", "market access"],
    "Safety/Security": ["safety", "security"],
    "Environment/Agriculture": ["environment", "agricultur", "climate", "sustainab"],
    "Training/Education": ["training", "education", "academic", "graduate trainee"],
}

def reassign_uncategorized(row):
    if row["job_category"] != "Other/Uncategorized":
        return row["job_category"]
    title_lower = row["title"].lower()
    for category, keywords in additional_field_keywords.items():
        if any(keyword in title_lower for keyword in keywords):
            return category
    return "Other/Uncategorized"

master_dataset_v4["job_category"] = master_dataset_v4.apply(reassign_uncategorized, axis=1)

print("\n=== Job category breakdown (after Step 4b refinement) ===")
print(master_dataset_v4["job_category"].value_counts())

# ============================================================
# STEP 4c: MSF "Medical" location fallback + Water/Sanitation keywords
# ============================================================
is_medical_location = master_dataset_v4["location"] == "Medical"
is_still_uncategorized = master_dataset_v4["job_category"] == "Other/Uncategorized"
master_dataset_v4.loc[is_medical_location & is_still_uncategorized, "job_category"] = "Health"

def catch_wash_titles(row):
    if row["job_category"] != "Other/Uncategorized":
        return row["job_category"]
    title_lower = row["title"].lower()
    if "water" in title_lower or "sanitation" in title_lower or "wash" in title_lower:
        return "Health"
    return row["job_category"]

master_dataset_v4["job_category"] = master_dataset_v4.apply(catch_wash_titles, axis=1)

print("\n=== Job category breakdown (after Step 4c Medical/WASH fixes) ===")
print(master_dataset_v4["job_category"].value_counts())

print("\n=== Seniority level breakdown (final) ===")
print(master_dataset_v4["seniority_level"].value_counts())

# ============================================================
# STEP 5: Save the final result
# ============================================================
master_dataset_v4.to_csv("data/master_dataset_v4.csv", index=False)
print("\nSaved to data/master_dataset_v4.csv")

# ============================================================
# VERIFICATION: Spot-check "Corporate Partnerships" row
# ============================================================
print("\n=== Checking 'Corporate Partnerships' row specifically ===")
check_row = master_dataset_v4[master_dataset_v4["title"].str.contains("Corporate Partnerships", case=False, na=False)]
print(check_row[["title", "job_category"]].to_string())