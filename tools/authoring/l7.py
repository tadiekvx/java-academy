from build import *   # ROOT defaults to stage-1

def lesson_tail(extra=""):
    return ""

# ============================ 7.1 ============================
Lesson("j1-l7.1", "Reading a program you didn't write", ["J1.15"], [
    ("o1", "Find where a program starts and list the methods it calls, in order"),
    ("o2", "Say what a program does overall, from its structure and not just its names"),
    ("o3", "Make a small change to an unfamiliar program without breaking what already works"),
], ["j1-l6.5", "j1-l5.5"], 40, ["R8", "R16"], r'''
## Before you start

You should be able to trace a program ([Variables and state](j1-l2.2)), write methods ([Parameters and return values](j1-l5.2)) and use arrays ([Arrays](j1-l6.1)).

**Quick check.** What does `clamp(15, 0, 10)` return if `clamp(v, lo, hi)` keeps `v` between `lo` and `hi`?

<details><summary>Show the answer</summary>

`10`. The value 15 is above the upper limit, so it's cut back to `hi`.

</details>

## Explanation

Until now, almost every program you ran was one you were told to write. Real work is the other way round: most of the time you open code **somebody else wrote** and have to understand it before changing it. Reading is a skill, and it can be practised.

### Start from `main`

Every program starts at `main`. Read it first, **ignoring the details of the other methods**. You're looking for the story: what gets created, what gets called, in what order, and what is printed.

```java
int clamp(int value, int low, int high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

int step(int position, int move) {
    return clamp(position + move, 0, 10);
}

void main() {
    int position = 5;
    int[] moves = {4, 3, -20, 2};
    for (int move : moves) {
        position = step(position, move);
        IO.println(position);
    }
}
```

The story in `main`: *start at 5; for each move, update the position with `step`; print it.* That already tells you what kind of program this is, before you've looked at `clamp`.

### Then read one method at a time

Pick a method that `main` calls and read just that one. Ask two questions:

1. **What goes in, and what comes out?** (the parameters and the return type)
2. **What is the rule?** (the body)

`step` takes a position and a move and returns a new position: the sum, kept between 0 and 10 by `clamp`. `clamp` returns the value limited to `low` .. `high`. You now understand all three methods without running anything.

### Trace with real values

To be sure, trace with the actual numbers, one row per loop pass:

| Move | `position + move` | After `clamp` | Printed |
|---|---|---|---|
| 4 | 9 | 9 | 9 |
| 3 | 12 | 10 | 10 |
| -20 | -10 | 0 | 0 |
| 2 | 2 | 2 | 2 |

The program prints `9`, `10`, `0`, `2`.

### Names help, but check them

Good names are clues, not guarantees. A method called `average` might actually return the total. Before you trust a name, check what the body does. When the name and the body disagree, the body is what the program really does, and the mismatch is often the bug.

### Changing code you didn't write

Once you understand a program, change it **a little at a time**:

1. **Run it first** and note what it prints, so you know what "still working" looks like.
2. **Change one thing**, in the smallest place that does the job.
3. **Run again** and compare with step 1. Anything that should have stayed the same but changed is a sign you changed too much.

Resist the urge to rewrite things you don't yet understand. A program that works, even if it's untidy, is worth more than a tidy one that doesn't.

## Worked examples

### Example 1: what does this program do?

*Task: say what this program does.*

```java
int process(int[] data) {
    int result = 0;
    for (int value : data) {
        if (value > data[0]) {
            result++;
        }
    }
    return result;
}
```

**Step 1 — Inputs and output.** It takes an array of ints and returns an int.

**Step 2 — The loop.** For each value, it compares with `data[0]`, the first element, and adds one to `result` when the value is bigger.

**Step 3 — The overall rule.** It counts **how many values are larger than the first one**. The name `process` told us nothing; the body did.

**Step 4 — Test the guess with a small case.** For `{3, 5, 1, 7}`: 5 > 3 yes, 1 > 3 no, 7 > 3 yes, and 3 > 3 no, so 2.

### Example 2: adding a feature to code you've just read

*Task: `summary` always says "items". Change it to say "item" when there is exactly one.*

```java
int total(int[] prices) {
    int sum = 0;
    for (int price : prices) {
        sum += price;
    }
    return sum;
}

String summary(int[] prices) {
    return prices.length + " items, total " + total(prices);
}
```

**Step 1 — Note the current behaviour.** `{10, 20, 30}` gives `3 items, total 60`.

**Step 2 — Find the smallest place to change.** Only `summary` builds the sentence, so only `summary` changes. `total` stays untouched.

**Step 3 — Make the change.**

```java
String summary(int[] prices) {
    String word = prices.length == 1 ? "item" : "items";
    return prices.length + " " + word + ", total " + total(prices);
}
```

**Step 4 — Check old and new.** `{10, 20, 30}` still gives `3 items, total 60`; `{5}` now gives `1 item, total 5`.

## Predict, then run

::exercise{id=j1-l7.1-predict-program}

## Where this is used

- **Joining a team:** your first weeks are spent reading code that already exists.
- **Fixing bugs:** you can't fix what you haven't understood, and the bug is usually in code someone else wrote, or you wrote last year.
- **Code review:** reviewing a colleague's change is reading code with the question "would this break anything?"

## Common mistakes

:::mistake{id=MC16}
**Trusting a method's name instead of its body.** A method called `total` that actually keeps only the largest value will fool you if you only read its name. Always check what the body does.
:::

:::mistake{id=MC17}
**Rewriting instead of reading.** Replacing code you don't understand with code you do is tempting, but you lose behaviour you didn't know the old code had. Understand first, then change the smallest part.
:::

## Practice

::exercise{id=j1-l7.1-explain-program}

::exercise{id=j1-l7.1-modify-summary}

## Further reading

- **"Students' misconceptions and other difficulties in introductory programming"** (Qian & Lehman, 2017) `[R8]` reviews research on novices' trouble with tracing and reading code, which this lesson practises.
- **Debugging and reading code** are discussed in the course's own method notes `[R16]`.

## How you'll be assessed

- The **predict** exercise checks that you can trace a program built from several methods (*identifying mistakes*).
- The **explain** exercise checks that you can say what a program does from its body and not its name (*explanation*).
- The **modify** exercise checks that you can add a feature without breaking the existing behaviour (*modification*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l7.1")
ex.predict("j1-l7.1-predict-program", "Trace a program of three methods", ["o1", "o2"], ["J1.15"],
    "Without running it, work out what this program prints. Trace the position after each move.",
    '''int clamp(int value, int low, int high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

int step(int position, int move) {
    return clamp(position + move, 0, 10);
}

void main() {
    int position = 3;
    int[] moves = {5, 4, -9, -4, 2};
    for (int move : moves) {
        position = step(position, move);
        IO.println(position);
    }
}''', "8\n10\n1\n0\n2",
    ("Make a table: for each move, work out position + move, then apply clamp's 0 to 10 limits.", "3+5=8; 8+4=12→10; 10-9=1; 1-4=-3→0; 0+2=2."),
    difficulty=2)
ex.explain("j1-l7.1-explain-program", "What does this really do?", ["o2"], ["J1.15"],
    "A colleague wrote this method and called it `process`:\n\n```java\nint process(int[] data) {\n    int result = 0;\n    for (int value : data) {\n        if (value > data[0]) {\n            result++;\n        }\n    }\n    return result;\n}\n```\n\nSay in plain words what it returns, and use the array `{4, 9, 2, 9, 4}` to show that you are right. Then suggest a better name.",
    "A full answer says it counts how many values are larger than the first element, traces {4,9,2,9,4} to 2 (the two 9s), and suggests a name such as countLargerThanFirst.",
    {2: ("Says it counts the values greater than the first element, gets 2 for the example (the two 9s), and gives a name that says that.",
         ["It counts how many values are bigger than the first one. For {4, 9, 2, 9, 4} the first is 4, and only the two 9s are greater, so it returns 2. A better name would be countLargerThanFirst.",
          "It returns the number of elements strictly greater than data[0]. With 4 first, the 9 and the other 9 count, 2 does not, and the last 4 does not, so 2. Name: countAboveFirst."]),
     1: ("Gets the idea of comparing with the first element, or traces the example, but not both, or the answer for the example is wrong.",
         ["It compares the values with the first one and counts some.", "It returns 2 for that array."]),
     0: ("Incorrect, for example says it adds up the values or finds the largest.",
         ["It returns the sum of the array.", "It finds the biggest number."])})
ex.method("modify", "j1-l7.1-modify-summary", "Say 'item' for one", ["o3"], ["J1.15"], ["MOD"],
    "`summary` describes a basket. Change it so that it says `1 item` (singular) when there is exactly one price, and keeps saying `items` otherwise (including for `0 items`). Don't change `total`.\n\nFor example `{10, 20, 30}` gives `3 items, total 60`, and `{5}` gives `1 item, total 5`.",
    [("summary", [("prices", "int[]")], "String")],
    {"summary": lambda p: f"{len(p)} {'item' if len(p) == 1 else 'items'}, total {sum(p)}"},
    [("summary", [[10, 20, 30]]), ("summary", [[5]]), ("summary", [[]])],
    [("summary", [[1, 1]]), ("summary", [[100]]), ("summary", [[-3]]), ("summary", [[2, 4, 6, 8, 10]]), ("summary", [[0]])],
    '''int total(int[] prices) {
    int sum = 0;
    for (int price : prices) {
        sum += price;
    }
    return sum;
}

String summary(int[] prices) {
    return prices.length + " items, total " + total(prices);
}''',
    '''int total(int[] prices) {
    int sum = 0;
    for (int price : prices) {
        sum += price;
    }
    return sum;
}

String summary(int[] prices) {
    String word = prices.length == 1 ? "item" : "items";
    return prices.length + " " + word + ", total " + total(prices);
}''',
    {"singular-for-zero": '''int total(int[] prices) {
    int sum = 0;
    for (int price : prices) { sum += price; }
    return sum;
}

String summary(int[] prices) {
    String word = prices.length > 1 ? "items" : "item";
    return prices.length + " " + word + ", total " + total(prices);
}''',
     "dropped-total": '''String summary(int[] prices) {
    String word = prices.length == 1 ? "item" : "items";
    return prices.length + " " + word;
}'''},
    ("Only summary builds the sentence, so only summary should change. Pick the word first.", "A conditional expression: prices.length == 1 ? \"item\" : \"items\"."),
    difficulty=2)

# ============================ 7.2 ============================
Lesson("j1-l7.2", "From requirements to a plan", ["J1.16", "J1.09"], [
    ("o1", "Restate a requirement in your own words, with its inputs, outputs and rules"),
    ("o2", "List test cases, including edges, before writing code"),
    ("o3", "Break the job into methods and build them one at a time"),
], ["j1-l7.1", "j1-l5.4"], 45, ["R8", "R16"], r'''
## Before you start

You should be able to split a problem into methods ([Decomposing a problem](j1-l5.4)) and read tests as a description ([Reading tests](j1-l5.5)).

**Quick check.** What is the difference between a parameter and a return value?

<details><summary>Show the answer</summary>

A parameter is a value a method receives; a return value is the result it hands back.

</details>

## Explanation

So far each exercise came with a clear method name, signature and tests. Real requests don't: someone says what they want in a sentence or two, and **you** decide what to build. Most beginners' trouble here isn't Java. It's starting to type before they know what they're making.

### Step 1: restate the requirement

Take this request:

> *A car park gives the first 30 minutes free. After that it charges 2 pounds for each hour, or part of an hour. The most it ever charges for a day is 15 pounds. Write a program that works out the fee.*

Restate it as plain facts:

- **Input:** how long the car stayed, in minutes (a whole number).
- **Output:** the fee in whole pounds.
- **Rules:** up to 30 minutes costs 0; after 30 minutes, 2 pounds per hour **or part of one**; never more than 15.

Writing it down shows what is *missing*. Does 30 minutes exactly cost nothing? (Yes: "first 30 minutes free" means up to and including 30.) What if the input is negative? (We'll decide it won't happen, and say so.)

### Step 2: list cases before code

Work out what the answer should be for chosen inputs, **by hand**:

| Minutes | Reasoning | Fee |
|---|---|---|
| 0 | free | 0 |
| 30 | still free | 0 |
| 31 | 1 minute over: one started hour | 2 |
| 90 | exactly 60 over: one hour | 2 |
| 91 | 61 over: two started hours | 4 |
| 600 | 570 over: 10 started hours = 20, capped | 15 |

The tricky ones are at the **edges**: 30 and 31 (where charging starts), 90 and 91 (where a new hour starts), and 600 (where the cap bites). This table is both your plan and your test.

### Step 3: decide the steps

Think about how you'd do it by hand:

1. If minutes is 30 or less, the fee is 0.
2. Otherwise take the minutes past 30, and count **started** hours: divide by 60, rounding **up**.
3. Multiply by 2.
4. If that is more than 15, the fee is 15.

Step 2 is the tricky one. Integer division rounds *down*, so to round up by 60 you can add 59 first: `(over + 59) / 60`. Check: 1 over → 60/60 = 1; 60 over → 119/60 = 1; 61 over → 120/60 = 2.

### Step 4: build in small pieces

Put the rule in a method with a clear name, and a thin `main` around it:

```java runnable
int parkingFee(int minutes) {
    if (minutes <= 30) {
        return 0;
    }
    int over = minutes - 30;
    int hours = (over + 59) / 60;
    return Math.min(hours * 2, 15);
}

void main() {
    int[] minutes = {0, 30, 31, 90, 91, 600};
    for (int m : minutes) {
        IO.println(m + " minutes: " + parkingFee(m));
    }
}
```

The output is `0, 0, 2, 2, 4, 15`, matching the table. Because you worked out the table first, you can tell straight away that the code is right.

### When it's more than one method

If the request is bigger (say, reading a number from the user, working out a fee, and printing a nice message), give each job its own method: one to read, one to calculate, one to format. Build and check the calculating method **first**, on its own, with the table, before connecting it to input and output.

## Worked examples

### Example 1: from a sentence to a plan

*Task: "Tell me how many whole weeks and leftover days there are in a number of days."*

**Step 1 — Restate.** Input: a number of days. Output: weeks and days left over. Rules: 7 days per week.

**Step 2 — Cases.** 0 days → 0 weeks 0 days. 6 → 0 and 6. 7 → 1 and 0. 15 → 2 and 1.

**Step 3 — Steps.** weeks = days / 7 (integer division); rest = days % 7.

**Step 4 — Code.**

```java runnable
void main() {
    int days = 15;
    int weeks = days / 7;
    int rest = days % 7;
    IO.println(weeks + " weeks and " + rest + " days");
}
```

### Example 2: a plan reveals a missing decision

*Task: "Average of the marks."*

**Step 1 — Ask the awkward question while planning.** What if there are no marks? Dividing by zero would crash an `int` calculation, and a `double` would give `NaN` (not-a-number).

**Step 2 — Decide, and write the decision down.** "With no marks the average is 0." Now the empty case is a row in the table.

**Step 3 — Build with that rule included.** It costs one `if` in the code, and a plan that skipped it would have cost a bug.

## Where this is used

- **Every ticket or feature request** starts as a few vague sentences, and the first job is turning them into inputs, outputs and rules.
- **Agreeing with a customer** is easier with a table of examples than with a paragraph.
- **Your plan is your test:** the table you write first becomes the checks you run later.

## Common mistakes

:::mistake{id=MC18}
**Coding before restating.** Starting to type before you know the inputs, outputs and rules usually means rewriting halfway.
:::

:::mistake{id=MC19}
**Testing only the typical case.** A method that works for 45 minutes can still be wrong at 30, 31 or 600. The edge rows are where the bugs are.
:::

:::mistake{id=MC20}
**Building everything at once.** Write and check the calculation on its own before you connect input and output; a bug is then in one place, not three.
:::

## Practice

::exercise{id=j1-l7.2-explain-plan}

::exercise{id=j1-l7.2-write-fee}

::exercise{id=j1-l7.2-write-program}

## Further reading

- **"Students' misconceptions and other difficulties in introductory programming"** (Qian & Lehman, 2017) `[R8]` covers problem-solving difficulties, not just syntax.
- The course's own notes on debugging and planning `[R16]`.

## How you'll be assessed

- The **explain** exercise checks that you can plan a program from a written request (*explanation*).
- The **write** exercises check that you can turn a plan into working code, including a whole program that reads input (*implementation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l7.2")
def fee(m):
    if m <= 30: return 0
    return min(((m - 30 + 59) // 60) * 2, 15)
ex.explain("j1-l7.2-explain-plan", "Plan before you code", ["o1", "o2"], ["J1.16"],
    "A cinema asks for a program: *\"Tickets cost 8 pounds. Groups of 4 or more people get a discount of 1 pound off each ticket. Work out the total price for a group.\"*\n\nWithout writing any Java, write the plan: (a) the input and output, (b) the rules, (c) at least four test cases with the answer for each, including the edge where the discount starts, and (d) one thing the request does not say that you would ask about.",
    "A full answer gives input = number of people, output = total price, rules (8 each; 7 each from 4 people), cases such as 1 -> 8, 3 -> 24, 4 -> 28, 10 -> 70 with the edge at 3 and 4, and a sensible question such as what happens for 0 or whether the discount applies to the whole group.",
    {2: ("States input and output, the rule, at least four correct cases including 3 and 4 at the edge (3 people cost 24, 4 people cost 28), and one reasonable open question.",
         ["Input: the number of people. Output: total price. Rule: 8 pounds each, but if there are 4 or more, 7 pounds each. Cases: 1 -> 8, 3 -> 24, 4 -> 28, 10 -> 70. I'd ask what happens for 0 people, or whether a group means exactly 4 or more.",
          "In: group size. Out: total. 8 per ticket, 7 per ticket from 4 upwards. 0 -> 0, 3 -> 24, 4 -> 28, 5 -> 35. Question: does the discount apply to everyone in the group or only extra tickets?"]),
     1: ("Has some of the plan, but misses the edge at 3 and 4, has an arithmetic error, or asks no question.",
         ["Number of people in, price out. 8 each, 7 each for 4 or more.", "1 -> 8, 4 -> 28, 10 -> 70."]),
     0: ("Incorrect or missing the main rule, for example applies the discount to groups of 3 or applies 1 pound off the total.",
         ["Just write the code and see.", "Total is 8 minus 1 for groups."])})
ex.method("write", "j1-l7.2-write-fee", "The car park fee", ["o3"], ["J1.16", "J1.09"], ["IMPL"],
    "Write `parkingFee(int minutes)` for the car park described in the lesson: the first 30 minutes are free; after that 2 pounds for each hour or part of an hour; never more than 15. It returns the fee in whole pounds.\n\nUse the table from the lesson as your checks: 0 and 30 give 0, 31 and 90 give 2, 91 gives 4, 600 gives 15.",
    [("parkingFee", [("minutes", "int")], "int")], {"parkingFee": fee},
    [("parkingFee", [30]), ("parkingFee", [31]), ("parkingFee", [91])],
    [("parkingFee", [0]), ("parkingFee", [90]), ("parkingFee", [150]), ("parkingFee", [270]), ("parkingFee", [271]), ("parkingFee", [600])],
    'int parkingFee(int minutes) {\n    return 0; // replace this\n}',
    'int parkingFee(int minutes) {\n    if (minutes <= 30) {\n        return 0;\n    }\n    int over = minutes - 30;\n    int hours = (over + 59) / 60;\n    return Math.min(hours * 2, 15);\n}',
    {"rounds-down": 'int parkingFee(int minutes) {\n    if (minutes <= 30) return 0;\n    return Math.min((minutes - 30) / 60 * 2, 15);\n}',
     "no-cap": 'int parkingFee(int minutes) {\n    if (minutes <= 30) return 0;\n    return (minutes - 30 + 59) / 60 * 2;\n}',
     "free-hour": 'int parkingFee(int minutes) {\n    if (minutes <= 60) return 0;\n    return Math.min((minutes - 60 + 59) / 60 * 2, 15);\n}'},
    ("Handle the free case first. Then work out the minutes over 30 and round the hours up with (over + 59) / 60.", "if minutes <= 30 return 0; hours = (minutes - 30 + 59) / 60; return Math.min(hours * 2, 15);"),
    difficulty=3)
def prog(stdin):
    return ["Fee: %d\n" % fee(int(stdin.strip()))]
ex.io("write", "j1-l7.2-write-program", "The whole car park program", ["o3"], ["J1.16", "J1.09"], ["IMPL"],
    "Write a **whole program**. It asks `Minutes parked: ` (using `IO.readln`), reads the number, works out the fee by the same rules as before (free for 30 minutes, 2 pounds per hour or part of an hour, capped at 15), and prints `Fee: ` followed by the number.\n\nFor example, if the person types `91`, the program prints `Fee: 4`.\n\nBuild the calculation as its own method first.",
    prog, [("91 minutes", "91\n"), ("free", "20\n"), ("capped", "600\n")],
    [("30 minutes", "30\n"), ("31 minutes", "31\n"), ("90", "90\n"), ("271", "271\n"), ("0", "0\n")],
    'void main() {\n    // your program here\n}',
    'int parkingFee(int minutes) {\n    if (minutes <= 30) {\n        return 0;\n    }\n    int hours = (minutes - 30 + 59) / 60;\n    return Math.min(hours * 2, 15);\n}\n\nvoid main() {\n    int minutes = Integer.parseInt(IO.readln("Minutes parked: ").trim());\n    IO.println("Fee: " + parkingFee(minutes));\n}',
    {"no-cap": 'void main() {\n    int minutes = Integer.parseInt(IO.readln("Minutes parked: ").trim());\n    int fee = minutes <= 30 ? 0 : (minutes - 30 + 59) / 60 * 2;\n    IO.println("Fee: " + fee);\n}',
     "wrong-label": 'void main() {\n    int minutes = Integer.parseInt(IO.readln("Minutes parked: ").trim());\n    int fee = minutes <= 30 ? 0 : Math.min((minutes - 30 + 59) / 60 * 2, 15);\n    IO.println("Cost: " + fee);\n}'},
    ("Reuse your parkingFee idea as a method, then main only reads, calls, and prints.", "int minutes = Integer.parseInt(IO.readln(\"Minutes parked: \").trim());"),
    contains=True, difficulty=3)

# ============================ 7.3 ============================
Lesson("j1-l7.3", "Writing your own checks", ["J1.14"], [
    ("o1", "Write a small check helper that reports PASS or FAIL with expected and actual values"),
    ("o2", "Choose edge and boundary cases for a rule"),
    ("o3", "Notice when a check itself is wrong, and decide whether the code or the check needs fixing"),
], ["j1-l7.2"], 40, ["R8", "R16"], r'''
## Before you start

You should have read tests as a description of behaviour ([Reading tests](j1-l5.5)) and planned with a table of cases ([From requirements to a plan](j1-l7.2)).

**Quick check.** Why is a table of cases worth writing before the code?

<details><summary>Show the answer</summary>

It tells you what "correct" means before you start, and the same table becomes the checks you run afterwards.

</details>

## Explanation

In [Reading tests](j1-l5.5) you saw the course's tests from the outside. In real projects you write them yourself. This lesson is about writing your own checks, and about the fact that **a check can be wrong too**.

### A check helper

Printing results by eye doesn't scale; a helper does the comparing for you:

```java runnable
int discount(int age) {
    if (age < 12) return 50;
    if (age >= 65) return 30;
    return 0;
}

void check(String name, int expected, int actual) {
    if (expected == actual) {
        IO.println("PASS " + name);
    } else {
        IO.println("FAIL " + name + ": expected " + expected + " but got " + actual);
    }
}

void main() {
    check("child", 50, discount(5));
    check("adult", 0, discount(30));
    check("senior", 30, discount(70));
}
```

A failure message with the name, the expected value and the actual value is worth the extra words: it tells you where to look without a debugger.

### Choose cases on purpose

The rule above is "under 12 get 50% off; 65 and over get 30% off; everyone else 0". Which ages should you test?

| Why | Ages |
|---|---|
| A typical value in each group | 5, 30, 70 |
| **Either side of each boundary** | 11 and 12 (child ends); 64 and 65 (senior starts) |
| The extremes | 0 |

The boundary pairs are the most valuable. The two classic mistakes, `<` where `<=` was meant and the reverse, only show up when you test *exactly at* the boundary.

### A check can be wrong

Suppose you add:

```java
check("boundary 12", 50, discount(12));
```

It fails: `expected 50 but got 0`. Is the code wrong? Go back to the rule: *under* 12 gets the discount, so 12 doesn't. The **check** was wrong, because its expected value came from a careless reading of the rule. The code is right.

When a check fails, decide which is at fault by going back to the **requirement**, not to the code. Whichever disagrees with the requirement gets fixed.

### Two helpers to avoid mistakes

- **Print the name.** `check("senior 65", 30, discount(65))` beats `check("test3", ...)`.
- **Compare strings with `.equals`**, not `==`. For text you'd write `expected.equals(actual)`.

### Tests prove less than they seem to

A full set of passing checks says the cases you thought of work. It doesn't say the method is correct for every input. So when you find a bug some other way, add a check for it first, make sure it fails, then fix the code and watch it pass. That way, the bug can't quietly return.

## Worked examples

### Example 1: a check helper for text

*Task: write `checkText` that reports PASS or FAIL for two strings.*

**Step 1 — Decide the comparison.** Strings are compared with `.equals`.

**Step 2 — Write the messages** in the same shape as the numbers: `FAIL name: expected "a" but got "b"`, with quotation marks so spaces are visible.

**Step 3 — Code.**

```java runnable
void checkText(String name, String expected, String actual) {
    if (expected.equals(actual)) {
        IO.println("PASS " + name);
    } else {
        IO.println("FAIL " + name + ": expected \"" + expected + "\" but got \"" + actual + "\"");
    }
}

void main() {
    checkText("same", "cat", "cat");
    checkText("different", "cat", "dog");
}
```

### Example 2: deciding who is wrong

*Task: `isLeapYear(1900)` returns false, but the check expects true. Who is wrong?*

**Step 1 — Return to the requirement.** A year is a leap year if divisible by 4, except century years, which must be divisible by 400.

**Step 2 — Apply it by hand.** 1900 is divisible by 4 and by 100 but not by 400, so it isn't a leap year.

**Step 3 — Conclusion.** The code is right and the check is wrong. Fix the check's expected value to `false`.

## Predict, then run

::exercise{id=j1-l7.3-predict-checks}

## Where this is used

- **Professional codebases** contain as much test code as ordinary code.
- **Fixing a bug** the proper way starts with a check that fails.
- **Reviewing** someone's tests is partly asking "is this expected value actually right?"

## Common mistakes

:::mistake{id=MC21}
**Writing the expected value from what the code does.** If you copy whatever the code returns into the check, the check can never fail. Work out the expected value from the requirement, before you run the code.
:::

:::mistake{id=MC22}
**Only testing the middle of a range.** Check 11 and 12, not just 5 and 30.
:::

:::mistake{id=MC23}
**Assuming a failing check means broken code.** Go back to the requirement and decide which is wrong.
:::

## Practice

::exercise{id=j1-l7.3-write-check}

::exercise{id=j1-l7.3-debug-check}

::exercise{id=j1-l7.3-explain-edges}

## Further reading

- **"Students' misconceptions and other difficulties in introductory programming"** (Qian & Lehman, 2017) `[R8]`.
- The course's debugging notes `[R16]`, which cover reproducing a bug before fixing it.

## How you'll be assessed

- The **predict** exercise checks that you can read checks and tell a wrong check from a wrong method (*identifying mistakes*).
- The **write** and **debug** exercises check that you can write and fix a check helper (*implementation, debugging*).
- The **explain** exercise checks that you can choose edge and boundary cases (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l7.3")
ex.predict("j1-l7.3-predict-checks", "Which checks fail?", ["o3"], ["J1.14"],
    "Work out exactly what this program prints. Then decide, for each FAIL, whether the method or the check is at fault. (The rule: under 12 gets 50, 65 and over gets 30, otherwise 0.)",
    '''int discount(int age) {
    if (age < 12) return 50;
    if (age >= 65) return 30;
    return 0;
}

void check(String name, int expected, int actual) {
    if (expected == actual) {
        IO.println("PASS " + name);
    } else {
        IO.println("FAIL " + name + ": expected " + expected + " but got " + actual);
    }
}

void main() {
    check("child", 50, discount(5));
    check("boundary 12", 50, discount(12));
    check("adult", 0, discount(30));
    check("senior", 30, discount(65));
    check("boundary 64", 30, discount(64));
}''',
    "PASS child\nFAIL boundary 12: expected 50 but got 0\nPASS adult\nPASS senior\nFAIL boundary 64: expected 30 but got 0",
    ("Work out each discount by hand: 12 is not under 12, and 64 is not 65 or over.", "Both failing checks have wrong expected values: the method follows the rule."),
    difficulty=2)

def check_msg(name, expected, actual):
    return f"PASS {name}" if expected == actual else f"FAIL {name}: expected {expected} but got {actual}"
check_cases_v = [("check", ["sum", 5, 5]), ("check", ["sum", 5, 6]), ("check", ["zero", 0, 0])]
check_cases_h = [("check", ["negative", -3, -3]), ("check", ["big", 1000, 999]), ("check", ["a b", 7, 8]), ("check", ["same", 42, 42]), ("check", ["swap", 10, 3])]
ex.method("write", "j1-l7.3-write-check", "Your own check helper", ["o1"], ["J1.14"], ["IMPL"],
    "Write `check(String name, int expected, int actual)` so that it **returns** a `String`:\n\n- if `expected` equals `actual`: `PASS ` followed by the name;\n- otherwise: `FAIL ` followed by the name, then `: expected `, the expected value, ` but got `, and the actual value.\n\nFor example, `check(\"sum\", 5, 6)` returns `FAIL sum: expected 5 but got 6`.",
    [("check", [("name", "String"), ("expected", "int"), ("actual", "int")], "String")], {"check": check_msg},
    check_cases_v, check_cases_h,
    'String check(String name, int expected, int actual) {\n    return ""; // replace this\n}',
    'String check(String name, int expected, int actual) {\n    if (expected == actual) {\n        return "PASS " + name;\n    }\n    return "FAIL " + name + ": expected " + expected + " but got " + actual;\n}',
    {"swapped-values": 'String check(String name, int expected, int actual) {\n    if (expected == actual) return "PASS " + name;\n    return "FAIL " + name + ": expected " + actual + " but got " + expected;\n}',
     "missing-colon": 'String check(String name, int expected, int actual) {\n    if (expected == actual) return "PASS " + name;\n    return "FAIL " + name + " expected " + expected + " but got " + actual;\n}'},
    ("Compare first. For the failing case, join the pieces carefully, with the exact spaces and colon.", "if (expected == actual) return \"PASS \" + name; return \"FAIL \" + name + \": expected \" + expected + \" but got \" + actual;"),
    difficulty=2)
ex.method("debug", "j1-l7.3-debug-check", "A check that cannot be trusted", ["o3", "o1"], ["J1.14"], ["DEBUG"],
    "This check helper has two bugs, so it reports wrong results. Find them and fix them so that `check(\"sum\", 5, 6)` returns `FAIL sum: expected 5 but got 6` and `check(\"sum\", 5, 5)` returns `PASS sum`.",
    [("check", [("name", "String"), ("expected", "int"), ("actual", "int")], "String")], {"check": check_msg},
    check_cases_v, check_cases_h,
    'String check(String name, int expected, int actual) {\n    if (expected != actual) {\n        return "PASS " + name;\n    }\n    return "FAIL " + name + ": expected " + actual + " but got " + expected;\n}',
    'String check(String name, int expected, int actual) {\n    if (expected == actual) {\n        return "PASS " + name;\n    }\n    return "FAIL " + name + ": expected " + expected + " but got " + actual;\n}',
    {"fixed-one-bug": 'String check(String name, int expected, int actual) {\n    if (expected == actual) {\n        return "PASS " + name;\n    }\n    return "FAIL " + name + ": expected " + actual + " but got " + expected;\n}'},
    ("There are two separate problems: check the condition, then check the order of the numbers in the message.", "The comparison should be == for PASS, and expected and actual are swapped in the FAIL message."),
    difficulty=2)
ex.explain("j1-l7.3-explain-edges", "Choose the edge cases", ["o2"], ["J1.14"],
    "A cinema sells tickets by age: under 5 is free, 5 to 17 is child, 18 to 64 is adult, and 65 and over is senior. List the ages you would test, and say why you picked each one. You should include more than one age in each group.",
    "A full answer includes the boundaries on both sides: 4 and 5, 17 and 18, 64 and 65, plus a typical age in each group and 0, with a reason that mistakes with < and <= appear exactly at the boundaries.",
    {2: ("Lists both sides of every boundary (4/5, 17/18, 64/65), a typical value in each group and an extreme such as 0, with the reason that boundary mistakes show up there.",
         ["0 (the smallest), 4 and 5 (free ends, child starts), 10 (typical child), 17 and 18 (child ends, adult starts), 40 (typical adult), 64 and 65 (adult ends, senior starts), 90 (typical senior). The boundaries matter most because < versus <= mistakes only show up exactly there.",
          "I'd test 0, 4, 5, 12, 17, 18, 30, 64, 65 and 80. The pairs around 5, 18 and 65 check each limit from both sides, and the others check the middle of each group."]),
     1: ("Gives sensible ages but misses a boundary pair, or gives no reason.",
         ["5, 18, 65 and 80.", "Test one age in each group."]),
     0: ("Incorrect, for example tests only one value or picks values at random with no reason.",
         ["Just try 30.", "Test lots of random numbers."])})

# ============================ 7.4 ============================
Lesson("j1-l7.4", "Mixed-skills challenges", ["J1.16", "J1.07", "J1.08"], [
    ("o1", "Choose the right tool (loop, conditional, method, array) for a problem that doesn't say which"),
    ("o2", "Solve a problem by planning cases first, then building and checking"),
    ("o3", "Debug a method by finding a failing case and tracing it"),
], ["j1-l7.3"], 60, ["R8", "R16"], r'''
## Before you start

This lesson uses everything from Stage 1. There is nothing new to learn; the point is to practise choosing the tool yourself.

**Quick check.** Which of these needs a loop: "double a number", "add up an array", "report whether a number is even"?

<details><summary>Show the answer</summary>

Only "add up an array": it has to visit every element.

</details>

## Explanation

Earlier exercises came with a lesson title that gave away the technique: a loops lesson, a methods lesson, a strings lesson. Real problems don't. This lesson's exercises are **unlabelled**: you decide whether you need a loop, a conditional, an array, a helper method, or several of them.

### A routine for an unlabelled problem

1. **Restate it.** Inputs, output, rules, in your own words.
2. **Work out cases by hand,** including an empty or smallest input and a case at each edge.
3. **Pick a shape.**
   - Do something to *every* item? → a loop.
   - Choose between ways? → `if` / `else`.
   - A job that appears twice, or deserves a name? → a method.
   - Keep a result as you go (a total, a count, a "best so far")? → a variable updated in the loop.
4. **Write the smallest thing that works** and check it against your cases.
5. **Fix and re-check one thing at a time.**

### A worked pattern: building a result as you go

Many problems fit one pattern: walk through the input, and keep track of something. A **count** (`count++` when something matches), a **total** (`sum += value`), a **best so far** (`if (value > best) best = value;`), or a **string being built** (`result += ...`). Spotting the pattern is most of the work.

For instance, "compress `aaabcc` into `a3b1c2`" is *build a string while counting the length of each run*:

- keep the current character and how many times you've seen it in a row;
- when the character changes, append the old one and its count, and start again;
- don't forget to append the last run once the loop ends.

The last point is the classic slip. After the loop ends, the final run has been counted but never written out.

### When it fails

If a case fails, **find the smallest input that fails**, and trace it by hand, as in [Debugging systematically](j1-l6.5). A bug in a loop is often one of: starting or stopping one step off, forgetting the final item, or not handling the empty input.

## Worked examples

### Example 1: run-length text

*Task: `compress("aaabcc")` should give `a3b1c2`. An empty string gives an empty string.*

**Step 1 — Cases.** `""` → `""`. `"a"` → `a1`. `"aab"` → `a2b1`. `"aaabcc"` → `a3b1c2`.

**Step 2 — Shape.** Walk along the string; keep the current character and its run length.

**Step 3 — Code, including the final run.**

```java runnable
String compress(String text) {
    if (text.isEmpty()) {
        return "";
    }
    String result = "";
    char current = text.charAt(0);
    int run = 1;
    for (int i = 1; i < text.length(); i++) {
        if (text.charAt(i) == current) {
            run++;
        } else {
            result += current + "" + run;
            current = text.charAt(i);
            run = 1;
        }
    }
    result += current + "" + run;
    return result;
}

void main() {
    IO.println(compress("aaabcc"));
    IO.println(compress("a"));
}
```

**Step 4 — Check.** It prints `a3b1c2` and `a1`. Remove the last `result +=` line and `"a"` would give an empty answer, which is why the final run is added after the loop.

### Example 2: second largest

*Task: return the second-largest **different** value in an array, or -1 if there are fewer than two different values.*

**Step 1 — Cases.** `{5, 9, 9, 3}` → 5 (the two 9s count once). `{4, 4}` → -1. `{}` → -1. `{1, 2}` → 1.

**Step 2 — Shape.** Two "best so far" variables, a `largest` and a `second`, updated in one pass.

**Step 3 — Code.**

```java runnable
int secondLargest(int[] values) {
    boolean haveLargest = false;
    boolean haveSecond = false;
    int largest = 0;
    int second = 0;
    for (int value : values) {
        if (!haveLargest || value > largest) {
            if (haveLargest) {
                second = largest;
                haveSecond = true;
            }
            largest = value;
            haveLargest = true;
        } else if (value < largest && (!haveSecond || value > second)) {
            second = value;
            haveSecond = true;
        }
    }
    return haveSecond ? second : -1;
}

void main() {
    IO.println(secondLargest(new int[]{5, 9, 9, 3}));
    IO.println(secondLargest(new int[]{4, 4}));
}
```

**Step 4 — Why the flags?** Starting `largest` at 0 would be wrong for arrays of negative numbers. The two booleans record "have I seen one yet?", so no made-up starting value is needed.

## Where this is used

- **Report building, parsing, data clean-up:** nearly every real task is "walk through some input and keep track of something".
- **Interviews and code reviews** pose unlabelled problems, and the routine above is how you stay calm.

## Common mistakes

:::mistake{id=MC24}
**Forgetting the last item.** Anything built "when the value changes" needs one more step after the loop for the final group.
:::

:::mistake{id=MC25}
**Inventing a starting value.** Starting a maximum at 0 breaks for negative numbers. Use the first element, or a flag that says nothing has been seen yet.
:::

:::mistake{id=MC26}
**Skipping the empty input.** Check the smallest input first (empty string, empty array, zero), because it's where code written for the typical case usually fails.
:::

## Practice

::exercise{id=j1-l7.4-write-compress}

::exercise{id=j1-l7.4-write-second}

::exercise{id=j1-l7.4-debug-words}

::exercise{id=j1-l7.4-explain-approach}

## Further reading

- **"Students' misconceptions and other difficulties in introductory programming"** (Qian & Lehman, 2017) `[R8]`, on why transferring a known technique to a new-looking problem is hard.
- The course's debugging notes `[R16]`.

## How you'll be assessed

- The **write** exercises check that you can solve problems that don't say which technique to use (*transfer*).
- The **debug** exercise checks that you can find a failing case and fix a method (*debugging*).
- The **explain** exercise checks that you can describe a plan for a larger problem (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l7.4")
def compress(s):
    if not s: return ""
    out, cur, n = "", s[0], 1
    for c in s[1:]:
        if c == cur: n += 1
        else:
            out += cur + str(n); cur, n = c, 1
    return out + cur + str(n)
ex.method("write", "j1-l7.4-write-compress", "Run-length text", ["o1", "o2"], ["J1.16", "J1.07"], ["XFER"],
    "Write `compress(String text)`. It replaces each run of the same character with that character and the length of the run. `\"aaabcc\"` becomes `\"a3b1c2\"`, and `\"a\"` becomes `\"a1\"`. An empty string gives an empty string.",
    [("compress", [("text", "String")], "String")], {"compress": compress},
    [("compress", ["aaabcc"]), ("compress", ["a"]), ("compress", [""])],
    [("compress", ["aab"]), ("compress", ["abc"]), ("compress", ["zzzzzzzzzzz"]), ("compress", ["aabbaa"]), ("compress", ["xyyx"])],
    'String compress(String text) {\n    return ""; // replace this\n}',
    'String compress(String text) {\n    if (text.isEmpty()) {\n        return "";\n    }\n    String result = "";\n    char current = text.charAt(0);\n    int run = 1;\n    for (int i = 1; i < text.length(); i++) {\n        if (text.charAt(i) == current) {\n            run++;\n        } else {\n            result += current + "" + run;\n            current = text.charAt(i);\n            run = 1;\n        }\n    }\n    result += current + "" + run;\n    return result;\n}',
    {"forgets-last-run": 'String compress(String text) {\n    if (text.isEmpty()) return "";\n    String result = "";\n    char current = text.charAt(0);\n    int run = 1;\n    for (int i = 1; i < text.length(); i++) {\n        if (text.charAt(i) == current) run++;\n        else { result += current + "" + run; current = text.charAt(i); run = 1; }\n    }\n    return result;\n}',
     "merges-separate-runs": 'String compress(String text) {\n    String result = "";\n    for (char c = \'a\'; c <= \'z\'; c++) {\n        int n = 0;\n        for (int i = 0; i < text.length(); i++) if (text.charAt(i) == c) n++;\n        if (n > 0) result += c + "" + n;\n    }\n    return result;\n}'},
    ("Keep the current character and a run count. When the character changes, write the old one out. What happens to the last run?", "After the loop, append the final current character and run count."),
    difficulty=3)
def second(a):
    d = sorted(set(a))
    return d[-2] if len(d) >= 2 else -1
ex.method("write", "j1-l7.4-write-second", "Second largest", ["o1", "o2"], ["J1.16", "J1.07", "J1.08"], ["XFER"],
    "Write `secondLargest(int[] values)`: the second-largest **different** value. In `{5, 9, 9, 3}` the largest is 9, so the answer is 5 (the two 9s count once). If there are fewer than two different values, return -1.\n\nThe array may contain negative numbers.",
    [("secondLargest", [("values", "int[]")], "int")], {"secondLargest": second},
    [("secondLargest", [[5, 9, 9, 3]]), ("secondLargest", [[4, 4]]), ("secondLargest", [[]])],
    [("secondLargest", [[1, 2]]), ("secondLargest", [[-5, -2, -9]]), ("secondLargest", [[7]]), ("secondLargest", [[3, 3, 2, 2]]), ("secondLargest", [[10, 1, 5, 8, 10]]), ("secondLargest", [[-1, -1, -3]])],
    'int secondLargest(int[] values) {\n    return -1; // replace this\n}',
    'int secondLargest(int[] values) {\n    boolean haveLargest = false;\n    boolean haveSecond = false;\n    int largest = 0;\n    int second = 0;\n    for (int value : values) {\n        if (!haveLargest || value > largest) {\n            if (haveLargest) {\n                second = largest;\n                haveSecond = true;\n            }\n            largest = value;\n            haveLargest = true;\n        } else if (value < largest && (!haveSecond || value > second)) {\n            second = value;\n            haveSecond = true;\n        }\n    }\n    return haveSecond ? second : -1;\n}',
    {"starts-at-zero": 'int secondLargest(int[] values) {\n    int largest = 0, second = 0;\n    boolean any = false;\n    for (int v : values) {\n        if (v > largest) { second = largest; largest = v; any = true; }\n        else if (v < largest && v > second) { second = v; any = true; }\n    }\n    return any && second != 0 ? second : -1;\n}',
     "counts-duplicates": 'int secondLargest(int[] values) {\n    if (values.length < 2) return -1;\n    int[] copy = values.clone();\n    java.util.Arrays.sort(copy);\n    return copy[copy.length - 2];\n}'},
    ("Track two 'best so far' values in one pass. Be careful what each starts as: 0 is wrong for negative numbers.", "Use flags (or the first element) to record that a largest and a second have been seen."),
    difficulty=4)
def count_words(t):
    return len(t.split())
ex.method("debug", "j1-l7.4-debug-words", "Count the words", ["o3"], ["J1.07", "J1.08"], ["DEBUG"],
    "`countWords` should return the number of words in the text, where words are separated by one or more spaces. It works for `\"one two three\"` but not for every input. Find a failing case, trace it, and fix the method.\n\nHint: try an empty string, extra spaces, and spaces at the start or end.",
    [("countWords", [("text", "String")], "int")], {"countWords": count_words},
    [("countWords", ["one two three"]), ("countWords", ["hello"]), ("countWords", [""])],
    [("countWords", ["  leading"]), ("countWords", ["trailing  "]), ("countWords", ["a  b"]), ("countWords", ["   "]), ("countWords", ["many   spaces   here"]), ("countWords", ["x y"])],
    'int countWords(String text) {\n    int count = 0;\n    for (int i = 0; i < text.length(); i++) {\n        if (text.charAt(i) == \' \') {\n            count++;\n        }\n    }\n    return count + 1;\n}',
    'int countWords(String text) {\n    int count = 0;\n    boolean inWord = false;\n    for (int i = 0; i < text.length(); i++) {\n        if (text.charAt(i) == \' \') {\n            inWord = false;\n        } else if (!inWord) {\n            inWord = true;\n            count++;\n        }\n    }\n    return count;\n}',
    {"still-counts-spaces": 'int countWords(String text) {\n    if (text.isEmpty()) return 0;\n    int count = 0;\n    for (int i = 0; i < text.length(); i++) {\n        if (text.charAt(i) == \' \') count++;\n    }\n    return count + 1;\n}'},
    ("Find the smallest failing input: what does the method return for an empty string, and for two spaces in a row?", "Count the start of each word instead of the spaces: a word starts at a non-space whose previous character was a space or the start."),
    difficulty=3)
ex.explain("j1-l7.4-explain-approach", "Plan a bigger program", ["o2", "o1"], ["J1.16"],
    "You are asked for a program that reads a list of exam marks (whole numbers from 0 to 100) typed one per line, stopping when the person types `done`, and then prints the number of marks, the highest, the lowest and the average. Describe your plan: what the methods would be and what each does, what you would keep track of while reading, and at least three cases you would check, including the awkward one where no marks are typed.",
    "A full answer names separate jobs (reading, calculating, printing), tracks count, total, highest and lowest as it reads, handles the empty case by deciding what to print instead of dividing by zero, and lists cases such as one mark, several marks, marks at 0 and 100, and no marks.",
    {2: ("Splits the job into methods, tracks count, total, highest and lowest while reading, decides what to do with no marks (no division by zero), and lists at least three sensible cases.",
         ["I'd have a method that reads lines until done and collects the marks, one that works out count, highest, lowest and average, and one that prints the report. While reading I keep a count, a total, the highest and the lowest. Cases: one mark (it is both highest and lowest), 0 and 100 together, three ordinary marks, and no marks, where I'd print a message instead of dividing by zero.",
          "Read in a loop until the line is done; keep count, sum, max and min as I go; print the results with a helper. I'd check one mark, several marks, the extremes 0 and 100, and an empty list, where the average would divide by zero so I'd handle it first."]),
     1: ("Has a reasonable outline but misses the empty case, or doesn't say what is tracked, or gives fewer than three cases.",
         ["Read the marks in a loop, then print the highest, lowest and average.", "Use a loop and variables for highest and lowest."]),
     0: ("Incorrect or unusable, for example puts everything in one place with no plan or ignores the stop word.",
         ["Just write it and see what happens.", "Use an array of 1000 marks and print them."])})
print("module 7 written")
