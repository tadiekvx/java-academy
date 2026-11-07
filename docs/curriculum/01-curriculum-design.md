# Java Engineering Academy — Curriculum Design

Status: Draft 1 · 2026-11-05 · Owner: curriculum lead
Related: [Stage 1 detailed design](02-stage-1-foundations.md) · [Content standards](03-content-standards.md) · [AI mentor policy](04-ai-mentor-policy.md) · [Source register](sources.md)

This document turns the research phase into decisions about the curriculum. Every claim that rests on outside evidence carries a source ID (e.g. `[R5]`) that resolves in the [source register](sources.md). Each source is labelled with one of three evidence classes:

| Label | Meaning | How we treat it |
|---|---|---|
| **Research** | Peer-reviewed educational or cognitive-science research | Strongest basis, but findings come from specific populations (school pupils, university CS1 students) and need adapting for self-paced adults |
| **Industry** | Official documentation, standards bodies, established professional references | Authoritative for *what* to teach and for technical accuracy |
| **Community** | Forum discussions, developer surveys, individual practitioner opinion | A signal worth investigating, never treated as established fact |
| **Platform** | Our own design decisions and recommendations | Must be labelled as ours and validated against learner outcome data (§8) |

---

## 1. Product scope: Java first

- Java is the only language at launch. All curriculum, exercises, tooling and mentorship are built for Java specifically. We add no language-agnostic abstractions for languages the platform doesn't support. *(Platform)*
- Platform modules (content, curriculum, assessment, execution, projects, progress, mentor) are separated by domain, not by language. A future Python track would add content and a runner. It would not require redesigning progress tracking or mastery. *(Platform)*

### 1.1 Java version policy

| Decision | Detail | Basis |
|---|---|---|
| **Target release: Java 25 (LTS)** | GA September 2025. Oracle Premier Support runs to September 2030. The learner runtime, platform runtime and all published code target 25. | Oracle Java SE Support Roadmap `[I1]` |
| Non-LTS releases are not targeted | JDK 26 (March 2026) and JDK 27 (September 2026) are non-LTS. Lessons may mention their features as "newer Java" sidebars only. | `[I1]` |
| **Next re-baseline: Java 29** | Planned LTS for September 2027. Start a curriculum review within 3 months of GA. | `[I1]` |
| Preview features are never core content | Examples in JDK 25: primitive patterns, structured concurrency, stable values. They may appear only in a clearly labelled "Preview" sidebar, and learner code never requires `--enable-preview`. | Platform |
| Every version-specific feature is labelled | Each lesson that relies on a feature added after Java 8 states the version it arrived in (e.g. *records — Java 16*, *pattern matching for `switch` — Java 21*). Learners will meet Java 8/11/17/21 codebases at work. | Platform |
| JDK 21 context | Oracle JDK 21 updates move to the OTN licence from the October 2026 CPU. This is a further reason not to target 21 for new learners. Employers may still run 21, so Stage 7+ includes a "working across versions" activity. | `[I1]` |

### 1.2 Beginner entry point: compact source files (Java 25)

JEP 512 `[I2]` (final in Java 25) allows a beginner's first program to be:

```java
void main() {
    IO.println("Hello, world");
}
```

- No `public class`, no `static`, no `String[] args`. `java.lang.IO` provides `print`, `println` and `readln`. Compact source files implicitly import the whole `java.base` module, so `ArrayList`, `List` and the rest of `java.util` need no imports.
- **Decision:** Stage 1 uses compact source files throughout. *Rationale:* the old ceremony makes novices learn several concepts (classes, access modifiers, static, arrays) as unexplained incantations before any of them can be taught. Removing it lowers extraneous cognitive load `[R3]`. *(Platform decision informed by Research)*
- **Mandatory transition:** The first lesson of Stage 2 explicitly rewrites Stage 1 programs into the traditional `public class Main { public static void main(String[] args) }` form and explains each keyword, now that classes are being taught. *Rationale:* most existing code, tutorials and interview material use the traditional form, and learners must be able to read it.
- **Known risk:** Resources published before 2025, and most Stack Overflow answers, show the traditional form. Lesson 1.1 includes a "You'll also see…" box so learners aren't confused when they use outside material.

---

## 2. The learning cycle

Every major concept passes through six activities. A single lesson rarely contains all six. They are spread across lessons, modules and stages, and the curriculum map (§5 and the [Stage 1 design](02-stage-1-foundations.md)) records where each happens for each concept.

| # | Activity | What the learner does | Platform mechanism | Evidence base |
|---|---|---|---|---|
| 1 | **Understand** | Reads the explanation, studies worked examples, **predicts** output before running code | Lesson pages, worked examples with subgoal labels, predict-then-run widgets | Worked examples `[R3]`, subgoal labels `[R4]`, PRIMM "Predict/Run" `[R6]` |
| 2 | **Apply** | Writes code independently against tests | Parsons problems (scaffolded) → write-from-scratch exercises with hidden tests | Parsons problems `[R7]`, fading of guidance as expertise grows `[R3]` |
| 3 | **Investigate** | Traces, reads and debugs unfamiliar code, and modifies working code | Trace tables, find-the-bug, modify-to-new-spec exercises | Reading/tracing precedes writing `[R5]`, PRIMM "Investigate/Modify" `[R6]`, debugging literature `[R16]` |
| 4 | **Build** | Applies concepts together in a project | Category A/B/C projects (§3) | Platform |
| 5 | **Explain** | Explains code, decisions and trade-offs in their own words | Short written explanations scored against rubrics, and mentor follow-up questions | Self-explanation effect `[R11]` |
| 6 | **Reinforce** | Retrieves the concept later in new contexts, without notes | Spaced retrieval checks and cumulative stage gates | Retrieval practice `[R1]`, spacing `[R2]` |

**Design tension, stated openly:** worked-examples research `[R3]` favours explicit instruction before problem solving for novices. Productive-failure research `[R14]` finds benefits from attempting problems *before* instruction in some conditions. Our resolution *(Platform)*:
- Stage 1 is mostly "example first".
- From Stage 2 onward, some lessons open with a short, low-stakes "try it first" challenge before the explanation.
- Outcome data (§8) decides whether to expand or reduce this.

The expertise-reversal effect `[R3]` also implies that scaffolding should **fade** as learners progress. The share of Category A projects drops stage by stage (§3).

---

## 3. Project categories

| Category | What the learner gets | What the learner must do | Typical size |
|---|---|---|---|
| **A — Guided build** | Explanations, examples, milestones, tests per milestone | Implement each milestone; explain choices at checkpoints | 2–6 hours |
| **B — Independent build** | Requirements, acceptance criteria, constraints, *no* implementation steps | Design and implement; submit tests and a short design note | 4–15 hours |
| **C — Professional assignment** | An existing codebase with bugs, technical debt, incomplete or changing requirements, architectural constraints, test/performance/security/documentation expectations | Triage, fix, extend, refactor, test, document; respond to a simulated code review | 6–30 hours |

Category C is introduced in Stage 2. Before that, learners don't have enough concepts to work productively in an existing codebase. Stage 1 still includes small "inherited code" investigate exercises.

**Target share of project time by category** *(Platform; revisit with outcome data)*:

| Stage | A | B | C |
|---|---|---|---|
| 1 Foundations | 60% | 40% | 0% |
| 2 Object-oriented design | 35% | 45% | 20% |
| 3 Core library & data | 25% | 45% | 30% |
| 4 Professional toolchain | 20% | 30% | 50% |
| 5 Data structures & algorithms | 15% | 60% | 25% |
| 6 Concurrency & the JVM | 20% | 40% | 40% |
| 7 Persistence & web services | 15% | 40% | 45% |
| 8 Professional engineering | 0% | 25% | 75% |

Across the whole curriculum, B + C is about 75% of project time.

---

## 4. Evidence-based mastery model

Mastery is a property of a **concept** (e.g. `J1.07 loops`), not of a lesson. Completing lessons, time spent and repeated exposure never award mastery. Progressing on demonstrated mastery rather than on time has strong meta-analytic support `[R10]`. The specific evidence rules below are platform decisions.

### 4.1 Evidence types

Each assessable activity records which kind of evidence it produces for which concepts:

| Code | Evidence | Typical activity |
|---|---|---|
| `IMPL` | Implements the concept independently | Write-code exercise, project milestone |
| `EXPL` | Explains the underlying principle | Rubric-scored explanation, mentor follow-up question |
| `MIST` | Identifies a common mistake | Multiple-choice misconception item, "spot the error" item |
| `DEBUG` | Debugs an incorrect implementation | Fix-the-bug exercise |
| `MOD` | Modifies an existing implementation | Modify-to-new-spec exercise |
| `XFER` | Applies the concept to a new problem | Novel-context problem, Category B/C project task |
| `TRADE` | Explains a relevant trade-off | Design-note prompts (Stage 2+) |

Not every concept needs every evidence type. Each concept definition lists its **required evidence set**. For example, `J1.02 values-and-types` requires `IMPL, MIST, EXPL`. `J1.07 loops` requires `IMPL, DEBUG, MOD, XFER, EXPL`.

### 4.2 Assisted vs independent

Every attempt records the **highest assistance level used** (see the [mentor policy](04-ai-mentor-policy.md) for levels H0–H4) and whether the reference solution was viewed.

- **Independent evidence:** passed with assistance ≤ H1 (a conceptual nudge at most) and no solution viewed.
- **Assisted evidence:** passed with H2–H4. This is recorded and shown to the learner, but it never counts towards mastery levels 3 and above.
- If a learner views the solution, that exercise is permanently ineligible as independent evidence. The system schedules an **isomorphic variant** (same concept, different surface problem) for a later session.

The learner's progress page shows both numbers side by side, for example *"Loops: 6 exercises passed — 4 independently, 2 with help."*

### 4.3 Mastery levels (per concept)

| Level | Name | Rule |
|---|---|---|
| 0 | Not started | — |
| 1 | Introduced | Lesson content viewed. Shown to the learner, but explicitly *not* mastery. |
| 2 | Practising | At least one passing attempt (assisted or independent) |
| 3 | Demonstrated | Independent evidence covers **every** evidence type in the concept's required set, across at least 2 distinct exercises |
| 4 | Secure | Demonstrated **and** passed at least one delayed retrieval check (≥ 3 days after reaching Demonstrated), independently, without access to prior solutions |
| 5 | Retained | Secure **and** passed a later cumulative assessment (stage gate or ≥ 21-day retrieval check) |

**Decay:** A failed retrieval check lowers the level by one, down to a minimum of 3 (Demonstrated), and adds the concept to the review queue. A failure never erases the record. History is append-only.

### 4.4 Retrieval checks ("knowledge checks")

- These are short (2–10 minute) tasks presented in a **clean editor**: no access to the learner's earlier solutions, notes panel hidden, mentor limited to H1.
- Items are drawn from a pool of isomorphic variants, so learners aren't re-solving the identical problem.
- Spacing schedule: about 3, 10 and 30 days after a concept reaches Demonstrated. On failure the schedule restarts at the shortest interval. *(Platform. The spacing literature `[R2]` supports expanding gaps but doesn't prescribe these exact intervals. Tune them with data.)*
- The learner's dashboard shows up to 3 due checks per session, interleaved across concepts. Interleaving is a desirable difficulty `[R2]`.

### 4.5 Stage gates

Each stage ends with a cumulative assessment. It contains new, unseen problems, one each of: write, debug, trace/predict, modify, and explain. It is taken independently (mentor capped at H1). Passing requires meeting each item's rubric threshold. A learner who fails gets a personalised review plan built from the failed concepts and can retake with fresh variants after 48 hours.

---

## 5. Curriculum stages

Each stage below records the seven required design fields. Stage 1 is designed in full detail in [02-stage-1-foundations.md](02-stage-1-foundations.md). Stages 2–8 are outline-level and will be designed in detail before build, using the same template.

### Stage 1 — Programming foundations in Java *(vertical slice)*

| Field | Decision |
|---|---|
| **Why included** | Every later stage assumes fluent use of values, control flow, methods and simple collections. Novices' biggest difficulties are tracing program state and composing constructs, not syntax `[R5][R8]`. |
| **Competency developed** | Reads, traces, writes, debugs and modifies small procedural programs (≤ 150 lines) that take input, make decisions, repeat work, decompose logic into methods and process lists of data. |
| **Prerequisites** | None beyond computer literacy and arithmetic. |
| **How taught** | Example-first lessons with subgoal-labelled worked examples `[R3][R4]`; predict-before-run for every new construct `[R6]`; trace tables before writing loops `[R5]`; explicit misconception treatment driven by novice-Java error data `[R9]`. Compact source files (§1.2). |
| **Reinforcing activities** | Parsons → write → debug → modify exercise ladders per concept; a Category A guided project (Study Log); a Category B independent project (Parking Fee Calculator); spaced retrieval checks. |
| **Mastery assessment** | Concept-level mastery (§4) plus the Stage 1 gate: unseen write + debug + trace + modify + explain items. |
| **Supporting resources** | dev.java Learn `[I3]`; Java 25 API docs `[I4]`; JEP 512 `[I2]`; *Think Java* 2e (free) `[I7]`; University of Helsinki MOOC Java Programming `[I8]` as optional additional practice. |

### Stage 2 — Object-oriented programming and program design

| Field | Decision |
|---|---|
| **Why included** | Java is class-based. Professional Java code is organised around types, encapsulation and interfaces, and learners can't work in real codebases without these. |
| **Competency** | Designs small multi-class programs; chooses between classes, records, enums, interfaces and sealed hierarchies; uses composition over inheritance where appropriate; handles exceptions deliberately; implements `equals`/`hashCode` correctly. |
| **Prerequisites** | Stage 1 at level ≥ 3 for methods, conditionals, loops and lists. |
| **How taught** | Opens with the traditional `main` transition (§1.2). Each language feature is introduced by a design problem it solves. Code-reading of well-designed vs poorly designed versions of the same program. First "try it first" lessons (§2). |
| **Reinforcing activities** | Category A: Library catalogue. Category B: Card game engine with sealed `Card` hierarchy. **First Category C:** inherited inventory system with mutable shared state bugs, a missing `hashCode`, and a changed requirement. |
| **Mastery assessment** | Concept mastery; design-note `TRADE` evidence (e.g. "record or class here, and why?"); stage gate including a refactor task. |
| **Resources** | dev.java Learn `[I3]`; *Effective Java* 3e, items on classes/interfaces and `equals`/`hashCode` `[I9]`; JLS 25 for records, sealed classes and pattern matching `[I5]`. |

### Stage 3 — The core library and data handling

| Field | Decision |
|---|---|
| **Why included** | Professional Java leans heavily on the collections framework, generics, lambdas/streams, `Optional`, `java.time` and NIO file handling. Misusing these is a frequent source of bugs and code-review findings. |
| **Competency** | Selects the right collection for a need and states its behaviour; writes generic methods; uses streams where they improve clarity and loops where they don't; processes files and text; handles dates and times correctly. |
| **Prerequisites** | Stage 2 (interfaces, records, exceptions). |
| **How taught** | Contrast-based: the same task with a loop and with a stream, discussed for readability. Comparisons between collection types. Real data files (CSV, logs). |
| **Reinforcing activities** | Category B: Log-file analyser. Category C: inherited report generator with time-zone bugs and performance problems from repeated list scans. |
| **Mastery assessment** | Concept mastery; trade-off explanations (loop vs stream; `List` vs `Set` vs `Map`); stage gate. |
| **Resources** | Java 25 API docs `[I4]`; dev.java collections and streams tutorials `[I3]`; *Effective Java* 3e, generics and lambdas chapters `[I9]`. |

### Stage 4 — Professional toolchain and practice

| Field | Decision |
|---|---|
| **Why included** | Employers expect testing, build tools, version control, debugging with a debugger, and code review from day one. Community advice consistently highlights these gaps in self-taught developers `[C1]`. This is treated as a signal, and it is consistent with the curriculum frameworks `[I10]`. |
| **Competency** | Writes meaningful JUnit tests (including edge cases); builds with Maven; uses Git branches and pull requests; uses a step debugger; reads and responds to code review; applies basic refactorings safely under tests; uses static analysis. |
| **Prerequisites** | Stage 3. *Note:* learners have **read** tests and test output since Stage 1, and have written simple tests since Stage 2. Stage 4 formalises the practice. |
| **How taught** | Mostly through Category C work in realistic repositories. Simulated code reviews with rubric-based feedback. |
| **Reinforcing activities** | Category C: "first week on the job" — clone, build, fix a ticket, add tests, open a PR, address review comments. |
| **Mastery assessment** | Concept mastery; test-quality rubric (do tests catch seeded mutants?); review-response rubric. |
| **Resources** | JUnit user guide `[I11]`; Maven docs `[I12]`; Pro Git `[I13]`; Feathers, *Working Effectively with Legacy Code* `[I14]`; Fowler, *Refactoring* 2e `[I15]`. |

### Stage 5 — Data structures and algorithms in Java

| Field | Decision |
|---|---|
| **Why included** | Complexity reasoning underpins performance work and technical interviews. Implementing core structures deepens understanding of the collections learners already use. |
| **Competency** | Analyses time/space complexity; implements and tests lists, hash tables, trees, heaps and graph traversals; chooses algorithms based on constraints. |
| **Prerequisites** | Stages 2–4 (generics, testing). |
| **How taught** | Implement-then-compare against `java.util` implementations; measure with simple benchmarks and discuss why micro-benchmarks mislead. |
| **Reinforcing activities** | Category B heavy: route planner, autocomplete index. Category C: optimise an inherited slow service under a performance requirement. |
| **Mastery assessment** | Concept mastery; complexity explanations; unseen problems in the stage gate. |
| **Resources** | Sedgewick & Wayne, *Algorithms* 4e (Java) `[I16]`; Java 25 API docs `[I4]`. |

### Stage 6 — Concurrency and the JVM

| Field | Decision |
|---|---|
| **Why included** | Server-side Java is concurrent. Virtual threads (Java 21) changed recommended practice. JVM memory and GC knowledge is needed to diagnose production problems. |
| **Competency** | Uses executors and virtual threads; identifies and fixes data races and deadlocks; uses `java.util.concurrent` correctly; reads GC logs and JFR recordings at a basic level. |
| **Prerequisites** | Stages 3–5. |
| **How taught** | Bugs first: learners observe a race condition before learning the fix. Scoped values (final in Java 25) are taught. Structured concurrency stays a Preview sidebar while it remains in preview. |
| **Reinforcing activities** | Category C: inherited web scraper with thread-safety bugs and a throughput requirement. |
| **Mastery assessment** | Debug-heavy stage gate; trade-off explanations (platform vs virtual threads). |
| **Resources** | Goetz et al., *Java Concurrency in Practice* `[I17]` (principles still valid; predates virtual threads, so supplemented); JEP 444 (virtual threads), JEP 506 (scoped values) `[I2]`. |

### Stage 7 — Persistence and web services

| Field | Decision |
|---|---|
| **Why included** | Most Java jobs involve building or maintaining web services backed by databases, commonly with Spring. |
| **Competency** | Writes SQL and uses JDBC; builds REST services with Spring Boot; validates input; applies basic security controls; writes integration tests against real databases. |
| **Prerequisites** | Stages 4 and 6. |
| **How taught** | Plain JDBC first, then Spring, so the framework isn't magic. Security issues are taught by finding them in inherited code. |
| **Reinforcing activities** | Category B: booking API. Category C: inherited API with an injection vulnerability, N+1 queries, missing validation and an undocumented endpoint. |
| **Mastery assessment** | Concept mastery; security review rubric; API documentation rubric. |
| **Resources** | Spring Boot reference docs `[I18]`; OWASP Top 10 `[I19]`; PostgreSQL docs `[I20]`. |

### Stage 8 — Professional engineering (capstone)

| Field | Decision |
|---|---|
| **Why included** | Brings everything together in conditions that resemble a job: ambiguity, changing requirements, legacy code and trade-offs. |
| **Competency** | Works effectively in an unfamiliar codebase; makes and documents architectural decisions; balances performance, security, maintainability and delivery. |
| **Prerequisites** | Stage 7. |
| **How taught** | Almost entirely Category C. Requirements change mid-assignment. Simulated stakeholder clarifications through the mentor. |
| **Reinforcing activities** | A multi-week capstone: an inherited service, a feature roadmap, architecture decision records, and an observability and deployment task. |
| **Mastery assessment** | Capstone rubric covering correctness, tests, design notes, a review response and an explanation interview. |
| **Resources** | SWEBOK v4 `[I21]`; ADR practice `[C2]`; prior-stage resources. |

---

## 6. Content depth over size

*(Platform)* Target size for Stage 1: about 25 lessons, about 120 exercises (counting isomorphic variants, which exist for retrieval, not to pad the count), and 2 projects. Every exercise must declare which concept(s) it serves and which evidence type it produces (§4.1). An exercise that doesn't add evidence or meaningful variation isn't written. The content architecture (see [content standards](03-content-standards.md)) supports thousands of items over time. The size of the catalogue is not a goal.

---

## 7. Platform architecture implications

The curriculum design imposes the following requirements on the build. *(Platform)*

| Module | Responsibility | Requirement from this document |
|---|---|---|
| `content` | Versioned lesson/exercise/project files in the repo, validated at build time | Every exercise's reference solution must compile and pass its own tests in CI. Placeholders can't be published. |
| `curriculum` | Stages → modules → lessons; concept graph with prerequisites | Concepts are first-class entities with required evidence sets. |
| `assessment` | Exercise definitions, grading, rubrics, retrieval-check scheduling | Hidden tests; isomorphic variant pools; clean-editor mode. |
| `execution` | Compiles and runs learner Java code | Java 25 only. **Local JVM process runner for development.** It is not safe for untrusted users, so a sandboxed runner is required before any public launch. |
| `projects` | Multi-file projects, milestones, acceptance tests | Milestone tests; design-note submissions. |
| `progress` | Attempts, evidence, mastery levels, retrieval schedule | Append-only attempt log; assistance level and solution-viewed recorded per attempt. |
| `mentor` | AI assistance with escalation levels and safeguards | See [mentor policy](04-ai-mentor-policy.md). Any code the mentor shows is compiled and tested first. |

**Grading compact source files:** the class a compact source file declares implicitly can't be named in source `[I2]`. The grader therefore compiles the learner's file and invokes the required methods **reflectively** on the implicit class. Test authors write tests against a small harness API (`call("average", 3, 4)`), not against the class directly.

---

## 8. Measuring educational outcomes

The product metric is **capability gained**, not content consumed. *(Platform)*

| Outcome | Measure | Data source |
|---|---|---|
| Independent exercise success | First-attempt independent pass rate on exercises the learner has never seen | Attempt log |
| Retention | Retrieval-check pass rate by concept and by delay (3/10/30 days) | Retrieval checks |
| Solving unfamiliar problems | Pass rate on `XFER` items and stage-gate novel items | Stage gates |
| Debugging proficiency | `DEBUG` pass rate and time to fix; number of runs before a fix | Attempt log |
| Code quality | Static analysis findings per submission; rubric scores on projects | Analysis pipeline, rubrics |
| Project quality | Acceptance criteria met; rubric scores | Projects |
| Explaining decisions | `EXPL`/`TRADE` rubric scores | Explanations |
| Hint dependency | Mean highest assistance level per exercise, trended over the learner's history | Mentor log |
| Working with unfamiliar code | Category C task success (Stage 2+) | Projects |

**Using the data to improve the curriculum:**
- A concept with high initial pass rates but low 10-day retrieval suggests too little practice or spacing.
- An exercise with very high H3+ usage suggests a gap in its lesson or an exercise that's too hard.
- Rising hint dependency for a learner cohort suggests the scaffolding has faded too quickly.

Each quarterly content review starts from these reports.

---

## 9. Review cycle

- **Technical accuracy:** a named reviewer approves every lesson before publication (see [content standards](03-content-standards.md)).
- **Java releases:** review "newer Java" sidebars every March and September. Fully re-baseline at each LTS (next: Java 29, planned September 2027 `[I1]`).
- **Sources:** re-verify the source register annually. Any source still marked *unverified* blocks publication of content that depends on it.
