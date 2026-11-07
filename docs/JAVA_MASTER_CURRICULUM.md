# Java Master Curriculum

Date: 2026-11-05 · Target: **Java 25 (LTS)** · Basis: `CURRICULUM_AUDIT.md`, `LEARNING_METHODOLOGY.md`

This is the roadmap from absolute beginner to a Java engineer who can build, test, secure, deploy and operate a backend service **independently**. It supersedes the stage outline in `01-curriculum-design.md`. Stage 1 is built (and is being expanded, §Stage 1). Every other stage is **planned**, not written.

## How to read this document

Each module lists:

- **Prerequisites** – what must be demonstrated before starting (concept IDs or earlier modules).
- **After this module the learner can…** – the competencies. These are statements about ability, and each is assessed.
- **Lessons** – the planned lessons, in order.
- **Practice** – guided exercises (G), independent challenges (I), debugging activities (D) and code-reading activities (R).
- **Project** – category A (guided), B (independent, requirements only) or C (professional assignment), as defined in `01-curriculum-design.md` §3.
- **Assessment** – what counts as evidence of mastery, always including independent performance.

### Principles that shape the whole sequence

1. **Fundamentals before frameworks.** Spring appears only after OOP, collections, testing, SQL and HTTP basics (methodology T5).
2. **Build early and keep building.** Every stage has a project; one application evolves across stages (below).
3. **Read others' code from the start.** Code-reading is a graded evidence type from Stage 1.
4. **Scaffolding fades.** Share of guided work falls from ~60% (Stage 1) to near zero (Stage 12); independent and professional assignments dominate later stages.
5. **Independent competence is assessed separately** at every stage: build without a tutorial, debug unfamiliar code, modify under changing requirements, justify a decision.
6. **Depth over volume.** Where a stage lists a topic, the module teaches *when to use it, when not to, and what goes wrong*, not a feature tour.

### Assessment types used throughout

| Code | Assessment | Independent? |
|---|---|---|
| G | Guided exercises (hints available) | partly |
| I | Independent challenge: requirements only, hidden tests, mentor capped at nudges | yes |
| D | Debug an unfamiliar program with several faults | yes |
| R | Read and explain unfamiliar code, then modify it | yes |
| P | Project milestones with acceptance tests and a rubric | yes (Cat. B/C) |
| X | Explain/justify: design note, trade-off, review response | yes |
| Gate | Stage gate: unseen problems of every type above | yes |

## The continuing project: "Brightbank"

A small retail bank grows with the learner. Each stage adds a capability **using only what has been taught**, and often requires the learner to *restructure* what they built earlier. That experience of professional software evolving is the point.

| Stage | Brightbank at this stage | New skills it forces |
|---|---|---|
| 1 | Console **account simulator**: deposit, withdraw, balance, statement, using methods and an array/list of transactions | Input validation, methods, arrays/lists, tracing |
| 2 | `Account`, `Transaction`, `Customer` classes; `SavingsAccount` and `CurrentAccount`; refactor Stage 1 | Encapsulation, interfaces, equals/hashCode, exceptions (`InsufficientFunds`) |
| 3 | Collections of accounts, search and reports with streams, **file persistence** (CSV/JSON), `java.time` for statements | Collections, generics, streams, I/O |
| 4 | Move to **Maven/Gradle**, **Git** history, **JUnit** tests, logging, a code review | Tooling, tests as design, refactoring under test |
| 5 | Statement search/sort, transaction history structures, interest calculation, duplicate detection | Complexity, hash maps, sorting, trade-offs |
| 6 | Relational schema, **SQL**, **JDBC**, then **JPA/Hibernate** repositories | Normalisation, transactions, N+1 |
| 7 | **Spring Boot REST API** over the same domain | HTTP, DI, validation, integration tests |
| 8 | **Authentication and authorisation**, audit log, secrets handling | Spring Security, OWASP, threat modelling |
| 9 | **Concurrent transfers**, deadlock and race bugs found and fixed; performance tuning | Locks, atomicity, executors, profiling |
| 10 | Split into services/modules; idempotent transfer API; events; resilience | Architecture, consistency, failure modes |
| 11 | **Docker**, CI/CD, deployment to a cloud environment, monitoring | Containers, pipelines, observability |
| 12 | Capstone: harden, scale and **operate** it; handle a seeded production incident | Production troubleshooting, ADRs |

Rule: a stage's project never requires an idea from a later stage. When an earlier design is awkward (parallel arrays in Stage 1, then objects in Stage 2), the awkwardness is intended.

---

## Stage 0 · Your own machine *(new; short; before or alongside Stage 1)*

### Module 0.1 — Running Java outside the browser
- **Prerequisites:** none.
- **After this module the learner can** install a JDK 25, check the version, compile and run a program from a terminal, run a program in an IDE (IntelliJ IDEA Community or VS Code with Java), and read a compiler error in each place.
- **Lessons:** What the JDK is and what `java`/`javac` do · Installing and checking your setup · Running from the terminal · Your first IDE project · Source file, class file, the older `public static void main` form.
- **Practice:** G: reproduce lesson 1.1 on the learner's machine (self-checked with a provided test program). D: three deliberately broken setups (wrong version on PATH, file name mismatch, missing semicolon). R: read a "Hello" project's folder layout.
- **Project:** none.
- **Assessment:** learner submits terminal output proving the toolchain works (checked by pattern), and answers the explain prompt on compile vs run.
- **Status:** planned; **gap identified in the audit.**

---

## Stage 1 · Programming foundations in Java *(built; being expanded)*

**Competency:** reads, traces, writes, debugs and modifies small procedural programs (up to ~150 lines) and builds a complete small program from requirements.

| Module | Status | Lessons |
|---|---|---|
| 1 First programs | built | 1.1, 1.2 |
| 2 Values and variables | built | 2.1–2.4 |
| 3 Input and decisions | built | 3.1–3.4 |
| 4 Repetition | built | 4.1–4.5 |
| 5 Methods | built | 5.1–5.5 |
| 6 Working with data | built | 6.1–6.5 |
| **7 Whole programs** | written (AI draft, unreviewed) | 7.1 Reading a program you didn't write · 7.2 From requirements to a plan · 7.3 Testing your own program · 7.4 Mixed-skills challenges |
| **8 Stage projects and assessment** | **P1–P3 and assessment built** | Projects P1–P3, independent assessment |

### Module 7 — Whole programs *(new)*
- **Prerequisites:** modules 1–6 at level ≥ 3 (Demonstrated) for loops, methods, arrays/lists.
- **After this module the learner can** read an unfamiliar 80-line program and say what it does; break a requirements paragraph into methods and test cases before coding; write simple checks for their own methods; and choose between a loop, a conditional, a method and a list for a new problem without being told which.
- **Lessons:** 7.1 Code reading (trace unfamiliar code, find the entry point, follow the calls) · 7.2 Requirements to plan (restate, list inputs/outputs, list cases, decompose) · 7.3 Writing your own checks (a `check` helper, edge cases, test-first) · 7.4 Mixed-skills challenges (no lesson topic given).
- **Practice:** R ×6 (read, predict, explain, then modify); I ×8 whole-program challenges (e.g. tip splitter, leap-year calendar printer, word-frequency counter, number-guessing game with validation); D ×4 programs with 2–3 faults each.
- **Assessment:** mixed-concept challenges where **the lesson does not name the construct**; at least 4 independent passes at ≤ H1 assistance.

### Module 8 — Stage 1 projects and assessment *(new)*
- **P1 Personal finance calculator (Cat. A) — built.** Input income and monthly expenses, validate, print a budget summary and savings rate. Teaches: input validation loops, methods, formatting numbers. Milestones with tests.
- **P2 Shopping basket and receipt generator (Cat. B) — built.** Requirements and acceptance criteria only: items with prices in pence, quantity discounts, receipt layout. Constraints: whole pence, ≥ 4 methods, none > 25 lines. Design note ≤ 150 words.
- **P3 Brightbank account logic (Cat. B, first stage of the continuing project) — built.** Balance, withdrawal rules with an overdraft, recording a transaction by copying an array, a mini statement, and a mid-assignment change request (a daily withdrawal limit). A menu-driven console front end is a stretch goal (needs the stdin milestone type from P1).
- **Other practice projects offered as alternatives:** savings tracker (compound growth table), number games (guess, nim), employee salary calculator (tax bands), transaction simulator (random deposits/withdrawals with a fixed seed).
- **Stage 1 independent assessment — built as `j1-a1-inherited-gradebook` (Cat. C):** three bug reports in inherited code, a new feature and a change request. The fuller gate described originally (unseen variant pools, retake after 48 h, read-and-explain items) is **not** built.
- **Expected competency on exit:** can build P2-sized programs alone.

---

## Stage 2 · Object-oriented programming *(written; AI draft, unreviewed; see "As built" below)*

**Competency:** designs small multi-class programs, chooses between classes, records, enums and interfaces, uses composition, handles errors with exceptions, and reads an unfamiliar class hierarchy.

### Module 2.1 — Classes and objects
- **Prerequisites:** Stage 1 gate; traditional `public static void main` form.
- **After this module the learner can** model a thing as a class with fields, constructors and methods; explain `this`, `new`, `static` vs instance; draw object/reference diagrams; and explain why `==` on objects differs from `equals`.
- **Lessons:** From the compact main to a class · Fields and constructors · Methods and `this` · Objects and references (memory diagram, aliasing revisited) · `static` and when not to use it · `toString`, `equals`, `hashCode`.
- **Practice:** G ×10; I: model a `Counter`, `Rectangle`, `Temperature`; D: aliasing and `equals` bugs; R: read a 120-line domain model and explain object relationships.
- **Project:** *Brightbank v2 (Cat. A)* — refactor the Stage 1 simulator into `Account` and `Transaction`.
- **Assessment:** I + R; explain-the-diagram prompt.

### Module 2.2 — Encapsulation and invariants
- **Prerequisites:** 2.1.
- **After this module the learner can** keep fields private, protect invariants in constructors and setters, and choose immutable designs; explain why encapsulation lets code change safely.
- **Lessons:** Access modifiers · Invariants and validation · Immutability · Defensive copies (arrays and lists in objects) · Value vs identity.
- **Practice:** I: `Money` class that never holds negative pence; D: a class whose invariant is broken through a returned list; X: critique a leaky class.
- **Assessment:** break-the-class exercise (find three ways to violate the invariant).

### Module 2.3 — Interfaces, inheritance and polymorphism
- **Prerequisites:** 2.1–2.2.
- **After this module the learner can** define and implement interfaces, use polymorphism, and say when to prefer composition over inheritance, with a reason.
- **Lessons:** Interfaces and implementations · Polymorphism and dynamic dispatch (trace) · Inheritance and `super` · Abstract classes · Composition over inheritance · The Liskov test (can I substitute?).
- **Practice:** G; I: payment-method hierarchy vs composition; D: `equals` broken by inheritance; R: read a framework-style hierarchy.
- **Project:** *Brightbank v2 (Cat. B)* — `SavingsAccount` and `CurrentAccount` with different fee rules; a new account type arrives mid-assignment.
- **Assessment:** X: justify inheritance vs composition in one case.

### Module 2.4 — Modern type features
- **After this module the learner can** use records, enums, sealed hierarchies and pattern matching `switch` to model fixed sets of possibilities; compare with classes.
- **Lessons:** Records · Enums with fields · Sealed interfaces · Pattern matching for `switch` and `instanceof` · Choosing: class, record, enum, sealed (version labels per feature).
- **Practice:** I: model transaction kinds as a sealed interface of records; D: non-exhaustive switch; X: trade-offs.

### Module 2.5 — Errors and exceptions
- **After this module the learner can** throw and catch exceptions, define a custom checked and unchecked exception, use try/finally and try-with-resources, and decide where an error should be handled.
- **Lessons:** Catching exceptions · Checked vs unchecked · Custom exceptions (`InsufficientFundsException`) · Cleanup (try-with-resources) · Where to catch (design) · Never swallow errors.
- **Practice:** I: make the bank reject invalid operations; D: swallowed exceptions and lost causes; R: read stack traces with `Caused by`.
- **Stage 2 project:** *Brightbank v2 complete (Cat. C)* — an existing small codebase with seeded design weaknesses, a changing requirement and a code review to respond to.
- **Stage 2 gate:** design a small class model from a paragraph; debug an unfamiliar hierarchy; justify one decision.

---

## Stage 3 · Core library and modern Java *(written; AI draft, unreviewed; see "As built" below)*

**Competency:** chooses and uses collections, writes generic and functional code with judgement, reads and writes files, and handles dates, text and numbers correctly.

### Module 3.1 — Collections
- **Prerequisites:** Stage 2.
- **After this module the learner can** choose `List`, `Set`, `Map`, `Deque` for a need and say how each behaves; iterate safely; explain what `hashCode` has to do with `HashMap`; avoid modifying a collection while iterating.
- **Lessons:** `List` and `ArrayList` vs `LinkedList` · `Set` and uniqueness · `Map` and counting · Ordering (`Comparable`, `Comparator`) · Iteration and `ConcurrentModificationException` · Immutable collections (`List.of`).
- **Practice:** I: word frequency, anagram groups, duplicate transactions; D: mutation during iteration; R: read a collection-heavy program.
- **Assessment:** choose-the-collection scenarios with justification.

### Module 3.2 — Generics
- **After this module the learner can** read and write generic classes and methods, and explain why a `List<int>` isn't allowed and what boxing costs.
- **Lessons:** Why generics · Generic methods and classes · Bounded types · Wildcards (read-only introduction) · Type erasure and its limits.
- **Practice:** I: write a generic `Pair` and `Stack`; D: unchecked warnings; R: collection API signatures.

### Module 3.3 — Lambdas and streams
- **After this module the learner can** use functional interfaces, lambdas and method references, write stream pipelines for filter/map/collect, and decide when a loop is clearer.
- **Lessons:** Lambdas and functional interfaces · Method references · Stream basics · `collect`, grouping and counting · `Optional` · When not to use streams.
- **Practice:** G: loop→stream rewrites; I: monthly spending report; D: a stream with a side effect; X: loop vs stream readability.

### Module 3.4 — Files, text and persistence
- **After this module the learner can** read and write text files with `java.nio.file`, parse CSV and JSON safely, serialise domain objects, and handle missing or malformed files.
- **Lessons:** Paths and files · Reading and writing text · Parsing CSV · JSON with a library · Formatting output · Handling I/O failures.
- **Practice:** I: save/load Brightbank; D: encoding and trailing-newline bugs; R: a file-processing script.

### Module 3.5 — Dates, numbers and text
- **After this module the learner can** use `java.time` correctly (time zones, durations), explain why money isn't a `double`, use `BigDecimal` or whole units, and use `String`/`StringBuilder`/text blocks.
- **Lessons:** `LocalDate`, `Instant`, zones · Durations and periods · Money and `BigDecimal` · Strings in depth · Locale and formatting.
- **Practice:** I: statement dates; D: daylight-saving and rounding bugs.
- **Stage 3 project:** *Brightbank v3 (Cat. B)* — multiple accounts, reports, persistence, statements by date. **Cat. C** inherited log-analyser with time-zone and performance bugs.
- **Stage 3 gate:** build a data-processing tool from a spec; debug a collections/streams program; explain a collection choice.

### As built: Stages 2 and 3

The module plans above are the design. What was written is smaller. Treat this as the record.

**Stage 2** (14 lessons, 54 exercises, 1 project): 2.1 Classes and objects (From main to a class · Methods and `this` · Objects and references · `static`, `toString` and `equals`); 2.2 Encapsulation (Private fields and invariants · Immutability and defensive copies); 2.3 Interfaces, inheritance, polymorphism (Interfaces and polymorphism · Inheritance, `super` and abstract classes · Composition over inheritance); 2.4 Modern type features (Records and enums · Sealed types and pattern-matching `switch`); 2.5 Errors (Catching exceptions · Custom and checked exceptions · Cleanup and where to catch).

- The plan's separate lessons on access modifiers, value vs identity, the Liskov test and "never swallow errors" are folded into these.
- **Built:** `j2-p0-brightbank-classes` (Category A, guided), `j2-p1-brightbank` (Category B: classes, a sealed `Transaction`, a checked exception, a tamper-proof history, and a change request that adds `CurrentAccount` and `SavingsAccount`) and `j2-a1-inherited-staff` (Category C: asymmetric `equals`, a missing `hashCode`, and a mutable `withRaise`, with a review to answer).
- **Not built:** the Stage 2 gate and the "read a 120-line domain model" retrieval exercises.

**Stage 3** (12 lessons, 47 exercises, 1 project): 3.1 Collections (Lists and sets · Maps · Ordering and safe iteration); 3.2 Generics (one lesson); 3.3 Lambdas and streams (Lambdas and functional interfaces · Stream pipelines · `Optional`, and choosing loops or streams); 3.4 Files and text (Reading and writing files · Parsing text data and handling failures); 3.5 Dates, numbers and text (Dates and time zones · Money and `BigDecimal` · Strings in depth).

- Not written: `LinkedList`/`Deque`, wildcards beyond a first look, JSON, serialisation, `Locale` formatting, and time-zone-aware formatting beyond the basics.
- **Built:** `j3-p1-brightbank` (Category B: parses a messy CSV, totals by month, produces a date-range statement and absorbs a change request about duplicates; its input is a `List<String>`, not a real file) and `j3-a1-log-analyser` (Category C: a London-time grouping bug, a quadratic scan, and a review about malformed lines).
- **Not built:** the Stage 3 gate.

**Platform limits that shaped the exercises.** A single compact file means `private` isn't enforced between classes, so exercises check for the `private` keyword in the source as well as behaviour (see the standards doc). The grader can pass and return scalars, arrays and `List`s of boxed types or `String`s only, so exercises on `Map`, `Set`, `Optional` and objects go through driver methods that return strings or lists.

### As built: Stage 6 (2026-11-07)

13 lessons and 34 exercises in four modules, AI draft and unreviewed. SQL and JDBC exercises run in the local runner against an in-memory **H2** database (`jdbc:h2:mem`, driver on the learner class path); H2's SQLState values differ from PostgreSQL's in places and the exercises say H2. Module 6.4 (JPA and Hibernate) cannot run a provider here, so it is assessed by a plain-Java model of the persistence context and of N+1 query counts, plus explanations. Not built: the Stage 6 projects (Brightbank v6, B and C) and the stage gate. Sources I69 to I83.

### As built: Stage 7 (2026-11-07)

12 lessons, 30 exercises and 2 projects in four modules, AI draft and unreviewed. Scoped for one learner, so lean: seven planned lessons were merged or dropped (versioning, OpenAPI, Testcontainers, test data, contract thinking and the profile/properties split). Spring does not run in the runner, so exercises are plain-Java models of what the framework does, plus explanations that read real code and tests from this repository. Real `curl` and startup-log captures come from this platform's own backend. Sources I84 to I94 (RFC 9110, RFC 9457, Spring Framework and Spring Boot reference pages, read 2026-11-07). Not built: the Stage 7 gate.

### As built: Stages 8 and 9 (2026-11-07)

Stage 8: 9 lessons, 26 exercises, 1 Category C project (security audit and remediation of an inherited handler, with a written report). Sources I95 to I107 (OWASP Top 10:2025 and cheat sheets, RFC 7519, RFC 6265, Spring Security reference, Java algorithm names). Dropped for the single-learner scope: OAuth2/OIDC lesson, method security, a Stage 8 gate. Stage 9: 11 lessons, 27 exercises, 1 Category C project (concurrent bank). Sources I108 to I116 (JEPs 444, 506 and 505, JLS chapter 17, the `java.util.concurrent` API, the G1 guide). Dropped: class loading, tuning flags, JMH, flame graphs, a Stage 9 gate. Both stages' JDK tool output (thread dump, GC log, JIT log, JFR counts) was captured on the author's machine on 2026-11-07 and will differ on yours.

### As built: Stages 10, 11 and 12 (2026-11-07)

Stage 10: 7 lessons, 15 exercises, 1 Category C project. Stage 11: 8 lessons, 18 exercises, 1 Category B project; the Docker lessons use real output captured on the author's machine (Docker Desktop 4.98, JDK 25.0.5); CI, deployment, cloud and IaC are modelled because no CI server, orchestrator or cloud account was available. Stage 12: 7 lessons, 17 exercises and the capstone (a four-change Category C project with a written note). Sources I117 to I138. Dropped for the single-learner scope: DDD essentials, messaging brokers beyond the outbox idea, CAP in depth, Kubernetes, a real cloud walkthrough, metrics/alerts tooling, tracing tooling, feature-flag services, and all stage gates.

### As built: Stages 4 and 5

**Stage 4** (9 lessons, 28 exercises, 1 project): 4.1 Git and collaboration (Snapshots, branches and merging · Conflicts, remotes and undoing safely); 4.2 Maven (Project layout and the POM · Lifecycle, dependencies and conflicts); 4.3 Automated testing (Your first unit tests · Good tests: edges, exceptions and test doubles); 4.4 Debugging, logging and refactoring (Logging and debugging · Refactoring under tests · Code smells and code review).

- **The platform can't run Git or Maven.** Those four lessons contain **real output** captured from real sessions (fixed identity and dates so the hashes are reproducible; Maven 3.10 with JUnit 6.1.3) and are assessed by **written explanations only**. The concepts' required evidence is therefore explanation alone. The plan's "repair a repository" assessment needs a repository sandbox that doesn't exist.
- **Testing uses a mutant-killing design** because JUnit isn't available in the runner: learners write a check method that must pass the correct code and fail every deliberately broken copy. The mutants are visible in the starter, so a learner can in principle compare against the correct class; the exercise tells them not to.
- **Built:** `j4-a1-first-ticket` (Category C: reproduce and fix a bug ticket, refactor under the checks, answer a review), in one file; it can't use a real repository or pull request.
- **Not covered:** Gradle (not installed here, so nothing about it could be verified), mutation-testing tools, flaky-test and mock-library detail, the debugger shown on screen (described, not demonstrated), and the Stage 4 gate.

**Stage 5** (13 lessons, 50 exercises, 2 projects): 5.1 Complexity and measurement (Counting steps and growth rates · Measuring honestly and spotting accidental quadratics); 5.2 Core structures (Dynamic arrays · Linked lists · Stacks and queues · Hash tables · Binary search trees · Heaps and priority queues); 5.3 Algorithms (Recursion · Binary search and sorting · Graphs · Shortest paths · Dynamic programming).

- **Fully runnable and graded.** Performance exercises run on large inputs under the 2-second limit; binary search is checked by counting array reads through a wrapper class, not by timing.
- **Built:** `j5-p1-brightbank` (Category B: sorted range count, duplicate ids with a hash set, top spenders, then a change request) and `j5-a1-slow-report` (Category C: three hidden quadratic costs behind a measured requirement).
- **Not covered:** JMH or any benchmarking tool, red-black or AVL trees, graph algorithms beyond BFS, DFS and Dijkstra, and the Stage 5 gate.
- **Platform fix made while writing it:** a `StackOverflowError` made the grading harness print thousands of stack frames in one report line, which was truncated and could not be parsed. The harness now reports at most 12 frames, with a regression test.

**Stage gates.** The plan lists a gate at the end of each stage. The platform has no gate concept, so none is built for any stage.

---

## Stage 4 · Professional engineering toolchain

**Competency:** works the way a professional team does: version control, builds, automated tests, debugging tools, code review, safe refactoring.

### Module 4.1 — Git and collaboration
- **Prerequisites:** Stage 3 (or concurrently with 3.4).
- **After this module the learner can** init, commit, branch, merge and resolve conflicts; write good commit messages; open and respond to a pull request (on a sandbox repository); recover from common mistakes.
- **Lessons:** Snapshots and commits · Branches and merging · Conflicts · Remotes and pull requests · History as documentation · Undoing safely.
- **Practice:** guided sandbox repository with seeded conflicts and a broken history to repair; I: team-style PR exchange with the mentor as reviewer; X: write the PR description.
- **Assessment:** repair a repository from a given state (checked by inspection of the result).

### Module 4.2 — Build tools: Maven and Gradle
- **After this module the learner can** create a project with Maven and with Gradle, add dependencies, run tests, package a JAR, read a dependency tree, and explain what a build lifecycle is.
- **Lessons:** Project layout · Maven basics (POM, lifecycle, dependencies, plugins) · Gradle basics (build scripts, tasks) · Dependency conflicts · Reproducible builds · Choosing between them.
- **Practice:** convert Brightbank to Maven, then to Gradle; D: broken builds (version clash, missing plugin); R: a multi-module POM.

### Module 4.3 — Automated testing
- **After this module the learner can** write unit tests with JUnit, name and structure them, test edge cases and exceptions, use test doubles sensibly, and explain what a test does *not* prove.
- **Lessons:** First JUnit test · Assertions and failure messages · Edge cases and parameterised tests · Testing exceptions · Test doubles and when to avoid them · Test-first on a small feature · Mutation testing idea (do my tests catch bugs?).
- **Practice:** I: test a given class so that seeded faulty versions fail; D: flaky and misleading tests; R: read a test suite as a specification.
- **Assessment:** test-quality rubric: hidden mutants caught.

### Module 4.4 — Debugging, logging and refactoring
- **After this module the learner can** use an IDE debugger (breakpoints, stepping, watches), add useful logging with levels, and refactor safely under tests (extract method, rename, introduce parameter object).
- **Lessons:** Debugger workflow · Reading logs and writing good log lines · Common refactorings · Code smells · Technical debt · Code review habits.
- **Practice:** D: three-fault unfamiliar program using the debugger; R: review a pull request and write review comments; I: refactor a messy class with tests as a safety net.
- **Stage 4 project:** *"First week on the job" (Cat. C)* — clone a repository, build it, fix a ticket, add tests, open a PR, respond to review. **Brightbank v4:** under Maven/Gradle, tested, with history.
- **Stage 4 gate:** repository task with a seeded bug and review feedback.

---

## Stage 5 · Data structures and algorithms

**Competency:** reasons about complexity, implements core structures, chooses algorithms from constraints, and measures performance honestly.

### Module 5.1 — Complexity and measurement
- **Prerequisites:** Stage 3 collections.
- **After this module the learner can** estimate time and space cost of loops and recursion, read big-O, and distinguish what benchmarks do and don't show (warm-up, noise).
- **Lessons:** Counting steps · Big-O intuition · Common growth rates · Space · Measuring (and why micro-benchmarks mislead) · JMH introduction.
- **Practice:** I: predict then measure; D: an accidentally quadratic loop.

### Module 5.2 — Core structures
- **After this module the learner can** implement a dynamic array, linked list, stack, queue and hash table; explain collisions; and compare them with `java.util` versions.
- **Lessons:** Dynamic arrays · Linked lists · Stacks and queues · Hash tables · Trees (BST) · Heaps and priority queues · Graphs (representation).
- **Practice:** I per structure with hidden tests; R: read the JDK `ArrayList` source; D: broken invariants.

### Module 5.3 — Algorithms
- **After this module the learner can** write and trace binary search, merge/quick sort ideas, recursion and backtracking, graph traversal (BFS/DFS), and a shortest-path algorithm; choose one with justification.
- **Lessons:** Recursion · Binary search (and its off-by-one traps) · Sorting · Graph traversal · Shortest paths · Dynamic programming (introduction) · Choosing the right tool.
- **Practice:** I: route planner, autocomplete index; D: infinite recursion; X: justify the algorithm for a given size.
- **Stage 5 project:** *Brightbank v5 (Cat. B)* — statement search and sort, duplicate detection with a hash structure; **Cat. C:** optimise an inherited slow report against a measured requirement.
- **Stage 5 gate:** implement a structure from the spec; analyse an algorithm's cost; fix a performance bug with evidence.

---

## Stage 6 · Databases and persistence

**Competency:** designs a relational schema, writes correct SQL, uses transactions, and persists domain objects with JDBC and JPA/Hibernate, avoiding the common performance and correctness traps.

### Module 6.1 — Relational thinking and SQL
- **Prerequisites:** Stage 3.
- **After this module the learner can** model entities and relationships, normalise to a sensible level, write `SELECT` with joins, grouping and subqueries, and write inserts, updates and deletes safely.
- **Lessons:** Tables, keys, relationships · Normalisation and its limits · `SELECT`, `WHERE`, `ORDER BY` · Joins · Aggregates and `GROUP BY` · Subqueries · Writing data safely · Indexes and `EXPLAIN`.
- **Practice:** guided SQL sandbox (real PostgreSQL); I: bank reporting queries; D: queries returning duplicated or missing rows; R: read a schema.

### Module 6.2 — Transactions and integrity
- **After this module the learner can** explain ACID, use transactions and isolation levels, and prevent lost updates; explain constraints and why they belong in the database.
- **Lessons:** Constraints · Transactions · Isolation and anomalies · Locking and optimistic concurrency · Migrations (Flyway).
- **Practice:** I: money transfer that is correct under concurrency; D: lost-update demo.

### Module 6.3 — JDBC
- **After this module the learner can** connect, run parameterised queries, map rows to objects, manage resources, and explain SQL injection with a working fix.
- **Lessons:** Connections and pools · `PreparedStatement` · Mapping results · Transactions in JDBC · Repositories by hand.
- **Practice:** I: Brightbank repository; D: injection and leaked connections.

### Module 6.4 — JPA and Hibernate
- **After this module the learner can** map entities and relationships, use repositories, explain the persistence context, lazy vs eager loading, N+1 queries and how to detect and fix them.
- **Lessons:** Entities and mapping · Relationships · The persistence context and dirty checking · Lazy loading and `LazyInitializationException` · N+1 and fetch strategies · Queries (JPQL, criteria, native) · When not to use an ORM.
- **Practice:** D: seeded N+1; I: model the bank domain; R: read generated SQL.
- **Stage 6 project:** *Brightbank v6 (Cat. B/C)* — schema, migrations, repositories; **Cat. C:** inherited persistence layer with N+1 and a transaction bug.
- **Stage 6 gate:** design a schema from a paragraph; fix a data bug; explain a transaction anomaly.

---

## Stage 7 · Spring and backend development

**Competency:** builds, tests and documents a REST API with Spring Boot, understanding what the framework does for them.

### Module 7.1 — HTTP and REST fundamentals
- **Prerequisites:** Stage 3, Stage 6.1.
- **After this module the learner can** read HTTP requests and responses, use status codes correctly, design resource-oriented URLs, and use `curl` and a browser's network tools.
- **Lessons:** Requests, responses, headers · Methods and idempotence · Status codes · Resource design · JSON · Errors and problem details · Versioning and compatibility.
- **Practice:** guided with a mock server; R: read real API responses; X: critique an API design.

### Module 7.2 — Spring core
- **After this module the learner can** explain inversion of control and dependency injection by first writing the wiring by hand; use beans, configuration and profiles.
- **Lessons:** The problem DI solves · Beans and the container · Constructor injection · Configuration and properties · Profiles · What auto-configuration actually does.
- **Practice:** D: bean wiring failures; R: read startup logs.

### Module 7.3 — Spring Boot REST APIs
- **After this module the learner can** build controllers, validate input, map errors to responses, call a database, and document the API.
- **Lessons:** Controllers and routing · Request/response objects · Validation · Error handling · Persistence integration · API documentation (OpenAPI) · Pagination.
- **Practice:** I: bank API endpoints; D: seeded API bugs; R: read a controller layer.

### Module 7.4 — Testing a Spring application
- **After this module the learner can** write slice and integration tests against a real database (containers), and judge when mocks mislead.
- **Lessons:** Unit vs slice vs integration · MockMvc and real HTTP · Testcontainers · Test data · Contract thinking.
- **Stage 7 project:** *Brightbank v7 (Cat. B)* — REST API with tests and docs; **Cat. C:** extend an inherited API under a changing requirement.
- **Stage 7 gate:** build and test an endpoint from a spec; debug a failing request; explain a framework behaviour.

---

## Stage 8 · Authentication and application security

**Competency:** designs and implements authentication and authorisation, and finds and fixes common vulnerabilities.

### Module 8.1 — Security fundamentals
- **Prerequisites:** Stage 7.
- **After this module the learner can** build a simple threat model, explain the OWASP Top 10 categories with examples, and store passwords correctly (hashing, salting, why not encryption).
- **Lessons:** Threat modelling · OWASP Top 10 · Passwords and hashing · Secrets management · Input as an attack surface · Logging without leaking.
- **Practice:** D: find vulnerabilities in a seeded app (injection, broken access control); R: security review of a PR.

### Module 8.2 — Authentication and authorisation with Spring Security
- **After this module the learner can** implement login, sessions or tokens, role- and ownership-based authorisation, CSRF and CORS settings, and explain the trade-offs between sessions and JWT.
- **Lessons:** Authentication vs authorisation · Sessions and cookies · Tokens and JWT (and their pitfalls) · Spring Security filter chain · Method security · OAuth2/OIDC overview · Rate limiting and lockout.
- **Practice:** I: secure Brightbank so one customer can't read another's account; D: broken access control; X: justify the session vs token choice.
- **Stage 8 project:** *Brightbank v8 (Cat. C)* — security audit and remediation of an inherited API with a written report.
- **Stage 8 gate:** find and fix seeded vulnerabilities; justify a design.

---

## Stage 9 · Concurrency, the JVM and performance

**Competency:** writes thread-safe code, diagnoses races and deadlocks, and understands enough of the JVM to reason about memory and performance.

### Module 9.1 — Concurrency fundamentals
- **Prerequisites:** Stages 2–3, Stage 5.1.
- **After this module the learner can** start threads, explain visibility and atomicity, reproduce a race condition, and fix it using synchronisation, atomics or immutability.
- **Lessons:** Threads and the cost of sharing · Races (make one happen) · `synchronized` and locks · `volatile` and the Java Memory Model (intuition) · Atomics · Deadlock (reproduce and diagnose).
- **Practice:** D: seeded races and deadlocks, with thread dumps; I: thread-safe counter and bank transfer.

### Module 9.2 — Modern concurrency
- **After this module the learner can** use executors, `CompletableFuture`, concurrent collections, virtual threads, and scoped values (final in Java 25), and decide between platform and virtual threads.
- **Lessons:** Executors · Futures and composition · Concurrent collections · Virtual threads (Java 21) · Scoped values (Java 25) · Structured concurrency (preview in Java 25; labelled as preview).
- **Practice:** I: parallel report builder; X: platform vs virtual threads.

### Module 9.3 — JVM internals and performance
- **After this module the learner can** explain stack and heap, the garbage collector's job, read GC logs and a JFR recording at a basic level, find a hot method, and reduce allocation; explain why measuring beats guessing.
- **Lessons:** Memory model · Class loading · Garbage collection · JIT compilation and warm-up · Profiling with JFR · Memory leaks in a GC language · Tuning flags and when not to touch them.
- **Practice:** D: seeded memory leak and CPU hot spot; R: read a flame graph.
- **Stage 9 project:** *Brightbank v9 (Cat. C)* — concurrent transfers with a seeded race and deadlock; throughput requirement.
- **Stage 9 gate:** diagnose a concurrency fault from evidence; explain a performance change with measurements.

---

## Stage 10 · Distributed systems and architecture

**Competency:** designs systems of several parts, reasons about failure, consistency and trade-offs, and records decisions.

### Module 10.1 — Architecture principles
- **Prerequisites:** Stages 6–8.
- **After this module the learner can** structure an application in layers or modules, apply dependency direction, explain coupling and cohesion, and write an architecture decision record.
- **Lessons:** Layers and modules · Hexagonal/ports-and-adapters · Domain-driven design essentials · Modular monolith vs microservices · Writing ADRs.
- **Practice:** R: read an architecture; X: ADRs for two decisions.

### Module 10.2 — Distributed systems fundamentals
- **After this module the learner can** explain latency, partial failure, timeouts, retries, idempotency, eventual consistency, and the CAP trade-off; design an idempotent transfer API.
- **Lessons:** Networks fail · Timeouts and retries · Idempotency keys · Consistency models · Messaging and events · Sagas and outbox pattern · Resilience patterns (circuit breaker, bulkhead).
- **Practice:** D: duplicate processing and lost messages in a simulator; I: design the bank's transfer flow across two services.
- **Stage 10 project:** *Brightbank v10 (Cat. C)* — split a module into a separate service with an idempotent API, and survive injected failures.
- **Stage 10 gate:** design review of a given architecture; handle a failure scenario.

---

## Stage 11 · Containers, deployment and cloud

**Competency:** packages, deploys, observes and updates a service in a real environment.

### Module 11.1 — Docker
- **Prerequisites:** Stage 7.
- **After this module the learner can** write a Dockerfile for a Java service, build small images, run with Compose (app + database), manage configuration and secrets, and explain image layers.
- **Lessons:** Containers vs VMs · Dockerfile · Multi-stage builds · Compose · Config and secrets · JVM in containers (memory limits).
- **Practice:** D: container that exits, runs out of memory, or can't reach the database.

### Module 11.2 — CI/CD
- **After this module the learner can** build a pipeline that builds, tests, scans and publishes an image, and explain deployment strategies.
- **Lessons:** Pipelines as code · Test and quality gates · Artifacts and registries · Deployment strategies (rolling, blue/green) · Rollbacks.

### Module 11.3 — Cloud engineering
- **After this module the learner can** deploy to a cloud environment (vendor-neutral concepts, one concrete provider for practice), use managed databases, configure networking and identity, and estimate cost.
- **Lessons:** Cloud building blocks · Managed databases · Networking and security groups · Identity and least privilege · Infrastructure as code · Cost awareness.
- **Stage 11 project:** *Brightbank v11 (Cat. B)* — pipeline and deployed environment with a smoke test.

---

## Stage 12 · Production engineering and capstone

**Competency:** operates a service: observes it, troubleshoots incidents under pressure, and improves it safely.

### Module 12.1 — Observability and troubleshooting
- **Prerequisites:** Stages 9, 11.
- **After this module the learner can** add metrics, structured logs and traces, define SLIs/SLOs, read dashboards, and diagnose an incident from logs, thread dumps, heap dumps and metrics.
- **Lessons:** The three signals · Structured logging · Metrics and alerts · Tracing · Reading a production incident · Post-incident reviews.
- **Practice:** D: seeded incidents (memory leak, connection-pool exhaustion, slow query, deadlock) with only logs and metrics available.

### Module 12.2 — Advanced engineering practices
- **After this module the learner can** plan a safe migration, evolve a schema without downtime, manage feature flags and technical debt, review others' designs, and estimate and communicate trade-offs.
- **Lessons:** Zero-downtime changes · Feature flags · Technical debt management · Design reviews · Estimation and communication · Working with legacy code.

### Module 12.3 — Capstone
- **Project (Cat. C, multi-week):** inherit the learner's own Brightbank *and* a deliberately flawed partner version; add features under changing requirements; harden, scale and deploy; respond to a seeded production incident; write ADRs and a post-incident review; defend decisions in a written interview.
- **Assessment:** rubric over correctness, tests, security, performance, operability, documentation, and the quality of the written justification. **No tutorial exists for it.**

---

## Cross-cutting threads

| Thread | Where it is taught | Where it is assessed |
|---|---|---|
| Code reading | Every stage (R activities) | Gates 1–12 |
| Debugging | Stage 1 module 6; Stage 4.4; every stage's D activities | Gates |
| Testing | Stage 1 module 5.5/7.3; Stage 4.3; Stage 7.4 | Stage 4 and 7 gates |
| Security | Stage 3 (input), Stage 6 (injection), Stage 8 | Stage 8 |
| Performance | Stage 5.1, Stage 9 | Stages 5, 9 |
| Communication | PR descriptions, ADRs, design notes, post-incident reviews | Stage 4, 10, 12 |

## Sequencing notes and risks

- **Order flexibility:** Stage 4.1–4.2 (Git, build tools) can move earlier (after Stage 2) if learners want to work on their own machines sooner; Stage 6.1 (SQL) can run in parallel with Stage 5.
- **Scale of content:** this is a multi-year content programme. Stage 1 expansion comes first; each later stage is designed in full (like `02-stage-1-foundations.md`) *before* its lessons are written.
- **Technology churn:** versions are not fixed in this document. Every stage records a "re-baseline" review (Java LTS releases, Spring Boot majors).
- **Unverified items:** industry resources listed in `sources.md` (JLS, JEPs, Spring reference) are verified per lesson at writing time, not here.

## Mapping to the earlier design

| Earlier stage | Now |
|---|---|
| 1 Foundations | Stage 0 + Stage 1 (expanded) |
| 2 OOP | Stage 2 |
| 3 Core library | Stage 3 |
| 4 Toolchain | Stage 4 |
| 5 DSA | Stage 5 |
| 6 Concurrency & JVM | Stage 9 |
| 7 Persistence & web | Stages 6, 7, 8 (split for depth) |
| 8 Professional capstone | Stages 10–12 |
