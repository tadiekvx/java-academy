import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router";
import { CircleCheck, Clock, Eye, GraduationCap, Sparkles } from "lucide-react";
import { api } from "../api";
import { useAuth } from "../auth";
import { ModuleIcon, moduleHue } from "../look";
import type { CurriculumView, LessonSummary } from "../types";

export function CurriculumPage() {
  const { learner } = useAuth();
  const location = useLocation();
  const [curriculum, setCurriculum] = useState<CurriculumView | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    document.title = learner ? "All lessons · Java Engineering Academy" : "Java Engineering Academy";
    api.curriculum().then(setCurriculum).catch((e) => setError(String(e)));
  }, [learner]);

  useEffect(() => {
    if (curriculum && location.hash) {
      document.getElementById(location.hash.slice(1))?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [curriculum, location.hash]);

  if (error) {
    return <p className="notice error">Couldn't load the curriculum. Is the backend running? ({error})</p>;
  }
  if (!curriculum) {
    return <p className="muted">Loading…</p>;
  }
  return (
    <>
      {learner === null ? (
        <section className="hero">
          <p className="hero-eyebrow">Java Engineering Academy</p>
          <h1>Learn to program in Java, properly.</h1>
          <p>
            Short explanations, lots of practice, and code that actually runs. Every lesson asks you to predict, write, fix,
            change and explain code, because that's how the ideas stick.
          </p>
          <div className="button-row">
            <Link to="/signup" className="button light">
              <Sparkles size={16} aria-hidden="true" /> Create a free account
            </Link>
            <span className="hero-note">You can read lessons without one; you need one to run and check code.</span>
          </div>
        </section>
      ) : (
        <header className="page-header">
          <h1>All lessons</h1>
          <p>Work through them in order: each one builds on the ones before.</p>
        </header>
      )}

      {curriculum.stages.map((stage) => (
        <section key={stage.number}>
          <div className="stage-heading">
            <span className="icon-tile small hue-blue">
              <GraduationCap size={20} aria-hidden="true" />
            </span>
            <h2>
              Stage {stage.number}: {stage.title}
              {stage.number === 0 && <span className="chip hue-teal stage-chip">Optional: do it when you want to code on your own computer</span>}
            </h2>
          </div>
          <div className="module-grid">
            {stage.modules.map((module) => {
              const ready = module.lessons.filter((l) => l.available).length;
              return (
                <article key={module.number} id={`module-${stage.number}-${module.number}`} className={`module-card ${moduleHue(module.number)}`}>
                  <div className="module-card-head">
                    <span className="icon-tile">
                      <ModuleIcon moduleNumber={module.number} />
                    </span>
                    <div>
                      <span className="module-number">Module {module.number}</span>
                      <h3>{module.title}</h3>
                    </div>
                  </div>
                  <p className="muted small" style={{ margin: "0 0 8px" }}>
                    {ready} of {module.lessons.length} lessons ready
                  </p>
                  <ol className="lesson-list">
                    {module.lessons.map((lesson, i) => (
                      <LessonRow key={lesson.id} lesson={lesson} number={`${module.number}.${i + 1}`} />
                    ))}
                  </ol>
                </article>
              );
            })}
          </div>
        </section>
      ))}
    </>
  );
}

function LessonRow({ lesson, number }: { lesson: LessonSummary; number: string }) {
  return (
    <li className={lesson.available ? "lesson-row available" : "lesson-row"}>
      <span className="lesson-number">{number}</span>
      {lesson.available ? <Link to={`/lessons/${lesson.id}`}>{lesson.title}</Link> : <span className="muted">{lesson.title}</span>}
      {lesson.status === "PUBLISHED" && lesson.available && (
        <span className="chip hue-green">
          <CircleCheck size={13} aria-hidden="true" /> Ready
        </span>
      )}
      {lesson.status === "IN_REVIEW" && (
        <span className="chip hue-purple">
          <Eye size={13} aria-hidden="true" /> In review
        </span>
      )}
      {!lesson.available && (
        <span className="chip hue-gray">
          <Clock size={13} aria-hidden="true" /> Coming soon
        </span>
      )}
    </li>
  );
}
