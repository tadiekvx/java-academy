import { useEffect, useState, type ReactNode } from "react";
import { Link, useLocation } from "react-router";
import { ArrowRight, Brain, CircleCheck, Flame, Info, Target } from "lucide-react";
import { api } from "../api";
import { useAuth } from "../auth";
import type { ConceptView, Coverage, ProgressView } from "../types";

const COVERAGE: Record<Coverage, { icon: string; text: string }> = {
  INDEPENDENT: { icon: "✓", text: "done on your own" },
  ASSISTED: { icon: "◐", text: "done with help" },
  PENDING_REVIEW: { icon: "⏳", text: "awaiting review" },
  MISSING: { icon: "○", text: "not yet" },
};

const LEVELS = 5;

export function DashboardPage() {
  const { learner } = useAuth();
  const [progress, setProgress] = useState<ProgressView | null>(null);
  const [error, setError] = useState<string | null>(null);
  const location = useLocation();

  useEffect(() => {
    if (progress && location.hash) {
      document.getElementById(location.hash.slice(1))?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [progress, location.hash]);

  useEffect(() => {
    document.title = "Dashboard · Java Engineering Academy";
    api.progress().then(setProgress).catch((e) => setError(e instanceof Error ? e.message : String(e)));
  }, []);

  if (error) {
    return <p className="notice error">{error}</p>;
  }
  if (!progress || !learner) {
    return <p className="muted">Loading…</p>;
  }

  const started = progress.concepts.filter((c) => c.level > 0);
  const notStarted = progress.concepts.filter((c) => c.level === 0);
  const practising = progress.concepts.filter((c) => c.level === 2).length;
  const demonstrated = progress.concepts.filter((c) => c.level >= 3).length;
  const onYourOwn = progress.concepts.reduce((sum, c) => sum + c.independentExercises, 0);

  return (
    <div className="dashboard">
      <section className="hero">
        <p className="hero-eyebrow">Welcome back</p>
        <h1>Hello, {learner.displayName}</h1>
        {progress.recommended ? (
          <>
            <p>Pick up where you left off:</p>
            <p className="hero-continue">{progress.recommended.title}</p>
            <div className="button-row">
              <Link className="button light" to={`/lessons/${progress.recommended.id}`}>
                Continue learning <ArrowRight size={16} aria-hidden="true" />
              </Link>
            </div>
          </>
        ) : (
          <p>You've worked through every lesson that's available. More are on the way.</p>
        )}
      </section>

      <div className="stat-grid">
        <Stat hue="hue-orange" icon={<Flame size={24} />} label="Ideas you're practising" value={practising} />
        <Stat hue="hue-green" icon={<Target size={24} />} label="Ideas demonstrated on your own" value={demonstrated} />
        <Stat hue="hue-blue" icon={<CircleCheck size={24} />} label="Exercises done on your own" value={onYourOwn} />
        <Stat hue="hue-purple" icon={<Brain size={24} />} label="Knowledge checks due" value={progress.dueChecks.length} />
      </div>

      <div className="dashboard-columns">
        <section className="card" aria-labelledby="concepts-heading">
          <div className="card-head">
            <span className="icon-tile small hue-blue">
              <Target size={20} aria-hidden="true" />
            </span>
            <div>
              <h2 id="concepts-heading" className="card-title">
                What you can do
              </h2>
              <p className="muted small" style={{ margin: 0 }}>
                Introduced → Practising → Demonstrated (on your own) → Secure (remembered days later) → Retained
              </p>
            </div>
          </div>
          {started.length === 0 ? (
            <p className="muted">Open a lesson to get started.</p>
          ) : (
            <ul className="concept-list">
              {started.map((c) => (
                <ConceptRow key={c.id} concept={c} />
              ))}
            </ul>
          )}
          {notStarted.length > 0 && (
            <details className="not-started">
              <summary>Not started yet ({notStarted.length})</summary>
              <ul>
                {notStarted.map((c) => (
                  <li key={c.id}>{c.name}</li>
                ))}
              </ul>
            </details>
          )}
        </section>

        <div className="side-stack">
          <section className="card" id="checks" aria-labelledby="checks-heading">
            <div className="card-head">
              <span className="icon-tile small hue-purple">
                <Brain size={20} aria-hidden="true" />
              </span>
              <h2 id="checks-heading" className="card-title">
                Knowledge checks
              </h2>
            </div>
            {progress.dueChecks.length === 0 ? (
              <p className="muted small">
                Nothing due. Once you've shown you can do something on your own, a short check appears here a few days
                later.
              </p>
            ) : (
              <ul className="check-list">
                {progress.dueChecks.map((check) => (
                  <li key={check.exerciseId}>
                    <div>
                      <Link to={`/checks/${check.exerciseId}`}>{check.title}</Link>
                      <div className="muted small">{check.conceptNames.join(", ")}</div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
          <section className="card" aria-labelledby="how-heading">
            <div className="card-head">
              <span className="icon-tile small hue-teal">
                <Info size={20} aria-hidden="true" />
              </span>
              <h2 id="how-heading" className="card-title">
                How progress works
              </h2>
            </div>
            <p className="muted small" style={{ margin: 0 }}>
              Work you do on your own counts most. Exercises you finish with the mentor's hints still count as practice,
              and the mentor will help you get to doing them on your own.
            </p>
          </section>
        </div>
      </div>

      <p style={{ marginTop: 24 }}>
        <Link to="/lessons">See all lessons →</Link>
      </p>
    </div>
  );
}

function Stat({ hue, icon, label, value }: { hue: string; icon: ReactNode; label: string; value: number }) {
  return (
    <div className={`stat-card ${hue}`}>
      <span className="icon-tile" aria-hidden="true">
        {icon}
      </span>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
    </div>
  );
}

function ConceptRow({ concept }: { concept: ConceptView }) {
  return (
    <li className="concept">
      <div className="concept-head">
        <span>{concept.name}</span>
        <span className={`chip ${concept.level >= 3 ? "hue-green" : concept.level === 2 ? "hue-orange" : "hue-blue"}`}>
          {concept.levelName}
        </span>
      </div>
      <div className="level-meter" role="img" aria-label={`Level ${concept.level} of ${LEVELS}: ${concept.levelName}`}>
        {Array.from({ length: LEVELS }, (_, i) => (
          <span key={i} className={i < concept.level ? "filled" : ""} />
        ))}
      </div>
      <p className="concept-counts small muted">
        {concept.independentExercises} exercise{concept.independentExercises === 1 ? "" : "s"} on your own ·{" "}
        {concept.assistedOnlyExercises} with help
        {concept.nextCheckDue && concept.level >= 3 && <> · next check {formatDate(concept.nextCheckDue)}</>}
      </p>
      <ul className="evidence-list">
        {concept.evidence.map((e) => (
          <li key={e.type} className={`evidence evidence-${e.coverage.toLowerCase()}`}>
            <span aria-hidden="true">{COVERAGE[e.coverage].icon}</span> {e.label}
            <span className="visually-hidden">: {COVERAGE[e.coverage].text}</span>
          </li>
        ))}
      </ul>
    </li>
  );
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, { day: "numeric", month: "short" });
}
