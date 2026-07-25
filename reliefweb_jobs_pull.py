import requests

api_url = "https://api.reliefweb.int/v2/jobs"
app_name = "naomi-ngo-talent-analysis"

response = requests.get(api_url, params={"appname": app_name, "limit": 20})
print(response.status_code)
print(response.json())