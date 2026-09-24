import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

POSTINGS_FILE = PROJECT_ROOT / "data/processed/usajobs_postings.csv"
ESCO_FILE = PROJECT_ROOT / "data/reference/esco_skills_en.csv"
MATCHES_FILE = PROJECT_ROOT / "data/processed/usajobs_esco_matches.csv"


def nullable_text(value):
    if pd.isna(value):
        return None
    return str(value).strip()


def required_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def nullable_date(value):
    if pd.isna(value) or not str(value).strip():
        return None

    parsed = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed):
        return None

    return parsed.date()


def execute_batches(cursor, query, rows, batch_size=500):
    for start in range(0, len(rows), batch_size):
        batch = rows[start : start + batch_size]
        cursor.executemany(query, batch)


def load_postings(cursor):
    postings = pd.read_csv(POSTINGS_FILE)

    rows = []

    for _, row in postings.iterrows():
        rows.append(
            (
                required_text(row["posting_id"]),
                "USAJOBS",
                required_text(row["title"]),
                nullable_text(row["organization"]),
                nullable_text(row["department"]),
                nullable_text(row["location"]),
                nullable_text(row["category"]),
                nullable_text(row["job_summary"]),
                nullable_text(row["duties_text"]),
                nullable_text(row["qualifications_text"]),
                nullable_text(row["requirements_text"]),
                nullable_text(row["evaluations_text"]),
                nullable_text(row["education_text"]),
                nullable_date(row["posted_date"]),
                nullable_date(row["closing_date"]),
                nullable_text(row["source_url"]),
                required_text(row["raw_text"]),
            )
        )

    query = """
        insert into public.postings (
            posting_id,
            source,
            title,
            organization,
            department,
            location,
            category,
            job_summary,
            duties_text,
            qualifications_text,
            requirements_text,
            evaluations_text,
            education_text,
            posted_date,
            closing_date,
            source_url,
            raw_text
        )
        values (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        on conflict (posting_id) do update set
            source = excluded.source,
            title = excluded.title,
            organization = excluded.organization,
            department = excluded.department,
            location = excluded.location,
            category = excluded.category,
            job_summary = excluded.job_summary,
            duties_text = excluded.duties_text,
            qualifications_text = excluded.qualifications_text,
            requirements_text = excluded.requirements_text,
            evaluations_text = excluded.evaluations_text,
            education_text = excluded.education_text,
            posted_date = excluded.posted_date,
            closing_date = excluded.closing_date,
            source_url = excluded.source_url,
            raw_text = excluded.raw_text
    """

    execute_batches(cursor, query, rows)

    return len(rows)


def load_reference_skills(cursor):
    skills = pd.read_csv(ESCO_FILE)

    rows = []

    for _, row in skills.iterrows():
        rows.append(
            (
                required_text(row["skill_uri"]),
                "ESCO",
                "v1.2.0",
                required_text(row["preferred_label"]),
                nullable_text(row["alternative_labels"]),
                nullable_text(row["description"]),
                nullable_text(row["skill_type"]),
                nullable_text(row["reuse_level"]),
                nullable_text(row["broader_skill_uris"]),
                nullable_text(row["broader_skill_labels"]),
                nullable_text(row["status"]),
            )
        )

    query = """
        insert into public.reference_skills (
            skill_uri,
            reference_source,
            source_version,
            preferred_label,
            alternative_labels,
            description,
            skill_type,
            reuse_level,
            broader_skill_uris,
            broader_skill_labels,
            status
        )
        values (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        on conflict (skill_uri) do update set
            reference_source = excluded.reference_source,
            source_version = excluded.source_version,
            preferred_label = excluded.preferred_label,
            alternative_labels = excluded.alternative_labels,
            description = excluded.description,
            skill_type = excluded.skill_type,
            reuse_level = excluded.reuse_level,
            broader_skill_uris = excluded.broader_skill_uris,
            broader_skill_labels = excluded.broader_skill_labels,
            status = excluded.status
    """

    execute_batches(cursor, query, rows)

    return len(rows)


def load_candidate_matches(cursor):
    matches = pd.read_csv(MATCHES_FILE)

    matches = matches.drop_duplicates(
        subset=["posting_id", "skill_uri"]
    )

    rows = []

    for _, row in matches.iterrows():
        rows.append(
            (
                required_text(row["posting_id"]),
                required_text(row["skill_uri"]),
                nullable_text(row["matched_text"]),
                "exact_label",
            )
        )

    query = """
        insert into public.posting_skill_candidates (
            posting_id,
            skill_uri,
            matched_text,
            matching_method
        )
        values (%s, %s, %s, %s)
        on conflict (posting_id, skill_uri) do update set
            matched_text = excluded.matched_text,
            matching_method = excluded.matching_method
    """

    execute_batches(cursor, query, rows)

    return len(rows)


def main():
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is missing from .env")

    required_files = [
        POSTINGS_FILE,
        ESCO_FILE,
        MATCHES_FILE,
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing required file: {file_path}")

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:
            posting_count = load_postings(cursor)
            skill_count = load_reference_skills(cursor)
            match_count = load_candidate_matches(cursor)

            cursor.execute("select count(*) from public.postings")
            database_postings = cursor.fetchone()[0]

            cursor.execute("select count(*) from public.reference_skills")
            database_skills = cursor.fetchone()[0]

            cursor.execute(
                "select count(*) from public.posting_skill_candidates"
            )
            database_matches = cursor.fetchone()[0]

    print(f"Loaded {posting_count} postings from CSV")
    print(f"Loaded {skill_count} ESCO concepts from CSV")
    print(f"Loaded {match_count} baseline matches from CSV")
    print()
    print(f"Database postings: {database_postings}")
    print(f"Database reference skills: {database_skills}")
    print(f"Database baseline matches: {database_matches}")


if __name__ == "__main__":
    main()
