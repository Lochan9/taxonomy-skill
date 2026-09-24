begin;

-- =========================================================
-- 1. SHARED JOB POSTINGS
-- =========================================================

create table if not exists public.postings (
    posting_id text primary key,
    source text not null default 'USAJOBS',
    title text not null,
    organization text,
    department text,
    location text,
    category text,
    job_summary text,
    duties_text text,
    qualifications_text text,
    requirements_text text,
    evaluations_text text,
    education_text text,
    posted_date date,
    closing_date date,
    source_url text,
    raw_text text not null,
    created_at timestamptz not null default now()
);

create index if not exists postings_title_idx
    on public.postings (title);

create index if not exists postings_source_idx
    on public.postings (source);


-- =========================================================
-- 2. REFERENCE SKILLS: ESCO AND LATER LIGHTCAST
-- =========================================================

create table if not exists public.reference_skills (
    skill_uri text primary key,
    reference_source text not null default 'ESCO',
    source_version text not null default 'v1.2.0',
    preferred_label text not null,
    alternative_labels text,
    description text,
    skill_type text,
    reuse_level text,
    broader_skill_uris text,
    broader_skill_labels text,
    status text,
    created_at timestamptz not null default now()
);

create index if not exists reference_skills_label_idx
    on public.reference_skills (preferred_label);

create index if not exists reference_skills_type_idx
    on public.reference_skills (skill_type);

create index if not exists reference_skills_source_idx
    on public.reference_skills (reference_source);


-- =========================================================
-- 3. ATOMIC TASK AND SKILL STATEMENTS
-- =========================================================

create table if not exists public.statements (
    statement_id uuid primary key default gen_random_uuid(),

    posting_id text not null
        references public.postings(posting_id)
        on delete cascade,

    statement_text text not null,

    kind text not null
        check (kind in ('task', 'skill')),

    source_section text,
    extraction_method text,
    model_name text,
    prompt_version text,

    confidence numeric(5,4)
        check (confidence between 0 and 1),

    raw_output jsonb,
    created_at timestamptz not null default now(),

    unique (posting_id, kind, statement_text)
);

create index if not exists statements_posting_idx
    on public.statements (posting_id);

create index if not exists statements_kind_idx
    on public.statements (kind);


-- =========================================================
-- 4. TOPICS OR CLUSTERS
-- =========================================================

create table if not exists public.topics (
    topic_id uuid primary key default gen_random_uuid(),

    kind text not null
        check (kind in ('task', 'skill')),

    topic_name text,
    description text,

    topic_size integer not null default 0
        check (topic_size >= 0),

    clustering_method text,
    representation_model text,

    is_leaf boolean not null default true,
    metadata jsonb,

    created_at timestamptz not null default now()
);

create index if not exists topics_kind_idx
    on public.topics (kind);


-- =========================================================
-- 5. STATEMENT-TO-TOPIC MEMBERSHIP
-- =========================================================

create table if not exists public.topic_membership (
    statement_id uuid not null
        references public.statements(statement_id)
        on delete cascade,

    topic_id uuid not null
        references public.topics(topic_id)
        on delete cascade,

    membership_score numeric(5,4)
        check (membership_score between 0 and 1),

    is_primary boolean not null default true,
    created_at timestamptz not null default now(),

    primary key (statement_id, topic_id)
);

create index if not exists topic_membership_topic_idx
    on public.topic_membership (topic_id);


-- =========================================================
-- 6. MULTI-LEVEL TAXONOMY HIERARCHY
-- =========================================================

create table if not exists public.hierarchy (
    parent_topic_id uuid not null
        references public.topics(topic_id)
        on delete cascade,

    child_topic_id uuid not null
        references public.topics(topic_id)
        on delete cascade,

    relation_type text not null default 'broader_than',

    hierarchy_level integer
        check (hierarchy_level >= 1),

    confidence numeric(5,4)
        check (confidence between 0 and 1),

    created_at timestamptz not null default now(),

    primary key (parent_topic_id, child_topic_id),

    check (parent_topic_id <> child_topic_id)
);

create index if not exists hierarchy_child_idx
    on public.hierarchy (child_topic_id);


-- =========================================================
-- 7. CURRENT EXACT-MATCH BASELINE RESULTS
-- =========================================================

create table if not exists public.posting_skill_candidates (
    posting_id text not null
        references public.postings(posting_id)
        on delete cascade,

    skill_uri text not null
        references public.reference_skills(skill_uri)
        on delete cascade,

    matched_text text,
    matching_method text not null default 'exact_label',

    is_validated boolean not null default false,

    validation_label text
        check (
            validation_label is null
            or validation_label in (
                'correct',
                'incorrect',
                'uncertain'
            )
        ),

    reviewer text,
    created_at timestamptz not null default now(),

    primary key (posting_id, skill_uri)
);

create index if not exists posting_skill_candidates_skill_idx
    on public.posting_skill_candidates (skill_uri);


-- =========================================================
-- 8. EXTRACTED SKILLS MAPPED TO ESCO OR LIGHTCAST
-- =========================================================

create table if not exists public.statement_reference_map (
    statement_id uuid not null
        references public.statements(statement_id)
        on delete cascade,

    skill_uri text not null
        references public.reference_skills(skill_uri)
        on delete cascade,

    mapping_method text not null,

    similarity_score numeric(5,4)
        check (similarity_score between 0 and 1),

    rank integer
        check (rank >= 1),

    is_validated boolean not null default false,

    validation_label text
        check (
            validation_label is null
            or validation_label in (
                'correct',
                'incorrect',
                'uncertain'
            )
        ),

    reviewer text,
    evidence jsonb,
    created_at timestamptz not null default now(),

    primary key (statement_id, skill_uri)
);

create index if not exists statement_reference_skill_idx
    on public.statement_reference_map (skill_uri);


-- =========================================================
-- 9. TEAM A TASKS MAPPED TO TEAM B SKILLS
-- =========================================================

create table if not exists public.task_skill_map (
    task_topic_id uuid not null
        references public.topics(topic_id)
        on delete cascade,

    skill_topic_id uuid not null
        references public.topics(topic_id)
        on delete cascade,

    affinity_score numeric(5,4) not null
        check (affinity_score between 0 and 1),

    semantic_similarity numeric(5,4)
        check (semantic_similarity between 0 and 1),

    cooccurrence_score numeric(5,4)
        check (cooccurrence_score between 0 and 1),

    onet_prior_score numeric(5,4)
        check (onet_prior_score between 0 and 1),

    method text,
    evidence jsonb,
    created_at timestamptz not null default now(),

    primary key (task_topic_id, skill_topic_id),

    check (task_topic_id <> skill_topic_id)
);

create index if not exists task_skill_map_skill_idx
    on public.task_skill_map (skill_topic_id);

commit;