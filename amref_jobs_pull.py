import requests

api_url = "https://api.smartrecruiters.com/v1/companies/AmrefHealthAfrica4/postings"

response = requests.get(api_url)
print(response.status_code)
print(response.json())