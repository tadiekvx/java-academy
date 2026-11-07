import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { api } from "../api";
import { PlainMarkdown } from "../components/Markdown";
import { CodeExercise } from "../components/exercises/CodeExercise";
import type { ExerciseView } from "../types";

/** A retrieval check: a fresh editor, no drafts, no lesson around it. */
export function CheckPage() {
  const { exerciseId = "" } = useParams();
  const [exercise, setExercise] = useState<ExerciseView | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    document.title = "Knowledge check · Java Engineering Academy";
    api.exercise(exerciseId).then(setExercise).catch((e) => setError(String(e)));
  }, [exerciseId]);

  if (error) {
    return <p className="notice error">{error}</p>;
  }
  if (!exercise) {
    return <p className="muted">Loading…</p>;
  }
  return (
    <div className="check-page">
      <nav className="breadcrumbs" aria-label="Breadcrumb">
        <Link to="/">Your progress</Link>
      </nav>
      <p className="exercise-kind">Knowledge check</p>
      <h1>{exercise.title}</h1>
      <p className="notice review">
        Do this one from memory: no notes, no earlier answers. Use <strong>Run</strong> as often as you like. Your first{" "}
        <strong>Check against tests</strong> is what counts.
      </p>
      <div className="exercise">
        <div className="exercise-prompt">
          <PlainMarkdown text={exercise.prompt} />
        </div>
        <CodeExercise exercise={exercise} mode="check" />
      </div>
    </div>
  );
}
