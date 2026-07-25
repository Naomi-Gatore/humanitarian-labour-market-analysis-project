import requests

api_url = "https://boards-api.greenhouse.io/v1/boards/humanrightswatch/jobs?content=true"

response = requests.get(api_url)
print(response.status_code)
print(response.json())