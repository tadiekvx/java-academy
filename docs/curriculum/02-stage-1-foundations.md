# Stage 1 — Programming Foundations in Java (Vertical Slice)

Status: Draft 1 · 2026-11-05
Parent: [Curriculum design](01-curriculum-design.md) · Standards: [Content standards](03-content-standards.md)

This is the complete design for the first learning journey. It is the specification that Stage 1 content is written against. Source IDs resolve in the [source register](sources.md).

**Target learner:** an adult with no programming experience, working alone at their own pace, about 5–8 hours per week.
**Expected duration:** 35–50 hours, including projects and retrieval checks. *(Platform estimate; replace with measured data.)*
**Language level:** Java 25, compact source files (see [design §1.2](01-curriculum-design.md#12-beginner-entry-point-compact-source-files-java-25)).

---

## 1. Exit competency

A learner who passes Stage 1 can, **without assistance**:

1. Write a 50–150 line program that reads input, validates it, makes decisions, repeats work, and stores and processes a list of values.
2. Decompose that program into methods with clear parameters and return values.
3. Trace a short program by hand (including loops and method calls) and predict its output exactly.
4. Read a compiler error or a runtime stack trace, locate the cause, and fix it.
5. Modify an unfamiliar working program to meet a changed requirement without breaking existing behaviour (as checked by tests).
6. Explain in plain language what their code does, and why one of their design choices was made.

---

## 2. Concept graph

Concepts are the unit of mastery. Prerequisites gate *recommendations*, not access. A learner may open any lesson, but the dashboard recommends the next concept whose prerequisites are at level ≥ 2.

| ID | Concept | Prerequisites | Required evidence (see [design §4.1](01-curriculum-design.md#41-evidence-types)) |
|---|---|---|---|
| J1.01 | Program execution and output | — | IMPL, MIST |
| J1.02 | Values, types and expressions | J1.01 | IMPL, MIST, EXPL |
| J1.03 | Variables and assignment | J1.02 | IMPL, MIST, DEBUG, EXPL |
| J1.04 | Strings | J1.03 | IMPL, MIST, DEBUG |
| J1.05 | Input and type conversion | J1.04 | IMPL, DEBUG |
| J1.06 | Boolean logic and conditionals | J1.03 | IMPL, MIST, DEBUG, MOD, EXPL |
| J1.07 | Loops | J1.06 | IMPL, DEBUG, MOD, XFER, EXPL |
| J1.08 | Methods: parameters and return values | J1.07 | IMPL, MIST, DEBUG, MOD, EXPL |
| J1.09 | Problem decomposition | J1.08 | IMPL, XFER, EXPL |
| J1.10 | Arrays | J1.07, J1.08 | IMPL, MIST, DEBUG, MOD |
| J1.11 | `ArrayList` | J1.10 | IMPL, MOD |
| J1.12 | Runtime exceptions and stack traces | J1.05, J1.10 | DEBUG, EXPL |
| J1.13 | Systematic debugging | J1.01 (developed across the stage) | DEBUG, EXPL |
| J1.14 | Reading tests and specifications | J1.08 | IMPL, EXPL |

---

## 3. Misconception catalogue

Each misconception is targeted at least three times:
1. In the lesson's "Common mistakes" section.
2. In a `MIST` item.
3. In a `DEBUG` exercise that contains it.

The mentor also receives this catalogue so it can name the misconception when it sees one.

| ID | Misconception | Concept | Source |
|---|---|---|---|
| MC01 | `=` is read as mathematical equality, or as symmetric (`a = b` same as `b = a`) | J1.03 | `[R8]` |
| MC02 | A variable can hold several values at once or "remembers" earlier values | J1.03 | `[R8]` |
| MC03 | After `b = a;`, changing `a` also changes `b` (for primitives) | J1.03 | `[R8]` |
| MC04 | Integer division keeps the fraction (`7 / 2` is `3.5`); `1 / 2 * x` is `x / 2` | J1.02 | Platform (common in CS1 practice; to be confirmed with our own attempt data) |
| MC05 | Strings are compared with `==` | J1.04 | `[R9]` |
| MC06 | Calling a non-void method changes something even when its result is ignored (`name.toUpperCase();`) | J1.04, J1.08 | `[R9]` |
| MC07 | Printing a value is the same as returning it | J1.08 | `[R8]` |
| MC08 | A semicolon after an `if`/`while` header is harmless (`if (x > 0); { … }`) | J1.06, J1.07 | `[R9]` |
| MC09 | Loop bounds and indices are off by one (`i <= arr.length`) | J1.07, J1.10 | `[R8]` |
| MC10 | A `while` loop exits the moment its condition becomes false mid-body | J1.07 | `[R8]` |
| MC11 | In an `if / else if` chain, every matching branch runs | J1.06 | `[R8]` |
| MC12 | Assigning an array to another variable copies it | J1.10 | `[R8]` |
| MC13 | Changing a primitive parameter inside a method changes the caller's variable | J1.08 | `[R8]` |
| MC14 | `&` / `|` and `&&` / `||` are interchangeable | J1.06 | `[R9]` |
| MC15 | The first line of a stack trace always points at the learner's own code | J1.12 | Platform |

---

## 4. Modules and lessons

Codes in the **Cycle** column refer to the [learning cycle](01-curriculum-design.md#2-the-learning-cycle): **U**nderstand, **A**pply, **I**nvestigate, **B**uild, **E**xplain, **R**einforce.

### Module 1 — First programs

| Lesson | Concepts | Learning objectives (learner can…) | Cycle | Key misconceptions |
|---|---|---|---|---|
| 1.1 Your first program | J1.01 | Run a program; explain that statements execute top to bottom; use `IO.println` and `IO.print`; recognise the traditional `public static void main` form in outside material | U A | — |
| 1.2 Errors are feedback | J1.01, J1.13 | Read a compiler error: file, line, message; fix missing semicolons, unbalanced braces and misspelt names; distinguish compile-time from run-time errors | U I | — |

### Module 2 — Values and variables

| Lesson | Concepts | Learning objectives | Cycle | Misconceptions |
|---|---|---|---|---|
| 2.1 Values and types | J1.02 | Identify `int`, `double`, `boolean`, `char`, `String` literals; predict the type of an expression | U A | — |
| 2.2 Variables and state | J1.03 | Declare, assign, reassign; trace variable state in a table; use `var` and `final` | U A I E | MC01–MC03 |
| 2.3 Arithmetic | J1.02 | Evaluate expressions with precedence; use `/` and `%` on integers; convert between `int` and `double` deliberately; round a division up | U A I E | MC04 |
| 2.4 Working with strings | J1.04 | Concatenate; use `length`, `charAt`, `substring`, `indexOf`, `equals`, `toUpperCase`; explain immutability | U A I | MC05, MC06 |

### Module 3 — Input and decisions

| Lesson | Concepts | Learning objectives | Cycle | Misconceptions |
|---|---|---|---|---|
| 3.1 Reading input | J1.05 | Use `IO.readln(prompt)`; convert with `Integer.parseInt` / `Double.parseDouble`; recognise `NumberFormatException` | U A I | — |
| 3.2 Boolean expressions | J1.06 | Write comparisons; combine with `&&`, `||` and `!`; explain short-circuit evaluation | U A | MC14 |
| 3.3 Making decisions | J1.06 | Write `if`, `if/else` and `else if` chains; order conditions correctly | U A I E | MC08, MC11 |
| 3.4 `switch` expressions | J1.06 | Use arrow-form `switch` expressions (Java 14); choose between `switch` and `if` | U A | — |

### Module 4 — Repetition

| Lesson | Concepts | Learning objectives | Cycle | Misconceptions |
|---|---|---|---|---|
| 4.1 `while` loops | J1.07 | Write a `while` loop with a correct update; identify infinite loops | U A | MC10 |
| 4.2 Tracing loops | J1.07 | Complete a trace table for a loop; predict final values and output | I E | MC10 |
| 4.3 `for` loops and boundaries | J1.07 | Write counting loops; reason about inclusive and exclusive bounds | U A I | MC09 |
| 4.4 Loop patterns | J1.07, J1.09 | Apply the count, sum, find-first and track-maximum patterns; choose the right pattern for a problem | U A I E | — |
| 4.5 Input validation loops | J1.05, J1.07 | Repeat a prompt until input is valid; handle non-numeric input | A B | — |

### Module 5 — Methods

| Lesson | Concepts | Learning objectives | Cycle | Misconceptions |
|---|---|---|---|---|
| 5.1 Defining and calling methods | J1.08 | Define a method; call it; explain why we name chunks of code | U A | — |
| 5.2 Parameters and return values | J1.08 | Pass arguments; return results; use returned values | U A I E | MC06, MC07, MC13 |
| 5.3 Scope and the call stack | J1.08 | Explain local scope; trace nested calls on a stack diagram | U I E | MC13 |
| 5.4 Decomposing problems | J1.09 | Break a problem into methods top-down; write the signatures before the bodies | U A B E | — |
| 5.5 Reading tests | J1.14 | Read a test and state the behaviour it checks; write a simple `check(expected, actual)` call for a new case | U A E | — |

### Module 6 — Working with data

| Lesson | Concepts | Learning objectives | Cycle | Misconceptions |
|---|---|---|---|---|
| 6.1 Arrays | J1.10 | Create, index and iterate (index loop and enhanced `for`); use `.length` | U A | MC09 |
| 6.2 Array algorithms and references | J1.10 | Search, count and reverse; explain aliasing; copy with `Arrays.copyOf` | U A I E | MC12 |
| 6.3 `ArrayList` | J1.11 | Use `add`, `get`, `set`, `remove`, `size`; choose between an array and a list | U A | — |
| 6.4 Exceptions and stack traces | J1.12 | Read a stack trace; identify the exception type, the message and the learner's frame; prevent common exceptions | U I E | MC15 |
| 6.5 Debugging systematically | J1.13 | Reproduce → hypothesise → test → fix → verify; debug a 60-line inherited program with three bugs | I E | — |

### Module 7 — Projects and stage gate

| Item | Category | Concepts integrated |
|---|---|---|
| P1 Study Log | A — Guided | J1.03–J1.11, J1.14 |
| P2 Parking Fee Calculator | B — Independent | J1.02–J1.12 |
| Stage 1 gate | Assessment | All |

**Reinforce across stages:** Stage 2 Lesson 1 reopens the learner's own Study Log. It refactors the parallel lists into a `record Session` and converts the file to the traditional class form. This retrieves Stage 1 code in a new context and motivates records.

---

## 5. Exercise ladders

### 5.0 Exercise frames before Module 5 *(Platform decision, made while building lesson 2.3)*

Exercises have to be tested with many inputs. Before Module 5, learners can't write methods, and before 3.1 they can't read input. So write, debug and modify exercises in Modules 1–4 use a **given method header** (an "exercise frame"):

```java
double average(int a, int b) {
    return 0.0; // replace 0.0 with your expression
}

void main() {
    IO.println(average(3, 4)); // should print 3.5
}
```

- Lesson 2.1 introduces frames ("How exercises with a method header work"), the first lesson that needs them. Lessons 1.1–1.2 use whole programs checked by their exact output. Later lessons repeat a one-line reminder.
- Module 5 then explains the header the learners have been using all along. This is a deliberate Reinforce moment.
- Every starter includes a `void main()` that calls the method. Java 25 requires a compact source file to declare a launchable `main`. It also lets learners run and experiment, not only submit.
- Lessons 2.2 (variables) and 2.3 (arithmetic) swapped places during the build, because arithmetic examples need variables.


Every concept gets an exercise ladder. A typical ladder for one lesson:

| Step | Exercise type | Evidence | Assistance cap | Example (Lesson 4.3 `for` loops) |
|---|---|---|---|---|
| 1 | **Predict** — predict output, then run | MIST | H4 | `for (int i = 1; i < 10; i += 3) IO.print(i + " ");` — what's printed? |
| 2 | **Parsons** — order the given lines | IMPL (assisted only) | H4 | Arrange lines to print the even numbers from 2 to 20 |
| 3 | **Write** — from a spec, with hidden tests | IMPL | H4 | `int sumOfMultiples(int n, int k)` — sum of multiples of `k` in `1..n` |
| 4 | **Debug** — a failing implementation | DEBUG | H4 | `countVowels` skips the last character (`i < s.length() - 1`) |
| 5 | **Modify** — extend working code | MOD | H4 | Change a times-table printer to print only a requested row range |
| 6 | **Explain** — short written answer | EXPL | H4 | "Why does your loop start at `k` rather than 1? Would starting at 1 change the result?" |
| — | **Retrieval variants** (scheduled later) | Any of the above | H1 | Isomorphic variants of 3–5 |

Rules:
- Parsons problems never count as independent `IMPL` evidence. They are scaffolding `[R7]`.
- Every write, debug and modify exercise has: a reference solution, ≥ 3 visible tests, ≥ 5 hidden tests including edge cases (empty, zero, negative, boundary), and at least one known-wrong solution that must *fail* the tests. The last item validates the tests themselves (see [standards §4](03-content-standards.md#4-exercise-standards)).
- Explain items have a 3-point rubric (0 = incorrect, 1 = partially correct, 2 = correct with reasoning) with anchor answers. For the vertical slice, AI scores them provisionally, and the learner sees the rubric and the score with "provisional" clearly shown. A human-review queue samples 10% of them to calibrate the scoring.

**Target per lesson:** 4–7 ladder exercises plus 3–5 retrieval variants per concept. Total for Stage 1: about 120 items.

---

## 6. Projects

> **Superseded 2026-11-05.** The Study Log and Parking Fee Calculator below were the original plan. The built projects are the personal finance calculator (guided), the shopping basket and receipt and Brightbank account logic (independent), and the inherited-gradebook assessment. See `docs/JAVA_MASTER_CURRICULUM.md` (Stage 1, module 8). The text below is kept for reference.

### P1 — Study Log (Category A: guided build)

**Purpose:** combine input, validation, loops, methods and lists into one program the learner might actually use.

**The program:** a menu-driven console app. It records study sessions (subject and minutes), lists them, totals minutes per subject, finds the longest session, and shows progress towards a weekly goal.

| Milestone | Learner builds | Concepts | Checked by |
|---|---|---|---|
| M1 Menu loop | A menu that repeats until the user quits; handles unknown options | J1.05–J1.07 | Scripted stdin/stdout tests |
| M2 Record sessions | `addSession` with validation (minutes 1–600, non-blank subject); listing | J1.08, J1.11 | Method tests + I/O tests |
| M3 Analysis | `totalFor(subject)`, `longestSession()`, `subjects()` (no duplicates) | J1.07, J1.09, J1.11 | Hidden method tests incl. empty log |
| M4 Weekly goal | A progress bar string such as `[######----] 60%` using integer arithmetic | J1.02, J1.04 | Method tests, boundary cases (0%, 100%, >100%) |
| M5 Explain checkpoint | Answers: *Why did you split the program into these methods? What happens with input `abc` for minutes, and where is that handled?* | J1.09, EXPL | Rubric |

- Each milestone ships with an explanation, a worked example of a *similar* (not identical) piece of code, and the tests.
- The design deliberately uses two parallel `ArrayList`s (subjects and minutes). Milestone M3's notes point out that this is awkward. Stage 2 fixes it with a record (§4 "Reinforce across stages").

### P2 — Parking Fee Calculator (Category B: independent build)

**Purpose:** first independent design. The learner gets requirements and acceptance criteria, but no steps.

**Requirements:**
1. Read lines of the form `<vehicle> <entry HH:MM> <exit HH:MM>` until a blank line. Vehicles: `car`, `motorbike`, `van`.
2. Fees: first 30 minutes free. After that, each *started* hour costs car 200p, motorbike 100p, van 300p. The daily maximum is car 1500p, motorbike 800p, van 2000p.
3. Print each fee as `£x.xx`. After the blank line, print the number of vehicles, total revenue and the longest stay.
4. For invalid lines (unknown vehicle, malformed time, exit before entry), print a clear error for that line and continue.

**Acceptance criteria (excerpt):**
- *Given* `car 09:00 09:30`, *then* the output is `£0.00` (the free period is inclusive of 30 minutes).
- *Given* `car 09:00 09:31`, *then* `£2.00`.
- *Given* `van 08:00 20:00`, *then* `£20.00` (the cap applies).
- *Given* `bike 09:00 10:00`, *then* an error line naming the unknown vehicle, and processing continues.
- *Given* `car 10:00 09:00`, *then* an error line stating that exit is before entry.
- The full set is 5 public and 20 hidden acceptance tests.

**Constraints:**
- Store money as `int` pence, never `double`. The lesson explains why.
- No `java.time`. Learners parse `HH:MM` themselves. *(This is deliberate string practice. Stage 3 revisits P2 and replaces the hand parsing with `java.time` as a Reinforce activity.)*
- At least four methods; none longer than 25 lines.

**Deliverables:**
- The code.
- A design note of at most 150 words: how the program is decomposed, the hardest edge case, and how it's handled.

**Assessment:**
- Hidden acceptance tests: all must pass.
- Rubric:
  - decomposition (0–2)
  - naming and readability (0–2)
  - edge-case handling (0–2)
  - design note (0–2)
- Pass: all tests pass and the rubric total is ≥ 5 out of 8, with no zero scores.

---

## 7. Stage 1 gate

The gate is taken independently: mentor capped at H1, no access to the learner's earlier solutions. Items are drawn from pools, so learners retaking the gate get different problems.

| Item | Type | Example | Pass condition |
|---|---|---|---|
| G1 | Write | `int longestRun(int[] values)` — length of the longest run of equal adjacent values | All hidden tests pass |
| G2 | Debug | A `classify(String grade)` method with an off-by-one boundary error and an `==` string comparison | All tests pass |
| G3 | Trace | Predict the exact output of a 15-line program with a loop calling a method | Exact match |
| G4 | Modify | Extend a working shopping-basket program with a "buy 3, pay for 2" rule | New + existing tests pass |
| G5 | Explain | "This `average` method crashes on an empty list. Explain why and how you would fix it." | Rubric ≥ 2/3 |

- **On pass:** concepts are confirmed (gate evidence counts towards level 5, Retained, for concepts already Secure), and Stage 2 is recommended.
- **On fail:** the learner gets a review plan built from the failed items' concepts. A retake with fresh variants is available after 48 hours.
- **Placement:** learners with prior experience may take the gate on day 1. Passing raises the gate-covered concepts to level 3 (Demonstrated) but not higher. Retrieval checks are still scheduled, because one pass is not evidence of retention.

---

## 8. Learning-cycle coverage check

| Concept | U | A | I | B | E | R |
|---|---|---|---|---|---|---|
| J1.01 Execution | 1.1 | 1.1 | 1.2 | P1 | — | checks |
| J1.02 Values/types | 2.1, 2.3 | 2.3 | 2.3 | P1 M4, P2 | 2.3 explain | checks, P2 |
| J1.03 Variables | 2.2 | 2.2 | 2.2 trace | P1 | 2.2 explain | checks |
| J1.04 Strings | 2.4 | 2.4 | 2.4 debug | P1 M4, P2 | — | checks, Stage 3 P2 revisit |
| J1.05 Input | 3.1 | 3.1, 4.5 | 3.1 debug | P1 M1, P2 | P1 M5 | checks |
| J1.06 Conditionals | 3.2–3.4 | 3.3 | 3.3 debug/modify | P1, P2 | 3.3 explain | checks, gate G2 |
| J1.07 Loops | 4.1, 4.3 | 4.3, 4.4 | 4.2 trace, 4.3 debug | P1, P2 | 4.4 explain | checks, gate G1/G3 |
| J1.08 Methods | 5.1, 5.2 | 5.2 | 5.3 trace | P1, P2 | 5.2, 5.3 explain | checks, gate G3 |
| J1.09 Decomposition | 5.4 | 5.4 | 4.4 | P1, P2 | P1 M5, P2 note | Stage 2 |
| J1.10 Arrays | 6.1 | 6.1, 6.2 | 6.2 debug | — | 6.2 explain | checks, gate G1 |
| J1.11 ArrayList | 6.3 | 6.3 | 6.3 modify | P1 | — | checks, Stage 2 refactor |
| J1.12 Exceptions | 6.4 | — | 6.4 | P2 | 6.4 explain | gate G5 |
| J1.13 Debugging | 1.2, 6.5 | — | 6.5 inherited program | P1, P2 | 6.5 explain | gate G2 |
| J1.14 Tests/specs | 5.5 | 5.5 | P1 milestones | P1 | 5.5 explain | Stage 2+ |

Every concept has Understand, Investigate (or an equivalent), Build and Reinforce coverage. Gaps in the Apply and Explain columns are deliberate where the concept is about reading rather than writing (J1.12, J1.13), or where explanation is assessed inside a project (J1.11 through P1).
