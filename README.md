# Team B — Skill Taxonomy Project

This project extracts skills from public job postings and maps them to the ESCO skill taxonomy. Team B is responsible for building the skill taxonomy and later connecting it with Team A's task taxonomy.

## Current Status

- 25 USAJOBS Data Analyst postings
- 14,579 ESCO skill and knowledge concepts
- 184 preliminary exact-label matches
- Shared Supabase PostgreSQL database
- Nine-table shared data contract for Teams A and B

The current matches are baseline candidates, not the completed taxonomy.

## Repository Structure

```text
data/processed/    Clean job postings and baseline matches
data/raw/          Raw API responses; not committed
data/reference/    ESCO reference data
reports/           Progress reports
sql/               Shared database schema
src/               Data collection and processing scripts
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local `.env` file:

```text
USAJOBS_EMAIL=your_registered_email
USAJOBS_API_KEY=your_usajobs_api_key
DATABASE_URL=your_supabase_postgresql_connection_string
```

Never commit `.env` or share database credentials.

## Run the Data Pipeline

```bash
python src/fetch_usajobs.py
python src/prepare_postings.py
python src/fetch_esco.py
python src/prepare_esco.py
python src/match_esco_skills.py
```

## Shared Database

The database schema is stored in:

```text
sql/001_create_shared_schema.sql
```

It creates these tables:

- `postings`
- `reference_skills`
- `statements`
- `topics`
- `topic_membership`
- `hierarchy`
- `posting_skill_candidates`
- `statement_reference_map`
- `task_skill_map`

Load the processed data into the database:

```bash
python src/load_to_database.py
```

Current database contents:

- 25 postings
- 14,579 ESCO concepts
- 184 baseline matches

## Next Step

The next stage is to extract atomic skill statements from job duties and qualifications, manually evaluate extraction quality, and map the extracted statements to ESCO concepts.
