from build import *

Lesson("j1-l5.1", "Defining and calling methods", ["J1.08"], [
    ("o1", "Define a method with a name, parameters, a return type and a body"),
    ("o2", "Call a method and use the value it returns"),
    ("o3", "Explain why programs are split into named methods"),
], ["j1-l4.5"], 35, ["R4", "R8"], r'''
## Before you start

You've completed methods by filling in a header someone else wrote ([Values and types](j1-l2.1)). Now you'll write them yourself.

**Quick check.** In `int secondsIn(int minutes)`, what does `int` before the name mean, and what does `int minutes` mean?

<details><summary>Show the answer</summary>

The first `int` is the type of the result the method produces. `int minutes` says the method is given one whole number, called `minutes`.

</details>

## Explanation

You've been using methods all along: `main`, `IO.println`, `charAt`, `parseInt`. A **method** is a named block of code that does one job. You write it once and use it as often as you like.

### Defining a method

```java
int doubleIt(int number) {
    return number * 2;
}
```

| Part | Here | Meaning |
|---|---|---|
| Return type | `int` | The type of value the method gives back |
| Name | `doubleIt` | What you call it by. Use camelCase, starting with a verb |
| Parameters | `(int number)` | The values it's given, each with a type and a name |
| Body | `{ return number * 2; }` | What it does. `return` hands back the answer |

This is a **definition**: it says what the method does, but runs nothing yet.

### Calling a method

To run it, **call** it by name, with a value (an **argument**) for each parameter:

```java runnable
int doubleIt(int number) {
    return number * 2;
}

void main() {
    int result = doubleIt(21);
    IO.println(result);
    IO.println(doubleIt(5) + doubleIt(1));
}
```

This prints `42` then `12`. A call is an **expression**: it produces a value, which you can store, print, or use inside a bigger calculation. When `doubleIt(21)` is called, `number` is set to 21, the body runs, and the returned value replaces the call.

The order you define methods in doesn't matter; Java finds them all.

### `void`: methods that don't return anything

A method that *does* something (like printing) instead of *calculating* something has the return type `void`:

```java runnable
void greet(String name) {
    IO.println("Hello, " + name + "!");
}

void main() {
    greet("Ada");
    greet("Grace");
}
```

A `void` method has no `return value;`, and you can't use a call to it as a value.

### Methods with no parameters, or several

```java
int roll() { return 4; }                          // no parameters
int area(int width, int height) { return width * height; }   // two parameters
```

With several parameters, the arguments go in the same order: `area(3, 5)` sets `width` to 3 and `height` to 5.

### Why split a program into methods?

- **No repeating yourself**: the same job done in two places is one method called twice.
- **Names explain**: `isLeapYear(year)` says more than five lines of arithmetic.
- **Testing**: a small method can be tested on its own, which is exactly what this course's tests do to your code.

## Worked examples

### Example 1: a method for a repeated calculation

*Task: three places in a program convert minutes to seconds. Write one method for it.*

**Step 1 — What goes in, what comes out?** In: a whole number of minutes. Out: a whole number of seconds. So `int secondsIn(int minutes)`.

**Step 2 — What does the body do?** `return minutes * 60;`

**Step 3 — Call it wherever it's needed.**

```java runnable
int secondsIn(int minutes) {
    return minutes * 60;
}

void main() {
    IO.println(secondsIn(2));
    IO.println(secondsIn(10));
    IO.println(secondsIn(2) + secondsIn(10));
}
```

### Example 2: a method that decides

*Task: a method `isEven` that says whether a whole number is even.*

**Step 1 — A yes/no answer is a `boolean`.** So `boolean isEven(int n)`.

**Step 2 — Think of the test.** Even numbers leave remainder 0 when divided by 2.

```java runnable
boolean isEven(int n) {
    return n % 2 == 0;
}

void main() {
    IO.println(isEven(4));
    IO.println(isEven(7));
}
```

Names for methods that answer yes/no usually start with `is` or `has`.

## Predict, then run

::exercise{id=j1-l5.1-predict-calls}

## Where this is used

Every program you'll ever work on is made of methods. Large systems have thousands, each small enough to understand at a glance.

## Common mistakes

:::mistake{id=MC07}
**Printing instead of returning.** A method declared `int` must `return` an int. Printing the answer with `IO.println` shows it on screen, but gives the caller nothing to use.
:::

### Forgetting to use the returned value

`doubleIt(21);` on its own line computes 42 and throws it away. Store it or use it: `int result = doubleIt(21);`.

### Arguments in the wrong order

`area(3, 5)` and `area(5, 3)` are different calls. Match the parameter order in the definition.

### A return type that doesn't match

`int half(int n) { return n / 2.0; }` won't compile: the result is a `double`.

## Practice

::exercise{id=j1-l5.1-write-rectangle}

::exercise{id=j1-l5.1-debug-print}

::exercise{id=j1-l5.1-explain-why}

## Further reading

- **"Subgoals, context, and worked examples in learning computing problem solving"** (Morrison et al., 2015) `[R4]`: why the "what goes in, what comes out" steps used here help beginners design methods.

## How you'll be assessed

- The **predict** exercise checks that you can follow method calls.
- The **write** exercises check that you can define methods from a description (*implementation*).
- The **debug** exercise checks that you can fix a method that prints instead of returning (*debugging*).
- The **explain** exercise checks that you can say why programs use methods.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l5.1")
ex.predict("j1-l5.1-predict-calls", "Follow the calls", ["o2"], ["J1.08"],
    "Predict exactly what this program prints. Work out each call's returned value before you use it.",
    '''
    int triple(int n) {
        return n * 3;
    }

    String label(int n) {
        return "Item " + n;
    }

    void main() {
        IO.println(triple(4));
        IO.println(triple(triple(2)));
        IO.println(label(triple(1)));
        int x = triple(5) - triple(2);
        IO.println(x);
    }
    ''', '''
    12
    18
    Item 3
    9
    ''', ("Work out the innermost call first.", "triple(triple(2)) is triple(6), which is 18. 15 - 6 is 9."), difficulty=2)

def rect(w, h): return w * h
ex.method("write", "j1-l5.1-write-rectangle", "Write a method", ["o1"], ["J1.08"], ["IMPL"],
    "Write a method called `area` that is given a width and a height (both `int`s, in that order) and returns the area of the rectangle, as an `int`. For example, `area(3, 5)` is 15.\n\nThere's no header this time: you write the whole method.",
    [("area", [("width", "int"), ("height", "int")], "int")], {"area": rect},
    [(None, [3, 5]), (None, [1, 1]), (None, [0, 9])],
    [(None, [10, 10], "a square"), (None, [2, 50], "tall and thin"), (None, [7, 3], "swapped order"), (None, [100, 100], "large"), (None, [1, 0], "zero height")],
    '// Write the area method here.\n\nvoid main() {\n    IO.println(area(3, 5)); // should print 15\n}\n',
    'int area(int width, int height) {\n    return width * height;\n}\n\nvoid main() {\n    IO.println(area(3, 5)); // should print 15\n}\n',
    {"adds": 'int area(int width, int height) {\n    return width + height;\n}\n\nvoid main() {\n}\n'},
    ("What goes in, and what comes out? That gives you the header.", "int area(int width, int height) { return width * height; }"),
    starter_compiles=False, group="define-method")

def perim(w, h): return 2 * (w + h)
ex.method("write", "j1-l5.1-retrieve-perimeter", "Perimeter", ["o1"], ["J1.08"], ["IMPL"],
    "Write a method called `perimeter` that is given a width and a height (both `int`s, in that order) and returns the distance around the rectangle, as an `int`. For example, `perimeter(3, 5)` is 16.",
    [("perimeter", [("width", "int"), ("height", "int")], "int")], {"perimeter": perim},
    [(None, [3, 5]), (None, [1, 1]), (None, [0, 9])],
    [(None, [10, 10], "a square"), (None, [2, 50], "tall and thin"), (None, [7, 3], "swapped order"), (None, [100, 1], "wide"), (None, [0, 0], "nothing")],
    '// Write the perimeter method here.\n\nvoid main() {\n    IO.println(perimeter(3, 5)); // should print 16\n}\n',
    'int perimeter(int width, int height) {\n    return 2 * (width + height);\n}\n\nvoid main() {\n    IO.println(perimeter(3, 5)); // should print 16\n}\n',
    {"missing-parentheses": 'int perimeter(int width, int height) {\n    return 2 * width + height;\n}\n\nvoid main() {\n}\n'},
    ("Two widths and two heights. How do you add them up and double?", "return 2 * (width + height);"),
    starter_compiles=False, role="retrieval", group="define-method")

def is_mult(n, k): return n % k == 0
ex.method("write", "j1-l5.1-retrieve-multiple", "A multiple?", ["o1"], ["J1.08"], ["IMPL"],
    "Write a method called `isMultipleOf` that is given two whole numbers, `n` and `k` (`k` is at least 1), and returns `true` if `n` is a multiple of `k`, and `false` otherwise. For example, `isMultipleOf(12, 4)` is `true`.",
    [("isMultipleOf", [("n", "int"), ("k", "int")], "boolean")], {"isMultipleOf": is_mult},
    [(None, [12, 4]), (None, [10, 3]), (None, [0, 5])],
    [(None, [7, 7], "same number"), (None, [7, 1], "multiple of one"), (None, [5, 10], "smaller than k"), (None, [100, 25], "hundred"), (None, [99, 2], "odd")],
    '// Write the isMultipleOf method here.\n\nvoid main() {\n    IO.println(isMultipleOf(12, 4)); // should print true\n}\n',
    'boolean isMultipleOf(int n, int k) {\n    return n % k == 0;\n}\n\nvoid main() {\n    IO.println(isMultipleOf(12, 4)); // should print true\n}\n',
    {"swapped": 'boolean isMultipleOf(int n, int k) {\n    return k % n == 0;\n}\n\nvoid main() {\n}\n'},
    ("A yes/no answer is a boolean. Which operator gives a remainder?", "return n % k == 0;"),
    starter_compiles=False, role="retrieval", group="define-method")

ex.method("debug", "j1-l5.1-debug-print", "The method that prints", ["o2"], ["J1.08"], ["DEBUG"],
    "`square` should return the square of a number, so `square(5)` is 25. It doesn't compile. Read the error and fix it, so that it returns the answer rather than printing it.",
    [("square", [("n", "int")], "int")], {"square": lambda n: n * n},
    [(None, [5]), (None, [0]), (None, [-3])],
    [(None, [1], "one"), (None, [10], "ten"), (None, [12], "twelve"), (None, [100], "hundred"), (None, [-1], "minus one")],
    'int square(int n) {\n    IO.println(n * n);\n}\n\nvoid main() {\n    int result = square(5);\n    IO.println(result); // should print 25\n}\n',
    'int square(int n) {\n    return n * n;\n}\n\nvoid main() {\n    int result = square(5);\n    IO.println(result); // should print 25\n}\n',
    {"returns-n": 'int square(int n) {\n    return n;\n}\n\nvoid main() {\n}\n'},
    ("Read the error: what does the method promise to do, and what does it do instead?", "Replace the println with return n * n;"),
    misconceptions=["MC07"], starter_compiles=False)

ex.explain("j1-l5.1-explain-why", "Why methods?", ["o3"], ["J1.08"],
    "A program works out the area of a rectangle in three different places, each time with `width * height` written out. Give two reasons it would be better to write an `area` method and call it.",
    "A full answer gives two valid reasons, such as: avoids repeating code (change it in one place), gives the calculation a clear name, makes the code shorter and easier to read, or lets the calculation be tested on its own.",
    {2: ("Gives two clear, valid reasons (for example no repetition so a change is made once, a descriptive name, easier to read, or testable alone).",
         ["It avoids repeating the same code, so if the rule changes you only fix it in one place. And area(w, h) is easier to read than width * height everywhere.",
          "You can test the method on its own, and it gives the calculation a name that explains what it does."]),
     1: ("Gives one valid reason, or two vague ones.",
         ["So you don't repeat yourself.", "It's neater and better."]),
     0: ("Gives no valid reason, or an incorrect one.",
         ["Methods make the program run faster.", "Because Java requires every calculation to be a method."])})
print("5.1 written")
