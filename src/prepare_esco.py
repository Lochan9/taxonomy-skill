import json
from pathlib import Path

import pandas as pd

input_path = Path("data/raw/esco_skills_v1_2_0.json")
output_path = Path("data/reference/esco_skills_en.csv")

skills = json.loads(input_path.read_text(encoding="utf-8"))
rows = []

for skill in skills:
    links = skill.get("_links", {})

    broader = links.get("broaderSkill", [])
    skill_type = links.get("hasSkillType", [])
    reuse_level = links.get("hasReuseLevel", [])

    english_description = skill.get("description", {}).get("en", {})
    if isinstance(english_description, dict):
        english_description = english_description.get("literal", "")

    alternatives = skill.get("alternativeLabel", {}).get("en", [])
    if isinstance(alternatives, str):
        alternatives = [alternatives]

    rows.append(
        {
            "skill_uri": skill.get("uri", ""),
            "preferred_label": skill.get("preferredLabel", {}).get("en", ""),
            "alternative_labels": " | ".join(alternatives),
            "description": english_description,
            "skill_type": skill_type[0].get("title", "") if skill_type else "",
            "reuse_level": reuse_level[0].get("title", "") if reuse_level else "",
            "broader_skill_uris": " | ".join(x.get("uri", "") for x in broader),
            "broader_skill_labels": " | ".join(x.get("title", "") for x in broader),
            "status": skill.get("status", ""),
        }
    )

df = pd.DataFrame(rows)
df = df.drop_duplicates(subset="skill_uri")
df = df[df["preferred_label"].str.strip().ne("")]

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} English ESCO skills to {output_path}")