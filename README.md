# Team B — Skill Taxonomy Project

This project extracts skills from job postings and maps them to the ESCO skill taxonomy.

## Data sources

- **USAJOBS:** 25 Data Analyst postings with complete duties and qualifications.
- **ESCO v1.2.0:** 14,579 English skill and knowledge concepts.
- **Adzuna:** Tested but not selected because descriptions were truncated.
- **LinkedIn dataset:** Being evaluated as a secondary source.

## Project structure

```text
data/processed/   Clean postings and skill matches
data/raw/         Raw API data (not committed)
data/reference/   ESCO reference data
src/              Data collection and processing scripts
reports/          Progress summaries




Setup
python3 -m venv .venv
source .venv/bin/activate
pip install requests pandas python-dotenv

Create .env:

USAJOBS_EMAIL=your_email
USAJOBS_API_KEY=your_key
Run
python src/fetch_usajobs.py
python src/prepare_postings.py
python src/fetch_esco.py
python src/prepare_esco.py
python src/match_esco_skills.py
Current results
25 job postings
22 unique titles
14,579 ESCO concepts
184 preliminary skill matches
All 25 postings received matches

The matches are an initial baseline and still require LLM-based extraction and manual validation.
