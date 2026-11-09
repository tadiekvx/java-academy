import { useState } from "react";
import { api } from "../../api";
import { useAuth } from "../../auth";
import { clearDraft, loadDraft, saveDraft } from "../../storage";
import type { Diagnostic, ExerciseStatus, ExerciseView, ProgramRun } from "../../types";
import { CodeEditor } from "../CodeEditor";
import { LoginPrompt } from "../LoginPrompt";
import { MentorPanel } from "../MentorPanel";
import { Results } from "../Results";
import { RunOutput } from "../RunOutput";
import { useAttempt } from "./useAttempt";

const MAIN_FILE = "Main.java";

interface Props {
  exercise: ExerciseView;
  /** "check" is a retrieval check: no saved drafts, and the first check against the tests is final. */
  mode?: "practice" | "check";
  /** The learner's last recorded attempt, put back when no newer unsent draft is saved in this browser. */
  last?: ExerciseStatus["last"];
  onRecorded?: () => void;
}

/** Write, debug and modify exercises: edit Main.java, run it, and check it against the tests. */
export function CodeExercise({ exercise, mode = "practice", last, onRecorded }: Props) {
  const { learner } = useAuth();
  const isCheck = mode === "check";
  const starter = exercise.files[MAIN_FILE] ?? "";
  const lastSource = isCheck ? undefined : last?.submission.files?.[MAIN_FILE];
  const [source, setSource] = useState(() => (isCheck ? null : loadDraft(`draft:${exercise.id}`) ?? lastSource) ?? starter);
  const [run, setRun] = useState<ProgramRun | null>(null);
  const [stdin, setStdin] = useState("");
  const [running, setRunning] = useState(false);
  const [runError, setRunError] = useState<string | null>(null);
  const [attemptCount, setAttemptCount] = useState(0);
  const attempt = useAttempt(exercise.id, isCheck ? "retrieval" : "practice", () => {
    setAttemptCount((n) => n + 1);
    onRecorded?.();
  }, isCheck || source !== lastSource ? null : (last?.report ?? null));
  const checkFinished = isCheck && attempt.report !== null;

  const edit = (value: string) => {
    setSource(value);
    if (!isCheck) {
      saveDraft(`draft:${exercise.id}`, value);
    }
  };

  const reset = () => {
    setSource(starter);
    clearDraft(`draft:${exercise.id}`);
    setRun(null);
    attempt.clear();
  };

  const execute = async () => {
    setRunning(true);
    setRunError(null);
    attempt.clear();
    try {
      setRun(await api.run({ [MAIN_FILE]: source }, stdin.endsWith("\n") || stdin === "" ? stdin : stdin + "\n"));
    } catch (e) {
      setRunError(e instanceof Error ? e.message : String(e));
    } finally {
      setRunning(false);
    }
  };

  const check = async () => {
    setRun(null);
    await attempt.submit({ files: { [MAIN_FILE]: source } });
  };

  const diagnostics: Diagnostic[] = attempt.report?.diagnostics ?? run?.diagnostics ?? [];

  return (
    <div className="code-exercise">
      {exercise.signatures.length > 0 && (
        <p className="signatures">
          The tests call{" "}
          {exercise.signatures.map((s, i) => (
            <span key={s}>
              {i > 0 && " and "}
              <code>{s}</code>
            </span>
          ))}
          .
        </p>
      )}
      <CodeEditor value={source} onChange={edit} diagnostics={diagnostics} label={`Code for ${exercise.title}`} />
      {!learner ? (
        <LoginPrompt action="run your code and check it against the tests" />
      ) : (
      <div className="button-row">
        <button type="button" className="button" onClick={execute} disabled={running || attempt.busy}>
          {running ? "Running…" : "▶ Run"}
        </button>
        <button type="button" className="button primary" onClick={check} disabled={running || attempt.busy || checkFinished}>
          {attempt.busy ? "Checking…" : "Check against tests"}
        </button>
        {source !== starter && !isCheck && (
          <button type="button" className="button subtle" onClick={reset}>
            Start again
          </button>
        )}
      </div>
      )}
      {learner && (
        <details className="program-input">
          <summary>Input for Run (what you'd type, one line per IO.readln)</summary>
          <textarea
            rows={3}
            spellCheck={false}
            value={stdin}
            onChange={(e) => setStdin(e.target.value)}
            aria-label="Input for your program"
          />
        </details>
      )}
      {exercise.visibleTests.length > 0 && !attempt.report && (
        <details className="examples">
          <summary>Examples the tests check ({exercise.visibleTests.length}, plus hidden tests)</summary>
          <table>
            <thead>
              <tr>
                <th scope="col">Call</th>
                <th scope="col">Expected</th>
              </tr>
            </thead>
            <tbody>
              {exercise.visibleTests.map((t, i) => (
                <tr key={i}>
                  <td>
                    <code>{t.call}</code>
                  </td>
                  <td>
                    <code>{t.expected}</code>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </details>
      )}
      {runError && <p className="notice error">{runError}</p>}
      {attempt.error && <p className="notice error">{attempt.error}</p>}
      {run && <RunOutput run={run} />}
      {attempt.report && <Results report={attempt.report} />}
      {learner && <MentorPanel exerciseId={exercise.id} code={source} attemptCount={attemptCount} />}
      {checkFinished && (
        <p className="notice review">
          Check recorded. {attempt.report?.outcome === "PASSED"
            ? "Nicely remembered. The next check for this idea will come later."
            : "No problem: this tells us to bring the idea back sooner. Revisit the lesson if you like, and you'll get another check in a few days."}
        </p>
      )}
    </div>
  );
}
