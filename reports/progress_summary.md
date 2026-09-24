# Team B: Skill Taxonomy Progress Summary

## Objective

Develop a skill taxonomy from public job postings and compare the extracted skills with ESCO and other reference taxonomies.

## Public Data Sources

### USAJOBS

- Selected as the pilot job-posting source.
- Provides complete duties and qualification text through a public API.
- Current pilot contains 25 Data Analyst postings.
- Limitation: the pilot represents U.S. federal employment only.

### ESCO

- Selected as the primary skill reference taxonomy.
- Downloaded 14,579 English skill and knowledge concepts.
- 14,446 concepts contain descriptions.
- 4,977 concepts contain parent-skill relationships.

### Adzuna

- API access was successfully tested.
- Not selected because the returned descriptions were shortened.

### Lightcast

- Identified as an additional reference for evaluating emerging skills.
- API access has not yet been requested.

## Pilot Data Quality

- 25 job postings
- 22 unique job titles
- 0 duplicate posting IDs
- 0 postings with empty text

## Shared Database

- Created a Supabase PostgreSQL database.
- Created the nine-table shared data contract for Teams A and B.
- Loaded 25 job postings.
- Loaded 14,579 ESCO concepts.
- Loaded 184 baseline skill matches.
- Added a reproducible SQL schema and database-loading script.
- Team-member invitations are still pending.

## Preliminary Matching

- Exact ESCO-label matching produced 184 candidate matches.
- All 25 postings received at least one candidate match.
- Average of 7.4 candidate skills per posting.
- Generic and ambiguous matches remain.
- These results are a baseline, not the completed taxonomy.

## Next Steps

- Invite Team A and Team B members to the database.
- Expand the job-posting corpus.
- Create the data-exploration notebook.
- Extract atomic skill statements.
- Build a manually labelled evaluation set.
- Measure extraction precision, recall and F1.
- Map extracted statements to ESCO concepts.