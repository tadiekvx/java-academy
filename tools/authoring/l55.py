from build import *

Lesson("j1-l5.5", "Reading tests", ["J1.14"], [
    ("o1", "Read a test and say what behaviour it checks"),
    ("o2", "Write a method so that it satisfies a list of tests used as its specification"),
    ("o3", "Write your own check calls for a new case, including the edges"),
], ["j1-l5.4"], 30, ["I5", "R15"], r'''
## Before you start

You should be able to write and call methods ([Parameters and return values](j1-l5.2)).

**Quick check.** What do the tests in this course's exercises do to your method?

<details><summary>Show the answer</summary>

They call it with different arguments and compare each result with the expected value.

</details>

## Explanation

Every exercise you've done has been checked by tests. Professional programmers read and write tests all day. This lesson looks at tests from the inside.

### A test is a question with a known answer

A test calls your code with chosen inputs, and compares the result with the answer you expect:

```java
check("area of 3 by 5", 15, area(3, 5));
```

Read it as: *"calling `area(3, 5)` should give 15."* If it does, the test passes. If not, it fails, and a good failure message says what was expected and what actually happened.

Here's a tiny version of what the course's test runner does:

```java runnable
int area(int width, int height) {
    return width * height;
}

void check(String name, int expected, int actual) {
    if (expected == actual) {
        IO.println("PASS " + name);
    } else {
        IO.println("FAIL " + name + ": expected " + expected + " but got " + actual);
    }
}

void main() {
    check("3 by 5", 15, area(3, 5));
    check("1 by 1", 1, area(1, 1));
    check("zero width", 0, area(0, 7));
}
```

All three pass. Notice that each check has a **name**, so a failure tells you which case went wrong.

### Tests as a specification

A list of tests also **describes** what a method must do, often more precisely than a sentence. Suppose you're told only:

| Call | Expected |
|---|---|
| `shorten("hello world", 5)` | `"hello"` |
| `shorten("hi", 5)` | `"hi"` |
| `shorten("", 3)` | `""` |
| `shorten("exactly", 7)` | `"exactly"` |

From these you can work out the rule: *keep at most the first `limit` characters.* The second and fourth rows say what happens when the text is already short enough. Reading tests this way, as examples of required behaviour, is a skill you'll use every day on real teams.

### Choosing good tests

Good tests cover:

- **Typical cases:** ordinary inputs.
- **Edges:** the smallest and largest valid values (0, 1, empty text, exactly at a limit).
- **Boundaries:** values either side of a rule, like 11 and 12 for "under 12".
- **Surprising cases:** inputs a careless programmer wouldn't think of.

Most bugs live at the edges, which is why the hidden tests in this course's exercises always include them.

### A passing test doesn't prove it's correct

Tests can only show that the cases they check work. A method can pass every test and still be wrong for an input nobody tried. That's why you should add a test whenever you find a bug, and think of cases the existing tests don't cover.

## Worked examples

### Example 1: working out the rule from tests

*Task: what does `mystery` do, judging by these tests?*

| Call | Expected |
|---|---|
| `mystery(10)` | `5` |
| `mystery(7)` | `3` |
| `mystery(1)` | `0` |
| `mystery(0)` | `0` |

**Step 1 — Look for a pattern.** 10 → 5; 7 → 3; 1 → 0; 0 → 0.

**Step 2 — Form a guess.** Half, with the fraction dropped: integer division by 2.

**Step 3 — Check the guess against every row.** 10 / 2 = 5 ✓. 7 / 2 = 3 ✓. 1 / 2 = 0 ✓. 0 / 2 = 0 ✓.

**Step 4 — Say what the tests don't cover.** What about negative numbers? `-7 / 2` is -3, but nothing here says that's wanted. A real team would ask.

### Example 2: adding tests for edges

*Task: `isTeenager(age)` is true for 13 to 19. Which checks would you add?*

**Step 1 — List the boundaries.** 12, 13, 19, 20.

**Step 2 — Add one typical case each side.** 16 (yes), 30 (no).

**Step 3 — Write them with clear names.**

```java runnable
boolean isTeenager(int age) {
    return age >= 13 && age <= 19;
}

void check(String name, boolean expected, boolean actual) {
    IO.println((expected == actual ? "PASS " : "FAIL ") + name);
}

void main() {
    check("just too young", false, isTeenager(12));
    check("youngest teenager", true, isTeenager(13));
    check("oldest teenager", true, isTeenager(19));
    check("just too old", false, isTeenager(20));
    check("typical teenager", true, isTeenager(16));
}
```

(`expected == actual ? "PASS " : "FAIL "` is a short way to choose between two values; you can read it as *if they match, "PASS ", otherwise "FAIL "*.)

## Predict, then run

::exercise{id=j1-l5.5-predict-checks}

## Where this is used

- **Every professional codebase** has tests that run automatically whenever anyone changes the code.
- **Understanding old code**: reading its tests is often the fastest way to learn what it's meant to do.
- **Fixing bugs**: a good first step is to write a failing test that shows the bug, then fix it.

## Common mistakes

### Testing only the easy cases

A method that passes `isTeenager(15)` may still be wrong at 13 or 19. Test the edges.

### Unclear test names

`check("test 1", …)` tells you nothing when it fails. Say what the case is.

### Treating a passing test as proof

Passing tests show the checked cases work, not that the method is perfect.

## Practice

::exercise{id=j1-l5.5-write-shorten}

::exercise{id=j1-l5.5-debug-test}

::exercise{id=j1-l5.5-explain-edges}

## Further reading

- **"A systematic literature review of automated feedback generation for programming exercises"** (Keuning et al., 2018) `[R15]`: how tools like this course's tests give feedback, and why feedback that says *why* matters.

## How you'll be assessed

- The **predict** exercise checks that you can read a set of checks.
- The **write** exercise checks that you can implement a method from tests alone (*implementation*).
- The **debug** exercise checks that you can find which case a method gets wrong (*debugging*).
- The **explain** exercise checks that you understand why edge cases matter (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l5.5-predict-checks".rsplit("-", 2)[0])
ex.predict("j1-l5.5-predict-checks", "What do the checks report?", ["o1"], ["J1.14"],
    "Predict exactly what this program prints. Work out each call's result, then whether the check passes.",
    '''
    int middle(int a, int b, int c) {
        if (a > b) {
            return a;
        }
        return b;
    }

    void check(String name, int expected, int actual) {
        if (expected == actual) {
            IO.println("PASS " + name);
        } else {
            IO.println("FAIL " + name + ": expected " + expected + " but got " + actual);
        }
    }

    void main() {
        check("ascending", 5, middle(1, 5, 9));
        check("descending", 5, middle(9, 5, 1));
        check("middle first", 5, middle(5, 1, 9));
    }
    ''', '''
    PASS ascending
    FAIL descending: expected 5 but got 9
    FAIL middle first: expected 5 but got 5
    '''.replace("FAIL middle first: expected 5 but got 5", "PASS middle first"),
    ("Work out middle(1, 5, 9) etc. by hand: which branch runs?",
     "middle(9, 5, 1) has a > b, so it returns 9, which isn't 5. middle(5, 1, 9) also has a > b and returns 5, which matches."),
    difficulty=2)

def shorten(t, n): return t[:n]
ex.method("write", "j1-l5.5-write-shorten", "Tests as a specification", ["o2", "o3"], ["J1.14"], ["IMPL"],
    "You aren't told in words what `shorten(text, limit)` should do. Work it out from the examples the tests show, then write it.\n\n| Call | Result |\n|---|---|\n| `shorten(\"hello world\", 5)` | `\"hello\"` |\n| `shorten(\"hi\", 5)` | `\"hi\"` |\n| `shorten(\"exactly\", 7)` | `\"exactly\"` |",
    [("shorten", [("text", "String"), ("limit", "int")], "String")], {"shorten": shorten},
    [(None, ["hello world", 5]), (None, ["hi", 5]), (None, ["exactly", 7])],
    [(None, ["", 3], "empty text"), (None, ["abc", 0], "limit zero"), (None, ["abc", 1], "limit one"), (None, ["a longer sentence here", 8], "long text"), (None, ["short", 100], "huge limit")],
    '// Write the shorten method here.\n\nvoid main() {\n    IO.println(shorten("hello world", 5)); // should print hello\n}\n',
    'String shorten(String text, int limit) {\n    if (text.length() <= limit) {\n        return text;\n    }\n    return text.substring(0, limit);\n}\n\nvoid main() {\n    IO.println(shorten("hello world", 5)); // should print hello\n}\n',
    {"crashes-when-short": 'String shorten(String text, int limit) {\n    return text.substring(0, limit);\n}\n\nvoid main() {\n}\n',
     "always-first-char": 'String shorten(String text, int limit) {\n    return text.length() <= limit ? text : text.substring(0, 1);\n}\n\nvoid main() {\n}\n'},
    ("Look at the second and third examples: what happens when the text is already short enough?",
     "If text.length() <= limit return text; otherwise return text.substring(0, limit)."),
    starter_compiles=False, difficulty=2)

def tickets(n): return 5 if n < 12 else 6 if n >= 65 else 10
ex.method("debug", "j1-l5.5-debug-test", "Which case fails?", ["o1"], ["J1.14"], ["DEBUG"],
    "Here are the tests for `ticketPrice`: under 12 pays 5, 65 and over pays 6, everyone else pays 10. The method passes most of them, but fails some at the boundaries. Find which case is wrong, and fix the method.",
    [("ticketPrice", [("age", "int")], "int")], {"ticketPrice": tickets},
    [(None, [8]), (None, [30]), (None, [70])],
    [(None, [11], "youngest ten-pound"), (None, [12], "just 12"), (None, [64], "just under 65"), (None, [65], "exactly 65"), (None, [0], "newborn")],
    'int ticketPrice(int age) {\n    if (age <= 12) {\n        return 5;\n    } else if (age > 65) {\n        return 6;\n    } else {\n        return 10;\n    }\n}\n\nvoid main() {\n    IO.println(ticketPrice(12)); // should print 10\n    IO.println(ticketPrice(65)); // should print 6\n}\n',
    'int ticketPrice(int age) {\n    if (age < 12) {\n        return 5;\n    } else if (age >= 65) {\n        return 6;\n    } else {\n        return 10;\n    }\n}\n\nvoid main() {\n    IO.println(ticketPrice(12)); // should print 10\n    IO.println(ticketPrice(65)); // should print 6\n}\n',
    {"fixed-one": 'int ticketPrice(int age) {\n    if (age < 12) {\n        return 5;\n    } else if (age > 65) {\n        return 6;\n    } else {\n        return 10;\n    }\n}\n\nvoid main() {\n}\n'},
    ("The failing tests are named after boundaries. Which two ages are on the boundaries, and what do the comparisons do with them?",
     "Both conditions are off by one: use age < 12 and age >= 65."))

ex.explain("j1-l5.5-explain-edges", "Why test the edges?", ["o3"], ["J1.14"],
    "A method `isTeenager(age)` passes the tests for ages 15, 8 and 40. A colleague says that isn't enough tests. Which ages would you add, and why those?",
    "A full answer names the boundary ages (12, 13, 19, 20), and explains that bugs usually hide at the edges of a rule, such as > instead of >=, so ordinary values in the middle can pass even when the method is wrong.",
    {2: ("Names boundary ages (12/13 and 19/20) and says mistakes like > versus >= only show up at the boundaries, which typical values don't test.",
         ["I'd add 12, 13, 19 and 20. A mistake like using > instead of >= only shows up exactly at 13 or 19. 15, 8 and 40 would pass either way.",
          "The edges of the range: 12 and 20 just outside, 13 and 19 just inside. Bugs usually hide at the boundaries, and the middle values don't catch them."]),
     1: ("Suggests testing more or extreme ages, without naming the boundaries or saying why they matter.",
         ["Test more ages, like 0 and 100.", "Add some more tests."]),
     0: ("Incorrect, for example says three tests are always enough, or that more tests slow it down.",
         ["Three tests is plenty.", "Tests aren't needed if the method looks right."])})
print("5.5 written")
