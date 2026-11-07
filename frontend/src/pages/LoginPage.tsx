import { useEffect, useState, type FormEvent } from "react";
import { Link, useLocation, useNavigate } from "react-router";
import { api } from "../api";
import { useAuth } from "../auth";
import { AuthPanel, Field, nextPath } from "./forms";

export function LoginPage() {
  const { setLearner } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    document.title = "Log in · Java Engineering Academy";
  }, []);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const me = await api.login(email, password);
      setLearner(me.learner);
      const next = nextPath(location.search, "/");
      navigate(me.learner?.onboarded ? next : `/welcome?next=${encodeURIComponent(next)}`);
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
          <h1>Log in</h1>
          <form onSubmit={submit} className="auth-form" noValidate>
            <Field id="email" label="Email" type="email" value={email} onChange={setEmail} autoComplete="email" />
            <Field
              id="password"
              label="Password"
              type="password"
              value={password}
              onChange={setPassword}
              autoComplete="current-password"
            />
            {error && (
              <p className="notice error" role="alert">
                {error}
              </p>
            )}
            <button type="submit" className="button primary wide" disabled={busy}>
              {busy ? "Logging in…" : "Log in"}
            </button>
          </form>
          <p className="auth-switch">
            New here? <Link to={`/signup${location.search}`}>Create an account</Link>
          </p>
        </div>
      </div>
      <AuthPanel />
    </div>
  );
}
