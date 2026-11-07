import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-5"
from build import *
import outline, re, math
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'

def copies_doubling(n):
    cap, size, copies = 4, 0, 0
    # capacities double when full; each growth copies `size` (= cap) elements
    while size < n:
        if size == cap:
            copies += cap; cap *= 2
        size += 1
        if size < n and size == cap:
            pass
    return copies
def copies_doubling_fast(n):
    cap, copies = 4, 0
    while n > cap:
        copies += cap; cap *= 2
    return copies
for n in (0, 1, 4, 5, 8, 9, 1000, 12345):
    assert copies_doubling(n) == copies_doubling_fast(n), n
COPY_1000 = copies_doubling_fast(1000)               # 1020
COPY_PLUS1_1000 = sum(range(4, 1000))                # growing by one: copies size elements for adds 5..n
assert (COPY_1000, COPY_PLUS1_1000) == (1020, 499494)

# ====================================================================== 5.1.1
Lesson("j5-l1.1", "Counting steps and growth rates", ["J5.01"], [
    ("o1", "Work out how many times a statement runs for a given n, as a formula, for single, nested, triangular and halving loops"),
    ("o2", "Classify the growth of a piece of code as constant, logarithmic, linear, n log n, quadratic or exponential"),
    ("o3", "Explain what big-O leaves out, and why the size of n decides whether a cost matters"),
], ["j3-l5.3"], 45, ["I58", "I57", "R8"], r'''
## Before you start

You should be comfortable with loops and nested loops ([for loops and boundaries](j1-l4.3)) and with the idea that different collections cost different amounts ([Lists and sets](j3-l1.1)).

**Quick check.** How many times does `count++` run in `for (int i = 0; i < 5; i++) { for (int j = 0; j < 3; j++) { count++; } }`?

<details><summary>Show the answer</summary>

`5 * 3 = 15`. The inner loop runs 3 times for each of the 5 passes of the outer loop.

</details>

## Explanation

Two programs can give the same answer and differ enormously in how long they take. Stage 5 is about **predicting** that difference before you run anything, and about choosing structures and algorithms because of it.

### Count steps, not seconds

A stopwatch measures one machine on one day. To compare **algorithms**, count how many times the work repeats as the input size, which we call **n**, grows. Pick one representative statement (the comparison, the addition, the array access) and ask: *how many times does this run?*

```java
int count = 0;
for (int i = 0; i < n; i++) {
    count++;                        // runs n times
}
```

### The loop shapes you'll meet

**One loop** over n items runs the statement **n** times.

**Nested loops** multiply: two loops of n each give **n × n = n²**.

**A triangular nest**, where the inner loop starts at the outer index, does less work than a full square:

```java
for (int i = 0; i < n; i++) {
    for (int j = i; j < n; j++) {
        count++;
    }
}
```

The inner loop runs `n`, then `n-1`, then `n-2`, ... then `1` times. That sum is `n + (n-1) + ... + 1 = n(n+1)/2`. For n = 100 that's 5,050, about half of 100². Half of n² is still a quadratic shape.

**Halving or doubling** shrinks or grows the work by a constant factor each pass:

```java
while (n > 1) {
    n = n / 2;
    count++;                        // runs about log2(n) times
}
```

Starting from 1,000: 1000 → 500 → 250 → 125 → 62 → 31 → 15 → 7 → 3 → 1 is 9 steps. Each pass throws away half the problem, so even n = 1,000,000 needs only about 20 steps. That is **logarithmic** growth, and it's why binary search is so fast.

### Growth rates

Ordered from cheapest to most expensive:

| Name | Written | Typical source |
|---|---|---|
| constant | O(1) | `array[i]`, `list.get(i)` on an `ArrayList` `[I58]` |
| logarithmic | O(log n) | halving the problem each step |
| linear | O(n) | one pass over the data |
| n log n | O(n log n) | good sorting `[I57]` |
| quadratic | O(n²) | a loop inside a loop over the same data |
| exponential | O(2ⁿ) | trying every subset; naive recursive Fibonacci |

How they compare, in rough numbers of steps:

| n | log n | n log n | n² | 2ⁿ |
|---|---|---|---|---|
| 10 | 3 | 33 | 100 | 1,024 |
| 1,000 | 10 | about 10,000 | 1,000,000 | a number with 302 digits |
| 1,000,000 | 20 | about 20,000,000 | 1,000,000,000,000 | unthinkable |

At n = 10 they are all instant. At a million, the quadratic one is a million times the linear one. **The shape matters once n is big.**

### Big-O: the shape, without the clutter

**Big-O notation** keeps only the part of the formula that dominates for large n, and drops constant multipliers and smaller terms. So `n(n+1)/2 = n²/2 + n/2` is **O(n²)**, and `3n + 7` is **O(n)**. It describes how cost *grows*, usually for the **worst case**.

### What big-O leaves out

- **Constants.** An O(n) loop doing 100 operations per item can be slower than an O(n²) loop doing one, for small n.
- **Small n.** For ten items, nothing matters. Choose the simplest code unless n will be large.
- **The machine and the memory.** Counting steps ignores caches, memory and the library's own tuning. The Java documentation itself notes that `ArrayList`'s constant factor is low compared with `LinkedList`'s `[I58]`, even where the big-O is similar.
- **Which case.** Best, average and worst cases can differ.

Use big-O to **rule out** options that can't scale, and measurement (next lesson) to choose between those that can.

### Reading the code

To classify code, find the loops and ask how each one's repeat count depends on n. A call inside a loop counts as a loop too: `list.contains(x)` inside a loop over the same list is a loop inside a loop. That is O(n²), even though no second `for` is visible.

## Worked examples

### Example 1: counting a triangular nest

*Task: how many times does `count++` run for n = 4?*

```java
for (int i = 0; i < n; i++) {
    for (int j = 0; j < i; j++) {
        count++;
    }
}
```

**Step 1 — Inner runs for each i:** i = 0 gives 0, i = 1 gives 1, i = 2 gives 2, i = 3 gives 3.

**Step 2 — Add them up:** 0 + 1 + 2 + 3 = 6.

**Step 3 — General formula:** `n(n-1)/2`, and for n = 4 that's 6. ✓ This is O(n²).

### Example 2: classifying by reading

*Task: what's the growth of this method?*

```java
boolean hasDuplicate(List<Integer> values) {
    for (int i = 0; i < values.size(); i++) {
        for (int j = i + 1; j < values.size(); j++) {
            if (values.get(i).equals(values.get(j))) return true;
        }
    }
    return false;
}
```

**Step 1 — Two loops over the same list.** The inner starts after the outer.

**Step 2 — That's a triangular nest:** about n²/2 comparisons in the worst case, when there's no duplicate.

**Step 3 — Classify:** O(n²). For n = 100,000 that's about 5 billion comparisons.

## Predict, then run

::exercise{id=j5-l1.1-predict-counts}

## Where this is used

- **Reviews and design:** "this is O(n²) and n is a million" is a common, valid objection to a design.
- **Choosing a collection:** knowing `contains` on a list costs a pass but on a set does not `[I58]` decides which to use.
- **Reading library docs:** the Java documentation states costs such as "amortised constant time" and you now know what they mean.

## Common mistakes

:::mistake{id=MC90}
**Thinking a single `for` loop means O(n).** A method call inside the loop can hide another loop (`list.contains`, `String.indexOf`, `list.remove(0)`).
:::

:::mistake{id=MC91}
**Treating big-O as an exact running time.** It describes growth, and drops constants. Two O(n) algorithms can differ by a factor of fifty.
:::

:::mistake{id=MC92}
**Optimising for large n when n is small.** For ten items, the clearest code wins.
:::

## Practice

::exercise{id=j5-l1.1-write-steps}

::exercise{id=j5-l1.1-explain-growth}

## Further reading

- **`java.util.ArrayList`** `[I58]` states which operations run in constant, amortised constant and linear time.
- **`java.util.Arrays`** `[I57]` states that its `int[]` sort offers O(n log n) performance.
- **Qian & Lehman (2017)** `[R8]` on how novices reason about loops.

## How you'll be assessed

- The **write** exercise checks that you can derive the number of steps as a formula instead of running the loop (*implementation*).
- The **predict** exercise checks that you can count steps for small n (*identifying mistakes*).
- The **explain** exercise checks that you can classify code and say what big-O leaves out (*explanation*).
''' + FOOT)

ex = Exercises("j5-l1.1")
ex.predict("j5-l1.1-predict-counts", "Count the steps", ["o1"], ["J5.01"],
    "Work out what this program prints. Each method counts how many times its inner statement runs.",
    '''int linear(int n) {
    int c = 0;
    for (int i = 0; i < n; i++) {
        c++;
    }
    return c;
}

int nested(int n) {
    int c = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            c++;
        }
    }
    return c;
}

int triangle(int n) {
    int c = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            c++;
        }
    }
    return c;
}

int halving(int n) {
    int c = 0;
    while (n > 1) {
        n = n / 2;
        c++;
    }
    return c;
}

void main() {
    IO.println(linear(16));
    IO.println(nested(16));
    IO.println(triangle(16));
    IO.println(halving(16));
    IO.println(halving(1000));
    IO.println(halving(1));
}''', "16\n256\n120\n4\n9\n0",
    ("Work out each loop's repeat count as a formula in n, then substitute.", "linear n, nested n squared, triangle 0+1+...+15 = 120, halving 16 -> 8 -> 4 -> 2 -> 1 is 4 steps."),
    difficulty=3)
def tri(n): return n * (n + 1) // 2
def halvings(n):
    c = 0
    while n > 1: n //= 2; c += 1
    return c
def doublings(n):
    c, k = 0, 1
    while k < n: k *= 2; c += 1
    return c
ex.method("write", "j5-l1.1-write-steps", "Formulas, not loops", ["o1"], ["J5.01"], ["IMPL"],
    "Each method asks for the number of times a loop's statement would run, for a given `n`. Write the answer **directly**, without running the loop: the checks use sizes (up to a billion) where running the loop would take far too long.\n\n- `triangular(n)`: `for (int i = 0; i < n; i++) for (int j = i; j < n; j++) count++;`\n- `halvings(n)`: `while (n > 1) { n = n / 2; count++; }`\n- `doublings(n)`: `for (int k = 1; k < n; k *= 2) count++;`\n\nAll three are 0 when `n` is 0 or 1 or less, as the loops show.",
    [("triangular", [("n", "int")], "long"), ("halvings", [("n", "int")], "int"), ("doublings", [("n", "int")], "int")],
    {"triangular": lambda n: tri(max(n, 0)), "halvings": halvings, "doublings": doublings},
    [("triangular", [4]), ("halvings", [1000]), ("doublings", [9])],
    [("triangular", [0]), ("triangular", [1]), ("triangular", [100000]), ("triangular", [2000000000]), ("halvings", [1]), ("halvings", [1024]), ("halvings", [1000000000]), ("doublings", [1]), ("doublings", [2]), ("doublings", [1024]), ("doublings", [1025]), ("doublings", [1000000000])],
    'long triangular(int n) {\n    return 0;\n}\n\nint halvings(int n) {\n    return 0;\n}\n\nint doublings(int n) {\n    return 0;\n}',
    'long triangular(int n) {\n    long m = Math.max(n, 0);\n    return m * (m + 1) / 2;\n}\n\nint halvings(int n) {\n    int count = 0;\n    while (n > 1) {\n        n = n / 2;\n        count++;\n    }\n    return count;\n}\n\nint doublings(int n) {\n    int count = 0;\n    long k = 1;\n    while (k < n) {\n        k *= 2;\n        count++;\n    }\n    return count;\n}',
    {"triangular-off-by-one": 'long triangular(int n) {\n    long m = Math.max(n, 0);\n    return m * (m - 1) / 2;\n}\n\nint halvings(int n) {\n    int count = 0;\n    while (n > 1) {\n        n = n / 2;\n        count++;\n    }\n    return count;\n}\n\nint doublings(int n) {\n    int count = 0;\n    long k = 1;\n    while (k < n) {\n        k *= 2;\n        count++;\n    }\n    return count;\n}',
     "loops-through-triangular": 'long triangular(int n) {\n    long count = 0;\n    for (int i = 0; i < n; i++) {\n        for (int j = i; j < n; j++) {\n            count++;\n        }\n    }\n    return count;\n}\n\nint halvings(int n) {\n    int count = 0;\n    while (n > 1) {\n        n = n / 2;\n        count++;\n    }\n    return count;\n}\n\nint doublings(int n) {\n    int count = 0;\n    long k = 1;\n    while (k < n) {\n        k *= 2;\n        count++;\n    }\n    return count;\n}'},
    ("triangular is the sum n + (n-1) + ... + 1. The other two count how many times you can halve, or double, before reaching n.", "triangular: n * (n + 1) / 2 (use long). halvings and doublings are short loops: they take about log2(n) passes."),
    difficulty=4)
ex.explain("j5-l1.1-explain-growth", "Classify and compare", ["o2", "o3"], ["J5.01"],
    "Classify each as O(1), O(log n), O(n), O(n log n) or O(n²), with one sentence of reasoning: (a) `values.get(0)` on an `ArrayList`; (b) a loop that adds up every element of an array; (c) `while (n > 1) n = n / 2;`; (d) for each element of a list, call `list.contains(x)` on the same list. Then say, for (b) and (d) with n = 1,000,000, roughly how many steps each takes, and give one thing big-O leaves out.",
    "A full answer classifies (a) O(1), (b) O(n), (c) O(log n), (d) O(n²) because contains is itself a loop inside the loop; gives about a million steps for (b) and about a trillion (10^12) for (d); and names something big-O leaves out, such as constant factors, small n, or the machine.",
    {2: ("Classifies a-d as O(1), O(n), O(log n), O(n²) with correct reasons (including that contains is a hidden inner loop), gives about a million for (b) and about 10^12 for (d), and names one thing big-O omits.",
         ["(a) O(1): ArrayList get is constant time. (b) O(n): one pass. (c) O(log n): it halves each time. (d) O(n squared): contains is a loop, so it's a loop inside a loop. For n = 1,000,000, (b) is about a million steps and (d) about a trillion. Big-O leaves out constant factors, so an O(n) method with heavy work per item can be slower than an O(n squared) one for small n.",
          "a is O(1), b is O(n), c is O(log n), d is O(n^2) since contains scans the list for every element. At a million items b takes about 10^6 steps and d about 10^12. Big-O ignores constants and doesn't say anything about small inputs."]),
     1: ("Gets three or four classifications right, or gives the classifications without the step counts or the omission.",
         ["(a) O(1) (b) O(n) (c) O(log n) (d) O(n).", "b is a million steps."]),
     0: ("Incorrect, for example says (d) is O(n) because there is only one visible loop.",
         ["(d) is O(n) because there's one for loop.", "They're all O(n)."])})
reg({"j5-l1.1": ("Counting steps and growth rates", ["J5.01"])},
    {"MC90": (["J5.01"], "Platform", "One visible loop means linear time, whatever its body calls"),
     "MC91": (["J5.01"], "Platform", "Big-O is the exact running time of the code"),
     "MC92": (["J5.01"], "Platform", "A lower growth rate is always the better choice, even for tiny n")})

# ====================================================================== 5.1.2
Lesson("j5-l1.2", "Measuring honestly and spotting accidental quadratics", ["J5.02"], [
    ("o1", "Say why a single stopwatch reading misleads, and what a fair measurement does instead"),
    ("o2", "Find a loop that is accidentally quadratic and replace it with a linear version"),
    ("o3", "Explain why you measure before optimising and what a performance requirement should say"),
], ["j5-l1.1"], 45, ["I60", "I58", "I59", "R16"], r'''
## Before you start

You should be able to count the steps of loops and name growth rates ([Counting steps and growth rates](j5-l1.1)).

**Quick check.** `list.contains(x)` inside a loop over the same list: what growth rate?

<details><summary>Show the answer</summary>

Quadratic, O(n²): `contains` scans the list, so it's a loop inside a loop.

</details>

## Explanation

### Accidental quadratics

Most slow programs aren't doing something exotic. They're doing something **ordinary inside a loop**, and the ordinary thing costs a pass over the data. These calls each hide a loop:

| Call | Why it costs O(n) |
|---|---|
| `list.contains(x)`, `list.indexOf(x)` | scans the list `[I58]` |
| `list.remove(0)` on an `ArrayList` | shifts every later element left |
| `text += piece` | copies the whole string so far |
| `string.indexOf(...)`, `string.contains(...)` | scans the string |

Put one of those inside a loop over n items and you have O(n²). With 100,000 items that's billions of steps, a program that takes minutes where a better one takes milliseconds.

### The usual fixes

- **A membership test in a loop** → put the items in a `HashSet` first. A hash set's `contains` doesn't scan: a hash-based collection's `get` and `put` take constant time, provided the hash function spreads the keys out `[I59]`. So "have I seen this before?" becomes O(1) per item, and the whole loop O(n).
- **Building a string** → use a `StringBuilder`, which appends without recopying.
- **Removing from the front repeatedly** → use an `ArrayDeque`, or index through the list instead.
- **Looking up the same thing repeatedly** → compute it once and keep it in a `Map`.

```java
// quadratic: contains() scans the list every time
boolean hasDuplicate(List<Integer> values) {
    List<Integer> seen = new ArrayList<>();
    for (int v : values) {
        if (seen.contains(v)) return true;      // O(n) inside an O(n) loop
        seen.add(v);
    }
    return false;
}

// linear: a set answers "seen it?" in constant time
boolean hasDuplicate(List<Integer> values) {
    Set<Integer> seen = new HashSet<>();
    for (int v : values) {
        if (!seen.add(v)) return true;          // add returns false if it was already there
    }
    return false;
}
```

### Measuring honestly

You can time code with `System.nanoTime()`. The Java documentation says it can only be used to measure **elapsed time**, and the value has an arbitrary starting point `[I60]`:

```java
long start = System.nanoTime();
doTheWork();
long elapsedNanos = System.nanoTime() - start;
```

One reading from one run proves very little:

- **Runs vary.** Other programs, the operating system and memory management all add noise. Run it **several times** and look at the spread, not one number.
- **The first runs are often slower than later ones.** The Java runtime may optimise code it sees used repeatedly, so code run once isn't typical of code run a million times. Do a few throwaway runs first, then measure.
- **Measure the thing you care about** with realistic input sizes, not a toy.
- **Compare ratios, not exact times.** "Ten times slower when n doubles twice" tells you a growth rate. "Took 38 ms" tells you only about today's laptop.

Specialised benchmarking tools exist for serious work. For this course, the best evidence is a **step count** or a **growth ratio**: run with n, then with 2n, and see how the cost changes. Double the work for double the input means linear; four times the work means quadratic.

### Measure before you optimise

Optimising code that isn't the slow part wastes effort and makes code harder to read. The order is:

1. **State the requirement:** "the report must finish in under two seconds for 200,000 transactions".
2. **Measure** to find where the time goes.
3. **Fix the biggest cost** first (usually a change of algorithm or structure, not a clever trick).
4. **Measure again** to confirm.

A requirement without numbers ("make it faster") can't be checked. The checks in this course's exercises work the same way: they run your code with a large input and a time limit.

## Worked examples

### Example 1: replacing contains with a set

*Task: `firstRepeat(values)` should return the index of the first value that has appeared before, or -1. It must handle 200,000 values quickly.*

**Step 1 — What's the slow part of the obvious version?** Scanning the earlier values for each new one: O(n²).

**Step 2 — What do we need to ask?** "Have I seen this value?" That's a set question.

**Step 3 — Write it with a `HashSet`:**

```java
int firstRepeat(List<Integer> values) {
    Set<Integer> seen = new HashSet<>();
    for (int i = 0; i < values.size(); i++) {
        if (!seen.add(values.get(i))) {
            return i;
        }
    }
    return -1;
}
```

**Step 4 — Check the growth.** One pass, constant work per item: O(n).

### Example 2: reading a doubling experiment

*Task: a method takes 1 second for n = 10,000 and 4 seconds for n = 20,000. What's its growth?*

**Step 1 — Doubling n multiplied the time by 4.**

**Step 2 — That's the signature of n²** (2² = 4).

**Step 3 — Predict n = 40,000:** about 16 seconds, and for n = 200,000, about 400 seconds. Time to look for the hidden loop.

## Where this is used

- **Slow reports and batch jobs** are very often one `contains` or `+=` inside a loop.
- **Performance reviews** ask for evidence: a measured baseline, a change, a measured improvement.
- **Capacity planning** needs to know how cost grows with load.

## Common mistakes

:::mistake{id=MC93}
**Judging performance from a single run.** Runs vary, and the first run is not typical. Repeat, and compare ratios.
:::

:::mistake{id=MC94}
**Using a list for membership tests.** `list.contains` scans. Use a `Set` when you ask "is it in there?" repeatedly.
:::

:::mistake{id=MC95}
**Optimising without a measurement or a requirement.** You may speed up code that wasn't the slow part, and you can't tell whether you're done.
:::

## Practice

::exercise{id=j5-l1.2-debug-duplicates}

::exercise{id=j5-l1.2-debug-concat}

::exercise{id=j5-l1.2-write-firstrepeat}

::exercise{id=j5-l1.2-explain-measure}

## Further reading

- **`System.nanoTime`** `[I60]` documents what it can and can't be used for.
- **`java.util.HashMap`** `[I59]` states the constant-time `get` and `put`, and `ArrayList` `[I58]` states the costs of list operations.
- **McCauley et al. (2008)** `[R16]` on debugging: a slow program is debugged the same way as a wrong one, by forming a hypothesis and testing it.

## How you'll be assessed

- The **debug** and **write** exercises run your code on large inputs under a time limit, so only a genuinely efficient solution passes (*debugging, implementation*).
- The **explain** exercise checks that you can say why a single timing misleads and why to measure before optimising (*explanation*).
''' + FOOT)

ex = Exercises("j5-l1.2")
DUP_DRV = '\n\nString run(int n, boolean duplicate) {\n    List<Integer> values = new ArrayList<>();\n    for (int i = 0; i < n; i++) {\n        values.add(i);\n    }\n    if (duplicate && n > 0) {\n        values.add(0);\n    }\n    return String.valueOf(hasDuplicate(values));\n}'
DUP_BAD = 'boolean hasDuplicate(List<Integer> values) {\n    for (int i = 0; i < values.size(); i++) {\n        for (int j = i + 1; j < values.size(); j++) {\n            if (values.get(i).equals(values.get(j))) {\n                return true;\n            }\n        }\n    }\n    return false;\n}'
DUP_OK = 'boolean hasDuplicate(List<Integer> values) {\n    Set<Integer> seen = new HashSet<>();\n    for (Integer v : values) {\n        if (!seen.add(v)) {\n            return true;\n        }\n    }\n    return false;\n}'
ex.method("debug", "j5-l1.2-debug-duplicates", "Correct, but far too slow", ["o2"], ["J5.02"], ["DEBUG"],
    "`hasDuplicate` gives the right answer, but the checks also run it on **100,000 values** with a 2-second limit, and it times out. The driver `run` builds the list (with one repeat at the very end when `duplicate` is true). Find the accidental quadratic and make `hasDuplicate` linear.",
    [("run", [("n", "int"), ("duplicate", "boolean")], "String")], {"run": lambda n, d: "true" if d and n > 0 else "false"},
    [("run", [5, True]), ("run", [5, False]), ("run", [0, True])],
    [("run", [1, True]), ("run", [100000, False]), ("run", [100000, True]), ("run", [50000, False]), ("run", [2, True])],
    DUP_BAD + DUP_DRV, DUP_OK + DUP_DRV,
    {"adjacent-only": 'boolean hasDuplicate(List<Integer> values) {\n    for (int i = 0; i + 1 < values.size(); i++) {\n        if (values.get(i).equals(values.get(i + 1))) {\n            return true;\n        }\n    }\n    return false;\n}' + DUP_DRV,
     "still-quadratic": 'boolean hasDuplicate(List<Integer> values) {\n    List<Integer> seen = new ArrayList<>();\n    for (Integer v : values) {\n        if (seen.contains(v)) {\n            return true;\n        }\n        seen.add(v);\n    }\n    return false;\n}' + DUP_DRV},
    ("Two loops over the same list make n squared work. What data structure answers \"have I seen this?\" in constant time?", "Keep a HashSet of what you've seen; if add returns false, it's a repeat."),
    difficulty=3)
CAT_DRV = '\n\nint run(int n) {\n    return build(n).length();\n}'
CAT_BAD = 'String build(int n) {\n    String text = "";\n    for (int i = 0; i < n; i++) {\n        if (i > 0) {\n            text += ",";\n        }\n        text += i;\n    }\n    return text;\n}'
CAT_OK = 'String build(int n) {\n    StringBuilder text = new StringBuilder();\n    for (int i = 0; i < n; i++) {\n        if (i > 0) {\n            text.append(",");\n        }\n        text.append(i);\n    }\n    return text.toString();\n}'
def build_len(n):
    return sum(len(str(i)) for i in range(n)) + max(n - 1, 0)
ex.method("debug", "j5-l1.2-debug-concat", "A string built the slow way", ["o2"], ["J5.02"], ["DEBUG"],
    "`build(n)` returns the numbers `0,1,2,...` up to `n - 1`, separated by commas. The driver `run` returns the length of the result. It's correct but, for 200,000 numbers, far too slow. Find out why, and fix it **without changing the result**.",
    [("run", [("n", "int")], "int")], {"run": build_len},
    [("run", [0]), ("run", [5]), ("run", [11])],
    [("run", [1]), ("run", [1000]), ("run", [200000]), ("run", [100000]), ("run", [12])],
    CAT_BAD + CAT_DRV, CAT_OK + CAT_DRV,
    {"insert-at-front": 'String build(int n) {\n    StringBuilder text = new StringBuilder();\n    for (int i = n - 1; i >= 0; i--) {\n        text.insert(0, i);\n        if (i < n - 1) {\n            text.insert(String.valueOf(i).length(), ",");\n        }\n    }\n    return text.toString();\n}' + CAT_DRV},
    ("Every += on a String copies the whole string built so far. What mutable type avoids that?", "Use a StringBuilder and append."),
    source_tests=[("builds with a StringBuilder", ["StringBuilder"], None)],
    difficulty=3)
def first_rep(n, at):
    return at if 1 <= at < n else -1
FR_DRV = '\n\nString run(int n, int repeatAt) {\n    List<Integer> values = new ArrayList<>();\n    for (int i = 0; i < n; i++) {\n        values.add(i * 2);\n    }\n    if (repeatAt >= 1 && repeatAt < n) {\n        values.set(repeatAt, 0);\n        if (repeatAt + 1 < n) {\n            values.set(repeatAt + 1, 2);\n        }\n    }\n    return String.valueOf(firstRepeat(values));\n}'
FR_OK = 'int firstRepeat(List<Integer> values) {\n    Set<Integer> seen = new HashSet<>();\n    for (int i = 0; i < values.size(); i++) {\n        if (!seen.add(values.get(i))) {\n            return i;\n        }\n    }\n    return -1;\n}'
ex.method("write", "j5-l1.2-write-firstrepeat", "Where does the first repeat appear?", ["o2"], ["J5.02"], ["IMPL"],
    "Write `firstRepeat(List<Integer> values)`: the **index** of the first value that has already appeared earlier in the list, or `-1` if every value is new. It must be fast: the checks use 200,000 values. The driver builds a list and plants repeats.",
    [("run", [("n", "int"), ("repeatAt", "int")], "String")], {"run": lambda n, a: str(first_rep(n, a))},
    [("run", [10, 4]), ("run", [10, 0]), ("run", [5, 99])],
    [("run", [2, 1]), ("run", [200000, 199999]), ("run", [200000, 100000]), ("run", [200000, 0]), ("run", [100000, 50000]), ("run", [1, 1])],
    'int firstRepeat(List<Integer> values) {\n    return -1;\n}' + FR_DRV,
    FR_OK + FR_DRV,
    {"quadratic": 'int firstRepeat(List<Integer> values) {\n    List<Integer> seen = new ArrayList<>();\n    for (int i = 0; i < values.size(); i++) {\n        if (seen.contains(values.get(i))) {\n            return i;\n        }\n        seen.add(values.get(i));\n    }\n    return -1;\n}' + FR_DRV,
     "returns-the-value": FR_OK.replace("return i;", "return values.get(i);") + FR_DRV},
    ("Go through the list once, remembering what you've seen in a set. add returns false when the value was already there.", "if (!seen.add(values.get(i))) return i;"),
    difficulty=3)
ex.explain("j5-l1.2-explain-measure", "Is it really faster?", ["o1", "o3"], ["J5.02"],
    "A teammate says: \"I ran my new version once and it took 40 ms; the old one took 55 ms, so it's faster.\" (a) Give two reasons this evidence is weak. (b) Describe a better way to compare them. (c) The report is \"slow\": what should the requirement look like, and what do you do **before** changing any code?",
    "A full answer says one run is affected by noise and by the first run being untypical, and the sizes may not be realistic; a better comparison repeats the measurements after a few warm-up runs, with realistic input sizes, and compares ratios or growth as n doubles; and the requirement should be a number (e.g. under two seconds for 200,000 records), measuring first to find where the time goes before changing anything.",
    {2: ("Gives two reasons one run is weak (noise and variation, first run not typical, unrealistic input), a better method (repeat after warm-up, realistic sizes, compare ratios or growth), and a numeric requirement with measuring first.",
         ["One run is noisy, and the first run is often slower than later ones, so 40 versus 55 could be chance. Better: warm up, run each several times on realistic sizes, and compare the ratio, or see how the time grows when n doubles. The requirement should be a number, like under two seconds for 200,000 records, and I'd measure first to find the slow part before changing code.",
          "It's a single measurement, which varies, and the input may not be realistic. I'd repeat both versions several times after a warm-up, with big inputs, and compare how they scale. The requirement needs a number and I'd profile or measure before editing anything."]),
     1: ("Gives a valid reason or a better method, but not both, or doesn't give a numeric requirement or the measure-first step.",
         ["One run isn't enough.", "Measure it several times."]),
     0: ("Incorrect, for example says the 15 ms difference proves it is faster, or that you should optimise first and measure later.",
         ["It's faster, 40 is less than 55.", "Just rewrite the code and see."])})
reg({"j5-l1.2": ("Measuring honestly and spotting accidental quadratics", ["J5.02"])},
    {"MC93": (["J5.02"], "I60", "One timing of one run shows which version is faster"),
     "MC94": (["J5.02"], "I58", "A List is a good choice for repeated membership tests"),
     "MC95": (["J5.02"], "R16", "Optimise first, then measure")})

# ====================================================================== 5.2.1
Lesson("j5-l2.1", "Dynamic arrays", ["J5.03"], [
    ("o1", "Implement a growable array of ints that doubles its capacity when full"),
    ("o2", "Count the element copies that growth causes, and explain why doubling gives constant average cost per add"),
    ("o3", "Find and fix an off-by-one error in the growth check"),
], ["j5-l1.2", "j2-l2.2"], 50, ["I58", "R8"], r'''
## Before you start

You should know that arrays have a fixed size ([Arrays](j1-l6.1)), what `ArrayList` offers ([ArrayList](j1-l6.3)), and how to protect an object's fields ([Private fields and invariants](j2-l2.1)).

**Quick check.** You have a full `int[4]` and want to add a fifth value. What can you do?

<details><summary>Show the answer</summary>

Make a **new, bigger** array, copy the old values into it, and add the new one there. An array can't be resized in place.

</details>

## Explanation

Over the next six lessons you'll **build** the structures the standard library gives you, so that you understand what they cost and when they fail. Each is small, and you'll compare it with the real one.

### What an `ArrayList` is inside

An `ArrayList` is a **resizable array** `[I58]`: inside is an ordinary array, with a `size` counting how many slots are in use, and a **capacity**, the length of the array:

```
capacity 8:  [ 7 | 3 | 9 | 4 | 0 | 0 | 0 | 0 ]
size 4:        used          unused
```

`add` puts the value at `data[size]` and increments `size`. When `size == capacity`, there is no room, so the list must **grow**: allocate a bigger array, copy everything across, and carry on.

### Writing it

```java
class IntList {
    private int[] data = new int[4];     // capacity starts at 4
    private int size;                    // slots in use

    void add(int value) {
        if (size == data.length) {                           // full
            data = Arrays.copyOf(data, data.length * 2);     // new array, twice as big, old values copied
        }
        data[size] = value;
        size++;
    }

    int get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("index " + index + ", size " + size);
        }
        return data[index];
    }

    int size() { return size; }
    int capacity() { return data.length; }
}
```

Three details deserve attention:

1. **The growth check.** `size == data.length` means *full*. Testing `size > data.length` is one step too late, because `data[size]` has already run off the end of the array.
2. **`get` checks against `size`, not the array length.** With capacity 8 and size 5, `data[6]` exists but holds a leftover 0. Without the check, `get(6)` would silently return garbage.
3. **Doubling.** Why double, and not add 1?

### Why double: counting the copies

Growing costs a copy of every element. Compare two policies for adding n values, starting from capacity 4:

- **Grow by 1** when full: every add after the fourth copies the whole array. Adding 1,000 values copies `4 + 5 + ... + 999 = 499,494` elements, about n²/2. That's O(n²).
- **Double** when full: growths happen at sizes 4, 8, 16, 32, ... 512. Adding 1,000 values copies `4 + 8 + ... + 512 = 1,020` elements, about n.

With doubling, the total copying is less than 2n, however large n gets. So adding n items costs O(n) in total, and the average cost per add is **constant**. We call that **amortised constant time**, which is the term the Java documentation uses for `ArrayList.add`, noting that adding n elements requires O(n) time `[I58]`.

*Amortised* means: most adds are cheap, a few (the growth ones) are expensive, and spread over all the adds the average stays constant. A single add can still be slow; many adds are not.

### What a dynamic array is good and bad at

| Operation | Cost | Why |
|---|---|---|
| `get(i)`, `set(i, v)` | O(1) | direct array access `[I58]` |
| `add` at the end | amortised O(1) | doubling `[I58]` |
| insert or remove at the front or middle | O(n) | everything after must shift |
| `contains` | O(n) | scan |

That mix, instant access by position and cheap appends, is why `ArrayList` is the default list.

## Worked examples

### Example 1: tracing the growth

*Task: after adding 9 values, what are `size` and `capacity`?*

**Step 1 — Capacity starts at 4.** Values 1-4 fit.

**Step 2 — Adding the 5th finds the array full:** capacity becomes 8, 4 values copied.

**Step 3 — Adding the 9th finds it full again:** capacity becomes 16, 8 values copied.

**Step 4 — Result:** `size = 9`, `capacity = 16`, and 4 + 8 = 12 elements were copied in total.

### Example 2: the missing bounds check

*Task: `list.get(6)` returns 0 when the list holds 5 values. Why?*

**Step 1 — What's `data.length`?** 8 after the first growth.

**Step 2 — So `data[6]` is a valid array index** (an unused slot, still 0).

**Step 3 — Fix:** check `index >= size`, and throw `IndexOutOfBoundsException`.

## Where this is used

- **`ArrayList`, `StringBuilder`, `ArrayDeque`, `HashMap`** all grow by allocating bigger arrays and copying.
- **Capacity hints:** `new ArrayList<>(100_000)` avoids repeated growth when you know the size.
- **Interviews and design:** "why is `add` amortised constant?" is a standard question.

## Common mistakes

:::mistake{id=MC96}
**Growing by a fixed amount (+1 or +10).** Every growth copies everything, so adding n items is O(n²). Grow by a factor, such as doubling.
:::

:::mistake{id=MC97}
**Checking the index against the array length instead of the size.** Unused slots look valid, and the list returns leftover zeros.
:::

:::mistake{id=MC98}
**Testing `size > data.length` for fullness.** It's one step too late and the add crashes. Test `size == data.length`.
:::

## Practice

::exercise{id=j5-l2.1-write-intlist}

::exercise{id=j5-l2.1-debug-grow}

::exercise{id=j5-l2.1-write-copies}

::exercise{id=j5-l2.1-explain-amortised}

## Further reading

- **`java.util.ArrayList`** `[I58]` documents the capacity, constant-time access and amortised constant-time add.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can implement the growth and count the copies (*implementation*).
- The **debug** exercise checks that you can fix an off-by-one in the growth check (*debugging*).
- The **explain** exercise checks that you can say why doubling gives constant average cost (*explanation*).
''' + FOOT)

ex = Exercises("j5-l2.1")
IL_DRV = '\n\nString run(int n) {\n    IntList list = new IntList();\n    for (int i = 0; i < n; i++) {\n        list.add(i);\n    }\n    long sum = 0;\n    for (int i = 0; i < n; i++) {\n        sum += list.get(i);\n    }\n    boolean badIndex;\n    try {\n        list.get(n);\n        badIndex = false;\n    } catch (IndexOutOfBoundsException e) {\n        badIndex = true;\n    }\n    return "size=" + list.size() + " capacity=" + list.capacity() + " sum=" + sum + " badIndex=" + badIndex;\n}'
IL_SOL = 'class IntList {\n    private int[] data = new int[4];\n    private int size;\n\n    void add(int value) {\n        if (size == data.length) {\n            data = Arrays.copyOf(data, data.length * 2);\n        }\n        data[size] = value;\n        size++;\n    }\n\n    int get(int index) {\n        if (index < 0 || index >= size) {\n            throw new IndexOutOfBoundsException("index " + index + ", size " + size);\n        }\n        return data[index];\n    }\n\n    int size() {\n        return size;\n    }\n\n    int capacity() {\n        return data.length;\n    }\n}'
def il_run(n):
    cap = 4
    while cap < n: cap *= 2
    return f"size={n} capacity={cap} sum={n * (n - 1) // 2} badIndex=true"
ex.method("write", "j5-l2.1-write-intlist", "Your own growable array", ["o1"], ["J5.03"], ["IMPL"],
    "Write `IntList`: a growable array of `int`s **built on a plain `int[]`** (no `ArrayList`). Start with capacity 4 and **double** it whenever the array is full. It needs `add(int)`, `get(int)`, `size()` and `capacity()`. `get` must throw an `IndexOutOfBoundsException` for an index that isn't in `0..size-1`, even when the array has room. The driver adds `0..n-1`, reads them back, and tries to read index `n`.",
    [("run", [("n", "int")], "String")], {"run": il_run},
    [("run", [3]), ("run", [5]), ("run", [0])],
    [("run", [4]), ("run", [8]), ("run", [9]), ("run", [100]), ("run", [1000]), ("run", [1])],
    'class IntList {\n    void add(int value) {\n    }\n\n    int get(int index) {\n        return 0;\n    }\n\n    int size() {\n        return 0;\n    }\n\n    int capacity() {\n        return 0;\n    }\n}' + IL_DRV,
    IL_SOL + IL_DRV,
    {"grows-by-one": IL_SOL.replace("data.length * 2", "data.length + 1") + IL_DRV,
     "no-size-check": IL_SOL.replace("index < 0 || index >= size", "index < 0 || index >= data.length") + IL_DRV},
    ("Fields: an int[] with length 4, and a size. add: if full, copy into an array twice as long; then store and count. get: check against size.", "if (size == data.length) data = Arrays.copyOf(data, data.length * 2);"),
    source_tests=[("built on an int array", ["int[]"], ["ArrayList"])],
    difficulty=3)
IL_BAD = IL_SOL.replace("if (size == data.length) {", "if (size > data.length) {")
ex.method("debug", "j5-l2.1-debug-grow", "The list that grows too late", ["o3"], ["J5.03"], ["DEBUG"],
    "This `IntList` works for up to 4 values, then crashes with an `ArrayIndexOutOfBoundsException`. Find the off-by-one in the growth check and fix it.",
    [("run", [("n", "int")], "String")], {"run": il_run},
    [("run", [3]), ("run", [5]), ("run", [0])],
    [("run", [4]), ("run", [8]), ("run", [9]), ("run", [100]), ("run", [1000])],
    IL_BAD + IL_DRV, IL_SOL + IL_DRV,
    {"grows-too-early-and-by-one": IL_SOL.replace("data.length * 2", "data.length + 4") + IL_DRV},
    ("When exactly is the array full? What's the first value of size for which data[size] is out of range?", "The array is full when size == data.length, so grow when that is true, before storing."),
    difficulty=2)
ex.method("write", "j5-l2.1-write-copies", "How many copies?", ["o2"], ["J5.03"], ["IMPL"],
    "Write `copiesWhenAdding(n)`: the total number of element copies caused by growth when `n` values are added one at a time to an `IntList` that starts at capacity 4 and **doubles** when full. (Growing from capacity `c` copies `c` elements.) Don't simulate adding `n` values one by one: the checks go up to a billion. Work out the capacities instead.",
    [("copiesWhenAdding", [("n", "int")], "long")], {"copiesWhenAdding": copies_doubling_fast},
    [("copiesWhenAdding", [9]), ("copiesWhenAdding", [4]), ("copiesWhenAdding", [0])],
    [("copiesWhenAdding", [5]), ("copiesWhenAdding", [8]), ("copiesWhenAdding", [1000]), ("copiesWhenAdding", [1000000]), ("copiesWhenAdding", [1000000000]), ("copiesWhenAdding", [1])],
    'long copiesWhenAdding(int n) {\n    return 0;\n}',
    'long copiesWhenAdding(int n) {\n    long capacity = 4;\n    long copies = 0;\n    while (n > capacity) {\n        copies += capacity;\n        capacity *= 2;\n    }\n    return copies;\n}',
    {"counts-the-final-capacity-too": 'long copiesWhenAdding(int n) {\n    long capacity = 4;\n    long copies = 0;\n    while (n >= capacity) {\n        copies += capacity;\n        capacity *= 2;\n    }\n    return copies;\n}',
     "grows-by-one": 'long copiesWhenAdding(int n) {\n    long copies = 0;\n    for (long size = 4; size < n; size++) {\n        copies += size;\n    }\n    return copies;\n}'},
    ("A growth happens each time the number of values exceeds the capacity. Add the capacity to the total, then double it, until the capacity covers n.", "while (n > capacity) { copies += capacity; capacity *= 2; }"),
    difficulty=4)
ex.explain("j5-l2.1-explain-amortised", "Doubling or adding one?", ["o2"], ["J5.03"],
    f"A dynamic array starts at capacity 4. Adding 1,000 values when it **doubles** copies {COPY_1000:,} elements in total; adding 1,000 values when it grows by **one** each time copies {COPY_PLUS1_1000:,}. (a) Explain why the difference is so large. (b) What does \"amortised constant time\" mean for `add` with doubling? (c) Does that mean every single `add` is fast?",
    "A full answer says growing by one copies the whole array on nearly every add so the total is about n squared over two, while doubling grows rarely so the total copies stay below about 2n; amortised constant means the average cost per add stays constant over many adds; and no, an individual add that triggers growth is slow, but those are rare.",
    {2: ("Explains that growing by one copies everything on almost every add (about n squared / 2) while doubling grows rarely and keeps the total below about 2n; says amortised constant is the average cost per add over many adds; and says an individual growth add is still slow.",
         ["Growing by one copies the whole array on almost every add, so the total is about n squared over two, around half a million for 1,000. Doubling only copies at sizes 4, 8, 16 and so on, so the total stays below about 2n. Amortised constant time means the average cost per add stays constant when you spread the expensive growth over all the adds. But the add that triggers a growth is still slow, so not every single add is fast.",
          "With +1 growth nearly every add copies all the elements, so the cost adds up to roughly n^2/2. With doubling the growths are rare and the copies add up to under 2n. Amortised constant means the average per add is constant. The growth adds are still slow individually."]),
     1: ("Explains why doubling copies less, or what amortised means, but not both, or says every add is fast.",
         ["Doubling copies less because it grows less often.", "Amortised means on average."]),
     0: ("Incorrect, for example says doubling wastes memory so is worse, or that amortised means each add takes exactly the same time.",
         ["Doubling is worse because of memory.", "Every add takes the same time."])})
reg({"j5-l2.1": ("Dynamic arrays", ["J5.03"])},
    {"MC96": (["J5.03"], "I58", "Growing an array by a fixed amount each time is just as efficient as doubling"),
     "MC97": (["J5.03"], "Platform", "An index inside the array's length is a valid index for the list"),
     "MC98": (["J5.03"], "Platform", "An array is full when size is greater than its length")})

# ====================================================================== 5.2.2
Lesson("j5-l2.2", "Linked lists", ["J5.04"], [
    ("o1", "Implement a singly linked list with addFirst, addLast, removeFirst and reverse"),
    ("o2", "Trace what changes when links are reassigned, and predict the result"),
    ("o3", "Find and fix a link-handling bug that loses part of the list"),
], ["j5-l2.1"], 50, ["I58", "R8", "R18"], r'''
## Before you start

You should know what a reference is, and that two variables can point at one object ([Objects and references](j2-l1.3)), and how a dynamic array behaves ([Dynamic arrays](j5-l2.1)).

**Quick check.** After `Player b = a; b = new Player("Bo");`, does `a` still refer to the first player?

<details><summary>Show the answer</summary>

Yes. Assigning to `b` changes only what `b` refers to, not `a`.

</details>

## Explanation

### A chain of nodes

A dynamic array keeps its values side by side in one block of memory. A **linked list** takes the opposite approach: each value lives in its own small object, a **node**, which holds the value and a **reference to the next node**:

```
head ──▶ [ 1 | • ]──▶ [ 2 | • ]──▶ [ 3 | null ]
```

The list object holds just the **head**, a reference to the first node, and `null` marks the end.

```java
class IntLinkedList {
    private Node head;
    private int size;

    private static class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
}
```

`static` on `Node` says a node doesn't need a reference to a particular list.

### Adding and removing at the front

The head makes front operations simple, and they take constant time, whatever the length:

```java
void addFirst(int value) {
    Node node = new Node(value);
    node.next = head;        // the new node points at the old first node
    head = node;             // the list now starts at the new node
    size++;
}

void removeFirst() {
    if (head != null) {
        head = head.next;    // skip the first node
        size--;
    }
}
```

Order matters: set `node.next` **before** moving `head`, or you lose the old list.

### Adding at the end: walking the chain

With only a head reference, reaching the end means walking the whole chain:

```java
void addLast(int value) {
    Node node = new Node(value);
    if (head == null) {
        head = node;
    } else {
        Node current = head;
        while (current.next != null) {
            current = current.next;
        }
        current.next = node;
    }
    size++;
}
```

That's O(n). (Real lists often keep a `tail` reference too.) The empty list is a special case: there's no node to walk from.

### Reversing: three references

Reversing a list means turning every link around. The classic way keeps three references while walking:

```java
void reverse() {
    Node previous = null;
    Node current = head;
    while (current != null) {
        Node next = current.next;    // 1. remember where to go next
        current.next = previous;     // 2. turn this link around
        previous = current;          // 3. step forward
        current = next;
    }
    head = previous;
}
```

Step 1 is essential. Once you overwrite `current.next` in step 2, the rest of the list would be unreachable if you hadn't saved it first, and the nodes after it become garbage. Forgetting to save `next` is the most common linked-list bug.

### Visiting every node

```java
for (Node current = head; current != null; current = current.next) {
    // use current.value
}
```

### Linked list versus dynamic array

| Operation | Linked list | Dynamic array |
|---|---|---|
| add or remove at the front | O(1) | O(n) (shifting) |
| add at the end | O(n) with only a head, O(1) with a tail | amortised O(1) |
| get the item at position i | O(n) (walk i steps) | O(1) |
| memory | an object per item, plus a reference | one block |

Java's `LinkedList` is a **doubly** linked list (each node knows both neighbours), and an indexed operation walks from whichever end is nearer `[I58]`. The documentation also notes that `ArrayList`'s constant factor is low compared with `LinkedList`'s `[I58]`. In practice an `ArrayList` is the better default; a linked structure pays off when you add and remove at the ends a lot, and there you'd more often use an `ArrayDeque` (lesson 5.2.3).

### Seeing the references

When a linked structure misbehaves, **draw the arrows**. Step-through visualisers such as the one described in `[R18]` draw exactly these node-and-arrow pictures, and drawing them on paper works just as well.

## Worked examples

### Example 1: tracing a reassignment

*Task: nodes `a(1) → b(2) → c(3)`. What does `a.next = c` do?*

**Step 1 — Before:** a points at b, b points at c.

**Step 2 — After `a.next = c`:** a points at c directly. The list from `a` is now `1 → 3`.

**Step 3 — What about b?** Nothing points to it any more (unless another variable does), so it drops out of the list.

### Example 2: reversing `1 → 2 → 3`

*Task: trace `reverse` on `1 → 2 → 3`.*

| Step | `previous` | `current` | links after the step |
|---|---|---|---|
| start | null | 1 | 1→2→3 |
| after 1st pass | 1 | 2 | 1→null, 2→3 |
| after 2nd pass | 2 | 3 | 2→1, 1→null, 3 unchanged |
| after 3rd pass | 3 | null | 3→2→1→null |

When `current` is null, `previous` (the old last node, 3) becomes the head. The list is `3 → 2 → 1`.

## Predict, then run

::exercise{id=j5-l2.2-predict-links}

## Where this is used

- **Inside the JDK:** `LinkedList`, hash-table buckets, and queues in many libraries are linked structures.
- **Interviews:** reversing a list is a classic, because it exercises exactly the careful reference handling above.
- **Other structures:** trees and graphs are nodes with several links, so this is the foundation for the next lessons.

## Common mistakes

:::mistake{id=MC99}
**Overwriting a link before saving it.** `current.next = previous` without first keeping `current.next` loses the rest of the list.
:::

:::mistake{id=MC100}
**Forgetting the empty list.** `head` is `null`, so code that does `head.next` throws a `NullPointerException`.
:::

:::mistake{id=MC101}
**Believing `get(i)` on a linked list is fast.** It has to walk `i` links. Use an array-based list for indexed access.
:::

## Practice

::exercise{id=j5-l2.2-write-list}

::exercise{id=j5-l2.2-debug-reverse}

::exercise{id=j5-l2.2-explain-compare}

## Further reading

- **`java.util.ArrayList` and `LinkedList`** `[I58]` describe the costs and the doubly linked design.
- **Guo (2013)** `[R18]` describes a step-through tool that draws references as arrows.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercise checks that you can implement the list, including reversal (*implementation*).
- The **predict** exercise checks that you can trace what links point at (*identifying mistakes*).
- The **debug** exercise checks that you can fix a reversal that loses nodes (*debugging*).
- The **explain** exercise checks that you can compare a linked list with an array list (*explanation*).
''' + FOOT)

ex = Exercises("j5-l2.2")
LL_DRV = '\n\nString run(String[] ops) {\n    IntLinkedList list = new IntLinkedList();\n    for (String op : ops) {\n        if (op.startsWith("first:")) {\n            list.addFirst(Integer.parseInt(op.substring(6)));\n        } else if (op.startsWith("last:")) {\n            list.addLast(Integer.parseInt(op.substring(5)));\n        } else if (op.equals("removeFirst")) {\n            list.removeFirst();\n        } else if (op.equals("reverse")) {\n            list.reverse();\n        }\n    }\n    return list + " size=" + list.size();\n}'
LL_SOL = 'class IntLinkedList {\n    private Node head;\n    private int size;\n\n    private static class Node {\n        int value;\n        Node next;\n\n        Node(int value) {\n            this.value = value;\n        }\n    }\n\n    void addFirst(int value) {\n        Node node = new Node(value);\n        node.next = head;\n        head = node;\n        size++;\n    }\n\n    void addLast(int value) {\n        Node node = new Node(value);\n        if (head == null) {\n            head = node;\n        } else {\n            Node current = head;\n            while (current.next != null) {\n                current = current.next;\n            }\n            current.next = node;\n        }\n        size++;\n    }\n\n    void removeFirst() {\n        if (head != null) {\n            head = head.next;\n            size--;\n        }\n    }\n\n    void reverse() {\n        Node previous = null;\n        Node current = head;\n        while (current != null) {\n            Node next = current.next;\n            current.next = previous;\n            previous = current;\n            current = next;\n        }\n        head = previous;\n    }\n\n    int size() {\n        return size;\n    }\n\n    @Override\n    public String toString() {\n        StringBuilder text = new StringBuilder("[");\n        for (Node current = head; current != null; current = current.next) {\n            if (current != head) {\n                text.append(", ");\n            }\n            text.append(current.value);\n        }\n        return text.append("]").toString();\n    }\n}'
def ll_run(ops):
    xs = []
    for op in ops:
        if op.startswith("first:"): xs.insert(0, int(op[6:]))
        elif op.startswith("last:"): xs.append(int(op[5:]))
        elif op == "removeFirst":
            if xs: xs.pop(0)
        elif op == "reverse": xs.reverse()
    return "[" + ", ".join(map(str, xs)) + f"] size={len(xs)}"
LL_CASES_V = [("run", [["last:1", "last:2", "last:3"]]), ("run", [["first:1", "first:2", "reverse"]]), ("run", [[]])]
LL_CASES_H = [("run", [["removeFirst"]]), ("run", [["last:5", "removeFirst", "last:6"]]), ("run", [["last:1", "last:2", "last:3", "last:4", "reverse"]]), ("run", [["reverse"]]), ("run", [["first:3", "last:4", "first:2", "removeFirst", "reverse", "last:9"]]), ("run", [["last:1", "reverse", "reverse", "first:0"]])]
ex.method("write", "j5-l2.2-write-list", "A linked list from nodes", ["o1"], ["J5.04"], ["IMPL"],
    "Write `IntLinkedList`, a **singly linked list of `int`s built from your own nodes** (no `LinkedList` or `ArrayList`). It needs `addFirst`, `addLast`, `removeFirst` (does nothing on an empty list), `reverse()` (changes the list in place), `size()` and a `toString()` that gives `[1, 2, 3]` (and `[]` when empty). The driver applies operations such as `\"first:5\"`, `\"last:7\"`, `\"removeFirst\"` and `\"reverse\"`.",
    [("run", [("ops", "String[]")], "String")], {"run": ll_run}, LL_CASES_V, LL_CASES_H,
    'class IntLinkedList {\n    void addFirst(int value) {\n    }\n\n    void addLast(int value) {\n    }\n\n    void removeFirst() {\n    }\n\n    void reverse() {\n    }\n\n    int size() {\n        return 0;\n    }\n\n    @Override\n    public String toString() {\n        return "[]";\n    }\n}' + LL_DRV,
    LL_SOL + LL_DRV,
    {"reverse-loses-nodes": LL_SOL.replace("            Node next = current.next;\n            current.next = previous;\n            previous = current;\n            current = next;", "            current.next = previous;\n            previous = current;\n            current = current.next;"),
     "add-last-skips-empty-case": LL_SOL.replace("        if (head == null) {\n            head = node;\n        } else {\n            Node current = head;", "        {\n            Node current = head;"),
     "size-not-updated-on-remove": LL_SOL.replace("            head = head.next;\n            size--;", "            head = head.next;")},
    ("Each node holds a value and a next reference. addFirst: point the new node at the old head, then move head. reverse: save next, turn the link, step forward.", "Node next = current.next; current.next = previous; previous = current; current = next;"),
    source_tests=[("built from nodes, not library lists", ["Node"], ["new LinkedList", "new ArrayList"])],
    difficulty=4)

ex.predict("j5-l2.2-predict-links", "Follow the arrows", ["o2"], ["J5.04"],
    "Work out what this program prints. Draw the nodes and arrows as you go: re-pointing a link changes what is reachable, not what exists.",
    '''class Node {
    int value;
    Node next;

    Node(int value, Node next) {
        this.value = value;
        this.next = next;
    }
}

void main() {
    Node c = new Node(3, null);
    Node b = new Node(2, c);
    Node a = new Node(1, b);
    Node head = a;
    IO.println(head.value + " " + head.next.value + " " + head.next.next.value);
    head = head.next;
    Node z = new Node(9, head);
    IO.println(z.next.next.value);
    b.next = null;
    IO.println(z.next.next == null);
    IO.println(a.next.value);
    IO.println(c.value);
}''', "1 2 3\n3\ntrue\n2\n3",
    ("Draw a -> b -> c. z points at b. After b.next = null, who still points at what?", "z -> b -> c at first, so z.next.next is 3. Then b no longer points at c, so z.next.next is null. a still points at b, and c still exists."),
    difficulty=3)
LL_BAD_REV = LL_SOL.replace("            Node next = current.next;\n            current.next = previous;\n            previous = current;\n            current = next;", "            current.next = previous;\n            previous = current;\n            current = current.next;")
ex.method("debug", "j5-l2.2-debug-reverse", "The reversal that loses the list", ["o3"], ["J5.04"], ["DEBUG"],
    "`reverse()` should turn `[1, 2, 3, 4]` into `[4, 3, 2, 1]`, but afterwards the list holds only one item. Find the bug in `reverse` and fix it. (Hint: what is `current.next` by the time the loop moves on?)",
    [("run", [("ops", "String[]")], "String")], {"run": ll_run}, LL_CASES_V, LL_CASES_H,
    LL_BAD_REV + LL_DRV, LL_SOL + LL_DRV,
    {"head-not-updated": LL_SOL.replace("        head = previous;\n", "")},
    ("Look at the order of the three assignments in the loop. Once current.next has been overwritten, where does the rest of the list go?", "Save the next node first: Node next = current.next; then turn the link, step previous, and move to next."),
    difficulty=3)
ex.explain("j5-l2.2-explain-compare", "Linked list or array list?", ["o1"], ["J5.04"],
    "You are choosing between a singly linked list (with only a head reference) and an array-based list for each task. For each, say which you would use and why, in terms of the cost of the operations: (a) read the 5,000th item, many times; (b) add and remove items at the **front** constantly; (c) add items at the end, millions of times, and read them back by position.",
    "A full answer chooses the array list for (a) because get by position is constant time while a linked list walks 5,000 links; the linked list for (b) because adding or removing at the head is constant time while an array must shift every element (though an ArrayDeque would be better still); and the array list for (c) because adding at the end is amortised constant and reading by position is constant, while a head-only linked list must walk the whole chain to add at the end.",
    {2: ("Chooses array list for (a), linked list (or a deque) for (b), and array list for (c), each with the cost reasoning: constant-time indexed access versus walking links, constant-time head operations versus shifting, amortised constant append versus walking to the end.",
         ["(a) Array list: get by position is constant time, but a linked list has to walk 5,000 links each time. (b) Linked list: adding and removing at the head is constant, whereas an array has to shift every element. (c) Array list: appending is amortised constant and reading by position is constant, while a linked list with only a head walks the whole chain to add at the end.",
          "a: array-based, because indexed access is O(1). b: linked, because front operations are O(1) and an array would shift everything (an ArrayDeque is even better). c: array-based, since add at the end is amortised O(1) and get(i) is O(1); the linked list needs to walk to the end each time."]),
     1: ("Gets two of the three right, or chooses correctly without the cost reasoning.",
         ["(a) array (b) linked (c) linked", "Array for reading and linked for the front."]),
     0: ("Incorrect, for example says linked lists are always faster, or always slower.",
         ["Linked lists are always faster.", "Arrays are always better."])})
reg({"j5-l2.2": ("Linked lists", ["J5.04"])},
    {"MC99": (["J5.04"], "R8", "Overwriting a node's next link and then following it still reaches the rest of the list"),
     "MC100": (["J5.04"], "Platform", "A linked list's head is never null, so head.next is always safe"),
     "MC101": (["J5.04"], "I58", "get(i) on a linked list is as fast as on an array list")})
print("5.1 and 5.2 (first two structures) written")
