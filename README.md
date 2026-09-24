# Team B — Skill Taxonomy Project

This project develops a skill taxonomy from job-posting text. It extracts candidate skills from job descriptions and maps them to the European Skills, Competences, Qualifications and Occupations (ESCO) taxonomy.

This repository currently contains a pilot pipeline using USAJOBS postings and ESCO skills.

## Project objective

The project aims to:

1. Collect public job-posting data.
2. Extract skills from duties and qualification text.
3. Standardize extracted skills using ESCO.
4. Organize skills into a hierarchical taxonomy.
5. Evaluate the taxonomy using manual review and reference taxonomies.

## Data sources

### USAJOBS

USAJOBS provides complete job descriptions, duties and qualification requirements through its public API.

Current pilot dataset:

- 25 Data Analyst postings
- 22 unique job titles
- No duplicate posting IDs
- No postings with empty text

An API key is required:

https://developer.usajobs.gov/

### ESCO

ESCO is the reference skill taxonomy used in this project.

Current dataset:

- ESCO API version: `v1.2.0`
- 14,579 English skill and knowledge concepts
- 14,446 concepts with descriptions
- 4,977 concepts with parent-skill relationships

ESCO API:

https://ec.europa.eu/esco/api

### Other sources evaluated

- **Adzuna:** API worked, but returned shortened job descriptions.
- **LinkedIn dataset on Hugging Face:** Contains approximately 124,000 postings and is being considered as a secondary source. Its licensing and provenance must be verified before primary use.

## Repository structure

```text
taxonomy-skill-project/
├── data/
│   ├── processed/
│   │   ├── usajobs_postings.csv
│   │   └── usajobs_esco_matches.csv
│   ├── raw/
│   │   ├── usajobs_data_analyst.json
│   │   └── esco_skills_v1_2_0.json
│   └── reference/
│       ├── esco_skills_en.csv
│       └── esco_skills_sample.json
├── reports/
│   └── progress_summary.md
├── src/
│   ├── fetch_usajobs.py
│   ├── prepare_postings.py
│   ├── fetch_esco.py
│   ├── prepare_esco.py
│   └── match_esco_skills.py
├── .gitignore
├── README.md
└── .env
