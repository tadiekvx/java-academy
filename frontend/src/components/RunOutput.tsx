import type { ProgramRun } from "../types";
import { Diagnostics } from "./Diagnostics";

/** The output of running a program: compiler errors, or what it printed and how it ended. */
export function RunOutput({ run }: { run: ProgramRun }) {
  if (run.result === null) {
    return (
      <div className="run-output" role="status">
        <p className="run-output-title">It doesn't compile yet. Start with the first error.</p>
        <Diagnostics diagnostics={run.diagnostics} />
      </div>
    );
  }
  const { stdout, stderr, timedOut, outputLimitExceeded, exitCode } = run.result;
  return (
    <div className="run-output" role="status">
      <p className="run-output-title">Output</p>
      <pre className="console">{stdout === "" ? <span className="muted">(nothing printed)</span> : stdout}</pre>
      {timedOut && <p className="notice warning">The program was stopped because it ran for too long. Is there a loop that never ends?</p>}
      {outputLimitExceeded && <p className="notice warning">The program was stopped because it printed too much.</p>}
      {!timedOut && exitCode !== 0 && stderr !== "" && (
        <>
          <p className="run-output-title">Error</p>
          <pre className="console console-error">{stderr}</pre>
        </>
      )}
    </div>
  );
}
