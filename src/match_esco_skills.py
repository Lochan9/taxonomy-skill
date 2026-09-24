import re
from pathlib import Path

import pandas as pd

jobs = pd.read_csv("data/processed/usajobs_postings.csv")
esco = pd.read_csv("data/reference/esco_skills_en.csv")

output_path = Path("data/processed/usajobs_esco_matches.csv")
patterns = []

for _, skill in esco.iterrows():
    labels = [str(skill["preferred_label"])]

    labels = sorted(
        {label.strip() for label in labels if len(label.strip()) >= 2},
        key=len,
        reverse=True,
    )

    if not labels:
        continue

    pattern = re.compile(
        r"(?<!\w)("
        + "|".join(re.escape(label) for label in labels)
        + r")(?!\w)",
        flags=re.IGNORECASE,
    )

    patterns.append((skill, pattern))

matches = []

for _, job in jobs.iterrows():
    text = " ".join(
        [
            str(job.get("duties_text", "")),
            str(job.get("qualifications_text", "")),
        ]
    )

    for skill, pattern in patterns:
        found = pattern.search(text)

        if found:
            matches.append(
                {
                    "posting_id": job["posting_id"],
                    "job_title": job["title"],
                    "skill_uri": skill["skill_uri"],
                    "preferred_label": skill["preferred_label"],
                    "matched_text": found.group(0),
                    "skill_type": skill["skill_type"],
                    "reuse_level": skill["reuse_level"],
                    "broader_skill_labels": skill["broader_skill_labels"],
                }
            )

result = pd.DataFrame(matches)
result = result.drop_duplicates(
    subset=["posting_id", "preferred_label"]
)
result.to_csv(output_path, index=False)

print(f"Saved {len(result)} job-skill matches to {output_path}")
print(f"Jobs with matches: {result['posting_id'].nunique()} of {len(jobs)}")