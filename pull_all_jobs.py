import requests
import pandas as pd
from bs4 import BeautifulSoup

sources_df = pd.read_csv("sources.csv")
active_sources = sources_df[sources_df["active"] == True]

all_jobs = []

def scrape_devnetjobs():
    url = "https://devnetjobs.org/standard_jobs.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    job_links = soup.find_all("a", class_="text-dark")

    jobs = []
    for link in job_links:
        title_tag = link.find("span", id=lambda x: x and x.endswith("lblJobTitle"))
        org_tag = link.find("span", id=lambda x: x and x.endswith("lblJobCo"))
        location_tag = link.find("span", id=lambda x: x and x.endswith("lblLocation"))
        deadline_tag = link.find("span", id=lambda x: x and x.endswith("lblApplyDate"))

        jobs.append({
            "organization": org_tag.text.strip() if org_tag else None,
            "title": title_tag.text.strip() if title_tag else None,
            "location": location_tag.text.strip() if location_tag else None,
            "date_posted": None,
            "deadline": deadline_tag.text.strip() if deadline_tag else None,
            "source_url": link.get("href"),
        })
    return jobs

for row in active_sources.itertuples():
    print(f"Fetching from {row.name}...")

    if row.method == "api":
        if row.platform == "greenhouse":
            api_url = f"https://boards-api.greenhouse.io/v1/boards/{row.identifier}/jobs"
            response = requests.get(api_url)
            jobs_data = response.json().get("jobs", [])
            for job in jobs_data:
                all_jobs.append({
                    "organization": row.name,
                    "title": job.get("title"),
                    "location": job.get("location", {}).get("name"),
                    "date_posted": job.get("first_published"),
                    "deadline": None,
                    "source_url": job.get("absolute_url"),
                })
        elif row.platform == "smartrecruiters":
            api_url = f"https://api.smartrecruiters.com/v1/companies/{row.identifier}/postings"
            response = requests.get(api_url)
            jobs_data = response.json().get("content", [])
            for job in jobs_data:
                all_jobs.append({
                    "organization": row.name,
                    "title": job.get("name"),
                    "location": job.get("location", {}).get("city"),
                    "date_posted": job.get("releasedDate"),
                    "deadline": None,
                    "source_url": job.get("ref"),
                })

    elif row.method == "scrape":
        if row.platform == "devnetjobs":
            all_jobs.extend(scrape_devnetjobs())

    print(f"{row.name}: {len([j for j in all_jobs if j['organization'] == row.name])} jobs found")

jobs_df = pd.DataFrame(all_jobs)
jobs_df.to_csv("data/master_dataset.csv", index=False)
print(f"\nTotal jobs collected: {len(jobs_df)}")
print("Saved to data/master_dataset.csv")