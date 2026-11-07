# Java Engineering Academy

A Java-first platform that turns beginners into capable software engineers. The platform measures capability gained, not content consumed.

## Status

- **Phase 1 — curriculum design:** draft complete.
- **Phase 2 — vertical slice:** in progress. Done so far:
  - the code runner, grader and content publication gates
  - a learner API
  - the web frontend: lesson reader, Monaco editor, and widgets for all five exercise types, styled after TailAdmin (MIT): sidebar layout, Outfit type, light theme by default with a dark toggle
  - learner accounts, onboarding, an append-only attempt log, concept mastery levels and spaced knowledge checks (PostgreSQL)
  - the AI mentor: help levels H0–H4 with server-enforced gates, attempt-first mode, code checked before it's shown, follow-up questions, and provisional explanation scoring (Claude via the official Java SDK)
  - **all 29 Stage 1 lessons** (including module 7, "Whole programs") with 186 exercises, plus **optional Stage 0** ("your own machine": 4 lessons, 12 exercises), plus **four projects** (guided finance calculator, independent receipt and Brightbank builds, and an inherited-code assessment), a verified **resources layer** (1 embedded video, 3 other resources), and three new curriculum documents (`docs/CURRICULUM_AUDIT.md`, `docs/LEARNING_METHODOLOGY.md`, `docs/JAVA_MASTER_CURRICULUM.md`), (predict, Parsons, write, debug, modify and explain, plus spaced-retrieval variants), all awaiting review. A beginner can work from "Hello, world" through methods, arrays and debugging. The Stage 1 projects and final assessment aren't built yet (see Next)
  - **Stages 2 to 5**, all AI drafts, unreviewed: **Stage 2** (object-oriented programming) 14 lessons, 54 exercises, 3 projects; **Stage 3** (core library) 12 lessons, 47 exercises, 2 projects; **Stage 4** (professional toolchain: Git, Maven, testing, debugging, refactoring, review) 9 lessons, 28 exercises, 1 project; **Stage 5** (data structures and algorithms) 13 lessons, 50 exercises, 2 projects. They are fewer lessons than the master plan lists; see `docs/JAVA_MASTER_CURRICULUM.md`, "As built".

| Document | Contents |
|---|---|
| [Curriculum design](docs/curriculum/01-curriculum-design.md) | Java version policy, learning cycle, project categories, mastery model, all 8 stages, outcome measurement |
| [Stage 1 — Foundations](docs/curriculum/02-stage-1-foundations.md) | Full design of the vertical slice: concept graph, misconception catalogue, 25 lessons, exercise ladders, two projects, stage gate |
| [Content standards](docs/curriculum/03-content-standards.md) | File formats, required lesson sections, exercise/test rules, automated and human publication gates |
| [AI mentor policy](docs/curriculum/04-ai-mentor-policy.md) | Assistance levels H0–H4, escalation gates, solution-seeking detection, code validation |
| [Source register](docs/curriculum/sources.md) | Every cited source, with evidence class and verification status |
| [Curriculum audit](docs/CURRICULUM_AUDIT.md) | What exists, what's real vs planned, what's shallow, what changed |
| [Learning methodology](docs/LEARNING_METHODOLOGY.md) | Research from developer communities and education literature, with a traceable register |
| [Master curriculum](docs/JAVA_MASTER_CURRICULUM.md) | Beginner to advanced roadmap: Stages 0–12, modules, projects, the Brightbank thread |

## Layout

```
content/java/       curriculum.yaml, lessons and exercises (see the content standards)
frontend/           React 19 + TypeScript + Vite + Monaco; `npm run build` → dist/, served by the backend
backend/            Spring Boot 4.1 app (Java 25)
  academy.content     loads content into a snapshot
  academy.execution   compiles and runs learner code (LocalJvmRunner, dev only)
  academy.assessment  grades submissions; AcademyGrader.java harness (resource)
  academy.validation  automated publication gates
  academy.learner     accounts, login, onboarding, security configuration
  academy.progress    attempt log, mastery calculation, knowledge checks, recommendations
  academy.mentor      AI mentor: escalation policy, prompts, Claude client, code checks
  academy.api         learner-facing REST API
docs/curriculum/    design documents and the source register
scripts/            dev-env.sh (pins JDK 25), validate-content.sh
```

## Running it

```bash
./scripts/start.sh                    # starts the database, builds the frontend, starts everything → http://localhost:8080
```

**AI mentor:** set `ANTHROPIC_API_KEY` in the environment before starting (for example `export ANTHROPIC_API_KEY=…` then `./scripts/start.sh`). Without it, everything works except the mentor, which shows as unavailable. To work on the mentor's UI without a key, run the scripted stand-in model (test sources only, never shipped):

```bash
cd backend && mvn spring-boot:test-run -Dspring-boot.run.main-class=academy.DemoMentorApplication \
  "-Dspring-boot.run.arguments=--spring.datasource.url=jdbc:postgresql://localhost:5433/academy"
```

For development:

```bash
source scripts/dev-env.sh             # JDK 25 + Maven (Homebrew's default JDK is a newer non-LTS release)
./scripts/db.sh start                 # project-local PostgreSQL 18 on :5433 (data in .data/, git-ignored); needed by the tests too
./scripts/validate-content.sh         # content publication gates only
cd backend && mvn test                # all backend tests, including the content gates
cd backend && mvn spring-boot:run     # backend on :8080
cd frontend && npm run dev            # frontend with hot reload on :5173 (proxies /api to :8080)
cd frontend && npm test               # frontend unit tests
```

API: content (`/api/curriculum`, `/api/lessons/{id}`, `/api/exercises/{id}`) is public. Everything that runs code or touches a learner's record needs a logged-in session: `/api/auth/*`, `/api/onboarding`, `POST /api/exercises/{id}/attempts[?context=retrieval]`, `POST /api/run`, `/api/progress`, `/api/progress/lessons/{id}`, `POST /api/lessons/{id}/visit`. State-changing requests need the CSRF header (`X-XSRF-TOKEN`, echoed from the `XSRF-TOKEN` cookie).

## Key decisions

- **Java 25 (LTS)** for learner code and the platform. Next re-baseline at Java 29 (planned for September 2027).
- Stage 1 uses **compact source files** (JEP 512). Before Module 5, exercises give learners a method header to complete (an "exercise frame"). Stages 2 and 3 keep the compact form (classes, records and interfaces sit beside `main` in one file); lesson 2.1.1 shows the traditional `public class Main` layout so learners can read it.
- Mastery is per concept and evidence-based. Assisted and independent performance are recorded separately. Retrieval checks are spaced.
- **Code execution:** `LocalJvmRunner` compiles in-process and runs each program in a separate JVM. Its limits are a time limit, a memory cap, an output cap and an empty environment. ⚠️ It is **not a sandbox**: learner code can read and write files and use the network. A sandboxed runner is required before any public launch.

## Known gaps

- **Explanation scores are AI-only.** They're provisional, and the human review queue that should sample and calibrate them doesn't exist yet. Without a mentor API key, explanations stay "awaiting review", so concepts that require `EXPL` can't reach *Demonstrated*.
- **The mentor hasn't been tested against the real model yet.** No API key was available during the build. Its policy and code checks are tested against a scripted model, and the request it builds is verified, but the replies' tone and quality need a live check. See the mentor policy doc §9 for what's implemented and what isn't.
- **Sessions are in memory.** Restarting the server logs everyone out. Move them to the database (Spring Session JDBC) before hosting.
- **No login rate limiting** or password reset yet.
- **The code runner is not a sandbox** (see above).

## Next

1. **Your review** of the 29 Stage 1 lessons, the 4 Stage 0 lessons, the four projects and the three new documents. Lesson 2.3 still sets the format.
2. **Stage 0 and Stage 1 module 7 are written but unreviewed**, like everything else: AI drafts with `technical_review` and `pedagogy_review` still empty, and no beginner has used them.
3. **Interactive step-through and memory visualisation** (the course links an external one for now).
4. **Videos:** 43 are linked across Stages 1 to 12 (32 added on 2026-11-07), each checked against its YouTube page but not watched in full by anyone. A person should watch them before relying on them; many lessons still have none.
5. **Live check of the mentor** with an API key; mentor support inside projects; review of design notes; the human review queue for AI-scored explanations.
6. **Platform hardening** before any public launch (sandboxed runner, password reset, rate limiting, persistent sessions).
7. **Stage 6** (databases: 13 lessons, 34 exercises, 2 projects, JDBC against in-memory H2) and **Stage 7** (Spring and REST: 12 lessons, 30 exercises, 2 projects, plain-Java models plus reading this platform's own code) are written and validated. **Stage 8** (security: 9 lessons, 26 exercises, 1 audit project) and **Stage 9** (concurrency and the JVM: 11 lessons, 27 exercises, 1 project) are written and validated too. **Stages 10 to 12** (distributed systems and architecture, containers and cloud with real Docker output, production engineering and a capstone) are written and validated as well. **All twelve stages now exist as AI drafts; none has been reviewed by a person or tried by a learner.** The build is scoped for a single learner.
8. Beginner walk-throughs before expanding.
