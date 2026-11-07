// Splits a lesson's Markdown body into plain Markdown and the platform's directives
// (docs/curriculum/03-content-standards.md §2.3). Directives inside code fences are left alone.

export type Segment =
  | { kind: "markdown"; text: string }
  | { kind: "exercise"; id: string }
  | { kind: "mistake"; id: string; text: string };

const EXERCISE = /^::exercise\{id=([\w.-]+)\}\s*$/;
const MISTAKE_OPEN = /^:::mistake\{id=(\w+)\}\s*$/;
const MISTAKE_CLOSE = /^:::\s*$/;
const FENCE = /^\s*```/;

export function parseSegments(body: string): Segment[] {
  const segments: Segment[] = [];
  let markdown: string[] = [];
  let mistake: { id: string; lines: string[] } | null = null;
  let inFence = false;

  const flushMarkdown = () => {
    const text = markdown.join("\n");
    if (text.trim() !== "") {
      segments.push({ kind: "markdown", text: markRunnable(text) });
    }
    markdown = [];
  };

  for (const line of body.split("\n")) {
    if (FENCE.test(line)) {
      inFence = !inFence;
    }
    const target = mistake ? mistake.lines : markdown;
    if (inFence || FENCE.test(line)) {
      target.push(line);
      continue;
    }
    if (mistake) {
      if (MISTAKE_CLOSE.test(line)) {
        segments.push({ kind: "mistake", id: mistake.id, text: markRunnable(mistake.lines.join("\n")) });
        mistake = null;
      } else {
        mistake.lines.push(line);
      }
      continue;
    }
    const exercise = EXERCISE.exec(line);
    if (exercise) {
      flushMarkdown();
      segments.push({ kind: "exercise", id: exercise[1] });
      continue;
    }
    const open = MISTAKE_OPEN.exec(line);
    if (open) {
      flushMarkdown();
      mistake = { id: open[1], lines: [] };
      continue;
    }
    markdown.push(line);
  }
  if (mistake) {
    // Unclosed block: show its content rather than lose it. The validator reports these.
    segments.push({ kind: "mistake", id: mistake.id, text: markRunnable(mistake.lines.join("\n")) });
  }
  flushMarkdown();
  return segments;
}

/**
 * Markdown renderers drop the info string after the language, so "```java runnable" becomes a
 * distinct language name the renderer can see.
 */
function markRunnable(text: string): string {
  return text.replace(/^```java runnable\s*$/gm, "```java-runnable");
}

