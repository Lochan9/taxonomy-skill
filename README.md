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
