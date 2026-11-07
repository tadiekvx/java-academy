from build import *

Lesson("j1-l5.3", "Scope and the call stack", ["J1.08"], [
    ("o1", "Say where a variable can be used, and why a variable can't be seen outside its method or block"),
    ("o2", "Trace nested method calls, saying which method is running and what each one is waiting for"),
    ("o3", "Explain that each call gets its own set of variables"),
], ["j1-l5.2"], 30, ["R8", "R5", "I5"], r'''
## Before you start

You should know that parameters are copies and that methods can call other methods ([Parameters and return values](j1-l5.2)).

**Quick check.** Can `sumOfSquares` use a variable declared inside `main`?

<details><summary>Show the answer</summary>

No. Variables belong to the method they're declared in. To share a value, pass it as an argument.

</details>

## Explanation

### Scope: where a name can be used

The **scope** of a variable is the part of the program where its name works. A variable declared inside a method, or inside any `{ }` block, exists from its declaration to the closing brace of the block it's in:

```java
void main() {
    int total = 0;
    for (int i = 1; i <= 3; i++) {
        int square = i * i;      // exists only inside this loop body
        total += square;
    }
    IO.println(total);           // fine
    IO.println(square);          // error: cannot find symbol
    IO.println(i);               // error: cannot find symbol
}
```

`square` and `i` are gone once the loop's braces close. That's useful: a name can't be used by accident somewhere it doesn't make sense, and different methods can reuse the same names without clashing.

If you need a value *after* a block, declare the variable **before** it, as `total` is here.

### Each call has its own variables

Every time a method is called, Java creates a fresh set of its parameters and variables. Two calls don't share anything:

```java runnable
int next(int n) {
    int result = n + 1;
    return result;
}

void main() {
    int a = next(1);
    int b = next(10);
    IO.println(a + " " + b);
}
```

This prints `2 11`. The two calls each had their own `n` and `result`.

### The call stack

When `main` calls `A`, which calls `B`, three methods are "in progress" at once. `main` is waiting for `A`; `A` is waiting for `B`; only `B` is running. Java keeps track of this with a **call stack**: a pile of in-progress calls, newest on top. When `B` returns, it's removed, and `A` carries on from where it paused.

```java
int add(int a, int b) { return a + b; }
int twice(int x)       { return add(x, x); }

void main() {
    IO.println(twice(5));
}
```

Tracing the stack as it runs:

| Step | Stack (top first) | What happens |
|---|---|---|
| 1 | `main` | `main` calls `twice(5)` |
| 2 | `twice(x=5)`, `main` | `twice` calls `add(5, 5)` |
| 3 | `add(a=5, b=5)`, `twice`, `main` | `add` returns 10 |
| 4 | `twice(x=5)`, `main` | `twice` returns 10 |
| 5 | `main` | prints `10` |

You'll see the call stack for real in [Exceptions and stack traces](j1-l6.4): when a program crashes, Java prints this pile.

## Worked examples

### Example 1: trace a nested call

*Task: what does this print?*

```java
int f(int n) { return g(n) + 1; }
int g(int n) { return n * 2; }

void main() {
    IO.println(f(3));
}
```

**Step 1 — Start in `main`.** It calls `f(3)`.

**Step 2 — `f` calls `g(3)` and waits.** `g(3)` returns 6.

**Step 3 — `f` resumes** with 6 + 1 = 7, and returns it.

**Step 4 — `main` prints 7.** Note that `f` and `g` both have a parameter called `n`; they're different variables.

### Example 2: spotting a scope error

*Task: why won't this compile?*

```java
int largest(int a, int b) {
    if (a > b) {
        int best = a;
    } else {
        int best = b;
    }
    return best;
}
```

**Step 1 — Where is `best` declared?** Inside each branch's braces.

**Step 2 — Where is it used?** After both blocks have ended, so it no longer exists: `cannot find symbol`.

**Step 3 — Fix: declare it before the `if`.**

```java runnable
int largest(int a, int b) {
    int best = a;
    if (b > a) {
        best = b;
    }
    return best;
}

void main() {
    IO.println(largest(3, 9));
}
```

## Predict, then run

::exercise{id=j1-l5.3-predict-stack}

## Where this is used

- **Reading crash reports**: the call stack in an error message is how you find which method called which.
- **Reusing names safely**: large programs use names like `i`, `total` and `result` in thousands of methods without clashing.
- **Recursion** (a method calling itself, which you'll meet later) relies on each call having its own variables.

## Common mistakes

### Declaring a variable inside a block, then using it outside

Declare it before the `if` or loop, and assign to it inside.

### Thinking two methods share variables

Two methods with a parameter `n` have two different `n`s. Pass values between methods as arguments and results.

### Redeclaring a variable in the same scope

`int total = 0;` twice in the same method is an error. The second time, just assign: `total = 5;`.

## Practice

::exercise{id=j1-l5.3-debug-scope}

::exercise{id=j1-l5.3-write-trace}

::exercise{id=j1-l5.3-explain-stack}

## Further reading

- **The Java Language Specification, §6.3 "Scope of a Declaration"** `[I5]`: the precise scope rules for every kind of declaration.

## How you'll be assessed

- The **predict** and **trace** exercises check that you can follow calls (*identifying mistakes*).
- The **debug** exercise checks that you can fix a scope error (*debugging*).
- The **explain** exercise checks that you understand the call stack.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l5.3")
ex.predict("j1-l5.3-predict-stack", "Which method is running?", ["o2", "o3"], ["J1.08"],
    "Predict exactly what this program prints. Trace the call stack, and remember that `n` in each method is a different variable.",
    '''
    int inner(int n) {
        n = n + 1;
        IO.println("inner " + n);
        return n * 2;
    }

    int outer(int n) {
        IO.println("outer " + n);
        int result = inner(n + 10);
        IO.println("back " + n);
        return result;
    }

    void main() {
        IO.println(outer(1));
    }
    ''', '''
    outer 1
    inner 12
    back 1
    24
    ''', ("outer's n is 1 throughout. inner gets its own n, a copy of 11.", "inner adds 1 to its own n (12) and returns 24. outer's n never changes."), difficulty=2)

ex.method("debug", "j1-l5.3-debug-scope", "The vanished variable", ["o1"], ["J1.08"], ["DEBUG"],
    "`largest` should return the larger of two numbers, but it doesn't compile. Read the error and fix it.",
    [("largest", [("a", "int"), ("b", "int")], "int")], {"largest": max},
    [(None, [3, 9]), (None, [9, 3]), (None, [5, 5])],
    [(None, [-1, -9], "negatives"), (None, [0, 0], "zeros"), (None, [100, 99], "close"), (None, [-5, 5], "mixed"), (None, [7, 8], "ascending")],
    'int largest(int a, int b) {\n    if (a > b) {\n        int best = a;\n    } else {\n        int best = b;\n    }\n    return best;\n}\n\nvoid main() {\n    IO.println(largest(3, 9)); // should print 9\n}\n',
    'int largest(int a, int b) {\n    int best = a;\n    if (b > a) {\n        best = b;\n    }\n    return best;\n}\n\nvoid main() {\n    IO.println(largest(3, 9)); // should print 9\n}\n',
    {"always-a": 'int largest(int a, int b) {\n    int best = a;\n    return best;\n}\n\nvoid main() {\n}\n'},
    ("Where is best declared, and where is it used? Are they in the same set of braces?", "Declare int best before the if, then assign to it inside."),
    starter_compiles=False)

def chain(n): return (n + 1) * 2 + 3
ex.method("write", "j1-l5.3-write-trace", "Chain of calls", ["o2", "o3"], ["J1.08"], ["IMPL"],
    "Write three methods, each calling the next: `step1(n)` returns `step2(n + 1)`; `step2(n)` returns `step3(n * 2)`; and `step3(n)` returns `n + 3`. All take and return an `int`. For example, `step1(4)` is `step2(5)`, which is `step3(10)`, which is 13.",
    [("step1", [("n", "int")], "int"), ("step2", [("n", "int")], "int"), ("step3", [("n", "int")], "int")],
    {"step1": chain, "step2": lambda n: n * 2 + 3, "step3": lambda n: n + 3},
    [(None, [4]), ("step2", [5]), ("step3", [10])],
    [(None, [0], "zero"), (None, [-1], "minus one"), ("step2", [0], "step2 of zero"), ("step3", [-3], "step3 negative"), (None, [100], "large")],
    '// Write step1, step2 and step3 here.\n\nvoid main() {\n    IO.println(step1(4)); // should print 13\n}\n',
    'int step1(int n) {\n    return step2(n + 1);\n}\n\nint step2(int n) {\n    return step3(n * 2);\n}\n\nint step3(int n) {\n    return n + 3;\n}\n\nvoid main() {\n    IO.println(step1(4)); // should print 13\n}\n',
    {"skips-a-step": 'int step1(int n) {\n    return step3(n + 1);\n}\n\nint step2(int n) {\n    return step3(n * 2);\n}\n\nint step3(int n) {\n    return n + 3;\n}\n\nvoid main() {\n}\n'},
    ("Each method does one small thing, then hands the result to the next.", "step1 returns step2(n + 1); step2 returns step3(n * 2); step3 returns n + 3."),
    starter_compiles=False, difficulty=2)

ex.explain("j1-l5.3-explain-stack", "Who is waiting?", ["o2", "o3"], ["J1.08"],
    "`main` calls `twice(5)`, and `twice` calls `add(5, 5)`. While `add` is running, which methods are in progress, and what is each of the other two waiting for?",
    "A full answer says three are in progress (main, twice, add), add is running at the top, twice is waiting for add's result, and main is waiting for twice's result; when add returns, twice carries on, and so on down.",
    {2: ("Says add is running, twice is waiting for add to return a value, and main is waiting for twice to return, naming all three in the right order.",
         ["All three are in progress. add is running right now. twice is paused, waiting for add to return its result, and main is paused waiting for twice's result.",
          "add is on top of the stack and running. twice is waiting for add's answer, and underneath main is waiting for twice to finish."]),
     1: ("Names the methods but is vague or wrong about what one of them is waiting for.",
         ["main, twice and add are all running at the same time.", "add is running and the others are waiting."]),
     0: ("Incorrect, for example says only main is running, or that they run at the same time.",
         ["Only main is in progress, the others haven't started.", "They all run at once."])})
print("5.3 written")
