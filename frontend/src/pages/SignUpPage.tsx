import { useEffect, useState, type FormEvent } from "react";
import { Link, useLocation, useNavigate } from "react-router";
import { api } from "../api";
import { useAuth } from "../auth";
import { AuthPanel, Field, nextPath } from "./forms";

export function SignUpPage() {
  const { setLearner } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    document.title = "Create an account · Java Engineering Academy";
  }, []);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const me = await api.register(email, displayName, password);
      setLearner(me.learner);
      navigate(`/welcome?next=${encodeURIComponent(nextPath(location.search, "/"))}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="auth-layout">
      <div className="auth-form-side">
        <div className="auth-page">
          <h1>Create your account</h1>
          <p className="muted">Free. Your progress is saved so you can pick up where you left off.</p>
          <form onSubmit={submit} className="auth-form" noValidate>
            <Field
              id="name"
              label="What should we call you?"
              value={displayName}
              onChange={setDisplayName}
              autoComplete="given-name"
            />
            <Field id="email" label="Email" type="email" value={email} onChange={setEmail} autoComplete="email" />
            <Field
              id="password"
              label="Password"
              type="password"
              value={password}
              onChange={setPassword}
              autoComplete="new-password"
              hint="At least 10 characters. A short phrase is easier to remember than a jumble."
            />
            {error && (
              <p className="notice error" role="alert">
                {error}
              </p>
            )}
            <button type="submit" className="button primary wide" disabled={busy}>
              {busy ? "Creating your account…" : "Create account"}
            </button>
          </form>
          <p className="auth-switch">
            Already have an account? <Link to={`/login${location.search}`}>Log in</Link>
          </p>
        </div>
      </div>
      <AuthPanel />
    </div>
  );
}
