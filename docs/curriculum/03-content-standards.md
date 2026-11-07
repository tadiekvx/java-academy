# Content Standards

Status: Draft 1 · 2026-11-05
Applies to: all lessons, exercises, projects and assessments.

A piece of content is **published** only when it passes every automated gate (§6) and every human gate (§7). Learners never see content in any other state. Placeholder or filler content can't be published, whether a person or a model wrote it.

---

## 1. Repository layout

Content lives in the platform repository as plain files, versioned with Git and validated in CI.

```
content/java/
  curriculum.yaml                  # concepts, misconceptions, stages → modules → lessons
  stage-1/
    lessons/
      j1-l2.3.md                   # file name = lesson id
    exercises/
      j1-l2.3-write-average/       # directory name = exercise id
        exercise.yaml
        starter/Main.java
        solution/Main.java
        wrong/integer-division.java  # known-wrong solutions; each must FAIL the tests
        reviewer-notes.md          # optional; never shown to learners
    projects/                      # (not yet built)
docs/curriculum/sources.md         # the source register; the validator reads its table rows directly
```

The source register has one copy, `docs/curriculum/sources.md`. Nothing duplicates it in YAML. `content/java/` is just a folder. There is no track abstraction in the code. A later track would add `content/python/` and its own runner.

---

## 2. Lesson standards

### 2.1 Front matter

```yaml
---
id: j1-l2.3
title: "Arithmetic: division, remainders and exact results"
concepts: [J1.02]
objectives:                   # exercises point at these ids with `assesses`
  - {id: o1, text: "Work out the value of an arithmetic expression using Java's order of operations"}
  - {id: o2, text: "Predict the result of / and % when both numbers are ints, including negative numbers"}
prerequisites: [j1-l2.1, j1-l2.2]
estimated_minutes: 35
status: in_review             # draft | in_review | published | retired
authors: [name]
ai_assisted: true             # true if any part was drafted with an AI model
technical_review: {by: null, date: null}
pedagogy_review: {by: null, date: null}
sources: [I5, I3, R3, R4, R6]
features: []                  # post-Java-8 features used, e.g. [{name: records, since: 16}]
---
```

### 2.2 Required sections

Leave a section out only when the "When optional" column allows it.

| Section | Purpose | When optional |
|---|---|---|
| **What you'll learn** | Rendered from `objectives` | Never |
| **Before you start** | Prerequisites with links; one retrieval question from a prerequisite lesson | Lesson 1.1 only |
| **Explanation** | The concept, in plain language, one idea at a time; new terms defined on first use | Never |
| **Worked examples** | At least 2, with **subgoal labels** (e.g. *"Step 1 — decide what to repeat"*) `[R4]` | Never |
| **Predict, then run** | At least 1 `predict` exercise, where the learner commits a prediction before seeing the output `[R6]` | Purely conceptual lessons (rare) |
| **Where this is used** | A real-world use of the concept, concrete rather than "this is used everywhere" | Never |
| **Common mistakes** | The misconceptions this lesson targets (by catalogue ID), each with a wrong example, why it's wrong, and the fix | Never |
| **Practice** | The ordered exercise ladder (`::exercise{id=…}` directives) | Never |
| **Version notes** | Which Java version introduced a feature; how older code looks | When no post-Java-8 feature is used |
| **Further reading** | 1–3 sources from the register, with one sentence on why each is worth reading | Never |
| **How you'll be assessed** | Which evidence types this lesson's exercises produce; what "independent" means | Never |

### 2.3 Interactive directives (Markdown extensions)

| Directive | Renders as |
|---|---|
| ` ```java runnable ` | An editable snippet with a Run button; output shown below. CI verifies it compiles. |
| `::exercise{id=j1-l2.3-write-average}` | An embedded exercise. Predict-then-run items are `predict` exercises embedded this way. Their `expected_output` is checked by CI against a real run. |
| `::trace{id=…}` | A trace-table widget. |
| `:::mistake{id=MC04}` … `:::` | A styled common-mistake block linked to the catalogue. |

### 2.4 Writing style

- UK English, second person ("you"), present tense. Keep paragraphs to 4 sentences or fewer.
- One new idea per paragraph. Introduce an example as soon as an idea needs one.
- Never use "simply", "just", "obviously" or "easy". Beginners who struggle with something called easy blame themselves.
- Code follows standard Java conventions: 4-space indentation, `camelCase` methods and variables, `PascalCase` types, meaningful names. Don't use single letters, except loop indices and the standard `i`/`j`.
- Every code block has been run. No pseudo-Java.
- Accessibility: every image has alt text; no meaning is conveyed by colour alone; diagrams have a text equivalent.

---

## 3. Explanation accuracy rules

1. Every technical claim must be true for Java 25. If behaviour differs by version, say so.
2. Simplifications are allowed only if they're **flagged** and won't need to be unlearned. Write *"for now, think of… — Stage 2 refines this"*. Don't make a false statement that will need to be retracted later.
3. Claims about the JVM, the language or the API must be checkable against the JLS `[I5]`, the API docs `[I4]` or a JEP `[I2]`. The technical reviewer checks them against these sources.
4. Educational claims made to learners (e.g. "practising recall helps you remember") must cite a source from the register.

---

## 4. Exercise standards

### 4.1 `exercise.yaml`

```yaml
id: j1-l2.3-write-average
type: write                       # predict | parsons | write | debug | modify | explain
title: An exact average
lesson: j1-l2.3
role: ladder                      # ladder (embedded in the lesson) | retrieval (scheduled later)
assesses: [o3]                    # objective ids of the lesson
concepts: [J1.02]
evidence: [IMPL]
misconceptions: [MC04]
difficulty: 2                     # 1–5 within the stage
variant_group: exact-division     # isomorphic variants share a group; used for retrieval checks
prompt: |
  Complete `average` so it returns the exact average of `a` and `b`, including any fractional part.
entry:                            # class defaults to Main (file Main.java)
  methods:
    - name: average
      params: [{name: a, type: int}, {name: b, type: int}]
      returns: double
tests:
  visible:
    - {args: [3, 4], expect: 3.5}
    - {args: [10, 10], expect: 10.0}
    - {args: [0, 5], expect: 2.5}
  hidden:                         # `name` is shown to learners; inputs and values are not
    - {name: both zero, args: [0, 0], expect: 0.0}
    - {name: negative half, args: [1, -2], expect: -0.5}
    - …
  tolerance: 1e-9                 # optional; for double results
hints:                            # authored hints: the mentor uses these as grounding for H1/H2
  h1: What type is the result when you divide an int by an int?
  h2: Make the division happen with a double, for example by dividing by 2.0 instead of 2.
limits: {time_ms: 2000}           # optional per-test time limit
starter_compiles: true            # false only for debug exercises with deliberate compile errors
ai_assisted: true
```

- **Supported test types:** `int`, `long`, `double`, `boolean`, `char`, `String`, one-dimensional arrays of those, and `List<…>`/`ArrayList<…>` of boxed types or `String`. A test may call any method declared in `entry.methods` using `method:`; it defaults to the first.
- **Input/output tests** use `{stdin: "…", stdout_equals: "…"}` or `{stdin: "…", stdout_contains: […]}`. Trailing spaces and trailing blank lines are ignored.
- **Other types.** `predict` exercises have `starter/Main.java` plus `expected_output`. `parsons` exercises have `blocks` (in a correct order) and `distractors`, and are graded by tests, so any correct order passes. `explain` exercises have a `rubric` and may name a `refers_to` exercise whose code is shown.
- **Starters must declare `void main()`.** Java 25 requires a launchable `main` method in a compact source file. Use `main` to call the learner's method with one example. Files in `wrong/` need only enough code to compile.

Input/output-style tests use `{stdin: "…", stdout_contains: […]}` or `{stdin: "…", stdout_equals: "…"}`. Complex checks may use a Java test class against the grading harness.

### 4.2 Required properties

| Property | Rule |
|---|---|
| Validated behaviour | The reference solution passes **all** tests on Java 25 in CI. |
| Test strength | At least 3 visible and 5 hidden tests for write/debug/modify. Hidden tests include the relevant edges: empty, zero, negative, boundary, large values. |
| Fixed behaviour | Exception to test strength: when no test gives the code any input (a program with no stdin, or methods without parameters), the code behaves the same on every run. Then each method needs at least one test, and an output-only program needs a `stdout_equals` test that checks its whole output. |
| Fair tests | Hidden tests only check behaviour stated in the prompt or covered by concepts already taught. For example, no `int`-overflow test before overflow has been taught. |
| Tests catch wrong answers | At least 1 file in `wrong/` that encodes a targeted misconception. Each must **fail** at least one test. |
| Starter is not a solution | The starter fails at least one test. |
| Debug exercises | The bug is described in the reviewer notes, and the bug *type* is listed under `misconceptions`. |
| Explain exercises | A rubric with 0/1/2 anchors and at least 2 sample answers per anchor level. |
| Variants | Exercises used for retrieval have at least 2 isomorphic variants in the same `variant_group`. |
| Purpose | Every exercise lists ≥ 1 concept and ≥ 1 evidence type. Exercises without these are rejected. |

---

## 5. Project standards

Every project has:

- `category: A | B | C` and a stated purpose.
- **Acceptance criteria** written as *given / when / then*, each linked to ≥ 1 automated test. Criteria that can't be automated (e.g. a design note) have a rubric instead.
- Public and hidden acceptance tests. The reference solution must pass all of them.
- A rubric with explicit anchors for each score.
- For Category A: milestones, each with tests and an explanation.
- For Category B: requirements and constraints **only**. Reviewers reject any text that prescribes implementation steps.
- For Category C: an existing codebase with listed seeded issues (bugs, debt, security, performance). There's a requirement change delivered mid-assignment and a simulated review. The full seeded-issue list lives only in `reviewer-notes.md`.

---

## 5a. Resources (`content/java/resources.yaml`)

A catalogue of outside learning material. Lessons list resource ids in front matter (`resources: [id, …]`); the lesson page shows them under "Go further". Rules enforced by the validator:

- Required: `id`, `title`, `creator`, `url` (**https**), `kind` (video, course, docs, article, tool), `level` (introductory, supplementary, advanced), `topic`, `why`, `verified_on` (yyyy-mm-dd).
- `verified_on` means **a person opened the URL and confirmed it is what the entry says**. Never add a resource that wasn't opened.
- A video is embedded only if it has a `youtube_id` (11 characters) that appears in its `url`; optional `start_seconds` is a verified timestamp. Embeds use the youtube-nocookie host.
- `caveat` is for anything a learner should know (age, scope, abandoned maintenance). Put honest limits here.
- Resources that no lesson uses are reported as warnings.

## 5b. Projects (`stage-N/projects/<id>/`)

A project is a larger program built in milestones, in one `Main.java`. Files: `project.yaml`, `starter/Main.java` (stubs that compile but are wrong), `solution/Main.java`, `wrong/<milestone>-<name>.java`.

- `category`: **A** guided (explanations per milestone), **B** independent (requirements, constraints and acceptance criteria only, a rubric of at least 3 criteria and a `design_note_prompt`), **C** professional (existing code, bug reports, a change request).
- Each milestone has `id`, `title`, `instructions`, and tests of the same kind exercises use (method tests with `entry.methods`, or stdin/`stdout_contains` tests).
- Validator, per milestone: the reference solution passes every test; the starter passes none and compiles; every known-wrong solution named for that milestone fails it.
- Passing a milestone records an attempt with id `projectId/milestoneId`. Mastery evidence: IMPL for category A, XFER for B and C.
- A test may check the **form of the source** instead of its output: `source_contains` / `source_not_contains` (lists, whitespace-collapsed). Use it only when form is the objective, such as the traditional `public class` form in Stage 0. A test uses exactly one kind: method, I/O or source.
- **Not yet supported:** multiple files, the AI mentor inside projects, review of the design note.

## 5c. Class-based exercises (Stages 2 and 3)

The grader calls the **top-level methods** of the learner's file by reflection and compares scalars, arrays and `List`s. To test a class the learner writes, the starter carries a **driver method** that uses the class and returns a string, number or list; the tests call the driver. The driver is part of the starter, and the exercise says so.

- Classes, records, enums and interfaces declared beside `main` compile as members of the implicit class, so the driver can use them. A learner-written class that the driver needs but that doesn't exist yet makes the starter fail to compile: set `starter_compiles: false`.
- A driver may use `try`/`catch` before the learner has met it. Say so in the lesson.
- **`private` is not enforced** between classes in one compact file (verified: code beside the class can read and write its private fields). Where encapsulation is the objective, add source tests (`source_contains: ["private"]`) so the starter fails and the keyword is required.
- Prefer driver outputs whose order is guaranteed: use `TreeMap`, `LinkedHashMap` or sorted output, never the iteration order of a `HashMap` or `HashSet`.
- An expected value must be computed independently of the Java reference solution (the content scripts use Python), so the validator cross-checks both.

## 6. Automated publication gates (CI)

A content change can't merge into `main` with `status: published` unless all of these pass:

1. Schema validation for every YAML/front-matter file.
2. Reference solutions compile on **Java 25** and pass all tests.
3. Each `wrong/` solution fails ≥ 1 test.
4. Each starter fails ≥ 1 test (and compiles, unless `starter_compiles: false`).
5. `runnable` snippets compile and run cleanly; each `predict` exercise's `expected_output` matches a real run.
6. All referenced concepts, misconceptions, lessons, exercises and source IDs resolve.
7. Each lesson objective is assessed by ≥ 1 exercise (via the exercise's `assesses`). Every exercise assesses ≥ 1 objective.
8. No placeholder text in published content: `TODO`, `TBD`, `lorem`, `placeholder`, `FIXME`, `XXX`, empty sections.
9. Published lessons cite no source marked `unverified` in the register.
10. Every `variant_group` has at least 3 exercises: the original plus 2 variants for retrieval.

Run the gates with `./scripts/validate-content.sh`. They also run as part of `mvn test`, through `ContentValidationTest`. Publication-standard checks are errors for `in_review` and `published` lessons, and warnings for drafts. An unverified source is a warning until a lesson is marked `published`, and then it's an error.

---

## 7. Human publication gates

| Gate | Reviewer | Checks |
|---|---|---|
| Technical review | An experienced Java engineer who isn't the author | Accuracy (§3), code quality, version correctness, tests sensible |
| Pedagogy review | A curriculum reviewer | Objectives ↔ explanation ↔ exercises ↔ assessment aligned; misconceptions addressed; difficulty progression; no implementation steps in Category B |
| Beginner walk-through (Stage 1 slice) | At least 3 people with no programming experience, unassisted | Can they complete the lesson and its ladder without developer help? Record where they got stuck; fix before publishing |

AI-assisted drafting is allowed. It must be declared (`ai_assisted: true`), and AI-assisted content goes through every gate above, the same as human-written content. A model's output is never considered reviewed.

---

## 8. Maintenance

- Every published item has an owner.
- Outcome reports (see [design §8](01-curriculum-design.md#8-measuring-educational-outcomes)) flag items for revision. Examples: an exercise with < 30% independent pass rate or > 50% H3+ usage; a concept with < 60% retrieval at 10 days. *(Initial thresholds are platform guesses; tune with data.)*
- A learner-reported error is triaged within 5 working days. A confirmed technical inaccuracy unpublishes the item until it's fixed.
