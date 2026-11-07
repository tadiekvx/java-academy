import { useState } from "react";
import { useAuth } from "../../auth";
import type { ExerciseView } from "../../types";
import { JavaCode } from "../JavaCode";
import { LoginPrompt } from "../LoginPrompt";
import { useAttempt } from "./useAttempt";

/** Learner commits to a prediction; only then is the real output revealed, line by line. */
export function PredictExercise({ exercise, onRecorded }: { exercise: ExerciseView; onRecorded?: () => void }) {
  const { learner } = useAuth();
  const [prediction, setPrediction] = useState("");
  const attempt = useAttempt(exercise.id, "practice", onRecorded);
  const report = attempt.report;

  return (
    <div className="predict-exercise">
      <JavaCode code={exercise.files["Main.java"] ?? ""} />
      {!report ? (
        <>
          <label className="field-label" htmlFor={`${exercise.id}-prediction`}>
            Your prediction (what the program prints, one line per line of output)
          </label>
          <textarea
            id={`${exercise.id}-prediction`}
            className="prediction-input"
            rows={6}
            spellCheck={false}
            value={prediction}
            onChange={(e) => setPrediction(e.target.value)}
          />
          {learner ? (
            <div className="button-row">
              <button
                type="button"
                className="button primary"
                disabled={prediction.trim() === "" || attempt.busy}
                onClick={() => attempt.submit({ prediction })}
              >
                {attempt.busy ? "Running…" : "Lock in prediction and run"}
              </button>
            </div>
          ) : (
            <LoginPrompt action="check your prediction" />
          )}
        </>
      ) : (
        <PredictionComparison prediction={prediction} actual={report.actualOutput ?? ""} message={report.message} passed={report.outcome === "PASSED"} />
      )}
      {attempt.error && <p className="notice error">{attempt.error}</p>}
    </div>
  );
}

function PredictionComparison(props: { prediction: string; actual: string; message: string; passed: boolean }) {
  const predicted = lines(props.prediction);
  const actual = lines(props.actual);
  const rows = Math.max(predicted.length, actual.length);
  return (
    <section className={`results ${props.passed ? "outcome-passed" : "outcome-failed"}`} aria-live="polite">
      <p className="results-headline">
        {props.passed && <span aria-hidden="true">✓ </span>}
        {props.message}
      </p>
      <table className="comparison">
        <thead>
          <tr>
            <th scope="col">Line</th>
            <th scope="col">You predicted</th>
            <th scope="col">Actual output</th>
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: rows }, (_, i) => {
            const match = predicted[i] === actual[i];
            return (
              <tr key={i} className={match ? "match" : "mismatch"}>
                <td>
                  {i + 1}
                  {!match && <span className="visually-hidden"> (different)</span>}
                </td>
                <td>
                  <code>{predicted[i] ?? "—"}</code>
                </td>
                <td>
                  <code>{actual[i] ?? "—"}</code>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </section>
  );
}

/** Same normalisation as the grader: ignore trailing spaces and trailing blank lines. */
function lines(text: string): string[] {
  const result = text.replace(/\r\n/g, "\n").split("\n").map((l) => l.trimEnd());
  while (result.length > 0 && result[result.length - 1] === "") {
    result.pop();
  }
  return result;
}
