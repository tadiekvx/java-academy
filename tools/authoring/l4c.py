import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-4"
from build import *
import outline
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'
def domestic(g): return 300 if g <= 500 else 450 if g <= 2000 else 450 + ((g - 2000 + 999) // 1000) * 100
def intl(g): return 800 if g <= 500 else 1200 if g <= 2000 else 1200 + ((g - 2000 + 999) // 1000) * 250
def ship(g, express, country):
    c = domestic(g) if country == "UK" else intl(g)
    return c * 2 if express else c

# ====================================================================== 4.4.1
Lesson("j4-l4.1", "Logging and debugging", ["J4.07"], [
    ("o1", "Choose log levels and write log lines that help someone find a problem later"),
    ("o2", "Find and fix several faults in one unfamiliar method, one at a time"),
    ("o3", "Describe how to use a debugger (breakpoints, stepping, watching variables) and when it beats printing"),
], ["j4-l3.2", "j1-l6.5"], 55, ["R16", "R8"], r'''
## Before you start

You know the debugging cycle from Stage 1 ([Debugging systematically](j1-l6.5)): reproduce, hypothesise, test, fix, verify.

**Quick check.** Why change one thing at a time when debugging?

<details><summary>Show the answer</summary>

So you know which change made the difference. Several changes at once hide the cause.

</details>

## Explanation

### Two ways to see inside a running program

When code misbehaves you need to see what it's doing. You have two main tools: **logging** (the program writes what it's doing as it runs) and a **debugger** (you pause it and look). They suit different jobs.

### Logging

Printing with `IO.println` while you work is fine. But a program running at a customer's site, or last night at 3 am, can't be paused, and a screen full of ad-hoc prints can't be turned off. Real programs use **logging**: every message has a **level**, and you decide which levels to keep.

| Level | Meaning | Example |
|---|---|---|
| `DEBUG` | detail for developers while investigating | `looked up customer 42, found 3 orders` |
| `INFO` | normal events worth recording | `order 1017 placed` |
| `WARN` | something unexpected that the program coped with | `payment retry 2 of 3` |
| `ERROR` | something failed | `could not save order 1017: disk full` |

A **threshold** sets how much you see: at `INFO`, the `DEBUG` lines are dropped; at `DEBUG`, you see everything. In production you usually run at `INFO` or `WARN`, and turn on `DEBUG` only to investigate. Java has built-in logging and several widely used libraries; they all share this idea of levels and a threshold.

A good log line:

- has a **level, a time and a message** (and often the name of the part of the program that wrote it);
- says **what happened and to which thing**: `order 1017 placed for customer 42`, not `done`;
- gives the **values** that explain a failure: `invalid quantity -3 for item 88`;
- **never contains secrets or personal data**: passwords, card numbers, tokens. Logs get copied, searched and kept for a long time.

Don't log inside a tight loop at `INFO`: a million lines hide the one you need.

### The debugger

A **debugger** runs your program under control. Every IDE has one, and the controls are much the same:

- **Breakpoint:** a marker on a line. The program **pauses** just before that line runs.
- **Inspect variables:** while paused, see the current value of every variable in scope, and look into objects and collections.
- **Step over:** run the current line and stop at the next one in the *same* method.
- **Step into:** if the line calls a method, go *inside* it and stop at its first line.
- **Step out:** run until the current method returns.
- **Call stack:** the chain of calls that led here, like a live stack trace; click a frame to see that method's variables.
- **Watch / conditional breakpoint:** keep an eye on an expression, or only pause when a condition is true (`i == 4999`).

The debugger is the best tool when you need to **see the state at one exact moment** and can reproduce the bug on your own machine. Logs are the best tool when the bug happens **somewhere you can't pause** (a server, last night's run), or when the bug depends on a long sequence of events you want to read through afterwards. Often you use both.

### A method for an unfamiliar bug

The cycle from Stage 1 still applies, now with better tools `[R16]`:

1. **Reproduce** it with the smallest input you can. A failing check is ideal.
2. **Find where** the wrong value first appears: break just before the suspect line, or log the values going in and out.
3. **Form one hypothesis,** ("the loop stops one item early") and **test just that**.
4. **Fix one thing,** then re-run **all** the checks.
5. **Look for the other bugs.** Code that has one fault often has more, and a method with three faults can show the symptom of whichever is hit first.

## Worked examples

### Example 1: choosing levels

*Task: which level for each message?*

- `customer 42 logged in`: **INFO** (a normal event worth recording).
- `loaded 3 orders for customer 42 in 12 ms`: **DEBUG** (detail for investigation).
- `card declined, retrying (attempt 2)`: **WARN** (unexpected, but handled).
- `could not connect to the payment service`: **ERROR** (something failed).

### Example 2: three faults in one method

*Task: `report(marks)` should give the average (whole number) and a grade: A for 70 or more, B for 50 to 69, C below 50; for no marks, `avg=0 grade=C`. It gives wrong answers. How do you find the faults?*

**Step 1 — Reproduce with tiny inputs:** `report(new int[]{70, 70, 70})` should be `avg=70 grade=A`.

**Step 2 — See which value goes wrong:** log or inspect `total` and `avg`. If `total` is 140, not 210, the loop skipped one mark. That's fault 1: the loop bound.

**Step 3 — Fix it and re-run.** Now `avg=70` but the grade is `B`: fault 2, a `>` that should be `>=` at the boundary.

**Step 4 — Re-run with no marks.** It crashes with a division by zero: fault 3, a missing guard for the empty case.

## Where this is used

- **Production incidents** are investigated from logs: nobody can attach a debugger to last night's run.
- **Feature work and bug fixes** use the IDE debugger constantly.
- **Log levels** are part of every operations team's vocabulary.

## Common mistakes

:::mistake{id=MC148}
**Logging everything at one level.** Without levels you can't turn the noise down, and the important line is lost.
:::

:::mistake{id=MC149}
**Logging passwords, tokens or personal data.** Logs are copied and kept far longer than you expect.
:::

:::mistake{id=MC150}
**Fixing the first fault and stopping.** A method can have several faults, and the first fix often reveals the next.
:::

## Practice

::exercise{id=j4-l4.1-write-log}

::exercise{id=j4-l4.1-debug-faults}

::exercise{id=j4-l4.1-explain-debugger}

## Further reading

- **McCauley et al. (2008)** `[R16]` review how debugging is learned and taught: systematic strategies beat guessing.
- **Qian & Lehman (2017)** `[R8]` on common novice difficulties that debugging tools help expose.

## How you'll be assessed

- The **write** exercise checks that you can implement level filtering and a log format (*implementation*).
- The **debug** exercise checks that you can find and fix several faults in one method (*debugging*).
- The **explain** exercise checks that you can describe a debugger workflow and choose between a debugger and logs (*explanation*).
''' + FOOT)

ex = Exercises("j4-l4.1")
LOG_DRV = '\n\nString run(String threshold, String[] entries) {\n    try {\n        SimpleLog log = new SimpleLog(threshold);\n        List<String> lines = new ArrayList<>();\n        for (String entry : entries) {\n            String[] parts = entry.split(":", 2);\n            String line = log.log(parts[0], parts[1]);\n            if (!line.isEmpty()) {\n                lines.add(line);\n            }\n        }\n        return String.join("|", lines);\n    } catch (IllegalArgumentException e) {\n        return "unknown level";\n    }\n}'
LOG_SOL = 'class SimpleLog {\n    private final int threshold;\n\n    SimpleLog(String threshold) {\n        this.threshold = rank(threshold);\n    }\n\n    private static int rank(String level) {\n        return switch (level) {\n            case "DEBUG" -> 0;\n            case "INFO" -> 1;\n            case "WARN" -> 2;\n            case "ERROR" -> 3;\n            default -> throw new IllegalArgumentException("unknown level: " + level);\n        };\n    }\n\n    String log(String level, String message) {\n        if (rank(level) >= threshold) {\n            return "[" + level + "] " + message;\n        }\n        return "";\n    }\n}'
RANK = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3}
def log_run(th, entries):
    if th not in RANK: return "unknown level"
    out = []
    for e in entries:
        lvl, msg = e.split(":", 1)
        if lvl not in RANK: return "unknown level"
        if RANK[lvl] >= RANK[th]: out.append(f"[{lvl}] {msg}")
    return "|".join(out)
ex.method("write", "j4-l4.1-write-log", "A log with levels", ["o1"], ["J4.07"], ["IMPL"],
    "Write `SimpleLog`. It's created with a **threshold** level (`\"DEBUG\"`, `\"INFO\"`, `\"WARN\"` or `\"ERROR\"`, in increasing order of severity). `log(level, message)` returns `\"[LEVEL] message\"` if `level` is **at or above** the threshold, and an empty string if it's below. An unknown level name must throw an `IllegalArgumentException` (the driver turns that into `unknown level`). The driver feeds in entries such as `\"WARN:disk almost full\"`.",
    [("run", [("threshold", "String"), ("entries", "String[]")], "String")], {"run": log_run},
    [("run", ["INFO", ["DEBUG:loading", "INFO:order placed", "ERROR:disk full"]]), ("run", ["DEBUG", ["DEBUG:a"]]), ("run", ["ERROR", []])],
    [("run", ["WARN", ["INFO:x", "WARN:y", "ERROR:z"]]), ("run", ["ERROR", ["WARN:w", "ERROR:e"]]), ("run", ["DEBUG", ["INFO:i", "DEBUG:d"]]), ("run", ["TRACE", ["INFO:x"]]), ("run", ["INFO", ["LOUD:x"]]), ("run", ["INFO", ["INFO:a:b"]])],
    'class SimpleLog {\n    SimpleLog(String threshold) {\n    }\n\n    String log(String level, String message) {\n        return "";\n    }\n}' + LOG_DRV,
    LOG_SOL + LOG_DRV,
    {"strictly-above": LOG_SOL.replace("rank(level) >= threshold", "rank(level) > threshold") + LOG_DRV,
     "compares-the-names-alphabetically": LOG_SOL.replace("rank(level) >= threshold", "level.compareTo(String.valueOf(threshold)) >= 0") + LOG_DRV,
     "no-brackets": LOG_SOL.replace('return "[" + level + "] " + message;', 'return level + " " + message;') + LOG_DRV},
    ("Turn each level name into a number (DEBUG 0 up to ERROR 3). A message is logged when its number is at least the threshold's. Format it as [LEVEL] message.", "if (rank(level) >= threshold) return \"[\" + level + \"] \" + message;"),
    difficulty=3)
REP_BAD = 'String report(int[] marks) {\n    int total = 0;\n    for (int i = 0; i < marks.length - 1; i++) {\n        total += marks[i];\n    }\n    int average = total / marks.length;\n    String grade = average > 70 ? "A" : average >= 50 ? "B" : "C";\n    return "avg=" + average + " grade=" + grade;\n}'
REP_OK = 'String report(int[] marks) {\n    if (marks.length == 0) {\n        return "avg=0 grade=C";\n    }\n    int total = 0;\n    for (int i = 0; i < marks.length; i++) {\n        total += marks[i];\n    }\n    int average = total / marks.length;\n    String grade = average >= 70 ? "A" : average >= 50 ? "B" : "C";\n    return "avg=" + average + " grade=" + grade;\n}'
def report(m):
    if not m: return "avg=0 grade=C"
    a = sum(m) // len(m)
    return f"avg={a} grade={'A' if a >= 70 else 'B' if a >= 50 else 'C'}"
ex.method("debug", "j4-l4.1-debug-faults", "Three faults in one method", ["o2"], ["J4.07"], ["DEBUG"],
    "`report(marks)` should return `avg=<average, rounded down> grade=<letter>`: **A** for an average of 70 or more, **B** for 50 to 69, **C** below 50. With no marks it returns `avg=0 grade=C`. It has **three separate faults**. Find them one at a time: make a tiny failing case, find where the wrong value appears, fix just that, and run everything again.",
    [("report", [("marks", "int[]")], "String")], {"report": report},
    [("report", [[70, 70, 70]]), ("report", [[40, 60]]), ("report", [[]])],
    [("report", [[100]]), ("report", [[50, 50]]), ("report", [[69, 70, 71]]), ("report", [[49]]), ("report", [[0, 0, 100]]), ("report", [[90, 10, 80, 20]])],
    REP_BAD, REP_OK,
    {"still-skips-the-last-mark": REP_OK.replace("i < marks.length; i++", "i < marks.length - 1; i++"),
     "still-excludes-seventy": REP_OK.replace("average >= 70", "average > 70"),
     "no-empty-guard": REP_OK.replace('    if (marks.length == 0) {\n        return "avg=0 grade=C";\n    }\n', "")},
    ("Start with report([70, 70, 70]). What total does the loop reach? Then check the grade boundary, then the empty array.", "Loop to marks.length, use >= for the grade boundary, and return early for an empty array."),
    difficulty=3)
ex.explain("j4-l4.1-explain-debugger", "Debugger or logs?", ["o3", "o1"], ["J4.07"],
    "A method `totalFor(customerId)` returns the wrong total for **one** customer, id 4,271, out of 100,000. (a) Describe how you'd use a debugger to find out why: which kind of breakpoint, what you'd inspect, and which stepping commands. (b) The same bug appears only on the production server, where you can't attach a debugger. What do you do instead, and what would make the log lines useful? (c) Name one thing you must never write to a log.",
    "A full answer describes a conditional breakpoint (customerId == 4271) at the start of the method, inspecting the variables and the collection being summed, stepping over lines and into calls to see where the value goes wrong; for production says to add log lines at a suitable level with the customer id and the values going in and out and read them afterwards; and says never log passwords, tokens, card numbers or personal data.",
    {2: ("Describes a conditional breakpoint on the id, inspecting variables and stepping over and into lines to find where the value goes wrong; says to use logging with the customer id and the key values at a suitable level in production; and names something never to log such as passwords or personal data.",
         ["I'd put a conditional breakpoint at the top of totalFor that only pauses when customerId == 4271, then inspect the variables and the list of items being added, and step over each line, or into any call that looks suspicious, until I see the total go wrong. On production I'd add log lines, at DEBUG so I can switch them on, with the customer id and the values going in and out, then read the log after reproducing it. I'd never log passwords, tokens or personal details.",
          "a) Conditional breakpoint for id 4271, inspect variables, step over and into. b) Log the id and intermediate values at DEBUG and read the logs. c) Never log passwords or card numbers."]),
     1: ("Answers some parts, for example the debugger part but not the logging part, or without the conditional breakpoint.",
         ["Use a breakpoint and step through.", "Add log lines."]),
     0: ("Incorrect, for example says to restart the server, or to log the customer's password to see what happens.",
         ["Restart the server and hope.", "Log the password to check."])})
reg({"j4-l4.1": ("Logging and debugging", ["J4.07"])},
    {"MC148": (["J4.07"], "Platform", "Logging everything at one level is fine"),
     "MC149": (["J4.07"], "Platform", "It is fine to log passwords or personal data while investigating"),
     "MC150": (["J4.07"], "R16", "Once the first fault is fixed, the method is correct")})

# ====================================================================== 4.4.2
Lesson("j4-l4.2", "Refactoring under tests", ["J4.08"], [
    ("o1", "Explain what refactoring is and why tests come first"),
    ("o2", "Extract methods and name constants without changing behaviour"),
    ("o3", "Replace a long parameter list with a parameter object, keeping every result the same"),
], ["j4-l4.1", "j4-l3.2"], 55, ["R16", "R8"], r'''
## Before you start

You can write tests that catch deliberately broken code ([Your first unit tests](j4-l3.1)) and you know records ([Records and enums](j2-l4.1)).

**Quick check.** Why can tests make it safe to change code?

<details><summary>Show the answer</summary>

If the tests still pass after the change, the behaviour they check hasn't changed.

</details>

## Explanation

### Refactoring: change the structure, keep the behaviour

**Refactoring** means improving how code is organised **without changing what it does**: clearer names, smaller methods, no duplication. Done well, it makes the next feature cheaper and the next bug easier to find. Done without a safety net, it's just rewriting, and rewriting changes behaviour by accident.

The safety net is the **tests**. The rule:

1. **Make sure there are tests** that pin down the current behaviour, including edge cases. (If there are none, write some first.)
2. **Change one small thing.**
3. **Run the tests.** If they fail, undo, or fix.
4. Repeat. Commit often, so a bad step is one `git restore` away.

If the tests are red *before* you start, you can't refactor safely: fix or understand that first. Never mix a refactor with a behaviour change in the same step; when something breaks, you wouldn't know which caused it.

### Common refactorings

**Rename.** The cheapest improvement. `proc` becomes `shippingCost`, `d` becomes `weightInGrams`. Names are the main documentation.

**Extract method.** Take a block of code that does one nameable job and move it into a method with a good name. Long methods become short ones that read like a summary:

```java
// before
int shippingCost(int grams, boolean express, String country) {
    int cost;
    if (country.equals("UK")) {
        if (grams <= 500) cost = 300;
        else if (grams <= 2000) cost = 450;
        else cost = 450 + ((grams - 2000 + 999) / 1000) * 100;
    } else {
        if (grams <= 500) cost = 800;
        else if (grams <= 2000) cost = 1200;
        else cost = 1200 + ((grams - 2000 + 999) / 1000) * 250;
    }
    if (express) cost = cost * 2;
    return cost;
}

// after
int shippingCost(int grams, boolean express, String country) {
    int cost = country.equals("UK") ? domesticCost(grams) : internationalCost(grams);
    return express ? cost * 2 : cost;
}

int domesticCost(int grams) {
    if (grams <= 500) return 300;
    if (grams <= 2000) return 450;
    return 450 + extraKilos(grams) * 100;
}

int internationalCost(int grams) {
    if (grams <= 500) return 800;
    if (grams <= 2000) return 1200;
    return 1200 + extraKilos(grams) * 250;
}

int extraKilos(int grams) {
    return (grams - 2000 + 999) / 1000;
}
```

Same answers for every input; but now `shippingCost` reads as a sentence, the "round up to whole kilos" logic exists **once**, and a change to UK prices touches one small method.

**Introduce a named constant.** A bare number in code (a **magic number**) says nothing about what it means or where else it must change:

```java
// before                              // after
int total(int pence) {                 static final int TAX_PERCENT = 20;
    int taxed = pence * 120 / 100;     static final int FREE_DELIVERY_FROM = 5000;
    if (pence >= 5000) return taxed;   static final int DELIVERY_FEE = 499;
    return taxed + 499;
}                                      int total(int pence) {
                                           int taxed = pence * (100 + TAX_PERCENT) / 100;
                                           if (pence >= FREE_DELIVERY_FROM) return taxed;
                                           return taxed + DELIVERY_FEE;
                                       }
```

`pence * 120 / 100` and `pence * (100 + TAX_PERCENT) / 100` give identical results. The second one says what it is.

**Introduce a parameter object.** A method with a long list of parameters that always travel together (`quote(int grams, boolean express, String country)`) is easy to call wrongly (swap two ints) and painful to extend. Group them into a record:

```java
record Order(int grams, boolean express, String country) {}

String quote(Order order) { ... }
```

Callers now say `quote(new Order(750, true, "UK"))`, each value has a name, and adding a field later doesn't change every call.

**Remove duplication.** The same logic in two places must be changed in two places, and sooner or later someone changes only one.

### Small steps

Each refactoring above is a **sequence of tiny, checkable steps**: add the new method alongside the old, run the tests, switch one caller over, run the tests, delete the old code, run the tests. Your IDE can do many of these automatically (rename, extract method) and safely; use that.

## Worked examples

### Example 1: extracting without changing behaviour

*Task: extract the UK price into `domesticCost(int grams)`.*

**Step 1 — Run the tests: green.**

**Step 2 — Copy the UK branch into a new method** `int domesticCost(int grams)`, returning the price.

**Step 3 — Replace the original branch with a call:** `cost = domesticCost(grams)`.

**Step 4 — Run the tests: still green.** Nothing observable changed.

### Example 2: spotting a hidden behaviour change

*Task: while extracting, you change `grams <= 500` to `grams < 500` "to tidy up". What happens?*

**Step 1 — Run the tests.** The check for exactly 500 grams fails.

**Step 2 — That's the safety net working:** the "tidy-up" changed behaviour at the boundary.

**Step 3 — Undo it.** If the new boundary is wanted, it's a separate, deliberate change with its own test.

## Where this is used

- **Every long-lived codebase** is constantly refactored; "leave the code better than you found it" is a team norm.
- **Before adding a feature** to messy code, you refactor first to make room for it.
- **IDE refactoring tools** (rename, extract, move) rely on the same discipline.

## Common mistakes

:::mistake{id=MC151}
**Refactoring without tests.** There's no way to know the behaviour didn't change. Write tests first.
:::

:::mistake{id=MC152}
**Changing behaviour and structure in one step.** When something breaks, you can't tell which change caused it. Do them separately.
:::

:::mistake{id=MC153}
**One giant refactor.** A big rewrite that you only test at the end is almost impossible to debug. Take small steps and run the tests after each.
:::

## Practice

::exercise{id=j4-l4.2-modify-extract}

::exercise{id=j4-l4.2-modify-constants}

::exercise{id=j4-l4.2-write-parameter-object}

::exercise{id=j4-l4.2-explain-safe}

## Further reading

- **McCauley et al. (2008)** `[R16]` on debugging: when a refactor breaks a test, the failing test is your reproduction.
- **Qian & Lehman (2017)** `[R8]` on how novices structure programs, and why long methods are hard to follow.

## How you'll be assessed

- The **modify** and **write** exercises check that your refactored code gives exactly the same answers as the original **and** has the requested structure (*modification, implementation*).
- The **explain** exercise checks that you can say why tests come first and how to refactor in small steps (*explanation*).
''' + FOOT)

ex = Exercises("j4-l4.2")
EXT_BAD = 'int shippingCost(int grams, boolean express, String country) {\n    int cost;\n    if (country.equals("UK")) {\n        if (grams <= 500) {\n            cost = 300;\n        } else if (grams <= 2000) {\n            cost = 450;\n        } else {\n            cost = 450 + ((grams - 2000 + 999) / 1000) * 100;\n        }\n    } else {\n        if (grams <= 500) {\n            cost = 800;\n        } else if (grams <= 2000) {\n            cost = 1200;\n        } else {\n            cost = 1200 + ((grams - 2000 + 999) / 1000) * 250;\n        }\n    }\n    if (express) {\n        cost = cost * 2;\n    }\n    return cost;\n}'
EXT_OK = 'int shippingCost(int grams, boolean express, String country) {\n    int cost = country.equals("UK") ? domesticCost(grams) : internationalCost(grams);\n    return express ? cost * 2 : cost;\n}\n\nint domesticCost(int grams) {\n    if (grams <= 500) {\n        return 300;\n    }\n    if (grams <= 2000) {\n        return 450;\n    }\n    return 450 + extraKilos(grams) * 100;\n}\n\nint internationalCost(int grams) {\n    if (grams <= 500) {\n        return 800;\n    }\n    if (grams <= 2000) {\n        return 1200;\n    }\n    return 1200 + extraKilos(grams) * 250;\n}\n\nint extraKilos(int grams) {\n    return (grams - 2000 + 999) / 1000;\n}'
SHIP_V = [("shippingCost", [250, False, "UK"]), ("shippingCost", [1500, True, "FR"]), ("shippingCost", [3500, False, "UK"])]
SHIP_H = [("shippingCost", [500, False, "UK"]), ("shippingCost", [501, False, "UK"]), ("shippingCost", [2000, False, "FR"]), ("shippingCost", [2001, False, "FR"]), ("shippingCost", [2000, True, "UK"]), ("shippingCost", [5000, True, "US"]), ("shippingCost", [3000, False, "UK"])]
ex.method("modify", "j4-l4.2-modify-extract", "Extract the pricing", ["o2"], ["J4.08"], ["MOD"],
    "`shippingCost` works, and its tests pass, but it's one long method with a repeated \"round up to whole kilos\" calculation. **Refactor** it without changing a single answer: extract `int domesticCost(int grams)` and `int internationalCost(int grams)` (the price before any express charge), and extract the repeated kilos calculation into a method of your choice. `shippingCost` should become a short method that calls them. The checks are the same ones that pass now, plus a check that the two new methods exist.",
    [("shippingCost", [("grams", "int"), ("express", "boolean"), ("country", "String")], "int")], {"shippingCost": ship}, SHIP_V, SHIP_H,
    EXT_BAD, EXT_OK,
    {"changes-a-boundary": EXT_OK.replace("if (grams <= 500) {\n        return 300;", "if (grams < 500) {\n        return 300;"),
     "forgets-express": EXT_OK.replace("return express ? cost * 2 : cost;", "return cost;")},
    ("Move the UK branch into domesticCost and the other branch into internationalCost, keep their numbers exactly, then run the checks.", "int cost = country.equals(\"UK\") ? domesticCost(grams) : internationalCost(grams); return express ? cost * 2 : cost;"),
    source_tests=[("domesticCost is extracted", ["int domesticCost("], None), ("internationalCost is extracted", ["int internationalCost("], None)],
    difficulty=3)
CON_BAD = 'int total(int pence) {\n    int taxed = pence * 120 / 100;\n    if (pence >= 5000) {\n        return taxed;\n    }\n    return taxed + 499;\n}'
CON_OK = 'static final int TAX_PERCENT = 20;\nstatic final int FREE_DELIVERY_FROM = 5000;\nstatic final int DELIVERY_FEE = 499;\n\nint total(int pence) {\n    int taxed = pence * (100 + TAX_PERCENT) / 100;\n    if (pence >= FREE_DELIVERY_FROM) {\n        return taxed;\n    }\n    return taxed + DELIVERY_FEE;\n}'
def total_fn(p):
    t = p * 120 // 100
    return t if p >= 5000 else t + 499
ex.method("modify", "j4-l4.2-modify-constants", "Name the magic numbers", ["o2"], ["J4.08"], ["MOD"],
    "`total` has three unexplained numbers. Replace them with **named constants**, exactly named `TAX_PERCENT` (20), `FREE_DELIVERY_FROM` (5000 pence) and `DELIVERY_FEE` (499 pence), without changing any result. Write the tax as `pence * (100 + TAX_PERCENT) / 100`.",
    [("total", [("pence", "int")], "int")], {"total": total_fn},
    [("total", [1000]), ("total", [5000]), ("total", [4999])],
    [("total", [0]), ("total", [1]), ("total", [10000]), ("total", [4000]), ("total", [5001]), ("total", [99])],
    CON_BAD, CON_OK,
    {"wrong-delivery-fee": CON_OK.replace("DELIVERY_FEE = 499", "DELIVERY_FEE = 500"),
     "free-delivery-from-5001": CON_OK.replace("pence >= FREE_DELIVERY_FROM", "pence > FREE_DELIVERY_FROM")},
    ("Declare the three constants as static final ints, then use them in the formula and the condition in place of the numbers.", "static final int TAX_PERCENT = 20; ... pence * (100 + TAX_PERCENT) / 100; ... pence >= FREE_DELIVERY_FROM; ... taxed + DELIVERY_FEE;"),
    source_tests=[("the three constants exist", ["TAX_PERCENT", "FREE_DELIVERY_FROM", "DELIVERY_FEE"], ["pence >= 5000", "+ 499", "* 120"])],
    difficulty=2)
def quote(g, express, country):
    c = 300 if g <= 500 else 450
    if express: c += 200
    if country != "UK": c += 500
    return f"cost={c}"
PO_DRV = '\n\nString run(int grams, boolean express, String country) {\n    return quote(new Order(grams, express, country));\n}'
PO_BAD = 'String quote(int grams, boolean express, String country) {\n    int cost = grams <= 500 ? 300 : 450;\n    if (express) {\n        cost += 200;\n    }\n    if (!country.equals("UK")) {\n        cost += 500;\n    }\n    return "cost=" + cost;\n}'
PO_OK = 'record Order(int grams, boolean express, String country) {}\n\nString quote(Order order) {\n    int cost = order.grams() <= 500 ? 300 : 450;\n    if (order.express()) {\n        cost += 200;\n    }\n    if (!order.country().equals("UK")) {\n        cost += 500;\n    }\n    return "cost=" + cost;\n}'
ex.method("write", "j4-l4.2-write-parameter-object", "Introduce a parameter object", ["o3"], ["J4.08"], ["IMPL"],
    "`quote` takes three values that always travel together. The callers (the driver `run`) have already been changed to use a parameter object: `quote(new Order(grams, express, country))`. Make that compile: create `record Order(int grams, boolean express, String country)` and change `quote` to take an `Order`, **keeping every answer the same**.",
    [("run", [("grams", "int"), ("express", "boolean"), ("country", "String")], "String")], {"run": quote},
    [("run", [250, False, "UK"]), ("run", [1000, True, "FR"]), ("run", [500, False, "UK"])],
    [("run", [501, False, "UK"]), ("run", [0, True, "UK"]), ("run", [2000, True, "US"]), ("run", [500, True, "IE"]), ("run", [3000, False, "UK"]), ("run", [10, False, "DE"])],
    PO_BAD + PO_DRV, PO_OK + PO_DRV,
    {"express-ignored": PO_OK.replace("    if (order.express()) {\n        cost += 200;\n    }\n", "") + PO_DRV,
     "swapped-fields": PO_OK.replace("record Order(int grams, boolean express, String country) {}", "record Order(int grams, boolean express, String country) {}").replace("order.grams() <= 500", "order.grams() < 500") + PO_DRV},
    ("Add the record Order with the three components in the order the driver uses, and change quote to read order.grams(), order.express() and order.country().", "record Order(int grams, boolean express, String country) {}  String quote(Order order) { ... }"),
    source_tests=[("Order is a record", ["record Order("], None), ("quote takes an Order", ["String quote(Order "], None)],
    starter_compiles=False, difficulty=3)
ex.explain("j4-l4.2-explain-safe", "Refactor safely", ["o1"], ["J4.08"],
    "A colleague wants to \"clean up\" a 300-line method that has no tests, and says: \"I'll just rewrite it and see if it still works.\" (a) What is refactoring, and why is that plan risky? (b) What should happen first? (c) Describe the cycle you would follow for each small change. (d) Why should a bug fix not be mixed into the same step as a refactor?",
    "A full answer says refactoring changes structure without changing behaviour, and rewriting an untested method risks changing behaviour without noticing; tests that pin down the current behaviour (including edge cases) should be written first; the cycle is make one small change, run the tests, and undo or fix if they fail, committing often; and mixing a bug fix with a refactor means that when a test fails you can't tell which change caused it.",
    {2: ("Defines refactoring as changing structure but not behaviour, says rewriting without tests risks silent behaviour changes, says to write tests for current behaviour first, describes a small change then run tests then undo or fix, and explains mixing changes hides which one broke something.",
         ["Refactoring is improving the structure of code without changing what it does. Rewriting an untested method is risky because I'd have no way to know if the behaviour changed. First I'd write tests that capture what it does now, including edge cases. Then for each small change I'd run the tests, and undo or fix if they fail, committing as I go. A bug fix shouldn't be mixed in, because if something breaks I wouldn't know whether the refactor or the fix caused it.",
          "(a) Changing structure not behaviour; without tests I can't tell if behaviour changed. (b) Write tests for the current behaviour. (c) Small change, run tests, undo if red. (d) Mixing makes it impossible to tell which change broke it."]),
     1: ("Answers some parts, for example says to write tests first without the cycle or the reason for separating fixes.",
         ["Write tests first.", "Change a bit at a time."]),
     0: ("Incorrect, for example says rewriting is the safest way, or that tests slow refactoring down so should be skipped.",
         ["Just rewrite it.", "Tests aren't needed for refactoring."])})
reg({"j4-l4.2": ("Refactoring under tests", ["J4.08"])},
    {"MC151": (["J4.08"], "Platform", "A method can be refactored safely without any tests"),
     "MC152": (["J4.08"], "Platform", "Fixing a bug and refactoring in the same step is efficient and safe"),
     "MC153": (["J4.08"], "R16", "One large rewrite tested at the end is the quickest safe way to improve code")})

# ====================================================================== 4.4.3
Lesson("j4-l4.3", "Code smells and code review", ["J4.09"], [
    ("o1", "Spot common code smells in a method and say how to fix each"),
    ("o2", "Write review comments that are specific, kind and actionable"),
    ("o3", "Respond to review feedback: what to accept, what to discuss, and what technical debt is"),
], ["j4-l4.2"], 55, ["R16", "R8"], r'''
## Before you start

You can refactor under tests ([Refactoring under tests](j4-l4.2)) and you know how Git branches and pull requests work ([Conflicts, remotes and undoing safely](j4-l1.2)).

**Quick check.** What's the rule for changing structure and behaviour in the same step?

<details><summary>Show the answer</summary>

Don't. Change one or the other, so that a failing test points at one cause.

</details>

## Explanation

### Code smells

A **code smell** is a pattern in code that isn't necessarily a bug but usually signals a deeper problem. Experienced developers notice them the way you notice a bad smell in a kitchen. The common ones:

| Smell | What it looks like | Why it hurts | Usual fix |
|---|---|---|---|
| **Unclear names** | `proc`, `d`, `t`, `x2` | the reader must reverse-engineer the meaning | rename |
| **Long method** | one method doing five jobs | hard to read, test and change | extract methods |
| **Duplicated code** | the same block in several places | a fix must be made everywhere, and one gets missed | extract and reuse |
| **Magic numbers** | `* 7 + 3` | no one knows what they mean or where else they matter | named constants |
| **Long parameter list** | `m(int a, int b, boolean c, int d, int e)` | easy to pass in the wrong order | parameter object |
| **Deep nesting** | `if` in `for` in `if` in `if` | hard to follow, hard to test | early returns, extract |
| **Comment that explains confusing code** | `// add the tax` above `x = y * 120 / 100` | the comment is doing the code's job, and goes stale | make the code say it |
| **God class** | one class that knows and does everything | every change touches it | split by responsibility |
| **String building with `+=` in a loop** | quadratic cost, as you saw in Stage 5 | slow on large input | `StringBuilder` |

A smell is a **prompt to look**, not an automatic order to change. A "long method" that reads clearly top to bottom may be fine. Judge by **how hard it is for the next person**.

### Technical debt

**Technical debt** is the future cost of a shortcut taken today: the quick copy-and-paste, the missing tests, the "temporary" workaround. Like financial debt, a little can be sensible (you ship on time), but it carries **interest**: every later change in that area is slower and riskier. Debt that is **recorded** (a ticket, or a comment at the shortcut that says why it's there) can be planned and repaid. Debt that nobody mentions just accumulates until the code is too fragile to change.

### Code review

In a **code review**, another developer reads your change before it's merged, usually as a **pull request**. It catches bugs, spreads knowledge of the codebase, and keeps standards consistent. It works best when:

**As the author:**
- Keep the change **small** and focused: one reason to change.
- Write a **description**: what changed, why, and how you tested it.
- Run the tests and read your own diff first.

**As the reviewer, look at:**
- **Correctness:** does it do what it claims, including edge cases and errors? (`==` on strings, null, boundaries.)
- **Tests:** is the new behaviour tested, including the awkward cases?
- **Readability:** names, structure, comments that explain *why*.
- **Risks:** security (input from outside), performance on large data, changes to other callers.

**Good review comments are:**
- **Specific:** point at the line and say what's wrong. "This is confusing" helps no one.
- **Actionable:** suggest a fix or ask a precise question. `` `code == "SAVE10"` compares references, so it can be false for equal text. Use `"SAVE10".equals(code)`. ``
- **About the code, not the person:** "this method does three things" rather than "you wrote a messy method".
- **Proportionate:** separate **must fix** (a bug) from **suggestion** (a style preference); say which.

### Responding to review

- **Assume good intent** and thank people: they spent time on your work.
- **Fix what's right** and say you did.
- **If you disagree,** explain your reasoning, politely and with evidence (a test, a measurement, a requirement). Sometimes the reviewer is missing context; sometimes you are.
- **Ask when a comment is unclear** instead of guessing.
- **Don't take it personally:** the review is of the code. And be as kind when you review others.

## Worked examples

### Example 1: smells in a method

*Task: what's wrong with this?*

```java
String proc(int[] d, String t, boolean f, int x) {
    // process the data
    String r = "";
    if (t.equals("A")) {
        for (int i = 0; i < d.length; i++) {
            r += d[i] * 7 + x;
        }
    }
    return r;
}
```

- **Unclear names:** `proc`, `d`, `t`, `f`, `r`, `x`: none says what it holds.
- **Magic number:** `7`.
- **Comment explains nothing:** "process the data" restates the method name.
- **Unused parameter:** `f` is never used.
- **`+=` on a `String` in a loop:** costs more as `d` grows.
- **Unclear contract:** what is `t`? What does `"A"` mean?

Fixes: rename everything, name the constant, delete the unused parameter, use a `StringBuilder`.

### Example 2: a good review comment

*Task: a diff has `if (code == "SAVE10")`. Write the comment.*

**Step 1 — Say where and what is wrong:** on this line, `==` compares references, not text.

**Step 2 — Say why it matters:** a code read from a form is a different object from the literal, so the discount would silently never apply.

**Step 3 — Suggest the fix, and mark its weight:** "**Must fix:** use `\"SAVE10\".equals(code)` (which also avoids a `NullPointerException` if `code` is null)."

## Where this is used

- **Every pull request** at a professional team is reviewed, and your own work will be.
- **Maintaining old code** is mostly recognising smells and deciding which to fix now.
- **Planning:** technical debt is a standard item in engineering planning.

## Common mistakes

:::mistake{id=MC154}
**Reviewing with vague comments.** "Messy" or "wrong" gives the author nothing to act on. Point at the line, say why, and suggest a fix.
:::

:::mistake{id=MC155}
**Treating every smell as a bug to fix right now.** Smells are prompts. Fix the ones that make the next change harder.
:::

:::mistake{id=MC156}
**Taking review comments personally, or accepting every one without thought.** Respond to the substance: fix what's right, discuss what isn't.
:::

## Practice

::exercise{id=j4-l4.3-explain-smells}

::exercise{id=j4-l4.3-explain-review}

::exercise{id=j4-l4.3-explain-respond}

## Further reading

- **McCauley et al. (2008)** `[R16]` on debugging: reviewers often find bugs a debugger never would, by reading closely.
- **Qian & Lehman (2017)** `[R8]` on misconceptions that careful review can catch early, such as comparing text with `==`.

## How you'll be assessed

- The **explain** exercises check that you can name and fix smells, write useful review comments, and respond to review feedback (*explanation*).
''' + FOOT)

ex = Exercises("j4-l4.3")
ex.explain("j4-l4.3-explain-smells", "Smell test", ["o1"], ["J4.09"],
    "Find **four** code smells in this method, say why each is a problem, and name the fix for each:\n\n```java\nString proc(int[] d, String t, boolean f, int x, int y) {\n    // loop through the data\n    String r = \"\";\n    if (t.equals(\"A\")) {\n        if (f) {\n            for (int i = 0; i < d.length; i++) {\n                r += d[i] * 7 + x;\n            }\n        } else {\n            for (int i = 0; i < d.length; i++) {\n                r += d[i] * 7 + y;\n            }\n        }\n    }\n    return r;\n}\n```",
    "A full answer names four smells such as unclear names (proc, d, t, f) fixed by renaming; a magic number 7 fixed by a named constant; duplicated loops fixed by choosing the offset first and looping once; deep nesting fixed by early returns or extraction; a long parameter list fixed by a parameter object or removing the flag; string += in a loop fixed by StringBuilder; or a comment that restates the code fixed by deleting or explaining why; each with a reason.",
    {2: ("Names at least four distinct smells present in the method (unclear names, magic number, duplicated loops, nesting, long parameter list or boolean flag, string += in a loop, useless comment), gives a reason for each and the matching fix.",
         ["Unclear names like proc, d, t and f: the reader can't tell what they mean, so rename them. The magic number 7: unexplained, so give it a named constant. The two loops are duplicated apart from x versus y: pick the offset first, then loop once. Deeply nested ifs make it hard to follow: use early returns. Also r += in a loop gets slower with size, so use a StringBuilder.",
          "1) Poor names, rename. 2) Magic number 7, named constant. 3) Duplicated loop, choose the value then loop once. 4) String concatenation in a loop, StringBuilder. Also the comment just repeats the code and could go."]),
     1: ("Names two or three smells, or names four without reasons or fixes.",
         ["The names are bad and there's a magic number.", "There's duplication."]),
     0: ("Incorrect, for example says the method has no problems, or lists style choices such as brace placement.",
         ["The method is fine.", "The braces are in the wrong place."])})
ex.explain("j4-l4.3-explain-review", "Write the review", ["o2"], ["J4.09"],
    "You're reviewing this pull request. The description says only \"discount\".\n\n```java\n+ public int discount(int price, String code) {\n+     if (code == \"SAVE10\") {\n+         return price - price * 10 / 100;\n+     }\n+     return price;\n+ }\n```\n\nThere are no tests in the PR. Write **three** review comments, each specific, kind and actionable. Mark each as \"must fix\" or \"suggestion\", and say what else you'd ask the author to add to the PR.",
    "A full answer writes three specific comments: == compares references so the discount may never apply and should be \"SAVE10\".equals(code) (must fix, also covers null); the 10 is an unexplained magic number and the method name says nothing about a code, so use a named constant and a clearer name (suggestion); and there are no tests for the discount, the no-discount path, a null or unknown code, so add them (must fix); and asks for a fuller description saying what changed, why and how it was tested.",
    {2: ("Gives three specific, polite, actionable comments (== on strings, magic number or naming, missing tests or null handling), labels their weight, and asks for a proper PR description.",
         ["1) Must fix: on line 2, == compares references, so code == \"SAVE10\" can be false even for equal text, and the discount would silently never apply. Please use \"SAVE10\".equals(code), which also avoids a NullPointerException. 2) Suggestion: the 10 is a magic number; a named constant like MEMBER_DISCOUNT_PERCENT would say what it means. 3) Must fix: there are no tests, so please add checks for a valid code, an unknown code, and a null code. Could you also expand the description to say what the discount is for and how you tested it?",
          "Must fix: use equals instead of == for the code string (reference comparison). Must fix: add tests covering the discount, no discount and null. Suggestion: name the 10, and the method, so a reader knows it applies a code. Please add a description of the change and testing."]),
     1: ("Gives one or two good comments, or three vague ones, or doesn't label weight or ask for a description.",
         ["Don't use ==.", "Add tests."]),
     0: ("Incorrect or unhelpful, for example says the code is bad, or only comments on formatting.",
         ["This code is bad.", "Put the brace on the next line."])})
ex.explain("j4-l4.3-explain-respond", "Reply to the reviewer", ["o3"], ["J4.09"],
    "A reviewer leaves three comments on your pull request: (1) \"`==` on strings is a bug here; use `equals`.\" (2) \"This method is too long, please split it into five.\" (your method is 12 lines and reads clearly) (3) \"Why is this loop `<=`? I think it reads one past the end.\" (you've checked, and `<=` is correct because the array is 1-based in this data format). Say how you respond to each: what you change, what you discuss, and how you word it. Then explain what **technical debt** is, and give one example of debt you might knowingly take on in this PR and how you'd record it.",
    "A full answer accepts (1) as a real bug and fixes it, thanking the reviewer; politely questions (2) by explaining the method is short and reads clearly while offering to extract a helper if they point to a specific part; answers (3) with the evidence that the format is 1-based, ideally adding a comment or a test so it's clear, rather than just changing it; defines technical debt as the future cost of a shortcut taken now, and gives an example such as a TODO to add validation or a missing test, recorded in a ticket or a TODO with the reason.",
    {2: ("Fixes (1) gratefully, politely pushes back on (2) with reasons and an offer, explains (3) with the 1-based evidence and adds a clarifying comment or test, and defines technical debt as the future cost of a shortcut with a recorded example such as a TODO or ticket.",
         ["(1) Good catch, I'll change it to equals and say so. (2) I'd explain that it's only 12 lines and reads straight through, and ask which part they'd split, offering to extract a helper if there's a clear one. (3) I'd reply that <= is right because the data format is 1-based, and add a short comment (and a test) so it's obvious. Technical debt is the future cost of a shortcut taken now, like skipping input validation to ship; I'd record it as a ticket or a TODO that says why, so it can be planned.",
          "Accept 1 and fix it. Politely discuss 2, explaining it's short and clear and asking what to split. Explain 3 with the 1-based format and add a comment. Technical debt is the cost later of a shortcut now; I'd log it in a ticket."]),
     1: ("Handles some of the comments well, or explains debt without an example of recording it.",
         ["I'd fix the == and explain the loop.", "Debt is a shortcut."]),
     0: ("Incorrect, for example says to ignore reviewers, change everything without thought, or reply rudely.",
         ["Ignore the comments I disagree with.", "Change everything they say."])})
reg({"j4-l4.3": ("Code smells and code review", ["J4.09"])},
    {"MC154": (["J4.09"], "Platform", "A review comment such as 'messy' is useful feedback"),
     "MC155": (["J4.09"], "Platform", "Every code smell must be fixed immediately"),
     "MC156": (["J4.09"], "Platform", "Review comments should be accepted or rejected without discussion")})
print("4.4 written")
