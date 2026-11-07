from build import *

Lesson("j1-l3.3", "Making decisions", ["J1.06"], [
    ("o1", "Write if, if/else and else-if chains that choose between actions"),
    ("o2", "Order the conditions in an else-if chain so each value reaches the right branch"),
    ("o3", "Explain why a semicolon straight after an if condition breaks it"),
], ["j1-l3.2"], 35, ["R8", "R9"], r'''
## Before you start

You should be able to write conditions with comparisons, `&&` and `||` ([Boolean expressions](j1-l3.2)).

**Quick check.** Write a condition that's true when `score` is between 50 and 59, including both.

<details><summary>Show the answer</summary>

`score >= 50 && score <= 59`

</details>

## Explanation

A condition on its own only answers a question. To **act** on the answer, use `if`.

### `if`

```java
if (temperature > 25) {
    IO.println("Take some water.");
}
```

The condition goes in parentheses. If it's true, the statements in the braces run; if it's false, they're skipped and the program carries on after the closing brace.

### `if` / `else`

`else` gives an alternative for when the condition is false. Exactly one of the two blocks runs:

```java runnable
void main() {
    int age = 16;
    if (age >= 18) {
        IO.println("You can vote.");
    } else {
        IO.println("Not yet: " + (18 - age) + " years to go.");
    }
}
```

### Else-if chains

For more than two possibilities, chain conditions with `else if`. Java checks them **from the top**, runs the **first** branch whose condition is true, and skips all the rest, even if later conditions would also be true:

```java runnable
String grade(int score) {
    if (score >= 70) {
        return "A";
    } else if (score >= 60) {
        return "B";
    } else if (score >= 50) {
        return "C";
    } else {
        return "Fail";
    }
}

void main() {
    IO.println(grade(75));
    IO.println(grade(65));
    IO.println(grade(20));
}
```

A score of 75 is also `>= 60` and `>= 50`, but it only ever reaches the first branch. That's why the **order** matters: put the most demanding condition first. If `score >= 50` came first, every score of 50 or more would get a C.

`return` ends the method immediately, which is why the branches above don't need anything after them.

### Braces and indentation

Always use braces, even for a single statement. Indent the code inside each branch so the structure is visible at a glance.

### The stray semicolon

```java
if (temperature > 25); {
    IO.println("Take some water.");
}
```

The `;` straight after the condition ends the `if` **right there**: it means *if the condition is true, do nothing*. The braces that follow are then just a block that always runs. Java compiles it without complaint, which makes this bug easy to miss. There's never a semicolon between `if (…)` and `{`.

## Worked examples

### Example 1: ticket prices

*Task: children under 12 pay £5, people aged 65 and over pay £6, everyone else pays £10. Write `ticketPrice(int age)`.*

**Step 1 — List the cases and their boundaries.** Under 12; 65 and over; everyone else.

**Step 2 — Choose an order.** The two special cases don't overlap, so either can go first. "Everyone else" goes last, as the `else`.

**Step 3 — Write the chain, then test each boundary.** 11, 12, 64 and 65.

```java runnable
int ticketPrice(int age) {
    if (age < 12) {
        return 5;
    } else if (age >= 65) {
        return 6;
    } else {
        return 10;
    }
}

void main() {
    IO.println(ticketPrice(11) + " " + ticketPrice(12) + " " + ticketPrice(64) + " " + ticketPrice(65));
}
```

This prints `5 10 10 6`.

### Example 2: describing the wind

*Task: below 1 mph is "Calm", below 13 is "Breeze", below 39 is "Windy", anything else is "Gale".*

**Step 1 — Notice the pattern.** Each band is "below the next limit", so check from the **smallest** limit upwards.

**Step 2 — Write it so each check only needs one comparison.** By the time `speed < 13` is checked, you already know `speed` isn't below 1.

```java runnable
String windDescription(int speed) {
    if (speed < 1) {
        return "Calm";
    } else if (speed < 13) {
        return "Breeze";
    } else if (speed < 39) {
        return "Windy";
    } else {
        return "Gale";
    }
}

void main() {
    IO.println(windDescription(0) + ", " + windDescription(12) + ", " + windDescription(39));
}
```

This prints `Calm, Breeze, Gale`.

## Predict, then run

::exercise{id=j1-l3.3-predict-branches}

## Where this is used

- **Pricing**: discounts, delivery bands and tax rates are all else-if chains.
- **Validation**: if a form field is empty, show an error; else if it's too long, show a different one; else accept it.
- **Games**: if the player's health reaches 0, the game ends.

## Common mistakes

:::mistake{id=MC11}
**Expecting every matching branch to run.** In an else-if chain only the **first** true branch runs. Put the most specific or demanding condition first.
:::

:::mistake{id=MC08}
**A semicolon after the condition.** `if (x > 0); { … }` runs the block every time. Delete the semicolon.
:::

### Missing the final `else`

If a method must return a value, every path has to return one. Without a final `else` (or a `return` after the chain), Java reports `missing return statement`.

## Practice

::exercise{id=j1-l3.3-write-grade}

::exercise{id=j1-l3.3-debug-order}

::exercise{id=j1-l3.3-debug-semicolon}

::exercise{id=j1-l3.3-modify-star}

::exercise{id=j1-l3.3-explain-order}

## Further reading

- **"Students' misconceptions and other difficulties in introductory programming"** (Qian & Lehman, 2017) `[R8]`: includes the research behind the two common mistakes above.

## How you'll be assessed

- The **predict** exercise checks that you can follow which branch runs (*identifying mistakes*).
- The **write** exercise checks that you can write an else-if chain (*implementation*).
- The **debug** exercises check that you can fix a wrongly ordered chain and a stray semicolon (*debugging*).
- The **modify** exercise checks that you can add a branch to a working chain (*modification*), and **explain** that you know why order matters.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l3.3")
ex.predict("j1-l3.3-predict-branches", "Which branch?", ["o1", "o2"], ["J1.06"],
    "Predict exactly what this program prints. For each call, work out which branch runs first.",
    '''
    String size(int litres) {
        if (litres >= 100) {
            return "large";
        } else if (litres >= 10) {
            return "medium";
        } else {
            return "small";
        }
    }

    void main() {
        IO.println(size(250));
        IO.println(size(10));
        IO.println(size(9));
        if (size(50).equals("medium")) {
            IO.println("fits");
        } else {
            IO.println("doesn't fit");
        }
    }
    ''', '''
    large
    medium
    small
    fits
    ''', ("Check the conditions from the top; the first true one wins.",
          "10 is not >= 100 but is >= 10, so it's medium. size(50) is \"medium\", so the if prints fits."), misconceptions=["MC11"], difficulty=2)

def grade(s):
    return "A" if s >= 70 else "B" if s >= 60 else "C" if s >= 50 else "Fail"
cases_v = [(None, [75]), (None, [62]), (None, [30])]
cases_h = [(None, [70], "exactly 70"), (None, [60], "exactly 60"), (None, [50], "exactly 50"), (None, [49], "just failing"), (None, [100], "full marks"), (None, [0], "zero")]
ex.method("write", "j1-l3.3-write-grade", "Exam grades", ["o1", "o2"], ["J1.06"], ["IMPL"],
    "Complete `grade`: 70 or more is `\"A\"`, 60 or more is `\"B\"`, 50 or more is `\"C\"`, and anything lower is `\"Fail\"`.",
    [("grade", [("score", "int")], "String")], {"grade": grade}, cases_v, cases_h,
    'String grade(int score) {\n    return ""; // replace this with an else-if chain\n}\n\nvoid main() {\n    IO.println(grade(75)); // should print A\n}\n',
    'String grade(int score) {\n    if (score >= 70) {\n        return "A";\n    } else if (score >= 60) {\n        return "B";\n    } else if (score >= 50) {\n        return "C";\n    } else {\n        return "Fail";\n    }\n}\n\nvoid main() {\n    IO.println(grade(75)); // should print A\n}\n',
    {"wrong-order": 'String grade(int score) {\n    if (score >= 50) {\n        return "C";\n    } else if (score >= 60) {\n        return "B";\n    } else if (score >= 70) {\n        return "A";\n    } else {\n        return "Fail";\n    }\n}\n\nvoid main() {\n}\n',
     "strict-boundaries": 'String grade(int score) {\n    if (score > 70) {\n        return "A";\n    } else if (score > 60) {\n        return "B";\n    } else if (score > 50) {\n        return "C";\n    } else {\n        return "Fail";\n    }\n}\n\nvoid main() {\n}\n'},
    ("Which condition is the most demanding? Check that one first.",
     "if (score >= 70) return \"A\"; else if (score >= 60) return \"B\"; else if (score >= 50) return \"C\"; else return \"Fail\";"),
    group="if-chains")

def price(age): return 5 if age < 12 else 6 if age >= 65 else 10
ex.method("write", "j1-l3.3-retrieve-tickets", "Cinema prices", ["o1", "o2"], ["J1.06"], ["IMPL"],
    "Complete `ticketPrice`: children under 12 pay 5, people aged 65 and over pay 6, and everyone else pays 10.",
    [("ticketPrice", [("age", "int")], "int")], {"ticketPrice": price},
    [(None, [8]), (None, [30]), (None, [70])],
    [(None, [11], "just under 12"), (None, [12], "exactly 12"), (None, [64], "just under 65"), (None, [65], "exactly 65"), (None, [0], "a baby")],
    'int ticketPrice(int age) {\n    return 0; // replace this with an else-if chain\n}\n\nvoid main() {\n    IO.println(ticketPrice(8)); // should print 5\n}\n',
    'int ticketPrice(int age) {\n    if (age < 12) {\n        return 5;\n    } else if (age >= 65) {\n        return 6;\n    } else {\n        return 10;\n    }\n}\n\nvoid main() {\n    IO.println(ticketPrice(8)); // should print 5\n}\n',
    {"inclusive-12": 'int ticketPrice(int age) {\n    if (age <= 12) {\n        return 5;\n    } else if (age >= 65) {\n        return 6;\n    } else {\n        return 10;\n    }\n}\n\nvoid main() {\n}\n'},
    ("Three cases. The last one, everyone else, goes in the else.", "if (age < 12) return 5; else if (age >= 65) return 6; else return 10;"),
    role="retrieval", group="if-chains")

def wind(s): return "Calm" if s < 1 else "Breeze" if s < 13 else "Windy" if s < 39 else "Gale"
ex.method("write", "j1-l3.3-retrieve-wind", "Wind speeds", ["o1", "o2"], ["J1.06"], ["IMPL"],
    "Complete `windDescription`: below 1 mph is `\"Calm\"`, below 13 is `\"Breeze\"`, below 39 is `\"Windy\"`, and anything else is `\"Gale\"`.",
    [("windDescription", [("mph", "int")], "String")], {"windDescription": wind},
    [(None, [0]), (None, [20]), (None, [50])],
    [(None, [1], "exactly 1"), (None, [12], "just under 13"), (None, [13], "exactly 13"), (None, [38], "just under 39"), (None, [39], "exactly 39")],
    'String windDescription(int mph) {\n    return ""; // replace this with an else-if chain\n}\n\nvoid main() {\n    IO.println(windDescription(20)); // should print Windy\n}\n',
    'String windDescription(int mph) {\n    if (mph < 1) {\n        return "Calm";\n    } else if (mph < 13) {\n        return "Breeze";\n    } else if (mph < 39) {\n        return "Windy";\n    } else {\n        return "Gale";\n    }\n}\n\nvoid main() {\n    IO.println(windDescription(20)); // should print Windy\n}\n',
    {"largest-first": 'String windDescription(int mph) {\n    if (mph < 39) {\n        return "Windy";\n    } else if (mph < 13) {\n        return "Breeze";\n    } else if (mph < 1) {\n        return "Calm";\n    } else {\n        return "Gale";\n    }\n}\n\nvoid main() {\n}\n'},
    ("Each band is 'below the next limit'. Which limit should be checked first?", "Check mph < 1, then < 13, then < 39, with Gale in the else."),
    role="retrieval", group="if-chains")

ex.method("debug", "j1-l3.3-debug-order", "Everyone gets a C", ["o2"], ["J1.06"], ["DEBUG"],
    "`grade` should give 70+ an A, 60+ a B, 50+ a C, and anything lower a Fail. A student who scored 92 got a C. Find and fix the bug.",
    [("grade", [("score", "int")], "String")], {"grade": grade}, cases_v, cases_h,
    'String grade(int score) {\n    if (score >= 50) {\n        return "C";\n    } else if (score >= 60) {\n        return "B";\n    } else if (score >= 70) {\n        return "A";\n    } else {\n        return "Fail";\n    }\n}\n\nvoid main() {\n    IO.println(grade(92)); // should print A\n}\n',
    'String grade(int score) {\n    if (score >= 70) {\n        return "A";\n    } else if (score >= 60) {\n        return "B";\n    } else if (score >= 50) {\n        return "C";\n    } else {\n        return "Fail";\n    }\n}\n\nvoid main() {\n    IO.println(grade(92)); // should print A\n}\n',
    {"partly-reordered": 'String grade(int score) {\n    if (score >= 60) {\n        return "B";\n    } else if (score >= 70) {\n        return "A";\n    } else if (score >= 50) {\n        return "C";\n    } else {\n        return "Fail";\n    }\n}\n\nvoid main() {\n}\n'},
    ("Trace grade(92). Which condition is checked first, and is it true?",
     "92 >= 50 is true, so the first branch wins. Reverse the order: check >= 70 first, then >= 60, then >= 50."),
    misconceptions=["MC11"])

def label(t): return "Hot" if t > 25 else "Mild"
ex.method("debug", "j1-l3.3-debug-semicolon", "Always hot", ["o3"], ["J1.06"], ["DEBUG"],
    "`label` should return `\"Hot\"` when the temperature is above 25, and `\"Mild\"` otherwise. It says every day is hot. Find and fix the bug.",
    [("label", [("temperature", "int")], "String")], {"label": label},
    [(None, [30]), (None, [10]), (None, [25])],
    [(None, [26], "just above 25"), (None, [0], "freezing"), (None, [-5], "below zero"), (None, [40], "very hot"), (None, [24], "just below")],
    'String label(int temperature) {\n    String result = "Mild";\n    if (temperature > 25); {\n        result = "Hot";\n    }\n    return result;\n}\n\nvoid main() {\n    IO.println(label(10)); // should print Mild\n}\n',
    'String label(int temperature) {\n    String result = "Mild";\n    if (temperature > 25) {\n        result = "Hot";\n    }\n    return result;\n}\n\nvoid main() {\n    IO.println(label(10)); // should print Mild\n}\n',
    {"flipped-condition": 'String label(int temperature) {\n    String result = "Mild";\n    if (temperature >= 25) {\n        result = "Hot";\n    }\n    return result;\n}\n\nvoid main() {\n}\n'},
    ("Look closely at the end of the if line. What's between the condition and the brace?",
     "The semicolon ends the if, so the block always runs. Delete the semicolon."),
    misconceptions=["MC08"])

def grade_star(s):
    return "A*" if s >= 90 else grade(s)
ex.method("modify", "j1-l3.3-modify-star", "A new top grade", ["o1", "o2"], ["J1.06"], ["MOD"],
    "The exam board has added a new top grade: 90 or more gets `\"A*\"`. Everything else stays the same. Change `grade` to include it.",
    [("grade", [("score", "int")], "String")], {"grade": grade_star},
    [(None, [95]), (None, [75]), (None, [30])],
    [(None, [90], "exactly 90"), (None, [89], "just under 90"), (None, [70], "exactly 70"), (None, [100], "full marks"), (None, [50], "exactly 50")],
    'String grade(int score) {\n    if (score >= 70) {\n        return "A";\n    } else if (score >= 60) {\n        return "B";\n    } else if (score >= 50) {\n        return "C";\n    } else {\n        return "Fail";\n    }\n}\n\nvoid main() {\n    IO.println(grade(95));\n}\n',
    'String grade(int score) {\n    if (score >= 90) {\n        return "A*";\n    } else if (score >= 70) {\n        return "A";\n    } else if (score >= 60) {\n        return "B";\n    } else if (score >= 50) {\n        return "C";\n    } else {\n        return "Fail";\n    }\n}\n\nvoid main() {\n    IO.println(grade(95));\n}\n',
    {"added-at-end": 'String grade(int score) {\n    if (score >= 70) {\n        return "A";\n    } else if (score >= 60) {\n        return "B";\n    } else if (score >= 50) {\n        return "C";\n    } else if (score >= 90) {\n        return "A*";\n    } else {\n        return "Fail";\n    }\n}\n\nvoid main() {\n}\n'},
    ("Where in the chain does the new condition need to go so that 95 reaches it?",
     "Add if (score >= 90) return \"A*\"; as the very first branch, before the >= 70 check."))

ex.explain("j1-l3.3-explain-order", "Why order matters", ["o2"], ["J1.06"],
    "In the original `grade` method, why must `score >= 70` be checked before `score >= 50`? Use a specific score to show what goes wrong in the other order.",
    "A full answer says an else-if chain runs only the first true branch; a high score like 85 also satisfies >= 50, so if that's checked first it returns C and the A branch is never reached.",
    {2: ("Says only the first true branch runs, and uses an example score (70 or above) to show it would wrongly get a C if >= 50 came first.",
         ["Java stops at the first true condition. If >= 50 came first, a score of 85 would match it and get a C, and the >= 70 check would never run.",
          "Only one branch runs, the first that's true. 92 is >= 50, so checking that first gives C even though it should be A."]),
     1: ("Gets the idea that order matters but with no example, or a vague explanation of why.",
         ["Because the higher grades need to be checked first.", "Otherwise everyone gets the wrong grade."]),
     0: ("Incorrect, for example says all matching branches run, or that the order doesn't matter.",
         ["It doesn't matter, Java checks all of them.", "Because 50 is smaller than 70 so it would be skipped."])},
    misconceptions=["MC11"])
print("3.3 written")
