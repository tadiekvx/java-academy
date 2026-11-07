-- Learners, and the append-only record of what they did. Mastery is computed from this record
-- on read (docs/curriculum/01-curriculum-design.md §4), so nothing here is ever updated in place
-- except a learner's own profile.

create table learner (
    id             bigint generated always as identity primary key,
    email          text        not null unique,   -- stored lower-case
    display_name   text        not null,
    password_hash  text        not null,
    created_at     timestamptz not null default now(),
    -- Onboarding answers; onboarded_at is null until the learner finishes onboarding.
    onboarded_at   timestamptz,
    experience     text,
    weekly_hours   integer,
    goal           text
);

create table lesson_visit (
    learner_id       bigint      not null references learner (id),
    lesson_id        text        not null,
    first_visited_at timestamptz not null default now(),
    primary key (learner_id, lesson_id)
);

create table attempt (
    id               bigint generated always as identity primary key,
    learner_id       bigint      not null references learner (id),
    exercise_id      text        not null,
    submitted_at     timestamptz not null default now(),
    -- practice (lesson exercises) | retrieval (a scheduled knowledge check)
    context          text        not null check (context in ('practice', 'retrieval')),
    outcome          text        not null check (outcome in ('PASSED', 'FAILED', 'COMPILE_ERROR', 'PENDING_REVIEW')),
    tests_passed     integer     not null,
    tests_total      integer     not null,
    -- Highest mentor assistance level used before this attempt (0 = H0 … 4 = H4).
    assistance_level integer     not null default 0 check (assistance_level between 0 and 4),
    solution_viewed  boolean     not null default false,
    submission       jsonb       not null
);

create index attempt_by_learner on attempt (learner_id, submitted_at);
