from build import *

Lesson("j1-l5.4", "Decomposing problems", ["J1.09"], [
    ("o1", "Break a problem into smaller methods, writing each method's header before its body"),
    ("o2", "Build a larger answer by calling small methods"),
    ("o3", "Explain why small named methods are easier to check than one long method"),
], ["j1-l5.3"], 40, ["R4", "R3"], r'''
## Before you start

You should be able to write methods and call one from another ([Parameters and return values](j1-l5.2)).

**Quick check.** Why is a name like `isLeapYear(year)` better than five lines of arithmetic in the middle of a program?

<details><summary>Show the answer</summary>

The name says what the code is for, so a reader doesn't have to work it out, and the method can be tested on its own.

</details>

## Explanation

Big problems are solved the same way as small ones: by splitting them into smaller problems until each one is easy. This is **decomposition**, and it's the most important skill in programming.

### The top-down method

1. **Say what the whole thing does,** in one sentence.
2. **List the smaller jobs** it needs.
3. **Write the header of each method first** (name, parameters, return type), with a one-line description of what it does. Don't worry about the bodies yet.
4. **Write the bodies, one at a time,** easiest first, testing each on its own.
5. **Combine them.**

Writing the headers first forces you to decide what goes in and what comes out of each piece before you get lost in details.

### An example: is it a leap year?

A year is a leap year if it's divisible by 4, **except** years divisible by 100, **unless** they're also divisible by 400. So 2024 is a leap year, 1900 isn't, and 2000 is.

Whole thing: `isLeapYear(year)`. Smaller jobs: a way to ask "is `year` divisible by `d`?"

```java runnable
boolean divisibleBy(int number, int d) {
    return number % d == 0;
}

boolean isLeapYear(int year) {
    if (divisibleBy(year, 400)) {
        return true;
    }
    if (divisibleBy(year, 100)) {
        return false;
    }
    return divisibleBy(year, 4);
}

void main() {
    IO.println(isLeapYear(2024));
    IO.println(isLeapYear(1900));
    IO.println(isLeapYear(2000));
}
```

This prints `true`, `false`, `true`. Read `isLeapYear` aloud: *if divisible by 400, yes; otherwise if divisible by 100, no; otherwise it's divisible by 4 or it isn't.* The rule is written in the order you'd explain it.

### Small methods are easy to check

Each helper can be tested alone: `divisibleBy(2024, 4)` should be `true`. If `isLeapYear` gives a wrong answer, you test the pieces to find which one is wrong. With one long method, you can't easily tell where the mistake is.

A good method does **one thing**, has a name that says what it does, and fits on a screen. If you find yourself writing a comment to explain a block inside a method, that block usually wants to be its own method.

## Worked examples

### Example 1: a time in words

*Task: given a number of seconds, return a string like `2h 5m 9s`. 7509 seconds is 2 hours, 5 minutes and 9 seconds.*

**Step 1 — One sentence.** Split seconds into hours, minutes and seconds, and join them.

**Step 2 — Smaller jobs, as headers.**
- `int hoursPart(int totalSeconds)` — whole hours.
- `int minutesPart(int totalSeconds)` — minutes left after the hours.
- `int secondsPart(int totalSeconds)` — seconds left after the minutes.

**Step 3 — Bodies.** Whole hours: `totalSeconds / 3600`. Minutes left: take what's left after the hours (`totalSeconds % 3600`), then divide by 60. Seconds: `totalSeconds % 60`.

**Step 4 — Combine.**

```java runnable
int hoursPart(int totalSeconds) {
    return totalSeconds / 3600;
}

int minutesPart(int totalSeconds) {
    return totalSeconds % 3600 / 60;
}

int secondsPart(int totalSeconds) {
    return totalSeconds % 60;
}

String describe(int totalSeconds) {
    return hoursPart(totalSeconds) + "h " + minutesPart(totalSeconds) + "m " + secondsPart(totalSeconds) + "s";
}

void main() {
    IO.println(describe(7509));
}
```

This prints `2h 5m 9s`. Test the helpers on their own first: `minutesPart(7509)` should be 5.

### Example 2: a rule built from smaller rules

*Task: a password is "strong" if it has at least 8 characters, contains a digit, and contains a capital letter.*

**Step 1 — Three smaller yes/no jobs.** Long enough? Has a digit? Has a capital?

**Step 2 — Write the checks as headers, then bodies** using the loop patterns you know. `Character.isUpperCase(c)` is true for capital letters.

**Step 3 — Combine with `&&`.**

```java runnable
boolean hasDigit(String text) {
    for (int i = 0; i < text.length(); i++) {
        if (Character.isDigit(text.charAt(i))) {
            return true;
        }
    }
    return false;
}

boolean hasCapital(String text) {
    for (int i = 0; i < text.length(); i++) {
        if (Character.isUpperCase(text.charAt(i))) {
            return true;
        }
    }
    return false;
}

boolean isStrong(String password) {
    return password.length() >= 8 && hasDigit(password) && hasCapital(password);
}

void main() {
    IO.println(isStrong("Tr0ub4dor"));
    IO.println(isStrong("password"));
}
```

## Predict, then run

::exercise{id=j1-l5.4-predict-helpers}

## Where this is used

Every real program. Professional code is organised so that you can read the top-level method like a short summary, and look inside a helper only when you need the detail.

## Common mistakes

### One enormous method

If a method does several jobs, it's hard to test, hard to read and hard to change. Split it.

### Helpers with unclear names

`check(x)` says nothing. `hasDigit(text)` says what it does and what it returns.

### Writing bodies before deciding the headers

Without deciding what goes in and out of each method first, the pieces often don't fit together. Headers first.

## Practice

::exercise{id=j1-l5.4-write-leap}

::exercise{id=j1-l5.4-write-timeparts}

::exercise{id=j1-l5.4-write-strong}

::exercise{id=j1-l5.4-explain-split}

## Further reading

- **"Subgoals, context, and worked examples in learning computing problem solving"** (Morrison et al., 2015) `[R4]`: the research on labelled subgoals that this lesson's "steps" follow.

## How you'll be assessed

- The **predict** exercise checks that you can read a decomposed program.
- The **write** exercises check that you can build a solution from helpers, including a problem you haven't seen before (*applying to a new problem*).
- The **explain** exercise checks that you can say why small methods are easier to check.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l5.4")
ex.predict("j1-l5.4-predict-helpers", "Read the summary", ["o2"], ["J1.09"],
    "Predict exactly what this program prints. Work from the small helpers up.",
    '''
    boolean divisibleBy(int number, int d) {
        return number % d == 0;
    }

    String fizz(int n) {
        if (divisibleBy(n, 15)) {
            return "FizzBuzz";
        }
        if (divisibleBy(n, 3)) {
            return "Fizz";
        }
        if (divisibleBy(n, 5)) {
            return "Buzz";
        }
        return "" + n;
    }

    void main() {
        IO.println(fizz(9));
        IO.println(fizz(10));
        IO.println(fizz(30));
        IO.println(fizz(7));
    }
    ''', '''
    Fizz
    Buzz
    FizzBuzz
    7
    ''', ("Each call goes through the checks from the top; the first that's true wins.", "30 is divisible by 15, which is checked first."), difficulty=2)

def leap(y): return y % 400 == 0 or (y % 100 != 0 and y % 4 == 0)
ex.method("write", "j1-l5.4-write-leap", "Leap years", ["o1", "o2"], ["J1.09"], ["IMPL"],
    "Write `divisibleBy(number, d)` (returns whether `number` is divisible by `d`) and `isLeapYear(year)`, which uses it. A year is a leap year if it's divisible by 400, or if it's divisible by 4 but not by 100.",
    [("isLeapYear", [("year", "int")], "boolean"), ("divisibleBy", [("number", "int"), ("d", "int")], "boolean")],
    {"isLeapYear": leap, "divisibleBy": lambda n, d: n % d == 0},
    [(None, [2024]), (None, [1900]), (None, [2000]), ("divisibleBy", [12, 4])],
    [(None, [2023], "ordinary"), (None, [2100], "century"), (None, [1600], "divisible by 400"), (None, [4], "four"), (None, [1999], "odd"), ("divisibleBy", [7, 2], "not divisible")],
    '// Write divisibleBy and isLeapYear here.\n\nvoid main() {\n    IO.println(isLeapYear(2024)); // should print true\n}\n',
    'boolean divisibleBy(int number, int d) {\n    return number % d == 0;\n}\n\nboolean isLeapYear(int year) {\n    if (divisibleBy(year, 400)) {\n        return true;\n    }\n    if (divisibleBy(year, 100)) {\n        return false;\n    }\n    return divisibleBy(year, 4);\n}\n\nvoid main() {\n    IO.println(isLeapYear(2024)); // should print true\n}\n',
    {"ignores-centuries": 'boolean divisibleBy(int number, int d) {\n    return number % d == 0;\n}\n\nboolean isLeapYear(int year) {\n    return divisibleBy(year, 4);\n}\n\nvoid main() {\n}\n'},
    ("Write the helper first. Then check 400 first, then 100, then 4.", "if divisibleBy 400 → true; else if divisibleBy 100 → false; else divisibleBy 4."),
    starter_compiles=False, difficulty=3)

def tp(s): return (s // 3600, s % 3600 // 60, s % 60)
ex.method("write", "j1-l5.4-write-timeparts", "Time in words", ["o1", "o2"], ["J1.09"], ["IMPL"],
    "Write `describe(totalSeconds)` so it returns a string like `2h 5m 9s`. For example, 7509 seconds is `\"2h 5m 9s\"`, and 59 seconds is `\"0h 0m 59s\"`. Split the work into small helper methods of your own.",
    [("describe", [("totalSeconds", "int")], "String")],
    {"describe": lambda s: f"{s // 3600}h {s % 3600 // 60}m {s % 60}s"},
    [(None, [7509]), (None, [59]), (None, [3600])],
    [(None, [0], "zero"), (None, [60], "one minute"), (None, [3661], "one of each"), (None, [86399], "almost a day"), (None, [86400], "a day"), (None, [119], "just under two minutes")],
    '// Write describe, and any helper methods you want, here.\n\nvoid main() {\n    IO.println(describe(7509)); // should print 2h 5m 9s\n}\n',
    'int hoursPart(int totalSeconds) {\n    return totalSeconds / 3600;\n}\n\nint minutesPart(int totalSeconds) {\n    return totalSeconds % 3600 / 60;\n}\n\nint secondsPart(int totalSeconds) {\n    return totalSeconds % 60;\n}\n\nString describe(int totalSeconds) {\n    return hoursPart(totalSeconds) + "h " + minutesPart(totalSeconds) + "m " + secondsPart(totalSeconds) + "s";\n}\n\nvoid main() {\n    IO.println(describe(7509)); // should print 2h 5m 9s\n}\n',
    {"forgot-remainders": 'String describe(int totalSeconds) {\n    return totalSeconds / 3600 + "h " + totalSeconds / 60 + "m " + totalSeconds + "s";\n}\n\nvoid main() {\n}\n'},
    ("Three small jobs: hours, minutes left, seconds left. Which operators give a whole part and a remainder?",
     "hours = s / 3600; minutes = s % 3600 / 60; seconds = s % 60. Join them with \"h \", \"m \" and \"s\"."),
    starter_compiles=False, difficulty=3)

def strong(p): return len(p) >= 8 and any(c.isdigit() for c in p) and any(c.isupper() for c in p)
ex.method("write", "j1-l5.4-write-strong", "A strong password", ["o1", "o2"], ["J1.09"], ["XFER"],
    "A password is strong if it has at least 8 characters, contains at least one digit, **and** contains at least one capital letter. Write `isStrong(password)`. Use small helper methods of your own for the digit and capital checks (`Character.isDigit` and `Character.isUpperCase` tell you about one character).",
    [("isStrong", [("password", "String")], "boolean")], {"isStrong": strong},
    [(None, ["Tr0ub4dor"]), (None, ["password"]), (None, ["Sh0rt"])],
    [(None, [""], "empty"), (None, ["ALLCAPS123"], "no lower case needed"), (None, ["lowercase123"], "no capital"), (None, ["NoDigitsHere"], "no digit"), (None, ["Abcdefg1"], "exactly 8"), (None, ["Abcdef1"], "7 characters")],
    '// Write isStrong, and any helper methods you want, here.\n\nvoid main() {\n    IO.println(isStrong("Tr0ub4dor")); // should print true\n}\n',
    'boolean hasDigit(String text) {\n    for (int i = 0; i < text.length(); i++) {\n        if (Character.isDigit(text.charAt(i))) {\n            return true;\n        }\n    }\n    return false;\n}\n\nboolean hasCapital(String text) {\n    for (int i = 0; i < text.length(); i++) {\n        if (Character.isUpperCase(text.charAt(i))) {\n            return true;\n        }\n    }\n    return false;\n}\n\nboolean isStrong(String password) {\n    return password.length() >= 8 && hasDigit(password) && hasCapital(password);\n}\n\nvoid main() {\n    IO.println(isStrong("Tr0ub4dor")); // should print true\n}\n',
    {"length-only": 'boolean isStrong(String password) {\n    return password.length() >= 8;\n}\n\nvoid main() {\n}\n',
     "needs-either": 'boolean hasDigit(String t) {\n    for (int i = 0; i < t.length(); i++) {\n        if (Character.isDigit(t.charAt(i))) {\n            return true;\n        }\n    }\n    return false;\n}\n\nboolean isStrong(String password) {\n    return password.length() >= 8 && hasDigit(password);\n}\n\nvoid main() {\n}\n'},
    ("Three yes/no questions joined with &&. Which loop pattern answers 'is there any digit?'", "Write hasDigit and hasCapital with find-the-first loops, then return length >= 8 && hasDigit && hasCapital."),
    starter_compiles=False, difficulty=3)

ex.explain("j1-l5.4-explain-split", "Why split it up?", ["o3"], ["J1.09"],
    "A programmer wrote a 40-line `isStrong` method with all the checks inside it. A colleague suggests splitting it into `hasDigit`, `hasCapital` and a short `isStrong`. Give two reasons the split version is better.",
    "A full answer gives two valid reasons, such as: each helper can be tested on its own; mistakes are easier to find; the short method reads like the rule; the helpers can be reused; names explain what each part does.",
    {2: ("Gives two clear, valid reasons (testable alone, easier to find mistakes, reads like the rule, reusable, descriptive names).",
         ["Each helper can be tested separately, so if the password check is wrong you can find which part. And isStrong then reads just like the rule, with length, digit and capital joined by &&.",
          "The helpers have names that explain what they do, and hasDigit can be reused somewhere else."]),
     1: ("Gives one valid reason, or two vague ones.",
         ["It's easier to read.", "It's neater and shorter."]),
     0: ("Gives no valid reason, or an incorrect one.",
         ["It runs faster.", "Java doesn't allow methods longer than 20 lines."])})
print("5.4 written")
