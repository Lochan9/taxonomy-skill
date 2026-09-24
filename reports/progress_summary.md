# Team B: Skill Taxonomy Progress Summary

## Objective
Develop a skill taxonomy from job-posting text and compare the extracted skills with the ESCO reference taxonomy.

## Public data sources evaluated

### USAJOBS
- Selected as the pilot job-posting source.
- Provides complete duties and qualification text through a public API.
- Current pilot: 25 Data Analyst postings.
- Limitation: postings represent the U.S. federal government sector.

### ESCO
- Selected as the reference skill taxonomy.
- Downloaded 14,579 English skill and knowledge concepts.
- Includes preferred labels, alternative labels, descriptions, skill types, reuse levels, and parent-skill relationships.
- 14,446 concepts contain descriptions.
- 4,977 concepts contain parent-skill links.

### Adzuna
- API access was successfully tested.
- Not selected as the primary source because the returned job descriptions were shortened or truncated.

## Pilot dataset quality
- 25 job postings
- 22 unique job titles
- 0 duplicate posting IDs
- 0 postings with empty text

## Preliminary matching
- Exact ESCO-label matching produced 184 candidate job-skill matches.
- All 25 postings received at least one candidate match.
- Average: 7.4 candidate skills per posting.
- Current results include generic or ambiguous terms and are not the final taxonomy.

## Next steps
- Use an LLM to extract job-specific skills.
- Map extracted skills to ESCO concepts.
- Remove generic and ambiguous matches.
- Validate a sample manually.
- Expand the job-posting dataset.