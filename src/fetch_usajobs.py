import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

email = os.environ["USAJOBS_EMAIL"]
api_key = os.environ["USAJOBS_API_KEY"]

url = "https://data.usajobs.gov/api/search"
headers = {
    "Host": "data.usajobs.gov",
    "User-Agent": email,
    "Authorization-Key": api_key,
}
params = {
    "Keyword": "Data Analyst",
    "ResultsPerPage": 25,
}

response = requests.get(url, headers=headers, params=params, timeout=30)
response.raise_for_status()
data = response.json()

items = data["SearchResult"]["SearchResultItems"]
output = Path("data/raw/usajobs_data_analyst.json")
output.write_text(json.dumps(data, indent=2), encoding="utf-8")

print(f"Saved {len(items)} postings to {output}")