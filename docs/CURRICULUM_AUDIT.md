# Curriculum Audit

Date: 2026-11-05 · Scope: the whole repository as it stands today · Method: counted and read the actual files, ran the content validator and the test suite, and exercised the app in a browser. Where something is "done" below, it means a test or a run showed it working.

## 1. Headline findings

1. **There is exactly one stage of content: Stage 1, 25 lessons.** Stages 2–8 exist only as outlines in `01-curriculum-design.md` (a few lines each). Nothing in the app lets a learner see them.
2. **Stage 1 is competent but narrow.** It teaches syntax and small procedural programs well. It never makes a learner build anything bigger than a single method, so it does not yet establish independent problem-solving. The two projects and the final assessment that the design called for **do not exist** (platform support is also missing).
3. **The research behind the course was thin and partly overstated.** The source register is mostly peer-reviewed papers cited from memory, 5 of them verified at the time. **No Reddit, Stack Overflow, Hacker News, blog or interview source had been consulted**, despite the register having a "community" section. That is corrected in `LEARNING_METHODOLOGY.md`, which is based on sources fetched this session. One register entry (R4) overstated its paper's findings; see §6.
4. **There are no videos, no step-through or memory visualisations, and no trace-table widget** anywhere. The only occurrence of the word "video" in the content is an example sentence.
5. **The platform mechanics that exist are real and tested** (grading, mastery, spaced checks, mentor policy). Several learning-experience features that the design promised are not built (§4).

## 2. What exists

### 2.1 Stage 1 content (all `status: in_review`)

| Module | Lessons | Exercises | Notes |
|---|---|---|---|
| 1 First programs | 1.1 Your first program; 1.2 Errors are feedback | 10; 8 | Predict/Parsons/write/debug/modify/explain; real javac messages |
| 2 Values and variables | 2.1 Values and types; 2.2 Variables and state; 2.3 Arithmetic; 2.4 Strings | 7; 10; 12; 11 | Covers three documented misconceptions (MC01–03) in 2.2 |
| 3 Input and decisions | 3.1 Reading input; 3.2 Boolean expressions; 3.3 Making decisions; 3.4 switch expressions | 7; 8; 9; 8 | |
| 4 Repetition | 4.1 while; 4.2 Tracing loops; 4.3 for; 4.4 Loop patterns; 4.5 Input validation loops | 7; 5; 7; 6; 5 | |
| 5 Methods | 5.1–5.5 | 6; 7; 4; 5; 4 | 5.3 (scope/stack) and 5.5 (reading tests) are the thinnest on practice |
| 6 Working with data | 6.1 Arrays; 6.2 Array algorithms; 6.3 ArrayList; 6.4 Exceptions; 6.5 Debugging | 7; 6; 7; 5; 4 | |

**Totals:** 25 lessons (160–290 lines each), **172 exercises**: write 67, debug 35, predict 31, explain 25, modify 11, Parsons 3. 132 are embedded in lessons, 40 are retrieval variants used only by the spaced-check scheduler.

### 2.2 Platform features

| Feature | Status | Evidence |
|---|---|---|
| Lesson reader, runnable snippets, Monaco editor | **Implemented** | Exercised by hand in Chrome; frontend build and 4 unit tests |
| Exercise types: predict, Parsons, write, debug, modify, explain | **Implemented** | `Grader`, 10 grader tests, content validator runs every reference and every known-wrong solution |
| Exercise type: trace table | **Planned only** | In the design doc (`::trace`), not built |
| Learner accounts, onboarding, sessions | **Implemented, not production-ready** | 17 tests; no password reset, no rate limiting, sessions in memory |
| Attempt log, assisted vs independent evidence | **Implemented** | `attempt` table; `MasteryCalculator` (11 unit tests) |
| Concept mastery levels 0–5, spaced knowledge checks | **Implemented** | Unit tests plus an integration test with back-dated attempts |
| Explanation scoring | **Partly**: AI provisional scores; **no human review queue** | `ExplanationScoreRepository`; tested with a fake model only |
| AI mentor (H0–H4, gates, attempt-first, code checks) | **Implemented, never run against the real model** | 12 flow tests with a scripted model; no API key available |
| Content validation gates in CI | **Implemented** | `ContentValidationTest`; 7 sabotage tests |
| Projects: milestones with their own tests, rubric, acceptance criteria | **Implemented after this audit** (single `Main.java`, method and stdin/stdout milestone tests, Category A/B/C). **Not implemented:** multi-file projects, mentor support inside projects, review and scoring of design notes (the box saves locally in the browser only) | `ProjectFlowTest` (6 tests), 3 project sabotage tests |
| Stage gates / independent assessments | **First one built after this audit**: Stage 1 assessment "the inherited gradebook" (Category C: three bug reports, a new feature, a change request, graded by the same engine). A general gate runner (unseen variants, retake rules) is **not** built | |
| Video embedding / curated resources | **Implemented after this audit**: `resources.yaml` catalogue, lesson references, validator rules (https, verification date, YouTube id must match URL), embed via youtube-nocookie. **Content: 4 resources, 1 embedded video.** More resources need to be found and opened by a person before they're added | 4 validator sabotage tests |
| Step-through execution, variable/memory visualisation | **Not implemented** | |
| Placement test for experienced learners | **Not implemented** | |
| Outcome reports (design §8) | **Not implemented** (data is recorded) | |
| Sandboxed code execution | **Not implemented** | `LocalJvmRunner` is explicitly unsafe for untrusted users |

### 2.3 Tests

76 automated tests pass (72 backend, 4 frontend). They cover the platform well and the **content** through the validator. No beginner has used the course.

## 3. What is good and should be retained

- **The learning cycle in every lesson:** predict-before-run, worked example with labelled steps, a ladder (Parsons → write → debug → modify → explain), then spaced retrieval. This matches the strongest evidence gathered (see methodology).
- **Evidence-based mastery with assisted/independent separation**, including the rule that only the first predict attempt counts and Parsons never counts as independent.
- **Misconception targeting:** 15 catalogued misconceptions, each with a lesson block, a debug exercise and (where possible) a wrong-answer solution that the tests must fail.
- **Content that is validated, not just written:** every reference solution passes; every known-wrong solution fails; test values are computed independently; hidden tests show only names.
- **Real compiler output** quoted in lessons, not remembered.
- **Content lives in files**, validated in CI, loaded by the backend. Nothing curricular is hard-coded in the frontend.
- **The mentor design:** server-enforced levels, leak and compile checks on any code it shows.

## 4. What is incomplete or missing

| Gap | Why it matters | Priority |
|---|---|---|
| No project in Stage 1; no independent assessment | Learners never design a program from a blank page, which is the point of the course. Community and expert sources (methodology §3) agree this is the main failure of tutorial-only learning | **1** |
| No platform support for projects, milestones, multi-file code | Blocks the above | **1** |
| Stages 2–8 undeveloped; no master roadmap | A learner cannot see where the course goes | **1** (roadmap now, content later) |
| No video or external resource layer | Requested; also the course currently ignores excellent free material (e.g. the University of Helsinki MOOC) | 2 |
| No step-through/memory visualisation | Tracing is taught (4.2, 2.2) only with static tables, yet tracing is the most evidenced skill; interactive state views are cheap to add | 2 |
| Only one placement path | Learners with experience must read 25 lessons | 3 |
| Mentor untested with a live model | Tone and level discipline are unverified | 2 |
| Explanation scores have no human calibration | Mastery for concepts requiring `EXPL` depends on unreviewed AI scores | 2 |
| Auth hardening, sandbox | Blocks any public launch | before launch |

## 5. Where Stage 1 is educationally shallow

Reading all 25 lessons against the methodology, these are the honest weaknesses:

1. **Everything is a method with a given shape.** Almost all exercises are "write this one method; the tests call it." Beginners rarely write a whole program that reads input, decides and prints. Only 3.1, 4.5 and a handful of 1.x/4.x exercises are whole programs. *Fix: add program-level independent challenges and the projects.*
2. **Practice is thin in some lessons.** 4.2 (5 exercises), 5.3 (4), 5.5 (4), 6.4 (5) and 6.5 (4) have fewer independent *writing* tasks than the rest; 5.3 and 5.5 have only one write exercise.
3. **No cumulative problems.** Exercises in a lesson use only that lesson's idea; retrieval variants repeat the same shape. Nothing forces the learner to *choose* between constructs (loop vs if vs method) without a hint from the lesson title. *Fix: mixed-concept challenges at module ends.*
4. **No code-reading exercises on unfamiliar programs.** Debug exercises are small. The design's "inherited code" investigation is missing. Sources agree reading others' code is among the most valued skills (methodology §2).
5. **The lessons are text-and-editor only.** The learner can't watch state change. Trace tables are asked of the learner but never demonstrated interactively.
6. **No "why Java" and professional context.** There is no lesson on tools (installing a JDK, an IDE, running outside the browser) so a learner finishes unable to run Java on their own machine. *Fix: a "your own machine" module.*
7. **Assessed breadth is low for some concepts** (e.g. J1.14 reading tests has only 4 exercises, no project use).
8. **Explain prompts are all short answers.** None asks the learner to critique an existing design or justify a trade-off, which the master curriculum needs from Stage 2.

## 6. Technical and accuracy corrections

| Item | Problem | Action |
|---|---|---|
| Source R4 (Morrison et al. 2015) | Register said subgoal labels "improve novice programming problem solving". The paper's abstract says results were **mixed**: gains did not replicate as expected for given labels in the intro CS task | Corrected in `sources.md`; lessons still use subgoal labels as a design choice, not as evidence-backed fact |
| Source R14 (Kapur 2008) | Subject domain differs between secondary descriptions | Marked "domain unconfirmed"; not cited to learners |
| Source R2 (Cepeda 2006) | Meta-analysis found benefits for verbal recall; fewer for intellectual skills (about a third of skill studies) | Caveat added: spacing for programming skill is an assumption to measure |
| Most register entries | Cited from memory | Bibliographic details and main claims re-checked this session against search results or the source itself: R1, R2, R3 (the expertise-reversal paper only, not Sweller & Cooper 1985), R4, R5 (Leeds Group 2004 only, not Lopez 2008), R6, R7, R8, R9, R13, R14, R16. **Still unverified:** R10, R11, R12, R15, Lopez 2008, Sweller & Cooper 1985. See the register for per-entry status |
| Lesson 2.3 and others | Cite unverified sources (publishing gate warns) | Verify or remove before publication |
| `README` claim "A beginner can work from Hello world…" | True only for reading and exercises; there is no way to run code on a local machine, no project, no assessment | Corrected wording in README |

## 7. Priorities (what this assignment will do, in order)

1. This audit. ✅
2. Developer-community and educational research, with a traceable source register. ✅ (`LEARNING_METHODOLOGY.md`)
3. A full master curriculum map, beginner to advanced. ✅ (`JAVA_MASTER_CURRICULUM.md`)
4. Close the highest-value Stage 1 gaps: program-level challenges, mixed-concept challenges, a code-reading module, a "your own machine" lesson, projects and an independent assessment.
5. Platform support for projects, milestones and curated resources (videos), plus a step-through state visualiser.
6. Verify the whole learner journey, then continue stage by stage.

Items 4–6 are larger than one pass; this document is the baseline against which each is checked.

## 8. What changed after this audit (same session)

| Change | Evidence |
|---|---|
| `LEARNING_METHODOLOGY.md`: research from HN threads, Norvig, Atwood, *Coders at Work* notes, the Stack Overflow survey and verified educational papers; themes, disagreements and a register that says what was read vs. only seen in a snippet | `docs/LEARNING_METHODOLOGY.md` |
| `JAVA_MASTER_CURRICULUM.md`: Stages 0–12, 40+ modules with prerequisites, competencies, practice, projects and assessment; the continuing Brightbank project | `docs/JAVA_MASTER_CURRICULUM.md` |
| Source register corrected (R4 overstated; C1 withdrawn) and extended; unverified-source warnings fell from 39 to 8 | `docs/curriculum/sources.md` |
| Resource layer: 4 verified resources, 1 embedded video, with honest caveats (the Helsinki MOOC says it is no longer maintained) | `content/java/resources.yaml`; lesson 1.1 in the browser |
| Project platform and 4 projects: P1 personal finance calculator (A, 7 milestones), P2 shopping basket and receipt (B, 4), P3 Brightbank account logic (B, 6, with a mid-assignment change request), Stage 1 assessment: inherited gradebook (C, 5) | Validator runs every reference solution, starter and 24 known-wrong solutions; verified in the browser against the assessment's bug reports |

## 9. What is still open

- **Stage 1 module 7 and Stage 0 are written (4 lessons each; 14 exercises in module 7 and 12 in Stage 0) but are AI drafts that no person has reviewed, and no beginner has used.** Stage 0 is optional: it stays out of the "Continue" recommendation unless the learner opens one of its lessons. Stage 0 gives no verified video; it links the Adoptium, VS Code and JetBrains pages, each opened by a person on 2026-11-06.
- **Interactive step-through and memory visualisation are not built.** The curated resources link to an external visualiser (Online Python Tutor) instead.
- Only **one** embedded video and **four** resources exist. The requirement is for relevance and verification, not volume, but coverage beyond Stage 1 lesson 1.1 is thin. Candidates seen but not yet verified end to end: the Inside Java Newscast #23 page on virtual threads (the page has no video link), Brian Goetz's data-oriented programming articles on inside.java.
- **No beginner has used the course**, and the mentor has never run against a real model. Human review of lessons, projects and AI-scored explanations has not started.
- Projects: no mentor, no multi-file, no design-note review, mastery credit comes only from milestone passes (XFER evidence for B/C, IMPL for A).
- Stages 2–12 are a map, not content.

### Stages 2 and 3 (added 2026-11-06)

- **Stage 2** (object-oriented programming) and **Stage 3** (core library) now have lessons: 14 and 12, with 54 and 47 exercises and one Category B project each. They are AI drafts. Nobody has reviewed them and no learner has used them. They are fewer lessons than the master plan lists; `docs/JAVA_MASTER_CURRICULUM.md` ("As built") records what was folded in or left out.
- Every library or language fact the lessons state was read by the author from the OpenJDK JEP pages, the Java SE 25 API pages or the JLS, and is registered as I25–I54 in `docs/curriculum/sources.md`. Where a behaviour wasn't in a source (for example that `private` isn't enforced between classes in one file, or that `[1, -2, 3]` slips through a for-each removal), it was run on JDK 25 and is stated as observed behaviour.
- **Still open:** no video for Stages 2 and 3; no Category A or C projects there; no stage gates; `Deque`, wildcards, JSON and serialisation aren't covered; the mentor hasn't been tried with class-based exercises.

### Stages 4 and 5 (added 2026-11-06)

- **Stage 4** (9 lessons) and **Stage 5** (13 lessons) now exist, with 28 and 50 exercises and 1 and 2 projects. Stage 2 and 3 now also have their Category A and C projects. All AI drafts, unreviewed and untried by a learner.
- Stage 4's Git and Maven lessons quote **real output** from real runs, and cite the Pro Git book, the Maven guides and the JUnit user guide (I61 to I68, read this session). They are assessed by explanation only, because the platform can't run those tools.
- Stage 5's sources (I55 to I60) were read from the Java SE 25 API pages. Its performance exercises use large inputs and counted reads, and the validator confirmed that known-slow and known-wrong solutions fail them.
- **Videos:** 11 are linked: 8 in Stage 1 and 3 in Stage 5. Stages 2 to 4 have none: I did not find and verify any I could stand behind. Each video was opened, checked for embedding, length and a frame matching the lesson, but none was watched in full.
- **Incident:** while adding videos I truncated `resources.yaml` by mistake and rebuilt it. Three older entries (`jep-512`, `helsinki-mooc`, `python-tutor-java`) could not be recovered verbatim; they were rewritten from the live pages (re-checked 2026-11-06), so their wording differs from the original.
- **Still open:** stage gates (no platform support), Gradle, Stages 6 to 12 (map only), and any review by a person or a trial with a learner.

## 10. Stage 6 audit notes (2026-11-07)

- Written by a second model from the handoff prompt, then patched and validated. Defects found and fixed: predict programs assembled with imports after the helper class or without the `Db` fixture; three predict exercises whose expected output did not match what the program prints (a missing label, a delete that succeeded because the child rows were already gone, and a visibility test that expected 0 rows from a 5-row fixture); a debug exercise whose tests expected cities that do have customers; a debug exercise whose reference solution returned constant strings instead of reading the database; locale-dependent `String.format` in a reference solution; weak tests that let wrong solutions pass; rubric levels with one sample; a draft module 6.4 with a syntax error and citations that pointed at a Flyway page for Hibernate facts.
- Module 6.4 was rewritten. Its N+1, dirty-checking and fetching claims were checked against the Hibernate 7 guide on 2026-11-07 and recorded under I80.
- Known weak: several Stage 6 lessons are shorter and thinner than Stage 2 to 5 lessons. The connection-pool sentence in lesson 3.1 has no recorded source. Stage 6 has no projects, no real `psql` output and no videos.

## 11. Stage 7 audit notes (2026-11-07)

- Written and validated in one pass after the scope was reduced to a single learner. Expected values come from Python models, not from the Java solutions; the validator confirmed every reference solution passes and every known-wrong solution fails (one wrong solution and one unassessed objective were caught and fixed).
- Real findings from the captures, stated in the lessons: this platform's own 401 has no `WWW-Authenticate` header (RFC 9110 says a 401 must carry one); its 404 and 405 bodies are Spring Boot's default JSON, not RFC 9457 problem details; a DELETE without a CSRF token gets 403 before any method check.
- Known weak: Spring annotations in the lessons are shown for reading and were never run; the Bean Validation annotation example is not backed by a recorded source fact beyond "constraints are declared on properties"; the `classify`, `autoConfigure` and `creationOrder` exercises are models, labelled as such, not Spring's real rules. The earlier `if False else None` fragment still sits in `tools/authoring/l0.py` (that script does not regenerate its lesson).

## 12. Stage 8 and 9 audit notes (2026-11-07)

- Both stages passed the validator on the second pass: every reference solution passes and every known-wrong solution fails. Defects the validator caught and that were fixed: a path-traversal wrong solution that was indistinguishable (added an absolute-path-inside-base case), a lockout wrong solution hidden by a test whose future failure did not change the outcome, a hash-order case that let an unsorted result pass, a test that mixed a boolean with a text result, and an oversized literal that broke the grading harness.
- Expectations come from Python (`hashlib`, `hmac`, `base64`, models), except the `CompletionException` detail in the CompletableFuture predict, which was derived from the API's behaviour and then confirmed by running it.
- Real findings recorded in lessons: this platform's 401 has no `WWW-Authenticate` header because `SecurityConfig` uses an `HttpStatusEntryPoint`; the session cookie is `HttpOnly` and the `XSRF-TOKEN` cookie is deliberately readable; neither cookie has `Secure` (the platform is HTTP on localhost).
- Known weak: Stage 9's race-fix exercises rely on source tests as well as behaviour because a race cannot be detected reliably by running; two misconceptions (MC196, MC197) cite the `Thread` API page only loosely; the explanations of `PrintCompilation` columns, the `jfr` and `jcmd` commands and the four deadlock conditions are standard knowledge without a recorded source; several rubric sample answers are shorter than a real learner's. Stage 8 has no OAuth2/OIDC coverage.

## 13. Stage 10 to 12 audit notes (2026-11-07)

- All three stages passed the validator on the first full run after fixes. Defects the validator caught and that were fixed: six wrong solutions that were indistinguishable from the reference by the tests (a key scoped by account, a breaker that closes instead of reopening, a CIDR /0 mask, a rollout boundary, a rejected request that was not remembered, an express-rounding "fix" that is arithmetically identical for every possible fee); a project whose milestones were not cumulative (the Stage 11 pipeline, rewritten so that each milestone tests only what its change decides); and a generator regex that did not strip the Stage 10 to 12 concepts, producing duplicate concept ids in `curriculum.yaml`.
- Real output captured: package dependency table from this repository's imports (acyclic); Docker builds, `docker images`, `docker history`, Compose `ps`, an HTTP 200 smoke test, JVM `MaxHeapSize` at 128/256/1024 MB limits, and two out-of-memory exits. Docker's first Compose attempt with host bind mounts hung (likely a macOS file-sharing prompt); the final Compose file copies the content into the image instead.
- Honesty limits that the lessons state: the GitHub Actions workflow was never run; no Kubernetes or cloud account was used; the AWS security-group and IAM exercises model only a part of the real rules; the trace, the incident and the capstone data are constructed; the Idempotency-Key header is an Internet-Draft, not a standard.
- Known weak: several explanations (layer caching order, blue/green, retry storms and jitter, PERT, mitigation before diagnosis) are standard practice without a recorded source; the Stage 11 image sizes will differ on other machines; the stage gates and videos are absent for all of Stages 6 to 12.

## 14. Videos added (2026-11-07)

- 32 videos from 30 creators were added to `resources.yaml` and linked from 35 lessons (Stages 2 to 4 and 6 to 12), after the first 11 (Stages 1 and 5). Selection rules: found by search, then checked on the video's own page (title, channel, length, publish date, embeddable, chapter list, description) and matched to a lesson by chapters or description; official or well-known channels preferred; at most two per lesson; caveats name what the video does not cover or where it is dated.
- **Not done:** no video was watched in full by the AI author or any person; the checker looked at metadata, so a video could still be weaker than its title suggests. Several are older than the Java or Spring versions the course uses (2017 to 2022), and the caveats say so. Four are from vendors and say so. The channel System Design Lab supplies two videos and the official Java channel two; every other creator supplies one.
- Lessons with no video are listed in `docs/HANDOFF_PROMPT.md`. For many of them the search found only unrelated, very old or non-Java videos, so none was linked.
- `tools/authoring/lesson_resources.json` records the lesson-to-video links so that regenerating a lesson from its script keeps them.
