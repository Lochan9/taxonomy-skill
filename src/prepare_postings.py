import json
from pathlib import Path

import pandas as pd

input_path = Path("data/raw/usajobs_data_analyst.json")
output_path = Path("data/processed/usajobs_postings.csv")

data = json.loads(input_path.read_text(encoding="utf-8"))
items = data["SearchResult"]["SearchResultItems"]

rows = []

for item in items:
    job = item["MatchedObjectDescriptor"]
    details = job.get("UserArea", {}).get("Details", {})

    duties = details.get("MajorDuties", [])
    categories = job.get("JobCategory", [])

    row = {
        "posting_id": item.get("MatchedObjectId", ""),
        "title": job.get("PositionTitle", ""),
        "organization": job.get("OrganizationName", ""),
        "department": job.get("DepartmentName", ""),
        "location": job.get("PositionLocationDisplay", ""),
        "category": " | ".join(c.get("Name", "") for c in categories),
        "job_summary": details.get("JobSummary", ""),
        "duties_text": " ".join(duties),
        "qualifications_text": job.get("QualificationSummary", ""),
        "requirements_text": details.get("Requirements", ""),
        "evaluations_text": details.get("Evaluations", ""),
        "education_text": details.get("Education", ""),
        "posted_date": job.get("PublicationStartDate", ""),
        "closing_date": job.get("ApplicationCloseDate", ""),
        "source_url": job.get("PositionURI", ""),
    }

    row["raw_text"] = "\n".join(
        [
            row["job_summary"],
            row["duties_text"],
            row["qualifications_text"],
            row["requirements_text"],
            row["evaluations_text"],
            row["education_text"],
        ]
    )

    rows.append(row)

df = pd.DataFrame(rows)
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} structured postings to {output_path}")