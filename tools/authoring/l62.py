from build import *

Lesson("j1-l6.2", "Array algorithms and references", ["J1.10"], [
    ("o1", "Search, count and reverse the elements of an array"),
    ("o2", "Explain that an array variable holds a reference, so assigning it makes an alias, not a copy"),
    ("o3", "Make a real copy with Arrays.copyOf, and say when a method changes the caller's array"),
], ["j1-l6.1"], 40, ["R8", "I4"], r'''
## Before you start

You should be able to create arrays and loop over them ([Arrays](j1-l6.1)).

**Quick check.** After `int[] a = {1, 2, 3};`, what is `a[a.length - 1]`?

<details><summary>Show the answer</summary>

`3`, the last element.

</details>

## Explanation

### Searching

To find where a value is, use the find-the-first pattern from [Loop patterns](j1-l4.4): return the index as soon as you find a match, and `-1` if you never do.

```java runnable
int indexOf(int[] values, int target) {
    for (int i = 0; i < values.length; i++) {
        if (values[i] == target) {
            return i;
        }
    }
    return -1;
}

void main() {
    int[] ids = {40, 17, 23, 17};
    IO.println(indexOf(ids, 17));
    IO.println(indexOf(ids, 99));
}
```

This prints `1` (the first 17) and `-1`.

### Reversing in place

To reverse an array, swap the first and last elements, then the second and second-last, and so on, meeting in the middle. A swap needs a temporary variable, as in [Variables and state](j1-l2.2):

```java runnable
void reverse(int[] values) {
    for (int i = 0; i < values.length / 2; i++) {
        int other = values.length - 1 - i;
        int saved = values[i];
        values[i] = values[other];
        values[other] = saved;
    }
}

void main() {
    int[] numbers = {1, 2, 3, 4, 5};
    reverse(numbers);
    IO.println(Arrays.toString(numbers));
}
```

This prints `[5, 4, 3, 2, 1]`. The loop runs only to `length / 2`: going further would swap everything back. (For 5 elements, `5 / 2` is 2: two swaps, and the middle element stays put.)

Notice that `reverse` is `void`, and yet `numbers` changed. That's the next idea.

### An array variable holds a reference

With ints, `int b = a;` copies the value. An array is different. The variable doesn't hold the elements themselves; it holds a **reference** (think: an address) to where they live. So:

```java runnable
void main() {
    int[] a = {1, 2, 3};
    int[] b = a;          // copies the reference, not the elements
    b[0] = 99;
    IO.println(a[0]);
}
```

This prints `99`. There is only **one** array, and two names for it (`a` and `b` are **aliases**). Changing it through either name is visible through the other.

### Why a method can change the caller's array

Back to the rule from [Parameters and return values](j1-l5.2): a parameter is a copy of the argument's value. For an array, that value is the **reference**. So the method gets its own reference to the **same array**:

- Changing which array the parameter points at (`values = something else`) has no effect on the caller.
- Changing the **elements** (`values[0] = 5`) changes the one shared array, so the caller sees it. That's why `reverse` works without returning anything.

### Making a real copy

To get an independent array, copy the elements with `Arrays.copyOf(original, newLength)`:

```java runnable
void main() {
    int[] a = {1, 2, 3};
    int[] b = Arrays.copyOf(a, a.length);
    b[0] = 99;
    IO.println(a[0] + " " + b[0]);
}
```

This prints `1 99`. Now there are two arrays. (Asking for a larger `newLength` pads with zeros; a smaller one cuts the array short.)

Remember that `Arrays.toString(a)` gives a readable text of the elements, and `a == b` on arrays checks whether they're the *same array*, not whether they hold the same values. To compare contents, use `Arrays.equals(a, b)`.

## Worked examples

### Example 1: a method that must not change its input

*Task: write `reversed(values)`, returning a reversed copy and leaving the original untouched.*

**Step 1 — What's the risk?** Reversing `values` in place would change the caller's array.

**Step 2 — Make a copy first,** and work on that.

**Step 3 — Reverse the copy and return it.**

```java runnable
int[] reversed(int[] values) {
    int[] copy = Arrays.copyOf(values, values.length);
    for (int i = 0; i < copy.length / 2; i++) {
        int other = copy.length - 1 - i;
        int saved = copy[i];
        copy[i] = copy[other];
        copy[other] = saved;
    }
    return copy;
}

void main() {
    int[] original = {1, 2, 3};
    int[] flipped = reversed(original);
    IO.println(Arrays.toString(original) + " " + Arrays.toString(flipped));
}
```

This prints `[1, 2, 3] [3, 2, 1]`.

### Example 2: counting duplicates

*Task: count how many times a value appears in an array.*

**Step 1 — Which pattern?** Count.

**Step 2 — Write it,** and test the empty array and a value that isn't there.

```java runnable
int countOf(int[] values, int target) {
    int count = 0;
    for (int value : values) {
        if (value == target) {
            count++;
        }
    }
    return count;
}

void main() {
    IO.println(countOf(new int[] {5, 7, 5, 5}, 5));
}
```

## Predict, then run

::exercise{id=j1-l6.2-predict-alias}

## Where this is used

- **Unexpected changes**: a function that quietly changes a list its caller still uses is a classic source of bugs in real systems.
- **Defensive copies**: libraries copy input they want to keep safe from outside changes.
- **Sorting and searching**: the building blocks of what you'll meet in Stage 5.

## Common mistakes

:::mistake{id=MC12}
**Thinking `int[] b = a;` copies the array.** It makes `b` another name for the same array. Change `b[0]` and `a[0]` changes too. Use `Arrays.copyOf` for a real copy.
:::

### Reversing too far

Looping over the whole array in a swap-based reverse swaps every pair twice, putting everything back. Stop at `length / 2`.

### Comparing arrays with `==`

`==` asks whether two names refer to the same array. Use `Arrays.equals` to compare contents.

## Practice

::exercise{id=j1-l6.2-write-reverse}

::exercise{id=j1-l6.2-debug-alias}

::exercise{id=j1-l6.2-write-search}

::exercise{id=j1-l6.2-explain-alias}

## Further reading

- **Java SE 25 API documentation for `Arrays`** `[I4]`: `copyOf`, `equals`, `fill`, `sort` and `toString`, with examples.

## How you'll be assessed

- The **predict** exercise checks that you can spot aliasing.
- The **write** exercises check that you can search and reverse (*implementation*), and **debug** that you can fix an aliasing bug.
- The **explain** exercise checks that you understand references.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l6.2")
ex.predict("j1-l6.2-predict-alias", "One array or two?", ["o2", "o3"], ["J1.10"],
    "Predict exactly what this program prints. For each line, ask: how many arrays are there?",
    '''
    void main() {
        int[] a = {1, 2, 3};
        int[] b = a;
        int[] c = Arrays.copyOf(a, a.length);
        b[0] = 10;
        c[1] = 20;
        IO.println(Arrays.toString(a));
        IO.println(Arrays.toString(b));
        IO.println(Arrays.toString(c));
        IO.println(a == b);
        IO.println(Arrays.equals(a, c));
    }
    ''', '''
    [10, 2, 3]
    [10, 2, 3]
    [1, 20, 3]
    true
    false
    ''', ("b is another name for a's array. c is a separate copy.", "Changing b[0] changes a too. c's change is only in c. a and c now differ."),
    misconceptions=["MC12"], difficulty=2)

ex.method("write", "j1-l6.2-write-reverse", "Reverse a copy", ["o1", "o3"], ["J1.10"], ["IMPL"],
    "Write a method called `reversed` that is given an `int[]` called `values` and returns a **new** array with the elements in reverse order. It must leave the original array unchanged.",
    [("reversed", [("values", "int[]")], "int[]")], {"reversed": lambda v: v[::-1]},
    [(None, [[1, 2, 3]]), (None, [[]]), (None, [[7]])],
    [(None, [[1, 2]], "two"), (None, [[1, 2, 3, 4]], "even length"), (None, [[5, 5, 5]], "all same"), (None, [[-1, 0, 1]], "negatives"), (None, [[9, 8, 7, 6, 5]], "five")],
    '// Write the reversed method here.\n\nvoid main() {\n    IO.println(Arrays.toString(reversed(new int[] {1, 2, 3}))); // should print [3, 2, 1]\n}\n',
    'int[] reversed(int[] values) {\n    int[] copy = Arrays.copyOf(values, values.length);\n    for (int i = 0; i < copy.length / 2; i++) {\n        int other = copy.length - 1 - i;\n        int saved = copy[i];\n        copy[i] = copy[other];\n        copy[other] = saved;\n    }\n    return copy;\n}\n\nvoid main() {\n    IO.println(Arrays.toString(reversed(new int[] {1, 2, 3}))); // should print [3, 2, 1]\n}\n',
    {"swaps-twice": 'int[] reversed(int[] values) {\n    int[] copy = Arrays.copyOf(values, values.length);\n    for (int i = 0; i < copy.length; i++) {\n        int other = copy.length - 1 - i;\n        int saved = copy[i];\n        copy[i] = copy[other];\n        copy[other] = saved;\n    }\n    return copy;\n}\n\nvoid main() {\n}\n'},
    ("Copy first, so the original is safe. Then swap pairs working inwards from both ends.", "Swap copy[i] with copy[length - 1 - i] for i from 0 to length / 2."),
    starter_compiles=False, difficulty=3, group="array-algorithms")

ex.method("write", "j1-l6.2-retrieve-search", "Find the position", ["o1"], ["J1.10"], ["IMPL"],
    "Write a method called `positionOf` that is given an `int[]` called `values` and an `int` called `target` (in that order). It returns the index of the **first** element equal to `target`, or -1 if there isn't one.",
    [("positionOf", [("values", "int[]"), ("target", "int")], "int")], {"positionOf": lambda v, t: v.index(t) if t in v else -1},
    [(None, [[40, 17, 23, 17], 17]), (None, [[40, 17, 23, 17], 99]), (None, [[], 5])],
    [(None, [[5], 5], "single match"), (None, [[5], 6], "single miss"), (None, [[1, 2, 3], 3], "last element"), (None, [[1, 2, 3], 1], "first element"), (None, [[7, 7, 7], 7], "all match")],
    '// Write the positionOf method here.\n\nvoid main() {\n    IO.println(positionOf(new int[] {40, 17, 23, 17}, 17)); // should print 1\n}\n',
    'int positionOf(int[] values, int target) {\n    for (int i = 0; i < values.length; i++) {\n        if (values[i] == target) {\n            return i;\n        }\n    }\n    return -1;\n}\n\nvoid main() {\n    IO.println(positionOf(new int[] {40, 17, 23, 17}, 17)); // should print 1\n}\n',
    {"last-match": 'int positionOf(int[] values, int target) {\n    int found = -1;\n    for (int i = 0; i < values.length; i++) {\n        if (values[i] == target) {\n            found = i;\n        }\n    }\n    return found;\n}\n\nvoid main() {\n}\n'},
    ("Find-the-first: return as soon as you find a match.", "Return i inside the loop; return -1 after it."),
    starter_compiles=False, role="retrieval", group="array-algorithms")

ex.method("write", "j1-l6.2-retrieve-minmax", "Smallest and largest apart", ["o1"], ["J1.10"], ["IMPL"],
    "Write a method called `spread` that is given a non-empty `int[]` called `values` and returns the difference between its largest and smallest elements. For example, `spread` of 4, 8, 15, 16 is 12.",
    [("spread", [("values", "int[]")], "int")], {"spread": lambda v: max(v) - min(v)},
    [(None, [[4, 8, 15, 16]]), (None, [[7]]), (None, [[-5, 5]])],
    [(None, [[3, 3, 3]], "all same"), (None, [[16, 15, 8, 4]], "descending"), (None, [[-9, -2, -5]], "all negative"), (None, [[0, 100]], "zero to hundred"), (None, [[2, 9, 1, 9, 2]], "repeated")],
    '// Write the spread method here.\n\nvoid main() {\n    IO.println(spread(new int[] {4, 8, 15, 16})); // should print 12\n}\n',
    'int spread(int[] values) {\n    int smallest = values[0];\n    int largest = values[0];\n    for (int value : values) {\n        if (value < smallest) {\n            smallest = value;\n        }\n        if (value > largest) {\n            largest = value;\n        }\n    }\n    return largest - smallest;\n}\n\nvoid main() {\n    IO.println(spread(new int[] {4, 8, 15, 16})); // should print 12\n}\n',
    {"first-and-last": 'int spread(int[] values) {\n    return values[values.length - 1] - values[0];\n}\n\nvoid main() {\n}\n'},
    ("Track the smallest and the largest in the same loop.", "Start both at values[0]; update each when a value beats it; return largest - smallest."),
    starter_compiles=False, role="retrieval", group="array-algorithms")

ex.method("debug", "j1-l6.2-debug-alias", "The backup that wasn't", ["o2", "o3"], ["J1.10"], ["DEBUG"],
    "`withBonus` should return a new array where every element is 10 higher, and leave the original array untouched. After calling it, the caller's own array has changed too. Find and fix the bug.",
    [("withBonus", [("scores", "int[]")], "int[]")], {"withBonus": lambda v: [x + 10 for x in v]},
    [(None, [[1, 2, 3]]), (None, [[]]), (None, [[0]]), ],
    [(None, [[50, 60]], "two scores"), (None, [[-10, 0, 10]], "negatives"), (None, [[100]], "one score"), (None, [[5, 5, 5, 5]], "four"), (None, [[1, 2, 3, 4, 5, 6]], "six")],
    'int[] withBonus(int[] scores) {\n    int[] result = scores;\n    for (int i = 0; i < result.length; i++) {\n        result[i] = result[i] + 10;\n    }\n    return result;\n}\n\nvoid main() {\n    int[] original = {1, 2, 3};\n    int[] boosted = withBonus(original);\n    IO.println(Arrays.toString(original)); // should print [1, 2, 3]\n    IO.println(Arrays.toString(boosted));\n}\n',
    'int[] withBonus(int[] scores) {\n    int[] result = Arrays.copyOf(scores, scores.length);\n    for (int i = 0; i < result.length; i++) {\n        result[i] = result[i] + 10;\n    }\n    return result;\n}\n\nvoid main() {\n    int[] original = {1, 2, 3};\n    int[] boosted = withBonus(original);\n    IO.println(Arrays.toString(original)); // should print [1, 2, 3]\n    IO.println(Arrays.toString(boosted));\n}\n',
    {"changes-nothing": 'int[] withBonus(int[] scores) {\n    return Arrays.copyOf(scores, scores.length);\n}\n\nvoid main() {\n}\n'},
    ("How many arrays exist after int[] result = scores;?", "That line makes result another name for the same array. Use Arrays.copyOf to make a separate one."),
    misconceptions=["MC12"],
    notes="The test checks the returned values; the main() output shows the aliasing (the original changes too). The mentor and the explain exercise cover the reasoning.")

ex.explain("j1-l6.2-explain-alias", "Two names, one array", ["o2"], ["J1.10"],
    "After `int[] a = {1, 2, 3}; int[] b = a; b[0] = 99;`, `a[0]` is also 99. Explain why, and how you would get an independent copy.",
    "A full answer says that b = a copies the reference, so a and b both refer to the same single array (aliases); changing an element through b changes the one array that a also sees; to get an independent copy use Arrays.copyOf.",
    {2: ("Says b = a makes both names refer to the same array (a reference is copied, not the elements), so a change via b shows through a, and names Arrays.copyOf for a real copy.",
         ["An array variable holds a reference. b = a copies the reference, so a and b are two names for the same array. Changing b[0] changes that one array, so a[0] shows 99. For a separate copy use Arrays.copyOf(a, a.length).",
          "There's only one array. a and b are aliases. To get an independent copy you have to copy the elements, e.g. with Arrays.copyOf."]),
     1: ("Says they're the same array or are linked, but doesn't explain references, or doesn't give a way to copy.",
         ["Because a and b are the same array.", "They're linked so use copyOf."]),
     0: ("Incorrect, for example says b is a separate copy, or that Java made a mistake.",
         ["b is a copy so a shouldn't change, it's a bug.", "a[0] changes because 99 is bigger."])},
    misconceptions=["MC12"])
print("6.2 written")
