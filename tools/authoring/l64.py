from build import *

Lesson("j1-l6.4", "Exceptions and stack traces", ["J1.12"], [
    ("o1", "Read a stack trace: the exception type, the message, and the line in your own code"),
    ("o2", "Recognise ArrayIndexOutOfBoundsException, ArithmeticException, NumberFormatException and NullPointerException and their usual causes"),
    ("o3", "Prevent a crash by checking the condition that would cause it"),
], ["j1-l6.3"], 35, ["R8", "R16", "I4"], r'''
## Before you start

You should know that a program can compile and still crash while it runs ([Errors are feedback](j1-l1.2)).

**Quick check.** Does a compile error or a runtime error happen before the program starts?

<details><summary>Show the answer</summary>

A compile error. Runtime errors happen while the program is running.

</details>

## Explanation

When something impossible happens while a program runs, such as dividing by zero or reading past the end of an array, Java **throws an exception** and, unless the program deals with it, stops. It prints a **stack trace**: a report of what went wrong and where. This lesson is about reading one calmly, because it tells you almost exactly where to look.

### Anatomy of a stack trace

```java
int average(int[] marks) {
    int total = 0;
    for (int i = 0; i <= marks.length; i++) {
        total += marks[i];
    }
    return total / marks.length;
}

void report(int[] marks) {
    IO.println("Average: " + average(marks));
}

void main() {
    int[] marks = {70, 80, 90};
    report(marks);
}
```

Running it prints:

```
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 3 out of bounds for length 3
	at Main.average(Main.java:4)
	at Main.report(Main.java:10)
	at Main.main(Main.java:15)
```

| Part | Meaning |
|---|---|
| `java.lang.ArrayIndexOutOfBoundsException` | The **type** of problem: an index outside the array |
| `Index 3 out of bounds for length 3` | The **message**: which index, and the array's length |
| `at Main.average(Main.java:4)` | **Where it happened**: method `average`, file `Main.java`, line 4 |
| the `at` lines below | **How it got there**: the call stack, newest first. `average` was called by `report` (line 10), which was called by `main` (line 15) |

Line 4 is `total += marks[i];`. The message says index 3 in an array of length 3, whose last index is 2: the loop's `i <= marks.length` is one too far, the mistake from [Arrays](j1-l6.1).

### Where to look first

Read the **first line** for the type and message, then find the **first `at` line that mentions your own file** (here `Main.java`). That's the line in your code where the problem showed up. Sometimes the very first `at` lines are inside Java's own library code (they mention `java.base`); skip those and keep going down to the first one in your code. The line it points at is where the program *noticed* the problem; the real mistake may be a little earlier, such as a wrong value passed in.

### Four exceptions you'll meet constantly

| Exception | What it means | Usual cause | Prevention |
|---|---|---|---|
| `ArrayIndexOutOfBoundsException` (and `StringIndexOutOfBoundsException`, `IndexOutOfBoundsException` for lists) | Index not in `0` to `length - 1` | A loop that goes one too far; an empty array or string | Check `i < length`; check for empty first |
| `ArithmeticException: / by zero` | Whole-number division or remainder by 0 | A count that can be 0 | `if (divisor != 0)` before dividing |
| `NumberFormatException` | Text isn't a number | Unchecked input, as in [Input validation loops](j1-l4.5) | Check the digits first |
| `NullPointerException` | Using something that is `null`, i.e. refers to nothing | A variable that was never given an object; `IO.readln` returning `null` at the end of input | Check `!= null` before using it |

A `NullPointerException` message names what was null. In this course's runner, a variable may appear as something like `<local1>` rather than its name: count the local variables from the top of the method to see which one it means.

### Preventing, not just fixing

The best fix removes the cause. If an average of an empty array would divide by zero, check for empty first:

```java runnable
double safeAverage(int[] values) {
    if (values.length == 0) {
        return 0;
    }
    int total = 0;
    for (int value : values) {
        total += value;
    }
    return (double) total / values.length;
}

void main() {
    IO.println(safeAverage(new int[] {70, 80, 90}));
    IO.println(safeAverage(new int[] {}));
}
```

This prints `80.0` and `0.0`. (Java also lets a program **catch** an exception and carry on; that's part of Stage 2. In this stage, prevent them with checks.)

## Worked examples

### Example 1: read a trace

*Task: what's wrong here, and where do you look?*

```
Exception in thread "main" java.lang.ArithmeticException: / by zero
	at Main.share(Main.java:3)
	at Main.main(Main.java:8)
```

**Step 1 — The type and message.** `ArithmeticException: / by zero`: a division by 0.

**Step 2 — The first line in your code.** `Main.java:3`, in method `share`. Look at the division on line 3.

**Step 3 — Why was the divisor 0?** `main` called `share` at line 8. Check what it passed in.

### Example 2: fixing the cause

*Task: `firstWord("hello")` crashes with `StringIndexOutOfBoundsException`. Find the cause.*

```java
String firstWord(String text) {
    int space = text.indexOf(" ");
    return text.substring(0, space);
}
```

**Step 1 — Trace `"hello"`.** There's no space, so `indexOf` gives -1.

**Step 2 — `substring(0, -1)` is invalid,** hence the exception.

**Step 3 — Handle the "no space" case explicitly.**

```java runnable
String firstWord(String text) {
    int space = text.indexOf(" ");
    if (space == -1) {
        return text;
    }
    return text.substring(0, space);
}

void main() {
    IO.println(firstWord("hello world"));
    IO.println(firstWord("hello"));
}
```

## Predict, then run

::exercise{id=j1-l6.4-predict-safe}

## Where this is used

- **Every bug report** includes a stack trace, and the first skill of a professional developer is reading one.
- **Logs**: servers print stack traces when something fails, and engineers read them to find the cause.
- **Interviews**: "what does this exception mean?" is a standard question.

## Common mistakes

:::mistake{id=MC15}
**Assuming the first `at` line is always your code.** Sometimes the top lines are inside Java's library. Look down for the first line that names your file.
:::

### Fixing the symptom, not the cause

Wrapping an access in a check that hides the problem is worse than finding out why the bad value got there. Trace back to where it came from.

### Ignoring the message

The message usually says exactly which index or which text. Read it before you read the code.

## Practice

::exercise{id=j1-l6.4-debug-last}

::exercise{id=j1-l6.4-debug-percentage}

::exercise{id=j1-l6.4-debug-firstword}

::exercise{id=j1-l6.4-explain-trace}

## Further reading

- **"Debugging: a review of the literature from an educational perspective"** (McCauley et al., 2008) `[R16]`: how people learn to diagnose errors, including reading error messages.

## How you'll be assessed

- The **predict** exercise checks that you can follow code that prevents a crash.
- The **debug** exercises check that you can find and prevent a crash from the exception type (*debugging*).
- The **explain** exercise checks that you can read a stack trace (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l6.4")
ex.predict("j1-l6.4-predict-safe", "Checked before it crashes", ["o3"], ["J1.12"],
    "Predict exactly what this program prints. Nothing here should crash: work out which checks protect the risky lines.",
    '''
    int safeDivide(int a, int b) {
        if (b == 0) {
            return 0;
        }
        return a / b;
    }

    char firstLetter(String text) {
        if (text.isEmpty()) {
            return '?';
        }
        return text.charAt(0);
    }

    void main() {
        IO.println(safeDivide(12, 4));
        IO.println(safeDivide(12, 0));
        IO.println(firstLetter("Java"));
        IO.println(firstLetter(""));
    }
    ''', '''
    3
    0
    J
    ?
    ''', ("Each method checks the dangerous case first and returns a fallback.", "b == 0 gives 0 without dividing; an empty text gives '?' without calling charAt."), difficulty=1)

ex.method("debug", "j1-l6.4-debug-last", "The last element", ["o1", "o2", "o3"], ["J1.12"], ["DEBUG"],
    "`lastElement` should return the last element of an array, or -1 if the array is empty. It crashes with an `ArrayIndexOutOfBoundsException` for every array. Find and fix the bug.",
    [("lastElement", [("values", "int[]")], "int")], {"lastElement": lambda v: v[-1] if v else -1},
    [(None, [[4, 8, 15]]), (None, [[]]), (None, [[7]])],
    [(None, [[1, 2]], "two"), (None, [[0]], "zero"), (None, [[9, 9, 9, 5]], "ends differently"), (None, [[-3, -2, -1]], "negatives"), (None, [[10, 20, 30, 40, 50]], "five")],
    'int lastElement(int[] values) {\n    return values[values.length];\n}\n\nvoid main() {\n    IO.println(lastElement(new int[] {4, 8, 15})); // should print 15\n}\n',
    'int lastElement(int[] values) {\n    if (values.length == 0) {\n        return -1;\n    }\n    return values[values.length - 1];\n}\n\nvoid main() {\n    IO.println(lastElement(new int[] {4, 8, 15})); // should print 15\n}\n',
    {"first-not-last": 'int lastElement(int[] values) {\n    if (values.length == 0) {\n        return -1;\n    }\n    return values[0];\n}\n\nvoid main() {\n}\n'},
    ("What is the last valid index? And what does the empty array need?", "Use values[values.length - 1], after checking for an empty array."),
    group="exceptions", misconceptions=["MC15"])

ex.method("debug", "j1-l6.4-debug-percentage", "Nothing to divide by", ["o2", "o3"], ["J1.12"], ["DEBUG"],
    "`percentage` should return the percentage `part` makes of `total` (a whole number, rounded down). If `total` is 0, it should return 0. It crashes with an `ArithmeticException` when `total` is 0. Find and fix the bug.",
    [("percentage", [("part", "int"), ("total", "int")], "int")], {"percentage": lambda p, t: 0 if t == 0 else p * 100 // t},
    [(None, [1, 4]), (None, [0, 10]), (None, [5, 0])],
    [(None, [0, 0], "both zero"), (None, [10, 10], "all of it"), (None, [1, 3], "a third"), (None, [3, 4], "three quarters"), (None, [7, 0], "nothing to divide by")],
    'int percentage(int part, int total) {\n    return part * 100 / total;\n}\n\nvoid main() {\n    IO.println(percentage(1, 4)); // should print 25\n}\n',
    'int percentage(int part, int total) {\n    if (total == 0) {\n        return 0;\n    }\n    return part * 100 / total;\n}\n\nvoid main() {\n    IO.println(percentage(1, 4)); // should print 25\n}\n',
    {"always-zero": 'int percentage(int part, int total) {\n    return 0;\n}\n\nvoid main() {\n}\n'},
    ("Which input makes the division impossible?", "Check total == 0 first and return 0."), group="exceptions", difficulty=1)

def first_word_len(t):
    s = t.find(" ")
    return len(t) if s == -1 else s
ex.method("debug", "j1-l6.4-debug-firstword", "A word with no space", ["o2", "o3"], ["J1.12"], ["DEBUG"],
    "`firstWordLength` should return the length of the first word in some text: the number of characters before the first space, or the length of the whole text if there's no space. It crashes with a `StringIndexOutOfBoundsException` for one-word texts. Find and fix the bug.",
    [("firstWordLength", [("text", "String")], "int")], {"firstWordLength": first_word_len},
    [(None, ["hello world"]), (None, ["hello"]), (None, [""])],
    [(None, [" leading"], "starts with a space"), (None, ["a b c"], "short words"), (None, ["longword"], "one long word"), (None, ["x"], "one letter"), (None, ["two  spaces"], "double space")],
    'int firstWordLength(String text) {\n    int space = text.indexOf(" ");\n    return text.substring(0, space).length();\n}\n\nvoid main() {\n    IO.println(firstWordLength("hello world")); // should print 5\n}\n',
    'int firstWordLength(String text) {\n    int space = text.indexOf(" ");\n    if (space == -1) {\n        return text.length();\n    }\n    return space;\n}\n\nvoid main() {\n    IO.println(firstWordLength("hello world")); // should print 5\n}\n',
    {"ignores-no-space": 'int firstWordLength(String text) {\n    return text.indexOf(" ");\n}\n\nvoid main() {\n}\n'},
    ("What does indexOf return when the text has no space?", "It returns -1. Handle that case separately and return text.length()."),
    group="exceptions", difficulty=2)

ex.explain("j1-l6.4-explain-trace", "Reading a stack trace", ["o1"], ["J1.12"],
    "Here is a stack trace. What went wrong, which line of your code would you look at first, and how did the program get there?\n\n```\nException in thread \"main\" java.lang.ArithmeticException: / by zero\n\tat Main.share(Main.java:3)\n\tat Main.main(Main.java:8)\n```",
    "A full answer says a number was divided by zero (ArithmeticException); look first at line 3 of Main.java in method share, the first line in the program's own code; and that main called share at line 8, which is how it got there.",
    {2: ("Says it's a division by zero, points to line 3 in share as the first place to look, and says it was called from main at line 8.",
         ["It divided by zero (ArithmeticException). I'd look at line 3 in the share method first. main called share on line 8, so I'd also check what main passed in.",
          "A / by zero error. The top line, Main.java:3 in share, is where it happened, and share was called from main at line 8."]),
     1: ("Gets the type of problem or the line, but not both, or doesn't mention how the program got there.",
         ["A divide by zero.", "Look at line 3."]),
     0: ("Incorrect, for example says it's a compile error, or points to the wrong line.",
         ["It's a compile error on line 8.", "Something is wrong with main."])})
print("6.4 written")
