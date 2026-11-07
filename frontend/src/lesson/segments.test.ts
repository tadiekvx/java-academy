import { describe, expect, it } from "vitest";
import { parseSegments } from "./segments";

describe("parseSegments", () => {
  it("splits out exercise directives", () => {
    const segments = parseSegments("Intro\n\n::exercise{id=j1-l2.3-write-average}\n\nOutro");

    expect(segments).toEqual([
      { kind: "markdown", text: "Intro\n" },
      { kind: "exercise", id: "j1-l2.3-write-average" },
      { kind: "markdown", text: "\nOutro" },
    ]);
  });

  it("keeps code fences inside mistake blocks", () => {
    const body = [":::mistake{id=MC04}", "**Wrong**", "```java", "double half = 1 / 2 * 10;", "```", ":::", "After"].join("\n");

    expect(parseSegments(body)).toEqual([
      { kind: "mistake", id: "MC04", text: "**Wrong**\n```java\ndouble half = 1 / 2 * 10;\n```" },
      { kind: "markdown", text: "After" },
    ]);
  });

  it("ignores directive-looking lines inside code fences", () => {
    const body = "```\n::exercise{id=not-real}\n:::\n```";

    expect(parseSegments(body)).toEqual([{ kind: "markdown", text: body }]);
  });

  it("marks runnable Java blocks with a distinct language", () => {
    const [segment] = parseSegments("```java runnable\nvoid main() {}\n```");

    expect(segment).toEqual({ kind: "markdown", text: "```java-runnable\nvoid main() {}\n```" });
  });
});
