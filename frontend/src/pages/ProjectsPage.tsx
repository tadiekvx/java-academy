import { useEffect, useState } from "react";
import { Link } from "react-router";
import { Clock, FolderKanban } from "lucide-react";
import { api } from "../api";
import type { ProjectSummary } from "../types";

export const CATEGORY = {
  A: { label: "Guided build", hue: "hue-green", blurb: "Steps and explanations, with tests for each milestone." },
  B: { label: "Independent build", hue: "hue-blue", blurb: "Requirements only. You design it." },
  C: { label: "Professional assignment", hue: "hue-purple", blurb: "Existing code, changing requirements, review." },
} as const;

export function ProjectsPage() {
  const [projects, setProjects] = useState<ProjectSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    document.title = "Projects · Java Engineering Academy";
    api.projects().then(setProjects).catch((e) => setError(String(e)));
  }, []);

  if (error) {
    return <p className="notice error">{error}</p>;
  }
  if (!projects) {
    return <p className="muted">Loading…</p>;
  }
  return (
    <>
      <header className="page-header">
        <h1>Projects</h1>
        <p>Bigger programs that combine what you've learned. Guided first, then more and more on your own.</p>
      </header>
      {projects.length === 0 ? (
        <p className="muted">No projects are available yet.</p>
      ) : (
        <div className="module-grid">
          {projects.map((p) => {
            const cat = CATEGORY[p.category];
            return (
              <article key={p.id} className={`module-card ${cat.hue}`}>
                <div className="module-card-head">
                  <span className="icon-tile">
                    <FolderKanban size={22} aria-hidden="true" />
                  </span>
                  <div>
                    <span className="module-number">{cat.label}</span>
                    <h3>
                      <Link to={`/projects/${p.id}`}>{p.title}</Link>
                    </h3>
                  </div>
                </div>
                <p className="muted small">{p.summary}</p>
                <p className="small">
                  <span className="chip hue-gray">{p.milestones} milestones</span>{" "}
                  {p.estimatedHours && (
                    <span className="chip hue-teal">
                      <Clock size={13} aria-hidden="true" /> About {p.estimatedHours} hours
                    </span>
                  )}{" "}
                </p>
              </article>
            );
          })}
        </div>
      )}
    </>
  );
}
