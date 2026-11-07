# AI Mentor Policy

Status: Draft 1 · 2026-11-05

The mentor's job is to make the learner more capable, not to finish the exercise for them. Unrestricted AI help can improve performance during practice while *harming* later independent performance. Guardrails that keep the assistant in a tutoring role largely remove that harm `[R13]`. Help-seeking research shows that learners often misuse on-demand help, both by avoiding it and by abusing it `[R12]`. These rules put the guardrails into practice.

---

## 1. Assistance levels

| Level | Name | What the mentor may do | What it may not do | Counts as independent? |
|---|---|---|---|---|
| **H0** | Clarify | Restate what the task asks; ask what the learner has tried; explain a word in the prompt | Hint at the approach | Yes |
| **H1** | Nudge | Point to the relevant lesson or concept; ask a guiding question; remind the learner of a pattern by name ("this is a *track the maximum* problem") | Locate the bug; show code | Yes |
| **H2** | Targeted hint | Say which part of the code is wrong; explain what a compiler error or failing test means; name the misconception (catalogue ID) | Show corrected code for this exercise | **No — assisted** |
| **H3** | Worked analogy | Show a worked example of a *different but analogous* problem, or a prose/pseudocode outline of the approach | Show code that solves this exercise | No — assisted |
| **H4** | Walkthrough | Walk through a solution to this exercise step by step, explaining each decision | — | No — assisted, and the exercise is marked **solution viewed** |

## 2. Escalation rules

- The learner escalates **one level at a time** using a "More help" control. Free-text chat is answered *at the learner's current level*. Asking "just give me the code" does not skip levels.
- **H2** requires ≥ 1 run or submission on this exercise.
- **H3** requires ≥ 2 attempts with code changes between them since H2, *or* ≥ 10 minutes of active editing since H2.
- **H4** requires H3 to have been given plus ≥ 1 further attempt. The learner must also confirm a notice: *"After a walkthrough, this exercise won't count towards independent mastery. We'll give you a similar one later so you can show you've got it."*
- Each level's gate is shown to the learner ("Make one more attempt to unlock a targeted hint"), so the rules are transparent rather than mysterious.

### 2.1 Caps by context

| Context | Maximum level |
|---|---|
| Lesson exercises | H4 |
| Category A project milestones | H3 |
| Category B projects | H2 for the learner's project code; H3 for general concept questions unrelated to the project's solution |
| Category C assignments | H2, plus "senior colleague" mode: answers questions about the codebase and tools, never writes the fix |
| Retrieval checks, stage gates | H1 |

## 3. Detecting solution-seeking

Signals *(Platform heuristic, informed by "gaming the system" research `[R12]`; tune thresholds with data)*:

- H2+ requested within 2 minutes of opening an exercise.
- ≥ 3 of the last 5 exercises reached H3 or higher.
- Consecutive escalation requests with no code changes in between.
- A submission that closely matches code the mentor showed (token similarity above a threshold).
- Chat messages classified as direct solution requests.

When the combined score crosses a threshold, the learner enters **attempt-first mode** for their next 3 exercises:

- H0 and H1 are never restricted.
- H2+ additionally requires a one-sentence note from the learner: *"What do you think is going wrong?"*
- The mentor's hints become smaller: one idea per message, ending with a question.
- The learner is told, without blame, what was noticed and why the change helps. They can see their own help-use pattern on the progress page.
- The mode ends after 3 exercises completed with ≤ H1.

## 4. Checking understanding

- After any exercise passed with H2+, the mentor asks **one** follow-up question. Examples: explain a specific line, predict the effect of changing an input, or say why the bug happened.
- The answer is scored against a short rubric and recorded as *assisted* `EXPL` evidence.
- If the answer shows a gap, the mentor gives a brief correction and the system schedules an isomorphic variant within the next 2 sessions.

## 5. Code correctness

Model output is never assumed to be correct `[R13]`.

1. **Every Java snippet the mentor intends to show is compiled and run by the execution service before display.** H3 examples run against the example's own stated expected output. H4 walkthroughs run against the exercise's full test suite.
2. If a snippet fails, it's regenerated once. If it fails again, the mentor responds in prose without code, and the failure is logged for review.
3. **Leak check:** any snippet shown at H1–H3 is also run against *this exercise's* hidden tests. If it passes them, it's a disguised solution and is withheld.
4. The mentor never tells a learner their code is correct. Correctness comes from the tests. The mentor may say what the tests show.
5. Static analysis (compiler warnings, a small lint ruleset) runs on mentor snippets as well as learner code. Snippets with warnings are fixed or withheld.

## 6. What the mentor sees

- The exercise prompt, visible tests, authored hints, and the misconception catalogue entries for the exercise.
- The learner's current code, compiler output and test results.
- The learner's concept mastery levels, used to pitch explanations at the right level.
- **The reference solution only from H2 upwards**, used to locate the bug accurately. The leak check (§5.3) enforces non-disclosure.

## 7. Tone and behaviour

- Encouraging and specific, never patronising. Doesn't use "simply", "just" or "obviously" (same rule as [content standards §2.4](03-content-standards.md#24-writing-style)).
- Treats mistakes as normal and informative. Names misconceptions neutrally ("This is a really common one — `==` compares whether two strings are the same object…").
- Stays on Java and the learner's current work. Off-topic requests get a brief redirect.

## 8. Logging and privacy

- Every mentor interaction is logged with: level, gate status, latency, snippets shown, execution-check results, and the follow-up outcome.
- Learners are told during onboarding that mentor conversations are stored to track progress and improve the curriculum. They can view their own logs.
- Mentor logs feed the outcome reports (see [design §8](01-curriculum-design.md#8-measuring-educational-outcomes)), especially the hint-dependency trend.

---

## 9. Implementation notes (2026-11-05)

How the build maps to this policy, and where it differs:

| Policy | Implementation |
|---|---|
| §1 levels, §2 gates, §2.1 caps, §3 attempt-first | `MentorPolicy` (pure, unit-tested) is the only place these decisions are made. The model is told the granted level and can't change it. Caps: H4 for lesson exercises, H1 for knowledge checks (`role: retrieval`). Projects aren't built yet, so their caps aren't either. |
| §2 "≥ 1 run or submission" | Gates count **submissions** ("Check against tests"), not Run presses, because runs aren't recorded. |
| §3 signals | Implemented: solution requests classified by the model (3 of the last 10 learner messages), and H3+ help on 3 of the last 5 exercises. Not implemented: the "H2+ within 2 minutes of opening" signal, because exercise opens aren't recorded, and submission similarity to shown code, because the H4 walkthrough already marks the exercise as solution-viewed. |
| §4 follow-up questions | Offered after any pass with H2+ help. The answer is scored 0–2 and the score is shown. **Not yet done:** feeding the score into mastery as assisted EXPL evidence, and scheduling an isomorphic variant after a weak answer. |
| §5 code correctness | `MentorService.checkCode`: code is only accepted at H3/H4. It must compile with no warnings and run cleanly. H3 code must print its stated output and must not pass the exercise's tests (the leak check). H4 code must pass them. A failure gets one regeneration, then the reply goes out without code. Fenced code in the message text is stripped at every level. |
| §6 what the mentor sees | As specified. The learner's current code is re-graded on the server for every request, so the model sees real test results, not what the browser claims. |
| §8 logging | `mentor_message` stores every message, its level, any code shown and its check result, and the solution-request flag. |
| Explanation scoring | Explanations are scored on submission against the exercise rubric. The score is stored as provisional (`scored_by: ai:<model>`). A 2/2 counts as a pass for mastery. **Not yet done:** the human review queue that samples and calibrates the AI scores. |
| Model | `claude-opus-5-5` at effort `medium`, with structured output. Server-side refusal fallbacks are on (`fallbacks: "default"`), so a classifier refusal is retried on a fallback model, not failed. A per-learner daily cap of 60 model calls guards cost. |
