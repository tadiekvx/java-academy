import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router";
import { AlertTriangle, CircleCheck, Target, Timer } from "lucide-react";
import { api, NotFoundError } from "../api";
import { useAuth } from "../auth";
import { Exercise } from "../components/Exercise";
import { Markdown } from "../components/Markdown";
import { Resources } from "../components/Resources";
import { parseSegments } from "../lesson/segments";
import type { ExerciseStatus, LessonProgress, LessonView } from "../types";

export function LessonPage() {
  const { id = "" } = useParams();
  const [lesson, setLesson] = useState<LessonView | null>(null);
  const [error, setError] = useState<"missing" | string | null>(null);
  const { learner } = useAuth();
  const [statuses, setStatuses] = useState<Record<string, ExerciseStatus>>({});
  // Exercises are only drawn once saved work is known, so they start from what the learner left.
  const [statusesLoaded, setStatusesLoaded] = useState(false);
  const [progress, setProgress] = useState<LessonProgress | null>(null);

  const refreshStatuses = useCallback(() => {
    if (learner) {
      api
        .lessonProgress(id)
        .then(setStatuses)
        .catch(() => setStatuses({}))
        .finally(() => setStatusesLoaded(true));
      api
        .lessonsProgress()
        .then((all) => setProgress(all[id] ?? null))
        .catch(() => setProgress(null));
    }
  }, [id, learner]);

  const toggleComplete = async () => {
    await (progress?.completed ? api.reopenLesson(id) : api.completeLesson(id));
    refreshStatuses();
  };

  useEffect(() => {
    if (learner && lesson) {
      api
        .visitLesson(lesson.id)
        .catch(() => undefined)
        .finally(refreshStatuses);
    }
  }, [learner, lesson, refreshStatuses]);

  useEffect(() => {
    setLesson(null);
    setError(null);
    setStatuses({});
    setStatusesLoaded(false);
    setProgress(null);
    api
      .lesson(id)
      .then((l) => {
        setLesson(l);
        document.title = `${l.title} · Java Engineering Academy`;
        window.scrollTo(0, 0);
      })
      .catch((e) => setError(e instanceof NotFoundError ? "missing" : String(e)));
  }, [id]);

  const segments = useMemo(() => (lesson ? parseSegments(lesson.body) : []), [lesson]);

  if (error === "missing") {
    return (
      <div className="lesson-missing">
        <h1>This lesson hasn't been written yet</h1>
        <p>
          It's part of the plan, but it isn't available yet. <Link to="/">Back to all lessons</Link>
        </p>
      </div>
    );
  }
  if (error) {
    return <p className="notice error">Couldn't load this lesson. ({error})</p>;
  }
  if (!lesson) {
    return <p className="muted">Loading…</p>;
  }

  let exerciseNumber = 0;
  const lessonNumber = lesson.id.replace(/^j\d+-l/, "");
  return (
    <article className="lesson">
      <nav className="breadcrumbs" aria-label="Breadcrumb">
        <Link to="/lessons">All lessons</Link> / Lesson {lessonNumber}
      </nav>
      <header className="lesson-header-card">
        <div className="lesson-meta">
          <span className="chip hue-blue">Lesson {lessonNumber}</span>
          <span className="chip hue-teal">
            <Timer size={13} aria-hidden="true" /> About {lesson.estimatedMinutes} minutes
          </span>
        </div>
        <h1>{lesson.title}</h1>
        <section className="objectives" aria-labelledby="objectives-heading">
          <h2 id="objectives-heading">
            <Target size={18} aria-hidden="true" /> What you'll learn
          </h2>
          <ul>
            {lesson.objectives.map((o) => (
              <li key={o.id}>{o.text}</li>
            ))}
          </ul>
        </section>
      </header>
      <div className="lesson-body">
        {learner !== undefined && (learner === null || statusesLoaded) && segments.map((segment, i) => {
          switch (segment.kind) {
            case "markdown":
              return <Markdown key={i} text={segment.text} />;
            case "mistake":
              return (
                <aside key={i} className="mistake" aria-label="Common mistake">
                  <p className="mistake-label">
                    <AlertTriangle size={14} aria-hidden="true" /> Common mistake
                  </p>
                  <Markdown text={segment.text} />
                </aside>
              );
            case "exercise":
              exerciseNumber += 1;
              return (
                <Exercise
                  key={segment.id}
                  id={segment.id}
                  number={exerciseNumber}
                  status={statuses[segment.id]}
                  onRecorded={refreshStatuses}
                />
              );
          }
        })}
      </div>
      {learner && statusesLoaded && (
        <section className="lesson-complete card" aria-label="Lesson progress">
          <p style={{ margin: 0 }}>
            {progress?.completed ? (
              <>
                <CircleCheck size={16} aria-hidden="true" /> You've completed this lesson.
              </>
            ) : (
              <>
                {progress ? `${progress.passed} of ${progress.exercises} exercises done.` : ""} Finished with this lesson?
              </>
            )}
          </p>
          <div className="button-row">
            {progress?.completed && progress.exercises > 0 && progress.passed === progress.exercises ? null : (
              <button type="button" className={progress?.completed ? "button subtle" : "button primary"} onClick={toggleComplete}>
                {progress?.completed ? "Mark as not finished" : "Mark lesson complete"}
              </button>
            )}
          </div>
        </section>
      )}
      <Resources resources={lesson.resources} />
    </article>
  );
}
