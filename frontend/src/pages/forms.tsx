import type { ReactNode } from "react";
import javaLogo from "../assets/java-logo.png";
import { Bug, Eye, Sparkles } from "lucide-react";

export function Field(props: {
  id: string;
  label: string;
  type?: string;
  value: string;
  onChange: (value: string) => void;
  autoComplete?: string;
  hint?: ReactNode;
}) {
  return (
    <div className="form-field">
      <label htmlFor={props.id}>{props.label}</label>
      <input
        id={props.id}
        type={props.type ?? "text"}
        value={props.value}
        autoComplete={props.autoComplete}
        onChange={(e) => props.onChange(e.target.value)}
        aria-describedby={props.hint ? `${props.id}-hint` : undefined}
        required
      />
      {props.hint && (
        <p id={`${props.id}-hint`} className="form-hint">
          {props.hint}
        </p>
      )}
    </div>
  );
}

/** The page to return to after logging in, limited to this site's own paths. */
export function nextPath(search: string, fallback: string): string {
  const next = new URLSearchParams(search).get("next");
  return next && next.startsWith("/") && !next.startsWith("//") ? next : fallback;
}

/** The coloured panel beside the sign-up and log-in forms. */
export function AuthPanel() {
  return (
    <aside className="auth-panel" aria-label="About the academy">
      <img className="brand-mark" src={javaLogo} alt="" width={36} height={36} />
      <h2>Become a Java engineer, one idea at a time.</h2>
      <p>Real code from the first lesson, checked by real tests, with a mentor who helps without handing you the answer.</p>
      <ul className="auth-features">
        <li>
          <span className="icon-tile" aria-hidden="true">
            <Eye size={20} />
          </span>
          <div>
            <strong>Predict, then run</strong>
            <span>Guess what code does before you see it. It's how the ideas stick.</span>
          </div>
        </li>
        <li>
          <span className="icon-tile" aria-hidden="true">
            <Bug size={20} />
          </span>
          <div>
            <strong>Write, fix and change code</strong>
            <span>Every exercise runs your code against real tests.</span>
          </div>
        </li>
        <li>
          <span className="icon-tile" aria-hidden="true">
            <Sparkles size={20} />
          </span>
          <div>
            <strong>Progress you can trust</strong>
            <span>What you can do on your own is tracked separately from what you did with help.</span>
          </div>
        </li>
      </ul>
    </aside>
  );
}
