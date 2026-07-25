import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://devnetjobs.org/standard_jobs.aspx"

response = requests.get(url)
print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

job_links = soup.find_all("a", class_="text-dark")
print(f"Found {len(job_links)} job listings")

all_jobs = []

for link in job_links:
    title_tag = link.find("span", id=lambda x: x and x.endswith("lblJobTitle"))
    org_tag = link.find("span", id=lambda x: x and x.endswith("lblJobCo"))
    location_tag = link.find("span", id=lambda x: x and x.endswith("lblLocation"))
    deadline_tag = link.find("span", id=lambda x: x and x.endswith("lblApplyDate"))

    all_jobs.append({
        "organization": org_tag.text.strip() if org_tag else None,
        "title": title_tag.text.strip() if title_tag else None,
        "location": location_tag.text.strip() if location_tag else None,
        "deadline": deadline_tag.text.strip() if deadline_tag else None,
        "source_url": link.get("href"),
    })

jobs_df = pd.DataFrame(all_jobs)
print(jobs_df.head())
print(f"\nTotal jobs collected: {len(jobs_df)}")
jobs_df.to_csv("data/devnetjobs.csv", index=False)
print("Saved to data/devnetjobs.csv")