import { useEffect, useState } from "react";
import { api, NotFoundError } from "../api";
import { useAuth } from "../auth";
import { EXERCISE_LOOK } from "../look";
import type { ExerciseStatus, ExerciseView } from "../types";
import { CodeExercise } from "./exercises/CodeExercise";
import { ExplainExercise } from "./exercises/ExplainExercise";
import { ParsonsExercise } from "./exercises/ParsonsExercise";
import { PredictExercise } from "./exercises/PredictExercise";
import { PlainMarkdown } from "./Markdown";
import { MentorPanel } from "./MentorPanel";


interface Props {
  id: string;
  number: number;
  status?: ExerciseStatus;
  onRecorded?: () => void;
}

/** Loads one exercise and renders the widget for its type. */
export function Exercise({ id, number, status, onRecorded }: Props) {
  const [exercise, setExercise] = useState<ExerciseView | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { learner } = useAuth();
  const [attemptCount, setAttemptCount] = useState(0);
  const recorded = () => {
    setAttemptCount((n) => n + 1);
    onRecorded?.();
  };

  useEffect(() => {
    api
      .exercise(id)
      .then(setExercise)
      .catch((e) => setError(e instanceof NotFoundError ? "This exercise isn't available." : String(e)));
  }, [id]);

  if (error) {
    return <p className="notice error">{error}</p>;
  }
  if (!exercise) {
    return <div className="exercise loading">Loading exercise…</div>;
  }
  const look = EXERCISE_LOOK[exercise.type];
  const Icon = look.icon;
  return (
    <section className={`exercise exercise-${exercise.type.toLowerCase()} ${look.hue}`} aria-labelledby={`${id}-title`}>
      <header className="exercise-header">
        <span className="icon-tile small" aria-hidden="true">
          <Icon size={18} />
        </span>
        <span className="exercise-kind">
          Exercise {number} · {look.label}
        </span>
        <h3 id={`${id}-title`}>{exercise.title}</h3>
        {status && <StatusBadge status={status} />}
      </header>
      <div className="exercise-prompt">
        <PlainMarkdown text={exercise.prompt} />
      </div>
      {exercise.type === "PREDICT" && <PredictExercise exercise={exercise} last={status?.last} onRecorded={recorded} />}
      {exercise.type === "PARSONS" && <ParsonsExercise exercise={exercise} last={status?.last} onRecorded={recorded} />}
      {(exercise.type === "WRITE" || exercise.type === "DEBUG" || exercise.type === "MODIFY") && (
        <CodeExercise exercise={exercise} last={status?.last} onRecorded={onRecorded} />
      )}
      {exercise.type === "EXPLAIN" && <ExplainExercise exercise={exercise} last={status?.last} onRecorded={recorded} />}
      {learner && (exercise.type === "PREDICT" || exercise.type === "PARSONS" || exercise.type === "EXPLAIN") && (
        <MentorPanel exerciseId={exercise.id} attemptCount={attemptCount} />
      )}
    </section>
  );
}

function StatusBadge({ status }: { status: ExerciseStatus }) {
  if (status.passedIndependently) {
    return <span className="status-badge done">✓ Done on your own</span>;
  }
  if (status.passed) {
    return <span className="status-badge assisted">✓ Done</span>;
  }
  if (status.pendingReview) {
    return <span className="status-badge pending">⏳ Awaiting review</span>;
  }
  if (status.attempts > 0) {
    return (
      <span className="status-badge tried">
        {status.attempts} attempt{status.attempts === 1 ? "" : "s"} so far
      </span>
    );
  }
  return null;
}
