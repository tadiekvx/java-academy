-- Remember what the learner saw as well as what they submitted, so returning to a lesson can show
-- their last answer and its result. Reports are null for attempts made before this migration.
alter table attempt add column report jsonb;

-- A learner can mark a lesson finished by hand (it also counts as finished once every exercise is passed).
alter table lesson_visit add column completed_at timestamptz;
