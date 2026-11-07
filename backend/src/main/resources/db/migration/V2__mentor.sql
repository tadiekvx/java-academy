-- The AI mentor's conversation log (docs/curriculum/04-ai-mentor-policy.md §8) and scores for
-- written explanations. Both are append-only.

create table mentor_message (
    id               bigint generated always as identity primary key,
    learner_id       bigint      not null references learner (id),
    exercise_id      text        not null,
    created_at       timestamptz not null,
    role             text        not null check (role in ('learner', 'mentor')),
    kind             text        not null check (kind in ('question', 'help', 'follow_up_question', 'follow_up_answer', 'follow_up_feedback')),
    -- For mentor help: the assistance level given (0 = H0 … 4 = H4). For learner messages: the level answered at.
    level            integer     not null check (level between 0 and 4),
    content          text        not null,
    -- Code shown with a mentor message, only after it compiled, ran and passed the leak check.
    code             text,
    -- passed | withheld_leak | withheld_failed; null when the mentor proposed no code.
    code_check       text check (code_check in ('passed', 'withheld_leak', 'withheld_failed')),
    -- Learner messages: whether the model classified the message as a direct request for the solution.
    solution_request boolean     not null default false,
    -- follow_up_feedback: rubric score 0–2 for the learner's answer.
    score            integer check (score between 0 and 2),
    model            text
);

create index mentor_message_by_learner on mentor_message (learner_id, created_at);

create table explanation_score (
    attempt_id  bigint primary key references attempt (id),
    score       integer     not null check (score between 0 and 2),
    rationale   text        not null,
    feedback    text        not null,
    -- 'ai:<model id>' for provisional AI scores; 'human:<learner id>' once a reviewer scores it.
    scored_by   text        not null,
    provisional boolean     not null,
    scored_at   timestamptz not null
);
