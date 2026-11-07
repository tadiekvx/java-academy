from build import *

Lesson("j1-l4.1", "while loops", ["J1.07"], [
    ("o1", "Write a while loop with a condition and an update that eventually makes it stop"),
    ("o2", "Explain that a while loop checks its condition only at the start of each pass"),
    ("o3", "Recognise a loop that never ends, and fix it"),
], ["j1-l3.3"], 35, ["R8", "R5"], r'''
## Before you start

You should be able to write conditions and `if` statements ([Making decisions](j1-l3.3)).

**Quick check.** After `int n = 3; n = n * 2;`, what is `n`?

<details><summary>Show the answer</summary>

`6`. The right side is worked out with the old value, 3, then stored back into `n`.

</details>

## Explanation

Computers are good at doing the same thing many times. A **loop** repeats a block of statements. The simplest is the `while` loop.

### The shape of a while loop

```java runnable
void main() {
    int count = 1;
    while (count <= 3) {
        IO.println("Pass " + count);
        count = count + 1;
    }
    IO.println("Done");
}
```

This prints `Pass 1`, `Pass 2`, `Pass 3`, then `Done`. Here's what happens:

1. Check the condition, `count <= 3`. If it's true, run the body (the statements in the braces).
2. Go back to step 1.
3. When the condition is false, skip the body and carry on after the loop.

Each run of the body is called a **pass** (or **iteration**). Every working while loop has three parts:

| Part | Here | Job |
|---|---|---|
| Start | `int count = 1;` | Set things up before the loop |
| Condition | `count <= 3` | Decide whether to do another pass |
| Update | `count = count + 1;` | Change something so the condition will eventually be false |

### The condition is checked at the start of each pass

Java checks the condition **only at the top**, before each pass, not continuously. If it becomes false halfway through the body, the rest of the body still runs, and the loop ends only when Java next gets back to the check:

```java runnable
void main() {
    int n = 1;
    while (n < 3) {
        n = n + 5;
        IO.println("n is " + n);
    }
}
```

After `n = n + 5`, `n` is 6, so the condition is already false, but `IO.println` still runs. The loop prints `n is 6` once and then stops.

If the condition is false the very first time, the body doesn't run at all.

### Loops that never end

If the update is missing, or never moves towards making the condition false, the loop runs forever:

```java
int count = 1;
while (count <= 3) {
    IO.println("Pass " + count);
    // forgot: count = count + 1;
}
```

`count` stays 1 forever. In this course, the runner stops any program that takes more than a few seconds, and reports it as **taking too long**. When that happens, check the update.

### Shortcuts for updating

You'll often see these shorter forms:

| Short form | Means |
|---|---|
| `count++;` | `count = count + 1;` |
| `count--;` | `count = count - 1;` |
| `total += 5;` | `total = total + 5;` |
| `n *= 2;` | `n = n * 2;` |

They do exactly the same thing; use whichever reads more clearly to you.

## Worked examples

### Example 1: adding up to a number

*Task: add up 1 + 2 + … + n.*

**Step 1 — What changes each pass?** The number being added (call it `i`) and the running total.

**Step 2 — Set them up.** `i` starts at 1; `total` starts at 0.

**Step 3 — Condition and update.** Keep going while `i <= n`; each pass adds `i` to `total`, then moves `i` on by 1.

```java runnable
int sumUpTo(int n) {
    int total = 0;
    int i = 1;
    while (i <= n) {
        total += i;
        i++;
    }
    return total;
}

void main() {
    IO.println(sumUpTo(4));
}
```

**Step 4 — Check a small case by hand.** For 4: 1 + 2 + 3 + 4 = 10. It prints `10`.

### Example 2: how many doublings?

*Task: a pond's lily pads double every day. Starting from `start` pads, how many days until there are at least `target`?*

**Step 1 — You don't know how many passes you need.** That's exactly when a while loop fits: keep going *while* there are fewer than `target`.

**Step 2 — Count the passes.** Each pass is one day: double the pads and add one to `days`.

```java runnable
int daysToReach(int start, int target) {
    int pads = start;
    int days = 0;
    while (pads < target) {
        pads *= 2;
        days++;
    }
    return days;
}

void main() {
    IO.println(daysToReach(3, 20));
}
```

**Step 3 — Trace it.** 3 → 6 (1 day) → 12 (2) → 24 (3). 24 isn't less than 20, so the loop stops. It prints `3`.

## Predict, then run

::exercise{id=j1-l4.1-predict-while}

## Where this is used

- **Games** run a main loop: *while the game isn't over*, read input, update, draw.
- **Servers** loop *while they're running*, handling one request after another.
- **Waiting**: retry a download *while* it keeps failing, up to a limit.

## Common mistakes

:::mistake{id=MC10}
**Thinking the loop stops the moment the condition becomes false.** The condition is only checked at the top of each pass, so the rest of the current pass still runs.
:::

### No update, or the wrong update

If nothing in the body moves the condition towards false, the loop never ends. Check that the variable in the condition changes, and in the right direction.

### Off by one

`while (i < n)` and `while (i <= n)` differ by one pass. Trace the first and last passes to check.

## Practice

::exercise{id=j1-l4.1-write-doublings}

::exercise{id=j1-l4.1-debug-forever}

::exercise{id=j1-l4.1-modify-countdown}

::exercise{id=j1-l4.1-explain-check}

## Further reading

- **"Students' misconceptions and other difficulties in introductory programming"** (Qian & Lehman, 2017) `[R8]`: the misconception about when loops stop is one of the most commonly reported.

## How you'll be assessed

- The **predict** exercise checks that you can follow a loop pass by pass.
- The **write** exercise checks that you can write a loop that counts passes (*implementation*).
- The **debug** exercise checks that you can fix a loop that never ends (*debugging*).
- The **modify** and **explain** exercises check that you can change a loop, and say when its condition is checked.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l4.1")
ex.predict("j1-l4.1-predict-while", "Pass by pass", ["o1", "o2"], ["J1.07"],
    "Trace this loop pass by pass, then predict exactly what it prints.",
    '''
    void main() {
        int n = 1;
        while (n < 20) {
            n = n * 3;
            IO.println(n);
        }
        IO.println("end " + n);
    }
    ''', '''
    3
    9
    27
    end 27
    ''', ("The condition is only checked at the top. What is n just before each check?",
          "n goes 1, 3, 9, 27. When n becomes 27 the println still runs, and only then is 27 < 20 checked."),
    misconceptions=["MC10"], difficulty=2)

def doublings(start, target):
    days = 0
    while start < target:
        start *= 2
        days += 1
    return days
ex.method("write", "j1-l4.1-write-doublings", "Doubling savings", ["o1"], ["J1.07"], ["IMPL"],
    "A savings scheme doubles your money every year. Complete `yearsToReach` so it returns how many years it takes for `start` pounds to reach at least `target` pounds. If `start` is already at least `target`, the answer is 0. `start` is always at least 1.",
    [("yearsToReach", [("start", "int"), ("target", "int")], "int")], {"yearsToReach": doublings},
    [(None, [100, 400]), (None, [3, 20]), (None, [50, 50])],
    [(None, [1, 1000], "from 1"), (None, [100, 101], "just over"), (None, [500, 100], "already there"), (None, [7, 7], "exactly equal"), (None, [10, 1000000], "a million")],
    'int yearsToReach(int start, int target) {\n    return 0; // replace this with a while loop\n}\n\nvoid main() {\n    IO.println(yearsToReach(100, 400)); // should print 2\n}\n',
    'int yearsToReach(int start, int target) {\n    int money = start;\n    int years = 0;\n    while (money < target) {\n        money *= 2;\n        years++;\n    }\n    return years;\n}\n\nvoid main() {\n    IO.println(yearsToReach(100, 400)); // should print 2\n}\n',
    {"one-too-many": 'int yearsToReach(int start, int target) {\n    int money = start;\n    int years = 0;\n    while (money <= target) {\n        money *= 2;\n        years++;\n    }\n    return years;\n}\n\nvoid main() {\n}\n'},
    ("Keep doubling while the money is below the target, counting each pass.",
     "int money = start; int years = 0; while (money < target) { money *= 2; years++; } return years;"),
    group="while-counting")

def halvings(n):
    c = 0
    while n > 1:
        n //= 2
        c += 1
    return c
ex.method("write", "j1-l4.1-retrieve-halvings", "Halving until one", ["o1"], ["J1.07"], ["IMPL"],
    "Complete `halvings` so it returns how many times you can halve `n` (with integer division, `n / 2`) before it reaches 1. For example, 8 → 4 → 2 → 1 is 3 halvings. `n` is always at least 1.",
    [("halvings", [("n", "int")], "int")], {"halvings": halvings},
    [(None, [8]), (None, [1]), (None, [10])],
    [(None, [2], "two"), (None, [3], "three"), (None, [1024], "1024"), (None, [1000], "a thousand"), (None, [7], "seven")],
    'int halvings(int n) {\n    return 0; // replace this with a while loop\n}\n\nvoid main() {\n    IO.println(halvings(8)); // should print 3\n}\n',
    'int halvings(int n) {\n    int count = 0;\n    while (n > 1) {\n        n = n / 2;\n        count++;\n    }\n    return count;\n}\n\nvoid main() {\n    IO.println(halvings(8)); // should print 3\n}\n',
    {"until-zero": 'int halvings(int n) {\n    int count = 0;\n    while (n > 0) {\n        n = n / 2;\n        count++;\n    }\n    return count;\n}\n\nvoid main() {\n}\n'},
    ("Keep halving while n is greater than 1, counting the passes.", "while (n > 1) { n = n / 2; count++; } return count;"),
    role="retrieval", group="while-counting")

def digit_count(n):
    c = 1
    while n >= 10:
        n //= 10
        c += 1
    return c
ex.method("write", "j1-l4.1-retrieve-digits", "Counting digits", ["o1"], ["J1.07"], ["IMPL"],
    "Complete `digitCount` so it returns how many digits a whole number has. For example, 4071 has 4 digits, and 0 has 1. `n` is never negative. Hint: dividing by 10 removes the last digit.",
    [("digitCount", [("n", "int")], "int")], {"digitCount": digit_count},
    [(None, [4071]), (None, [7]), (None, [0])],
    [(None, [10], "ten"), (None, [99], "ninety-nine"), (None, [100], "a hundred"), (None, [123456789], "nine digits"), (None, [9], "nine")],
    'int digitCount(int n) {\n    return 0; // replace this with a while loop\n}\n\nvoid main() {\n    IO.println(digitCount(4071)); // should print 4\n}\n',
    'int digitCount(int n) {\n    int count = 1;\n    while (n >= 10) {\n        n = n / 10;\n        count++;\n    }\n    return count;\n}\n\nvoid main() {\n    IO.println(digitCount(4071)); // should print 4\n}\n',
    {"zero-has-none": 'int digitCount(int n) {\n    int count = 0;\n    while (n > 0) {\n        n = n / 10;\n        count++;\n    }\n    return count;\n}\n\nvoid main() {\n}\n'},
    ("Every number has at least one digit. How many times can you remove a digit while the number is 10 or more?",
     "Start count at 1; while (n >= 10) { n = n / 10; count++; }"),
    role="retrieval", group="while-counting")

def sum_to(n): return n * (n + 1) // 2
ex.method("debug", "j1-l4.1-debug-forever", "The loop that never ends", ["o3"], ["J1.07"], ["DEBUG"],
    "`sumUpTo` should return 1 + 2 + … + n. When you check it against the tests, every test takes too long. Find and fix the bug.",
    [("sumUpTo", [("n", "int")], "int")], {"sumUpTo": sum_to},
    [(None, [4]), (None, [1]), (None, [0])],
    [(None, [10], "ten"), (None, [100], "a hundred"), (None, [2], "two"), (None, [3], "three"), (None, [50], "fifty")],
    'int sumUpTo(int n) {\n    int total = 0;\n    int i = 1;\n    while (i <= n) {\n        total += i;\n    }\n    return total;\n}\n\nvoid main() {\n    IO.println(sumUpTo(4)); // should print 10\n}\n',
    'int sumUpTo(int n) {\n    int total = 0;\n    int i = 1;\n    while (i <= n) {\n        total += i;\n        i++;\n    }\n    return total;\n}\n\nvoid main() {\n    IO.println(sumUpTo(4)); // should print 10\n}\n',
    {"stops-early": 'int sumUpTo(int n) {\n    int total = 0;\n    int i = 1;\n    while (i < n) {\n        total += i;\n        i++;\n    }\n    return total;\n}\n\nvoid main() {\n}\n'},
    ("Which variable is in the condition? Does anything in the body change it?", "i never changes, so i <= n stays true. Add i++; inside the loop."),
    notes="Bug: no update to `i`, so the loop never ends and every test times out.")

def countdown_out(stdin): return "10\n8\n6\n4\n2\nGo!"
ex.io("modify", "j1-l4.1-modify-countdown", "Count down in twos", ["o1"], ["J1.07"], ["MOD"],
    "This program counts down from 10 to 1 and then prints `Go!`. Change it to count down **in twos**: it should print `10`, `8`, `6`, `4`, `2`, then `Go!`.",
    countdown_out, [("counts down in twos", "")], [],
    'void main() {\n    int n = 10;\n    while (n >= 1) {\n        IO.println(n);\n        n--;\n    }\n    IO.println("Go!");\n}\n',
    'void main() {\n    int n = 10;\n    while (n >= 1) {\n        IO.println(n);\n        n -= 2;\n    }\n    IO.println("Go!");\n}\n',
    {"skips-ten": 'void main() {\n    int n = 10;\n    while (n >= 1) {\n        n -= 2;\n        IO.println(n);\n    }\n    IO.println("Go!");\n}\n'},
    ("Which line decides how far n moves each pass?", "Change n--; to n -= 2;"))

ex.explain("j1-l4.1-explain-check", "When is the condition checked?", ["o2"], ["J1.07"],
    "In this loop, `n` becomes 6 on the first pass, which makes `n < 3` false. Explain why `n is 6` is still printed.\n\n```java\nint n = 1;\nwhile (n < 3) {\n    n = n + 5;\n    IO.println(\"n is \" + n);\n}\n```",
    "A full answer says the condition is only checked at the start of each pass, not continuously, so once the body starts it runs to the end; the loop only stops at the next check.",
    {2: ("Explains that the condition is checked only at the top of each pass, so the whole body runs even after n becomes 6, and the loop stops at the next check.",
         ["The while condition is only checked before each pass. When n is 1 the check passes, so the whole body runs, including the println, even though n is now 6. It stops when it checks again.",
          "Java doesn't watch the condition all the time. It checks n < 3 at the start, then runs the full body. The next check sees 6 and ends the loop."]),
     1: ("Says something partly right, such as the body finishes first, without clearly saying the check only happens at the start of each pass.",
         ["Because the println is still in the loop.", "It has to finish the loop first."]),
     0: ("Incorrect, for example says the loop runs twice, or that it stops immediately when n changes.",
         ["It prints because n < 3 is still true.", "The loop stops straight away when n becomes 6, so it shouldn't print."])},
    misconceptions=["MC10"])
print("4.1 written")
