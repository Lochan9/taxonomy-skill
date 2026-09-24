# Team B — Skill Taxonomy Project

This project extracts skills from job postings and maps them to the ESCO skill taxonomy.

## Data Sources

- **USAJOBS:** 25 Data Analyst postings
- **ESCO v1.2.0:** 14,579 English skill concepts
- **Adzuna:** Tested but not used because descriptions were truncated
- **LinkedIn dataset:** Under evaluation as a secondary source

## Project Structure

```text
data/processed/   Clean postings and skill matches
data/raw/         Raw API data (not committed)
data/reference/   ESCO reference data
src/              Collection and processing scripts
reports/          Progress summaries
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests pandas python-dotenv
```

Create a `.env` file:

```text
USAJOBS_EMAIL=your_email
USAJOBS_API_KEY=your_api_key
```

## Run the Pipeline

```bash
python src/fetch_usajobs.py
python src/prepare_postings.py
python src/fetch_esco.py
python src/prepare_esco.py
python src/match_esco_skills.py
```

## Current Results

- 25 job postings
- 22 unique job titles
- 14,579 ESCO concepts
- 184 preliminary job-skill matches
- All 25 postings received matches

These are preliminary candidate matches. LLM-based extraction and manual validation are the next steps.
