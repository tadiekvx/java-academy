import { BookOpen, ExternalLink, Film, Info, Wrench } from "lucide-react";
import type { ResourceView } from "../types";

const KIND_ICON: Record<string, typeof Film> = { Video: Film, Course: BookOpen, Docs: BookOpen, Article: BookOpen, Tool: Wrench };
const LEVEL_LABEL = { introductory: "Introductory", supplementary: "Supplementary", advanced: "Advanced" } as const;
const LEVEL_HUE = { introductory: "hue-green", supplementary: "hue-blue", advanced: "hue-purple" } as const;

/**
 * Curated outside material for a lesson. Videos are embedded only when the content marks them as
 * embeddable (a verified YouTube id), via the privacy-friendly youtube-nocookie host.
 */
export function Resources({ resources }: { resources: ResourceView[] }) {
  if (resources.length === 0) {
    return null;
  }
  return (
    <section className="resources" aria-labelledby="resources-heading">
      <h2 id="resources-heading">Go further</h2>
      <p className="muted small">
        Hand-picked, checked material from other people. It supplements this lesson; it doesn't replace it.
      </p>
      <ul className="resource-list">
        {resources.map((r) => (
          <ResourceCard key={r.id} resource={r} />
        ))}
      </ul>
    </section>
  );
}

function ResourceCard({ resource: r }: { resource: ResourceView }) {
  const Icon = KIND_ICON[r.kind] ?? BookOpen;
  return (
    <li className="resource">
      <div className="resource-head">
        <span className="icon-tile small hue-pink" aria-hidden="true">
          <Icon size={18} />
        </span>
        <div>
          <a href={r.url} target="_blank" rel="noreferrer noopener" className="resource-title">
            {r.title} <ExternalLink size={13} aria-hidden="true" />
          </a>
          <div className="muted small">
            {r.creator}
            {r.published && r.published !== "n/d" ? ` · ${r.published}` : ""}
          </div>
        </div>
        <span className="chip hue-gray">{r.kind}</span>
        <span className={`chip ${LEVEL_HUE[r.level]}`}>{LEVEL_LABEL[r.level]}</span>
      </div>
      {r.embedUrl && (
        <div className="video-frame">
          <iframe
            src={r.embedUrl}
            title={r.title}
            loading="lazy"
            referrerPolicy="strict-origin-when-cross-origin"
            allow="encrypted-media; picture-in-picture; fullscreen"
            allowFullScreen
          />
        </div>
      )}
      <p className="resource-topic">
        <strong>Topic:</strong> {r.topic}
      </p>
      <p className="resource-why">
        <strong>Why this one:</strong> {r.why}
      </p>
      {r.caveat && (
        <p className="resource-caveat">
          <Info size={14} aria-hidden="true" /> <span>{r.caveat}</span>
        </p>
      )}
    </li>
  );
}
