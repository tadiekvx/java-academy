import { useState } from "react";
import { api } from "../../api";
import type { AttemptContext, GradeReport, Submission } from "../../types";

/** Submits attempts for one exercise and tracks the latest report. {@code onRecorded} runs after each recorded attempt. */
export function useAttempt(exerciseId: string, context: AttemptContext = "practice", onRecorded?: () => void, initialReport: GradeReport | null = null) {
  const [report, setReport] = useState<GradeReport | null>(initialReport);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (submission: Submission) => {
    setBusy(true);
    setError(null);
    try {
      const result = await api.attempt(exerciseId, submission, context);
      setReport(result);
      onRecorded?.();
      return result;
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      return null;
    } finally {
      setBusy(false);
    }
  };

  return { report, busy, error, submit, clear: () => setReport(null) };
}
