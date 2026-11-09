import { useState } from "react";
import { useAuth } from "../../auth";
import { loadDraft, saveDraft } from "../../storage";
import type { ExerciseStatus, ExerciseView } from "../../types";
import { JavaCode } from "../JavaCode";
import { LoginPrompt } from "../LoginPrompt";
import { Results } from "../Results";
import { useAttempt } from "./useAttempt";

/** A short written explanation, saved for rubric scoring. */
export function ExplainExercise({ exercise, last, onRecorded }: { exercise: ExerciseView; last?: ExerciseStatus["last"]; onRecorded?: () => void }) {
  const { learner } = useAuth();
  const [text, setText] = useState(() => loadDraft(`draft:${exercise.id}`) ?? last?.submission.explanation ?? "");
  const attempt = useAttempt(exercise.id, "practice", onRecorded);
  const words = text.trim() === "" ? 0 : text.trim().split(/\s+/).length;

  return (
    <div className="explain-exercise">
      {exercise.relatedCode && (
        <>
          <p className="field-label">The code you're explaining</p>
          <JavaCode code={exercise.relatedCode} />
        </>
      )}
      <label className="field-label" htmlFor={`${exercise.id}-answer`}>
        Your explanation
      </label>
      <textarea
        id={`${exercise.id}-answer`}
        className="explain-input"
        rows={6}
        value={text}
        onChange={(e) => {
          setText(e.target.value);
          saveDraft(`draft:${exercise.id}`, e.target.value);
        }}
      />
      <p className="muted small">{words} words</p>
      {learner ? (
        <div className="button-row">
          <button
            type="button"
            className="button primary"
            disabled={words < 5 || attempt.busy}
            onClick={() => attempt.submit({ explanation: text })}
          >
            {attempt.busy ? "Saving…" : "Submit explanation"}
          </button>
        </div>
      ) : (
        <LoginPrompt action="submit your explanation" />
      )}
      {attempt.error && <p className="notice error">{attempt.error}</p>}
      {attempt.report && <Results report={attempt.report} />}
    </div>
  );
}
