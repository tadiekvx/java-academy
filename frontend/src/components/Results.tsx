import type { GradeReport, TestResult, TestStatus } from "../types";
import { Diagnostics } from "./Diagnostics";

const STATUS_LABEL: Record<TestStatus, string> = {
  PASS: "Passed",
  FAIL: "Wrong result",
  ERROR: "Error",
  TIMEOUT: "Too slow",
  NOT_RUN: "Not run",
};

const STATUS_ICON: Record<TestStatus, string> = {
  PASS: "✓",
  FAIL: "✗",
  ERROR: "!",
  TIMEOUT: "⏱",
  NOT_RUN: "–",
};

/** Feedback for a graded attempt. Hidden tests arrive without inputs or values, so only their name shows. */
export function Results({ report }: { report: GradeReport }) {
  const passed = report.tests.filter((t) => t.status === "PASS").length;
  return (
    <section className={`results outcome-${report.outcome.toLowerCase()}`} aria-live="polite">
      <p className="results-headline">
        <span aria-hidden="true">{report.outcome === "PASSED" ? "✓ " : report.outcome === "PENDING_REVIEW" ? "✎ " : ""}</span>
        {report.message}
        {report.tests.length > 0 && report.outcome !== "PASSED" && (
          <span className="muted"> ({passed} passed)</span>
        )}
      </p>
      <Diagnostics diagnostics={report.diagnostics} />
      {report.tests.length > 0 && (
        <ol className="test-list">
          {report.tests.map((test, i) => (
            <TestRow key={i} test={test} number={i + 1} />
          ))}
        </ol>
      )}
    </section>
  );
}

function TestRow({ test, number }: { test: TestResult; number: number }) {
  const statusClass = `test-${test.status.toLowerCase().replace("_", "-")}`;
  return (
    <li className={`test-row ${statusClass}`}>
      <div className="test-summary">
        <span className="test-icon" aria-hidden="true">
          {STATUS_ICON[test.status]}
        </span>
        <span className="test-status">{STATUS_LABEL[test.status]}</span>
        <span className="test-name">
          {test.visible ? (
            <>
              {test.name && <span className="test-label">{test.name}: </span>}
              <code>{test.call}</code>
            </>
          ) : (
            <>
              Hidden test {number}
              {test.name ? `: ${test.name}` : ""}
            </>
          )}
        </span>
      </div>
      {test.visible && test.status !== "PASS" && (
        <dl className="test-details">
          {test.expected !== null && (
            <>
              <dt>Expected</dt>
              <dd>
                <pre>{test.expected}</pre>
              </dd>
            </>
          )}
          {test.actual !== null && (
            <>
              <dt>Got</dt>
              <dd>
                <pre>{test.actual === "" ? "(nothing)" : test.actual}</pre>
              </dd>
            </>
          )}
          {test.error && (
            <>
              <dt>Problem</dt>
              <dd>
                <pre>{test.error}</pre>
              </dd>
            </>
          )}
        </dl>
      )}
      {test.visible && test.output && (
        <details className="test-output">
          <summary>What your code printed during this test</summary>
          <pre>{test.output}</pre>
        </details>
      )}
    </li>
  );
}
