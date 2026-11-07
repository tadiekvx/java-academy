import { useEffect, useState, type FormEvent } from "react";
import { Navigate, useLocation, useNavigate } from "react-router";
import { api } from "../api";
import { useAuth } from "../auth";
import { nextPath } from "./forms";

const EXPERIENCE = [
  { value: "none", label: "None. This is my first time programming." },
  { value: "other-language", label: "I've done some programming, but not in Java." },
  { value: "some-java", label: "I've written some Java before." },
];

const HOURS = [
  { value: 2, label: "1–2 hours" },
  { value: 5, label: "3–5 hours" },
  { value: 8, label: "6–10 hours" },
  { value: 12, label: "More than 10 hours" },
];

const GOALS = [
  { value: "career-change", label: "To get a job as a software developer" },
  { value: "current-job", label: "For my current job" },
  { value: "study", label: "For a course or qualification" },
  { value: "curiosity", label: "Because I'm curious" },
];

/** Onboarding: three questions, then how the platform works. */
export function WelcomePage() {
  const { learner, setLearner } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [experience, setExperience] = useState("");
  const [hours, setHours] = useState<number | null>(null);
  const [goal, setGoal] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    document.title = "Welcome · Java Engineering Academy";
  }, []);

  if (learner === null) {
    return <Navigate to="/signup" replace />;
  }
  if (learner === undefined) {
    return <p className="muted">Loading…</p>;
  }

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    if (!experience || hours === null || !goal) {
      setError("Answer all three questions to continue.");
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const me = await api.onboard(experience, hours, goal);
      setLearner(me.learner);
      navigate(nextPath(location.search, "/"));
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="welcome">
      <h1>Welcome, {learner.displayName}</h1>
      <p className="lead">Three quick questions so we can pitch things right, then a minute on how this works.</p>
      <form onSubmit={submit}>
        <fieldset className="choice-group">
          <legend>How much programming have you done?</legend>
          {EXPERIENCE.map((o) => (
            <label key={o.value} className="choice">
              <input type="radio" name="experience" value={o.value} checked={experience === o.value} onChange={() => setExperience(o.value)} />
              {o.label}
            </label>
          ))}
          {experience === "some-java" && (
            <p className="form-hint">
              A placement check, so you can skip what you already know, is on its way. For now, start at the beginning and move
              quickly through anything familiar.
            </p>
          )}
        </fieldset>
        <fieldset className="choice-group">
          <legend>How much time can you give it each week?</legend>
          {HOURS.map((o) => (
            <label key={o.value} className="choice">
              <input type="radio" name="hours" checked={hours === o.value} onChange={() => setHours(o.value)} />
              {o.label}
            </label>
          ))}
        </fieldset>
        <fieldset className="choice-group">
          <legend>What are you learning Java for?</legend>
          {GOALS.map((o) => (
            <label key={o.value} className="choice">
              <input type="radio" name="goal" value={o.value} checked={goal === o.value} onChange={() => setGoal(o.value)} />
              {o.label}
            </label>
          ))}
        </fieldset>

        <section className="how-it-works" aria-labelledby="how-heading">
          <h2 id="how-heading">How this works</h2>
          <ol>
            <li>
              <strong>Predict before you run.</strong> You'll often be asked what code will print before you see it. Guessing
              wrong is fine; it's how the idea sticks.
            </li>
            <li>
              <strong>Write, fix, change and explain.</strong> Every idea comes with exercises that check your code against
              real tests, including some you can't see.
            </li>
            <li>
              <strong>On your own counts most.</strong> We track what you can do without help separately from what you did
              with help. Both are progress, but only independent work moves an idea to "Demonstrated".
            </li>
            <li>
              <strong>Short check-ins later.</strong> A few days after you've got something, we'll ask you to do a similar
              problem from memory. That's what turns "I followed it" into "I know it".
            </li>
          </ol>
        </section>

        {error && (
          <p className="notice error" role="alert">
            {error}
          </p>
        )}
        <button type="submit" className="button primary" disabled={busy}>
          {busy ? "Saving…" : "Start learning"}
        </button>
      </form>
    </div>
  );
}
