import json
import time
from pathlib import Path

import requests

url = "https://ec.europa.eu/esco/api/resource/skill"

params = {
    "isInScheme": "http://data.europa.eu/esco/concept-scheme/skills",
    "language": "en",
    "limit": 1000,
    "selectedVersion": "v1.2.0",
    "viewObsolete": "false",
}

all_skills = []
offset = 0
total = None

while total is None or len(all_skills) < total:
    params["offset"] = offset

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    data = response.json()

    page = list(data.get("_embedded", {}).values())
    total = data["total"]

    if not page:
        break

    all_skills.extend(page)
    offset += 1

    print(f"Downloaded {len(all_skills)} of {total}")
    time.sleep(0.2)

output = Path("data/raw/esco_skills_v1_2_0.json")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(
    json.dumps(all_skills, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(f"Saved {len(all_skills)} ESCO skills to {output}")