import type { Diagnostic } from "../types";

export function Diagnostics({ diagnostics }: { diagnostics: Diagnostic[] }) {
  if (diagnostics.length === 0) {
    return null;
  }
  return (
    <ul className="diagnostics">
      {diagnostics.map((d, i) => (
        <li key={i} className={d.kind === "ERROR" ? "diagnostic error" : "diagnostic warning"}>
          <span className="diagnostic-where">
            {d.kind === "ERROR" ? "Error" : "Warning"}
            {d.line > 0 ? `, line ${d.line}` : ""}:
          </span>{" "}
          <span className="diagnostic-message">{d.message}</span>
        </li>
      ))}
    </ul>
  );
}
