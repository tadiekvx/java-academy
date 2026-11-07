import { Link, useLocation } from "react-router";

/** Shown in place of Run/Check buttons when nobody is logged in. */
export function LoginPrompt({ action }: { action: string }) {
  const location = useLocation();
  const next = encodeURIComponent(location.pathname);
  return (
    <p className="login-prompt">
      <Link to={`/signup?next=${next}`}>Create a free account</Link> or <Link to={`/login?next=${next}`}>log in</Link> to{" "}
      {action}.
    </p>
  );
}
