import requests

url = "https://boards-api.greenhouse.io/v1/boards/givedirectly/jobs?content=true"
response = requests.get(url)
jobs = response.json()["jobs"]

deadline_values = [job.get("application_deadline") for job in jobs]
print("Sample application_deadline values from GiveDirectly:")
print(deadline_values[:10])

non_null_count = sum(1 for d in deadline_values if d is not None)
print(f"\nJobs with actual deadline value: {non_null_count} out of {len(deadline_values)}")