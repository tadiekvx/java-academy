from build import *

Lesson("j1-l6.1", "Arrays", ["J1.10"], [
    ("o1", "Create an array, read and change its elements by index, and use length"),
    ("o2", "Visit every element with an index loop and with an enhanced for loop"),
    ("o3", "Say which index is the last one and what happens if you go past it"),
], ["j1-l5.5"], 40, ["R8", "I5"], r'''
## Before you start

You should be able to write for loops over a range and over a string ([for loops and boundaries](j1-l4.3)).

**Quick check.** What are the first and last valid indexes of `"Java"`?

<details><summary>Show the answer</summary>

0 and 3. The length is 4, and indexes run from 0 to length − 1.

</details>

## Explanation

So far each variable has held one value. To handle a whole list (a week of temperatures, a class's marks), you'd need dozens of variables. An **array** holds many values of the same type in one variable.

### Creating an array

```java
int[] marks = {72, 58, 91, 64};
```

`int[]` means *an array of ints*. The braces list the values. You can make arrays of any type: `double[]`, `String[]`, `boolean[]`.

To create one of a given size, filled with default values (0 for numbers, `false` for booleans, `null` for text), use `new`:

```java
int[] scores = new int[5];     // five zeros
```

### Reading and changing elements

Each value in an array is an **element**, found by its **index**, and **indexes start at 0**, just like in a string:

| Index | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| `marks` | 72 | 58 | 91 | 64 |

```java runnable
void main() {
    int[] marks = {72, 58, 91, 64};
    IO.println(marks[0]);
    marks[1] = 60;
    IO.println(marks[1]);
    IO.println(marks.length);
}
```

This prints `72`, `60`, `4`. Note three things:

- `marks[0]` reads an element; `marks[1] = 60;` changes one.
- **`length` has no brackets** for an array (`marks.length`), unlike a string's `length()`.
- Unlike a string, an array's elements **can** be changed.

An array's size is fixed when it's created. You can't add a fifth element to `marks`; in [ArrayList](j1-l6.3) you'll meet a list that can grow.

### Going past the end

The last valid index is `length - 1`. Using any other index stops the program with a runtime error:

```
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 4 out of bounds for length 4
```

It names the bad index and the length, which makes it quick to diagnose.

### Visiting every element

With an index loop, you can use the index as well as the value:

```java runnable
void main() {
    int[] marks = {72, 58, 91, 64};
    int total = 0;
    for (int i = 0; i < marks.length; i++) {
        total += marks[i];
    }
    IO.println(total);
}
```

When you only need the values, the **enhanced for loop** is shorter and can't go past the end:

```java runnable
void main() {
    int[] marks = {72, 58, 91, 64};
    int total = 0;
    for (int mark : marks) {
        total += mark;
    }
    IO.println(total);
}
```

Read `for (int mark : marks)` as *for each `mark` in `marks`*. Both print `285`. Use the index version when you need to know the position, or to change elements.

### Printing an array

`IO.println(marks)` doesn't print the values, only an unhelpful label. Use `Arrays.toString`:

```java runnable
void main() {
    int[] marks = {72, 58, 91, 64};
    IO.println(Arrays.toString(marks));
}
```

This prints `[72, 58, 91, 64]`.

## Worked examples

### Example 1: the average mark

*Task: return the average of an array of marks, as a `double`. Assume the array isn't empty.*

**Step 1 — Which pattern?** A sum, then divide by how many.

**Step 2 — Sum with an enhanced for loop.** We don't need the positions.

**Step 3 — Divide as doubles.** `(double) total / marks.length`, or you'll lose the fraction ([Arithmetic](j1-l2.3)).

```java runnable
double average(int[] marks) {
    int total = 0;
    for (int mark : marks) {
        total += mark;
    }
    return (double) total / marks.length;
}

void main() {
    IO.println(average(new int[] {72, 58, 91, 64}));
}
```

This prints `71.25`. (`new int[] {…}` creates an array on the spot, for passing straight into a call.)

### Example 2: the position of the highest mark

*Task: return the **index** of the highest mark.*

**Step 1 — Which pattern?** Track the largest, but remember where it was, so you need the index.

**Step 2 — Start with index 0 as the best so far,** and compare from index 1.

```java runnable
int indexOfHighest(int[] marks) {
    int best = 0;
    for (int i = 1; i < marks.length; i++) {
        if (marks[i] > marks[best]) {
            best = i;
        }
    }
    return best;
}

void main() {
    IO.println(indexOfHighest(new int[] {72, 58, 91, 64}));
}
```

This prints `2`.

## Predict, then run

::exercise{id=j1-l6.1-predict-arrays}

## Where this is used

- **Collections of readings**: temperatures, prices, scores, pixels.
- **Fixed-size data**: the days of a week, the months of a year.
- **Under the hood**: most of the collections you'll use later, like lists and strings, are built on arrays.

## Common mistakes

:::mistake{id=MC09}
**Going one past the end.** `i <= marks.length` makes `i` reach `marks.length`, which isn't a valid index. Use `i < marks.length`.
:::

### Mixing up `length` and `length()`

Arrays use `marks.length`; strings use `word.length()`. The compiler tells you which you got wrong.

### Expecting `new int[5]` to be empty

It holds five zeros, not nothing. The elements exist from the start.

## Practice

::exercise{id=j1-l6.1-write-sum}

::exercise{id=j1-l6.1-debug-bounds}

::exercise{id=j1-l6.1-modify-double}

::exercise{id=j1-l6.1-explain-index}

## Version notes

`Arrays` is in `java.util`. Compact source files import it automatically; in ordinary Java files you'd write `import java.util.Arrays;` at the top.

## Further reading

- **The Java Language Specification, §10 "Arrays"** `[I5]`: the precise rules, including default values and the exceptions thrown.

## How you'll be assessed

- The **predict** exercise checks that you can follow array code.
- The **write**, **debug** and **modify** exercises check that you can use arrays, fix a bounds mistake, and change elements (*implementation, debugging, modification*).
- The **explain** exercise checks that you understand indexes and length.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l6.1")
ex.predict("j1-l6.1-predict-arrays", "Index by index", ["o1", "o2"], ["J1.10"],
    "Predict exactly what this program prints.",
    '''
    void main() {
        int[] values = {4, 8, 15, 16};
        values[2] = values[0] + values[1];
        IO.println(Arrays.toString(values));
        IO.println(values.length);
        IO.println(values[values.length - 1]);
        int sum = 0;
        for (int v : values) {
            sum += v;
        }
        IO.println(sum);
    }
    ''', '''
    [4, 8, 12, 16]
    4
    16
    40
    ''', ("Element 2 changes before anything is printed. The last index is length - 1.",
          "values[2] becomes 4 + 8 = 12. The sum is 4 + 8 + 12 + 16 = 40."), misconceptions=["MC09"], difficulty=2)

ex.method("write", "j1-l6.1-write-sum", "Total of an array", ["o1", "o2"], ["J1.10"], ["IMPL"],
    "Write a method called `total` that is given an `int[]` called `values` and returns the sum of all its elements. The sum of an empty array is 0.",
    [("total", [("values", "int[]")], "int")], {"total": sum},
    [(None, [[4, 8, 15, 16]]), (None, [[]]), (None, [[-5, 5]])],
    [(None, [[7]], "one element"), (None, [[1, 1, 1, 1, 1]], "ones"), (None, [[100, -100, 100]], "mixed"), (None, [[0, 0]], "zeros"), (None, [[10, 20, 30, 40, 50, 60]], "longer")],
    '// Write the total method here.\n\nvoid main() {\n    IO.println(total(new int[] {4, 8, 15, 16})); // should print 43\n}\n',
    'int total(int[] values) {\n    int sum = 0;\n    for (int value : values) {\n        sum += value;\n    }\n    return sum;\n}\n\nvoid main() {\n    IO.println(total(new int[] {4, 8, 15, 16})); // should print 43\n}\n',
    {"skips-first": 'int total(int[] values) {\n    int sum = 0;\n    for (int i = 1; i < values.length; i++) {\n        sum += values[i];\n    }\n    return sum;\n}\n\nvoid main() {\n}\n'},
    ("It's the sum pattern, applied to an array.", "int sum = 0; for (int value : values) sum += value; return sum;"),
    starter_compiles=False, group="array-patterns")

ex.method("write", "j1-l6.1-retrieve-above", "How many above?", ["o1", "o2"], ["J1.10"], ["IMPL"],
    "Write a method called `countAbove` that is given an `int[]` called `values` and an `int` called `limit` (in that order), and returns how many elements are **greater than** `limit`.",
    [("countAbove", [("values", "int[]"), ("limit", "int")], "int")], {"countAbove": lambda v, l: sum(1 for x in v if x > l)},
    [(None, [[4, 8, 15, 16], 10]), (None, [[], 5]), (None, [[3, 3, 3], 3])],
    [(None, [[1, 2, 3], 0], "all above"), (None, [[1, 2, 3], 3], "none above"), (None, [[-1, -2, 5], -2], "negatives"), (None, [[10], 9], "one element"), (None, [[5, 6, 7, 8, 9], 7], "half")],
    '// Write the countAbove method here.\n\nvoid main() {\n    IO.println(countAbove(new int[] {4, 8, 15, 16}, 10)); // should print 2\n}\n',
    'int countAbove(int[] values, int limit) {\n    int count = 0;\n    for (int value : values) {\n        if (value > limit) {\n            count++;\n        }\n    }\n    return count;\n}\n\nvoid main() {\n    IO.println(countAbove(new int[] {4, 8, 15, 16}, 10)); // should print 2\n}\n',
    {"at-least": 'int countAbove(int[] values, int limit) {\n    int count = 0;\n    for (int value : values) {\n        if (value >= limit) {\n            count++;\n        }\n    }\n    return count;\n}\n\nvoid main() {\n}\n'},
    ("It's the count pattern.", "count++ whenever value > limit."), starter_compiles=False, role="retrieval", group="array-patterns")

ex.method("write", "j1-l6.1-retrieve-largest", "The largest element", ["o1", "o2"], ["J1.10"], ["IMPL"],
    "Write a method called `largest` that is given a non-empty `int[]` called `values` and returns its largest element. The elements may be negative.",
    [("largest", [("values", "int[]")], "int")], {"largest": max},
    [(None, [[4, 8, 15, 16]]), (None, [[-5, -2, -9]]), (None, [[7]])],
    [(None, [[16, 15, 8, 4]], "descending"), (None, [[0, 0, 0]], "all equal"), (None, [[-1, 0, -1]], "zero is largest"), (None, [[100, 5, 100]], "repeated max"), (None, [[3, 9, 2, 9, 1]], "two nines")],
    '// Write the largest method here.\n\nvoid main() {\n    IO.println(largest(new int[] {4, 8, 15, 16})); // should print 16\n}\n',
    'int largest(int[] values) {\n    int best = values[0];\n    for (int value : values) {\n        if (value > best) {\n            best = value;\n        }\n    }\n    return best;\n}\n\nvoid main() {\n    IO.println(largest(new int[] {4, 8, 15, 16})); // should print 16\n}\n',
    {"starts-at-zero": 'int largest(int[] values) {\n    int best = 0;\n    for (int value : values) {\n        if (value > best) {\n            best = value;\n        }\n    }\n    return best;\n}\n\nvoid main() {\n}\n'},
    ("Track the largest. What should the first 'best so far' be if every element could be negative?", "Start with int best = values[0]; and replace it whenever a bigger value appears."),
    starter_compiles=False, role="retrieval", group="array-patterns")

ex.method("debug", "j1-l6.1-debug-bounds", "One too far", ["o3"], ["J1.10"], ["DEBUG"],
    "`average` should return the average of an array of ints, as a `double`. It crashes with an `ArrayIndexOutOfBoundsException`. Find and fix the bug.",
    [("average", [("values", "int[]")], "double")], {"average": lambda v: sum(v) / len(v)},
    [(None, [[4, 8, 15, 16]]), (None, [[10]]), (None, [[1, 2]])],
    [(None, [[0, 0, 0]], "zeros"), (None, [[-4, 4]], "cancels out"), (None, [[1, 2, 3, 4, 5]], "five"), (None, [[100, 1]], "unbalanced"), (None, [[7, 7, 7]], "all same")],
    'double average(int[] values) {\n    int total = 0;\n    for (int i = 0; i <= values.length; i++) {\n        total += values[i];\n    }\n    return (double) total / values.length;\n}\n\nvoid main() {\n    IO.println(average(new int[] {4, 8, 15, 16})); // should print 10.75\n}\n',
    'double average(int[] values) {\n    int total = 0;\n    for (int i = 0; i < values.length; i++) {\n        total += values[i];\n    }\n    return (double) total / values.length;\n}\n\nvoid main() {\n    IO.println(average(new int[] {4, 8, 15, 16})); // should print 10.75\n}\n',
    {"integer-division": 'double average(int[] values) {\n    int total = 0;\n    for (int value : values) {\n        total += value;\n    }\n    return total / values.length;\n}\n\nvoid main() {\n}\n'},
    ("What is the last valid index of an array of length 4? What does the loop's last pass use?", "Change <= to < so i stops at length - 1."),
    misconceptions=["MC09"])

ex.method("modify", "j1-l6.1-modify-double", "Double every element", ["o1", "o2"], ["J1.10"], ["MOD"],
    "`doubleAll` changes an array so that every element is doubled, and returns the same array. It currently only doubles the first element. Change it so that it doubles **every** element.",
    [("doubleAll", [("values", "int[]")], "int[]")], {"doubleAll": lambda v: [x * 2 for x in v]},
    [(None, [[1, 2, 3]]), (None, [[]]), (None, [[-4, 0, 4]])],
    [(None, [[5]], "one element"), (None, [[10, 20, 30, 40]], "four"), (None, [[0, 0]], "zeros"), (None, [[7, -7, 7]], "alternating"), (None, [[1, 1, 1, 1, 1, 1]], "six ones")],
    'int[] doubleAll(int[] values) {\n    if (values.length > 0) {\n        values[0] = values[0] * 2;\n    }\n    return values;\n}\n\nvoid main() {\n    IO.println(Arrays.toString(doubleAll(new int[] {1, 2, 3})));\n}\n',
    'int[] doubleAll(int[] values) {\n    for (int i = 0; i < values.length; i++) {\n        values[i] = values[i] * 2;\n    }\n    return values;\n}\n\nvoid main() {\n    IO.println(Arrays.toString(doubleAll(new int[] {1, 2, 3})));\n}\n',
    {"enhanced-for": 'int[] doubleAll(int[] values) {\n    for (int value : values) {\n        value = value * 2;\n    }\n    return values;\n}\n\nvoid main() {\n}\n'},
    ("To change elements you need to know where they are. Which kind of loop gives you the index?", "Use an index loop: for (int i = 0; i < values.length; i++) values[i] = values[i] * 2;"))

ex.explain("j1-l6.1-explain-index", "Length and the last index", ["o3"], ["J1.10"],
    "An array has `length` 5. What are its first and last valid indexes? What happens if your code uses `values[5]`, and why?",
    "A full answer says the first index is 0 and the last is 4 (length - 1); values[5] is past the end, so the program stops with an ArrayIndexOutOfBoundsException because there's no element 5.",
    {2: ("Gives 0 and 4 (length - 1), and says values[5] doesn't exist so it throws an ArrayIndexOutOfBoundsException (crashes).",
         ["The first index is 0 and the last is 4, because indexes start at 0 so the last is length - 1. values[5] is past the end, so Java stops with an ArrayIndexOutOfBoundsException.",
          "0 to 4. There's no element at index 5, so using it crashes the program with ArrayIndexOutOfBounds."]),
     1: ("Gets the indexes right but doesn't say what happens, or says what happens without the correct last index.",
         ["0 and 4.", "It crashes because 5 is too big."]),
     0: ("Incorrect, for example says the indexes are 1 to 5, or that values[5] gives 0.",
         ["1 to 5, and values[5] is the last one.", "values[5] returns 0 as a default."])},
    misconceptions=["MC09"])
print("6.1 written")
