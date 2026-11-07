from build import *

Lesson("j1-l4.2", "Tracing loops", ["J1.07"], [
    ("o1", "Complete a trace table for a loop, recording each variable after every pass"),
    ("o2", "Predict a loop's output and final values by tracing it"),
    ("o3", "Work out how many times a loop body runs"),
], ["j1-l4.1"], 30, ["R5", "R6", "R4"], r'''
## Before you start

You should be able to write a while loop ([while loops](j1-l4.1)) and trace variables in a table ([Variables and state](j1-l2.2)).

**Quick check.** When does a while loop check its condition?

<details><summary>Show the answer</summary>

Only at the start of each pass, never in the middle of one.

</details>

## Explanation

Loops are where programs get hard to follow in your head. The same few lines run again and again, with different values each time. The reliable way to understand a loop is to **trace** it: write down every variable's value, pass by pass.

Research on how people learn to program finds that beginners who can trace code accurately also tend to be better at writing it. Tracing is a skill worth practising on purpose, not something to skip.

### A trace table for a loop

Give the table one column per variable, plus one for the condition. Add a row each time the condition is checked:

```java
int total = 0;
int i = 1;
while (i <= 3) {
    total += i * i;
    i++;
}
```

| Check | `i` | `i <= 3`? | `total` after the pass |
|---|---|---|---|
| 1st | 1 | true | 0 + 1 = 1 |
| 2nd | 2 | true | 1 + 4 = 5 |
| 3rd | 3 | true | 5 + 9 = 14 |
| 4th | 4 | **false** | (loop ends) |

So `total` ends as 14, and the body ran **3** times. There's always **one more check than passes**: the last check is the one that comes out false.

### Counting passes without a full table

For a simple counting loop, you can count passes directly:

- `i` from 1 while `i <= n`, adding 1: **n** passes.
- `i` from 0 while `i < n`, adding 1: also **n** passes.
- `i` from 1 while `i < n`, adding 1: **n − 1** passes.

When in doubt, trace the first two passes and the last two.

### Tracing output

When the loop prints, write the output in its own column, so you can read it off at the end in order.

## Worked examples

### Example 1: a loop with two changing values

*Task: trace this, and give the output.*

```java runnable
void main() {
    int a = 1;
    int b = 1;
    while (b < 10) {
        int next = a + b;
        a = b;
        b = next;
        IO.print(b + " ");
    }
    IO.println();
}
```

**Step 1 — Columns for every variable,** including `next`, plus output.

**Step 2 — One row per pass, in order, using the values from the row before.**

| Pass | `next` | `a` | `b` | output |
|---|---|---|---|---|
| start | | 1 | 1 | |
| 1 | 2 | 1 | 2 | `2 ` |
| 2 | 3 | 2 | 3 | `3 ` |
| 3 | 5 | 3 | 5 | `5 ` |
| 4 | 8 | 5 | 8 | `8 ` |
| 5 | 13 | 8 | 13 | `13 ` |

**Step 3 — Check the condition after each pass.** After pass 4, `b` is 8 < 10, so there's another pass. After pass 5, `b` is 13, so the loop ends. Output: `2 3 5 8 13`.

### Example 2: how many passes?

*Task: how many times does the body run?*

```java
int n = 100;
while (n > 5) {
    n = n / 3;
}
```

**Step 1 — Trace `n` only.** 100 → 33 → 11 → 3.

**Step 2 — Count the arrows.** Three passes; at 3, `3 > 5` is false.

## Predict, then run

::exercise{id=j1-l4.2-predict-table}

::exercise{id=j1-l4.2-predict-passes}

## Where this is used

- **Code review**: reviewers trace loops in their heads to check edge cases, such as an empty list or a single item.
- **Debugging**: when a loop gives a wrong answer, tracing on paper (or printing values each pass) is usually the fastest way to find out why.
- **Interviews**: "what does this code print?" is a common job-interview question.

## Common mistakes

### Using values from the wrong pass

Each row must use the values **after** the previous row. Update in the order the statements run.

### Forgetting the final check

The last check, the one that's false, doesn't run the body, but it's still there. A loop that checks 4 times runs its body 3 times.

### Skipping the trace for "obvious" loops

Off-by-one mistakes hide in loops that look obvious. Trace at least the first and last passes.

## Practice

::exercise{id=j1-l4.2-predict-strings}

::exercise{id=j1-l4.2-write-collatz}

::exercise{id=j1-l4.2-explain-passes}

## Further reading

- **"Relationships between reading, tracing and writing skills in introductory programming"** (Lopez et al., 2008) `[R5]`: the study behind the claim that tracing and writing skills go together.

## How you'll be assessed

- The **predict** exercises check that you can trace loops accurately.
- The **write** exercise is a new kind of problem where you apply loops on your own (*applying to a new problem*).
- The **explain** exercise checks that you can reason about how many passes a loop makes (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l4.2")
ex.predict("j1-l4.2-predict-table", "Trace the total", ["o1", "o2"], ["J1.07"],
    "Draw a trace table with columns for `i` and `total`, then predict exactly what this prints.",
    '''
    void main() {
        int total = 0;
        int i = 2;
        while (i <= 8) {
            total += i;
            i += 3;
        }
        IO.println(total);
        IO.println(i);
    }
    ''', '''
    15
    11
    ''', ("i takes the values 2, 5, 8, then 11. Which of those pass the check?",
          "Passes with i = 2, 5 and 8 add up to 15. Then i becomes 11, which fails the check, so i is 11 at the end."), difficulty=2)

ex.predict("j1-l4.2-predict-passes", "How many times?", ["o3"], ["J1.07"],
    "Predict exactly what this prints. How many passes does each loop make?",
    '''
    void main() {
        int a = 0;
        int count = 0;
        while (a < 10) {
            a += 4;
            count++;
        }
        IO.println(count);

        int n = 64;
        int halvings = 0;
        while (n > 1) {
            n = n / 2;
            halvings++;
        }
        IO.println(halvings);
    }
    ''', '''
    3
    6
    ''', ("Trace just the variable in each condition: a goes 0, 4, 8, … and n goes 64, 32, …",
          "a: 4, 8, 12 is three passes. n: 32, 16, 8, 4, 2, 1 is six passes."), difficulty=2)

ex.predict("j1-l4.2-predict-strings", "Building a string", ["o1", "o2"], ["J1.07"],
    "Trace `word` and `i` pass by pass, then predict exactly what this prints.",
    '''
    void main() {
        String word = "";
        int i = 3;
        while (i > 0) {
            word = word + i;
            i--;
        }
        IO.println(word);
        IO.println(word.length());
    }
    ''', '''
    321
    3
    ''', ("Each pass joins the current i onto the end of word.", "i is 3, then 2, then 1, so word becomes \"3\", \"32\", \"321\"."), difficulty=1)

def collatz(n):
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps
ex.method("write", "j1-l4.2-write-collatz", "The 3n + 1 puzzle", ["o1", "o3"], ["J1.07"], ["XFER"],
    "Start with a whole number `n`. If it's even, halve it; if it's odd, multiply by 3 and add 1. Repeat until you reach 1. Mathematicians believe every starting number gets to 1 eventually, but nobody has proved it!\n\nComplete `steps` so it returns how many steps it takes to reach 1. For example, 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1 is 8 steps. `n` is always at least 1.",
    [("steps", [("n", "int")], "int")], {"steps": collatz},
    [(None, [6]), (None, [1]), (None, [8])],
    [(None, [2], "two"), (None, [3], "three"), (None, [7], "seven"), (None, [27], "twenty-seven"), (None, [97], "ninety-seven")],
    'int steps(int n) {\n    return 0; // replace this with a loop\n}\n\nvoid main() {\n    IO.println(steps(6)); // should print 8\n}\n',
    'int steps(int n) {\n    int count = 0;\n    while (n != 1) {\n        if (n % 2 == 0) {\n            n = n / 2;\n        } else {\n            n = 3 * n + 1;\n        }\n        count++;\n    }\n    return count;\n}\n\nvoid main() {\n    IO.println(steps(6)); // should print 8\n}\n',
    {"counts-the-one": 'int steps(int n) {\n    int count = 1;\n    while (n != 1) {\n        if (n % 2 == 0) {\n            n = n / 2;\n        } else {\n            n = 3 * n + 1;\n        }\n        count++;\n    }\n    return count;\n}\n\nvoid main() {\n}\n'},
    ("Loop while n isn't 1. Inside, decide even or odd with n % 2, update n, and count the step.",
     "while (n != 1) { if (n % 2 == 0) n = n / 2; else n = 3 * n + 1; count++; } return count;"), difficulty=3)

ex.explain("j1-l4.2-explain-passes", "Checks and passes", ["o3"], ["J1.07"],
    "This loop prints `Hi` three times. How many times is the condition `i < 3` checked? Explain how you know.\n\n```java\nint i = 0;\nwhile (i < 3) {\n    IO.println(\"Hi\");\n    i++;\n}\n```",
    "A full answer says the condition is checked 4 times: once before each of the 3 passes (i = 0, 1, 2, all true) and once more when i is 3, which is false and ends the loop.",
    {2: ("Says 4 checks, and explains that there is one check before each of the three passes plus a final false check when i is 3.",
         ["Four times. It's checked when i is 0, 1 and 2, which are true so it prints, and then when i is 3, which is false so the loop stops.",
          "4. There's always one more check than passes, because the last check is the one that fails and ends the loop."]),
     1: ("Gets the number right without a clear reason, or explains the final check but miscounts.",
         ["4 times.", "It checks once for each Hi and then once more, so 3."]),
     0: ("Says 3 (one check per pass) with no extra check, or another incorrect answer.",
         ["3 times, once for each Hi.", "Only once, at the start."])})
print("4.2 written")
