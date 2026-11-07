import { useState } from "react";
import { api } from "../api";
import { useAuth } from "../auth";
import type { ProgramRun } from "../types";
import { CodeEditor } from "./CodeEditor";
import { LoginPrompt } from "./LoginPrompt";
import { RunOutput } from "./RunOutput";

/** A lesson code sample the learner can edit and run. */
export function RunnableSnippet({ code }: { code: string }) {
  const { learner } = useAuth();
  const original = code.replace(/\n$/, "");
  const [source, setSource] = useState(original);
  const [run, setRun] = useState<ProgramRun | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async () => {
    setBusy(true);
    setError(null);
    try {
      setRun(await api.run({ "Main.java": source }));
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="runnable">
      <CodeEditor value={source} onChange={setSource} label="Example code you can edit and run" />
      {learner ? (
        <div className="button-row">
          <button type="button" className="button primary" onClick={execute} disabled={busy}>
            {busy ? "Running…" : "▶ Run"}
          </button>
          {source !== original && (
            <button type="button" className="button" onClick={() => setSource(original)}>
              Reset
            </button>
          )}
        </div>
      ) : (
        <LoginPrompt action="run this code" />
      )}
      {error && <p className="notice error">{error}</p>}
      {run && <RunOutput run={run} />}
    </div>
  );
}
