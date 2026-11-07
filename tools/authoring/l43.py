from build import *

Lesson("j1-l4.3", "for loops and boundaries", ["J1.07"], [
    ("o1", "Write a for loop that counts up or down in steps of any size"),
    ("o2", "Choose inclusive or exclusive bounds correctly, and say how many times a loop runs"),
    ("o3", "Use the loop variable inside the body"),
], ["j1-l4.2"], 35, ["R8", "R9"], r'''
## Before you start

You should be able to write and trace while loops ([while loops](j1-l4.1), [Tracing loops](j1-l4.2)).

**Quick check.** How many passes does a loop make with `i` starting at 0, while `i < 5`, adding 1 each pass?

<details><summary>Show the answer</summary>

5 passes: `i` is 0, 1, 2, 3 and 4.

</details>

## Explanation

Most loops you've written so far had the same shape: set up a counter, check it, update it. That's so common that Java has a loop that puts all three on one line: the `for` loop.

### The for loop

```java runnable
void main() {
    for (int i = 1; i <= 3; i++) {
        IO.println("Pass " + i);
    }
}
```

The brackets hold three parts, separated by semicolons:

| Part | Here | When it runs |
|---|---|---|
| Start | `int i = 1` | Once, before anything else |
| Condition | `i <= 3` | Before each pass; the loop stops when it's false |
| Update | `i++` | After each pass |

It does exactly what this while loop does:

```java
int i = 1;
while (i <= 3) {
    IO.println("Pass " + i);
    i++;
}
```

Use `for` when you know how many passes you need; use `while` when you're waiting for something to happen (like doubling until you pass a target).

The variable `i` only exists inside the loop. After the closing brace it's gone, so you can use `i` again in the next loop.

### Counting down and in steps

```java runnable
void main() {
    for (int i = 10; i >= 0; i -= 5) {
        IO.print(i + " ");
    }
    IO.println();
    for (int i = 0; i < 10; i += 3) {
        IO.print(i + " ");
    }
    IO.println();
}
```

This prints `10 5 0` and then `0 3 6 9`.

### Boundaries: `<` or `<=`?

The most common loop bug is running one pass too many or too few. These rules of thumb help:

| Loop | Values of `i` | Passes |
|---|---|---|
| `for (int i = 0; i < n; i++)` | 0 … n−1 | n |
| `for (int i = 1; i <= n; i++)` | 1 … n | n |
| `for (int i = 1; i < n; i++)` | 1 … n−1 | n−1 |

Starting at 0 with `<` is the most common form in Java, because string positions (and, soon, arrays) start at 0. To visit every character of a string, use `for (int i = 0; i < word.length(); i++)`. The last index is `length() - 1`, so `<=` would go one past the end and crash.

## Worked examples

### Example 1: multiples of a number

*Task: add up every multiple of `k` from 1 to `n`. With `n = 10` and `k = 3`: 3 + 6 + 9 = 18.*

**Step 1 — What should the loop variable be?** Option A: every number from 1 to n, and check if it's a multiple. Option B: only the multiples: start at `k`, step by `k`. B does less work.

**Step 2 — Get the boundary right.** `n` itself counts if it's a multiple, so use `<= n`.

**Step 3 — Use the loop variable in the body.**

```java runnable
int sumOfMultiples(int n, int k) {
    int total = 0;
    for (int m = k; m <= n; m += k) {
        total += m;
    }
    return total;
}

void main() {
    IO.println(sumOfMultiples(10, 3));
}
```

**Step 4 — Test a boundary.** `sumOfMultiples(9, 3)` should include 9: 3 + 6 + 9 = 18.

### Example 2: every character of a string

*Task: print a word with a dash between its letters: `J-a-v-a`.*

**Step 1 — Loop over the indexes,** 0 up to (not including) `length()`.

**Step 2 — Decide what happens on the first pass.** No dash before the first letter, so only add a dash when `i > 0`.

```java runnable
void main() {
    String word = "Java";
    String result = "";
    for (int i = 0; i < word.length(); i++) {
        if (i > 0) {
            result += "-";
        }
        result += word.charAt(i);
    }
    IO.println(result);
}
```

## Predict, then run

::exercise{id=j1-l4.3-predict-for}

## Where this is used

- **Processing every item**: every character of a message, every line of a file, every pixel of an image.
- **Fixed repetitions**: retry a connection three times; run a test 1,000 times.
- **Tables and charts**: one pass per row.

## Common mistakes

:::mistake{id=MC09}
**One pass too many or too few.** `i <= word.length()` goes one past the last index and crashes. `i < n` when you meant to include `n` misses the last value. Trace the first and last passes.
:::

### A semicolon after the brackets

`for (int i = 0; i < 3; i++);` runs an empty loop three times, and then the block after it runs once. As with `if`, there's never a semicolon before the `{`.

### Changing the loop variable inside the body

Changing `i` inside the body as well as in the update makes the loop very hard to follow. Let the update do it.

## Practice

::exercise{id=j1-l4.3-write-multiples}

::exercise{id=j1-l4.3-debug-boundary}

::exercise{id=j1-l4.3-modify-table}

::exercise{id=j1-l4.3-explain-bounds}

## Further reading

- **"37 Million Compilations"** (Altadmri & Brown, 2015) `[R9]`: a study of real beginner Java mistakes, including stray semicolons after `if` and `for` headers.

## How you'll be assessed

- The **predict** exercise checks that you can follow for loops with different steps.
- The **write**, **debug** and **modify** exercises check that you can write a for loop, fix its boundary, and change what it produces.
- The **explain** exercise checks that you can reason about `<` and `<=`.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l4.3")
ex.predict("j1-l4.3-predict-for", "Steps and boundaries", ["o1", "o2"], ["J1.07"],
    "Predict exactly what this program prints.",
    '''
    void main() {
        for (int i = 0; i < 4; i++) {
            IO.print(i);
        }
        IO.println();
        for (int i = 5; i > 0; i -= 2) {
            IO.print(i);
        }
        IO.println();
        int count = 0;
        for (int i = 1; i <= 10; i += 4) {
            count++;
        }
        IO.println(count);
    }
    ''', '''
    0123
    531
    3
    ''', ("For each loop, list the values the variable takes before the condition fails.",
          "0, 1, 2, 3 (4 fails). 5, 3, 1 (-1 fails). 1, 5, 9 (13 fails) is three passes."), misconceptions=["MC09"], difficulty=2)

def mult(n, k): return sum(range(k, n + 1, k))
ex.method("write", "j1-l4.3-write-multiples", "Multiples", ["o1", "o3"], ["J1.07"], ["IMPL"],
    "Complete `sumOfMultiples` so it returns the sum of every multiple of `k` from 1 up to and including `n`. For example, `sumOfMultiples(10, 3)` is 3 + 6 + 9 = 18. `k` is always at least 1.",
    [("sumOfMultiples", [("n", "int"), ("k", "int")], "int")], {"sumOfMultiples": mult},
    [(None, [10, 3]), (None, [10, 5]), (None, [2, 3])],
    [(None, [9, 3], "n is a multiple"), (None, [10, 1], "every number"), (None, [100, 7], "sevens"), (None, [0, 4], "n is zero"), (None, [5, 5], "exactly k")],
    'int sumOfMultiples(int n, int k) {\n    return 0; // replace this with a for loop\n}\n\nvoid main() {\n    IO.println(sumOfMultiples(10, 3)); // should print 18\n}\n',
    'int sumOfMultiples(int n, int k) {\n    int total = 0;\n    for (int m = k; m <= n; m += k) {\n        total += m;\n    }\n    return total;\n}\n\nvoid main() {\n    IO.println(sumOfMultiples(10, 3)); // should print 18\n}\n',
    {"excludes-n": 'int sumOfMultiples(int n, int k) {\n    int total = 0;\n    for (int m = k; m < n; m += k) {\n        total += m;\n    }\n    return total;\n}\n\nvoid main() {\n}\n'},
    ("You can step straight from one multiple to the next. Where does the loop start, and what's the step?",
     "for (int m = k; m <= n; m += k) { total += m; }"), group="for-sums")

def odds(n): return sum(range(1, n + 1, 2))
ex.method("write", "j1-l4.3-retrieve-odds", "Odd numbers", ["o1", "o3"], ["J1.07"], ["IMPL"],
    "Complete `sumOfOdds` so it returns the sum of every odd number from 1 up to and including `n`. For example, `sumOfOdds(7)` is 1 + 3 + 5 + 7 = 16.",
    [("sumOfOdds", [("n", "int")], "int")], {"sumOfOdds": odds},
    [(None, [7]), (None, [1]), (None, [10])],
    [(None, [0], "zero"), (None, [2], "two"), (None, [99], "ninety-nine"), (None, [100], "a hundred"), (None, [5], "five")],
    'int sumOfOdds(int n) {\n    return 0; // replace this with a for loop\n}\n\nvoid main() {\n    IO.println(sumOfOdds(7)); // should print 16\n}\n',
    'int sumOfOdds(int n) {\n    int total = 0;\n    for (int i = 1; i <= n; i += 2) {\n        total += i;\n    }\n    return total;\n}\n\nvoid main() {\n    IO.println(sumOfOdds(7)); // should print 16\n}\n',
    {"excludes-n": 'int sumOfOdds(int n) {\n    int total = 0;\n    for (int i = 1; i < n; i += 2) {\n        total += i;\n    }\n    return total;\n}\n\nvoid main() {\n}\n'},
    ("Start at 1 and step by 2: that only ever visits odd numbers.", "for (int i = 1; i <= n; i += 2) { total += i; }"),
    role="retrieval", group="for-sums")

def fact(n): return math.factorial(n)
ex.method("write", "j1-l4.3-retrieve-factorial", "Factorials", ["o1", "o3"], ["J1.07"], ["IMPL"],
    "The factorial of n is 1 × 2 × 3 × … × n. For example, the factorial of 4 is 24. The factorial of 0 is defined as 1. Complete `factorial` for any `n` from 0 to 12.",
    [("factorial", [("n", "int")], "int")], {"factorial": fact},
    [(None, [4]), (None, [1]), (None, [0])],
    [(None, [5], "five"), (None, [10], "ten"), (None, [12], "twelve"), (None, [2], "two"), (None, [3], "three")],
    'int factorial(int n) {\n    return 0; // replace this with a for loop\n}\n\nvoid main() {\n    IO.println(factorial(4)); // should print 24\n}\n',
    'int factorial(int n) {\n    int result = 1;\n    for (int i = 2; i <= n; i++) {\n        result *= i;\n    }\n    return result;\n}\n\nvoid main() {\n    IO.println(factorial(4)); // should print 24\n}\n',
    {"starts-at-zero": 'int factorial(int n) {\n    int result = 0;\n    for (int i = 1; i <= n; i++) {\n        result *= i;\n    }\n    return result;\n}\n\nvoid main() {\n}\n'},
    ("You're multiplying, not adding. What should the running result start at?", "int result = 1; for (int i = 2; i <= n; i++) { result *= i; }"),
    role="retrieval", group="for-sums")

def count_spaces(s): return s.count(" ")
ex.method("debug", "j1-l4.3-debug-boundary", "The missing space", ["o2"], ["J1.07"], ["DEBUG"],
    "`countSpaces` should count the spaces in a message. It gets most messages right, but it misses a space at the very start. Find and fix the bug.",
    [("countSpaces", [("message", "String")], "int")], {"countSpaces": count_spaces},
    [(None, ["a b c"]), (None, [" hello"]), (None, ["none"])],
    [(None, [""], "empty"), (None, [" "], "just a space"), (None, ["ends with "], "space at the end"), (None, ["  two at start"], "two at the start"), (None, ["one two three four"], "several")],
    "int countSpaces(String message) {\n    int count = 0;\n    for (int i = 1; i < message.length(); i++) {\n        if (message.charAt(i) == ' ') {\n            count++;\n        }\n    }\n    return count;\n}\n\nvoid main() {\n    IO.println(countSpaces(\" hello\")); // should print 1\n}\n",
    "int countSpaces(String message) {\n    int count = 0;\n    for (int i = 0; i < message.length(); i++) {\n        if (message.charAt(i) == ' ') {\n            count++;\n        }\n    }\n    return count;\n}\n\nvoid main() {\n    IO.println(countSpaces(\" hello\")); // should print 1\n}\n",
    {"one-too-far": "int countSpaces(String message) {\n    int count = 0;\n    for (int i = 0; i <= message.length(); i++) {\n        if (message.charAt(i) == ' ') {\n            count++;\n        }\n    }\n    return count;\n}\n\nvoid main() {\n}\n"},
    ("What is the index of the first character of a string? Where does this loop start?", "Indexes start at 0. Start the loop at int i = 0."),
    misconceptions=["MC09"])

def table_out(stdin):
    return "\n".join(f"7 x {i} = {7 * i}" for i in range(1, 13))
ex.io("modify", "j1-l4.3-modify-table", "The full times table", ["o1", "o3"], ["J1.07"], ["MOD"],
    "This program prints the 7 times table from 1 to 10, one number per line. Change it to print the table from 1 to **12**, in the form `7 x 3 = 21`.",
    table_out, [("prints the full table", "")], [],
    'void main() {\n    for (int i = 1; i <= 10; i++) {\n        IO.println(7 * i);\n    }\n}\n',
    'void main() {\n    for (int i = 1; i <= 12; i++) {\n        IO.println("7 x " + i + " = " + (7 * i));\n    }\n}\n',
    {"stops-at-11": 'void main() {\n    for (int i = 1; i < 12; i++) {\n        IO.println("7 x " + i + " = " + (7 * i));\n    }\n}\n'},
    ("Two changes: how far the loop goes, and what each line prints.",
     "Use i <= 12, and print \"7 x \" + i + \" = \" + (7 * i)."))

ex.explain("j1-l4.3-explain-bounds", "Why less than?", ["o2"], ["J1.07"],
    "To visit every character of `word`, a learner wrote `for (int i = 0; i <= word.length(); i++)`. It crashes. Explain why, and why `i < word.length()` is right.",
    "A full answer says indexes run from 0 to length() - 1, so with <= the loop reaches i == length(), an index that doesn't exist, and charAt crashes; with < the last value of i is length() - 1, the last character.",
    {2: ("Explains that the last index is length() - 1, so <= makes i reach length(), which is past the end and crashes charAt, while < stops at the last real index.",
         ["Indexes go from 0 to length - 1. With <= the loop also runs with i equal to length, and there's no character there, so charAt fails. With < the last i is length - 1.",
          "For \"cat\", length is 3 but the indexes are 0, 1, 2. i <= 3 would try charAt(3), which doesn't exist. i < 3 stops at 2."]),
     1: ("Says it goes one too far, without explaining that indexes end at length() - 1.",
         ["<= goes one too far.", "Because it should be < not <=."]),
     0: ("Incorrect, for example blames starting at 0.",
         ["It should start at 1 instead of 0.", "length() is wrong, you should use size()."])},
    misconceptions=["MC09"])
print("4.3 written")
