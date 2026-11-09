import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router";
import { CircleCheck, Flag, ListChecks, Target } from "lucide-react";
import { api, NotFoundError } from "../api";
import { useAuth } from "../auth";
import { CodeEditor } from "../components/CodeEditor";
import { LoginPrompt } from "../components/LoginPrompt";
import { Markdown } from "../components/Markdown";
import { Results } from "../components/Results";
import { RunOutput } from "../components/RunOutput";
import { loadDraft, saveDraft, clearDraft } from "../storage";
import type { ExerciseStatus, GradeReport, ProgramRun, ProjectView } from "../types";
import { CATEGORY } from "./ProjectsPage";

const MAIN = "Main.java";

export function ProjectPage() {
  const { id = "" } = useParams();
  const { learner } = useAuth();
  const [project, setProject] = useState<ProjectView | null>(null);
  const [missing, setMissing] = useState(false);
  const [source, setSource] = useState("");
  const [stdin, setStdin] = useState("");
  const [run, setRun] = useState<ProgramRun | null>(null);
  const [reports, setReports] = useState<Record<string, GradeReport>>({});
  const [statuses, setStatuses] = useState<Record<string, ExerciseStatus>>({});
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [note, setNote] = useState("");

  useEffect(() => {
    api
      .project(id)
      .then((p) => {
        setProject(p);
        document.title = `${p.title} · Java Engineering Academy`;
        setSource(loadDraft(`project:${p.id}`) ?? p.files[MAIN] ?? "");
        setNote(loadDraft(`project-note:${p.id}`) ?? "");
      })
      .catch((e) => setMissing(e instanceof NotFoundError));
  }, [id]);

  const refresh = useCallback(() => {
    if (learner) {
      api.projectProgress(id).then(setStatuses).catch(() => setStatuses({}));
    }
  }, [id, learner]);
  useEffect(refresh, [refresh]);

  const passed = useMemo(() => Object.values(statuses).filter((s) => s.passed).length, [statuses]);

  if (missing) {
    return <p>This project isn't available. <Link to="/projects">All projects</Link></p>;
  }
  if (!project) {
    return <p className="muted">Loading…</p>;
  }
  const cat = CATEGORY[project.category];
  const starter = project.files[MAIN] ?? "";

  const edit = (value: string) => {
    setSource(value);
    saveDraft(`project:${project.id}`, value);
  };
  const execute = async () => {
    setBusy("run");
    setError(null);
    try {
      setRun(await api.run({ [MAIN]: source }, stdin === "" || stdin.endsWith("\n") ? stdin : stdin + "\n"));
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(null);
    }
  };
  const check = async (milestoneId: string) => {
    setBusy(milestoneId);
    setError(null);
    try {
      const report = await api.projectAttempt(project.id, milestoneId, { files: { [MAIN]: source } });
      setReports((r) => ({ ...r, [milestoneId]: report }));
      refresh();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(null);
    }
  };

  return (
    <article className="project">
      <nav className="breadcrumbs" aria-label="Breadcrumb">
        <Link to="/projects">Projects</Link> / {project.title}
      </nav>
      <header className="lesson-header-card">
        <div className="lesson-meta">
          <span className={`chip ${cat.hue}`}>{cat.label}</span>
          {project.estimatedHours && <span className="chip hue-teal">About {project.estimatedHours} hours</span>}
          {learner && (
            <span className="chip hue-green">
              <CircleCheck size={13} aria-hidden="true" /> {passed} of {project.milestones.length} milestones
            </span>
          )}
        </div>
        <h1>{project.title}</h1>
        <p className="muted">{cat.blurb}</p>
      </header>

      <div className="lesson-body">
        <Markdown text={project.brief} />
        {project.requirements.length > 0 && <Bullets icon={<ListChecks size={18} />} title="Requirements" items={project.requirements} />}
        {project.constraints.length > 0 && <Bullets icon={<Flag size={18} />} title="Constraints" items={project.constraints} />}
        {project.acceptance.length > 0 && <Bullets icon={<Target size={18} />} title="Acceptance criteria" items={project.acceptance} />}

        <h2>Your program</h2>
        <p className="muted small">One file for the whole project. Your work is saved in this browser as you type.</p>
        <CodeEditor value={source} onChange={edit} label={`Code for ${project.title}`} />
        {!learner ? (
          <LoginPrompt action="run and check your project" />
        ) : (
          <>
            <details className="program-input">
              <summary>Input for Run (one line per IO.readln)</summary>
              <textarea rows={3} spellCheck={false} value={stdin} onChange={(e) => setStdin(e.target.value)} aria-label="Input for your program" />
            </details>
            <div className="button-row">
              <button type="button" className="button" disabled={busy !== null} onClick={execute}>
                {busy === "run" ? "Running…" : "▶ Run"}
              </button>
              {source !== starter && (
                <button
                  type="button"
                  className="button subtle"
                  onClick={() => {
                    setSource(starter);
                    clearDraft(`project:${project.id}`);
                  }}
                >
                  Start again
                </button>
              )}
            </div>
          </>
        )}
        {error && <p className="notice error">{error}</p>}
        {run && <RunOutput run={run} />}

        <h2>Milestones</h2>
        <ol className="milestones">
          {project.milestones.map((m, i) => {
            const status = statuses[m.id];
            const report = reports[m.id];
            return (
              <li key={m.id} className={`milestone${status?.passed ? " done" : ""}`}>
                <div className="milestone-head">
                  <span className="lesson-number">{i + 1}</span>
                  <h3>{m.title}</h3>
                  {status?.passed && <span className="status-badge done">✓ Passed</span>}
                  {!status?.passed && status && status.attempts > 0 && (
                    <span className="status-badge">{status.attempts} attempt{status.attempts === 1 ? "" : "s"}</span>
                  )}
                </div>
                <Markdown text={m.instructions} />
                {m.visibleTests.length > 0 && (
                  <details className="examples">
                    <summary>Examples this milestone checks ({m.visibleTests.length}, plus hidden tests)</summary>
                    <table>
                      <thead><tr><th scope="col">Call or input</th><th scope="col">Expected</th></tr></thead>
                      <tbody>
                        {m.visibleTests.map((t, k) => (
                          <tr key={k}>
                            <td><code>{t.call}</code></td>
                            <td><code>{t.expected}</code></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </details>
                )}
                {learner && (
                  <div className="button-row">
                    <button type="button" className="button primary" disabled={busy !== null} onClick={() => check(m.id)}>
                      {busy === m.id ? "Checking…" : `Check milestone ${i + 1}`}
                    </button>
                  </div>
                )}
                {report && <Results report={report} />}
              </li>
            );
          })}
        </ol>

        {project.rubric.length > 0 && (
          <>
            <h2>How it will be assessed</h2>
            <div className="table-scroll">
              <table>
                <thead><tr><th scope="col">Criterion</th><th scope="col">0</th><th scope="col">1</th><th scope="col">2</th></tr></thead>
                <tbody>
                  {project.rubric.map((r) => (
                    <tr key={r.criterion}>
                      <th scope="row">{r.criterion}</th>
                      <td>{r.zero}</td>
                      <td>{r.one}</td>
                      <td>{r.two}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

        {project.designNotePrompt && (
          <>
            <h2>Design note</h2>
            <Markdown text={project.designNotePrompt} />
            <textarea
              rows={5}
              value={note}
              onChange={(e) => {
                setNote(e.target.value);
                saveDraft(`project-note:${project.id}`, e.target.value);
              }}
              aria-label="Design note"
            />
            <p className="muted small">
              Saved in this browser only. Reviewing design notes against the rubric isn't built yet, so for now this is for you:
              write it, then compare it with the rubric above.
            </p>
          </>
        )}
      </div>
    </article>
  );
}

function Bullets({ icon, title, items }: { icon: React.ReactNode; title: string; items: string[] }) {
  return (
    <section className="project-list">
      <h3>
        {icon} {title}
      </h3>
      <ul>
        {items.map((i) => (
          <li key={i}>{i}</li>
        ))}
      </ul>
    </section>
  );
}
