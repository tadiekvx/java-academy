import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-5"
from build import *
import outline, re, itertools, heapq
from collections import deque, Counter
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'

def fib(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a
def naive_fib_calls(n): return 2 * fib(n + 1) - 1
assert naive_fib_calls(5) == 15
CALLS_40 = naive_fib_calls(40)

# ====================================================================== 5.3.1
Lesson("j5-l3.1", "Recursion", ["J5.09"], [
    ("o1", "Write recursive methods with a base case and a call on a smaller problem, including fast power and backtracking over subsets"),
    ("o2", "Trace a recursive method and predict what is printed before and after each call returns"),
    ("o3", "Fix a recursion that never stops, and explain what StackOverflowError means"),
], ["j5-l2.6", "j1-l5.3"], 55, ["I60", "R8", "R18"], r'''
## Before you start

You should understand the call stack ([Scope and the call stack](j1-l5.3)) and have met recursion in the tree code ([Binary search trees](j5-l2.5)).

**Quick check.** When a method calls another, what happens to the first method's local variables while the second runs?

<details><summary>Show the answer</summary>

They stay in the first method's **stack frame**, waiting. The second method gets its own frame with its own variables.

</details>

## Explanation

### A method that calls itself

A **recursive** method solves a problem by solving a **smaller version of the same problem**, then combining the result. Every correct recursive method has two parts:

1. **A base case:** an input small enough to answer directly, with no further call.
2. **A recursive case:** a call on a **smaller** input, which moves towards the base case.

```java
long sumTo(int n) {
    if (n <= 0) {
        return 0;                    // base case
    }
    return n + sumTo(n - 1);         // recursive case: a smaller problem
}
```

`sumTo(3)` is `3 + sumTo(2)`, which is `3 + (2 + sumTo(1))`, which is `3 + (2 + (1 + sumTo(0)))`, and `sumTo(0)` is 0. The answer is 6. A loop would do this job fine; recursion earns its place when the problem **naturally splits into smaller copies of itself**: trees, searching, sorting, backtracking.

### What the computer does: stack frames

Each call gets its own **stack frame** holding its own `n`. The calls pile up until the base case answers, then they **unwind**, each frame returning to the one below it. Printing on the way down and on the way back shows the order:

```java runnable
void countdown(int n) {
    if (n == 0) {
        IO.println("liftoff");
        return;
    }
    IO.println("down " + n);
    countdown(n - 1);
    IO.println("up " + n);
}

void main() {
    countdown(3);
}
```

It prints `down 3`, `down 2`, `down 1`, `liftoff`, `up 1`, `up 2`, `up 3`. The "down" lines come before the recursive call; the "up" lines run **after** it returns, in reverse order. Tracing means following exactly this.

### No base case, or no progress: `StackOverflowError`

The stack has a limited size. A recursion that never reaches its base case keeps adding frames until the Java runtime throws a **`StackOverflowError`**, which the documentation describes as thrown when an application **recurses too deeply** `[I60]`. Two usual causes:

- **A missing base case**: `return n + sumTo(n - 1);` with nothing to stop it.
- **A base case that's never reached**: the recursive call doesn't make the problem smaller (for example, `sumTo(n)` calling `sumTo(n)`), or the base case tests the wrong thing (`n == 0` when `n` can start negative).

Very deep but correct recursion (a hundred thousand levels) can overflow too. When depth could be huge, use a loop.

### Divide the problem: fast power

Computing `base^exp` by multiplying `exp` times is slow for a huge `exp`. But `base^exp = (base^(exp/2))²`, and that halves the problem each time, so the depth is only about log₂(exp). It also lets you keep numbers small by taking the remainder as you go (a "modular" power, widely used in cryptography):

```java
long powMod(long base, long exp, long mod) {
    if (exp == 0) return 1 % mod;
    long half = powMod(base, exp / 2, mod);
    long result = half * half % mod;
    if (exp % 2 == 1) result = result * (base % mod) % mod;
    return result;
}
```

For `exp = 10^18` that's about 60 calls. The loop version would run for longer than the universe has existed.

### Backtracking: try every choice

**Backtracking** explores choices, and at each step recurses on what's left. Generating all subsets of `"abc"`: for each letter, either **leave it out** or **put it in**, and recurse on the remaining letters:

```java
void collect(String letters, int index, String chosen, List<String> out) {
    if (index == letters.length()) {            // base case: every letter decided
        out.add(chosen);
        return;
    }
    collect(letters, index + 1, chosen, out);                         // leave letter out
    collect(letters, index + 1, chosen + letters.charAt(index), out); // put letter in
}
```

For n letters that's 2ⁿ subsets: exponential, and unavoidable if you want them all.

### Naive recursion can be exponential

The natural recursive Fibonacci, `fib(n) = fib(n-1) + fib(n-2)`, recomputes the same values over and over, and makes about 1.6ⁿ calls. The lesson on dynamic programming fixes this. Recursion isn't automatically fast or slow; **count the calls**.

## Worked examples

### Example 1: tracing a sum of digits

*Task: what is `sumDigits(9875)`?*

```java
int sumDigits(int n) {
    if (n == 0) return 0;
    return n % 10 + sumDigits(n / 10);
}
```

**Step 1 — Unwind the calls:** `5 + sumDigits(987)` → `5 + 7 + sumDigits(98)` → `5 + 7 + 8 + sumDigits(9)` → `5 + 7 + 8 + 9 + sumDigits(0)`.

**Step 2 — Base case:** `sumDigits(0)` is 0.

**Step 3 — Total:** 29. Each call removed one digit, so it makes progress, and `n / 10` eventually reaches 0.

### Example 2: spotting the missing base case

*Task: `sumTo(5)` crashes with `StackOverflowError`. Why?*

```java
long sumTo(int n) {
    return n + sumTo(n - 1);
}
```

**Step 1 — What stops it?** Nothing: `n` goes 5, 4, 3, 2, 1, 0, -1, ... forever.

**Step 2 — Add a base case** that handles the smallest input: `if (n <= 0) return 0;`.

**Step 3 — Check progress:** `n - 1` moves toward the base case.

## Predict, then run

::exercise{id=j5-l3.1-predict-trace}

## Where this is used

- **Trees and file systems:** walking a folder and everything inside it is naturally recursive.
- **Parsers and compilers** process nested structure recursively.
- **Search and puzzles** (solving a sudoku, finding routes, generating combinations) are backtracking.

## Common mistakes

:::mistake{id=MC114}
**Writing the recursive case without a base case.** The calls never stop and the program ends with `StackOverflowError`.
:::

:::mistake{id=MC115}
**A recursive call that doesn't make the problem smaller.** It repeats forever. Check that the argument moves toward the base case.
:::

:::mistake{id=MC116}
**Expecting the lines after a recursive call to run before it returns.** They run afterwards, as the calls unwind, in reverse order.
:::

## Practice

::exercise{id=j5-l3.1-write-powmod}

::exercise{id=j5-l3.1-write-subsets}

::exercise{id=j5-l3.1-debug-base}

::exercise{id=j5-l3.1-explain-stack}

## Further reading

- **`java.lang.StackOverflowError`** `[I60]` describes the error recursion can cause.
- **Guo (2013)** `[R18]` describes tools that show stack frames growing and unwinding.
- **Qian & Lehman (2017)** `[R8]` on how novices understand recursion.

## How you'll be assessed

- The **write** exercises check that you can write fast power and a backtracking enumeration (*implementation*).
- The **predict** exercise checks that you can trace calls and their unwinding (*identifying mistakes*).
- The **debug** exercise checks that you can add a missing base case (*debugging*).
- The **explain** exercise checks that you understand the stack and its limit (*explanation*).
''' + FOOT)

ex = Exercises("j5-l3.1")
ex.predict("j5-l3.1-predict-trace", "Down, then up", ["o2"], ["J5.09"],
    "Work out what this program prints. Remember that lines after a recursive call run as the calls unwind.",
    '''void countdown(int n) {
    if (n == 0) {
        IO.println("liftoff");
        return;
    }
    IO.println("down " + n);
    countdown(n - 1);
    IO.println("up " + n);
}

int sumDigits(int n) {
    if (n == 0) {
        return 0;
    }
    return n % 10 + sumDigits(n / 10);
}

int fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

void main() {
    countdown(3);
    IO.println(sumDigits(9875));
    IO.println(fib(10));
}''', "down 3\ndown 2\ndown 1\nliftoff\nup 1\nup 2\nup 3\n29\n55",
    ("The \"down\" lines print before the recursive call and the \"up\" lines after it returns. For sumDigits, peel off the last digit each time.", "countdown prints down 3, 2, 1, then liftoff, then up 1, 2, 3. sumDigits(9875) is 5+7+8+9 = 29. fib(10) is 55."),
    difficulty=3)
def powmod(b, e, m): return pow(b, e, m)
PM_SOL = 'long powMod(long base, long exp, long mod) {\n    if (exp == 0) {\n        return 1 % mod;\n    }\n    long half = powMod(base, exp / 2, mod);\n    long result = half * half % mod;\n    if (exp % 2 == 1) {\n        result = result * (base % mod) % mod;\n    }\n    return result;\n}'
ex.method("write", "j5-l3.1-write-powmod", "Fast power, recursively", ["o1"], ["J5.09"], ["IMPL"],
    "Write `powMod(base, exp, mod)`: `base` raised to the power `exp`, **remainder `mod`**, using recursion that **halves `exp`** each time (`base^exp = (base^(exp/2))²`, times another `base` if `exp` is odd). `exp` goes up to 10^18, so multiplying `exp` times is impossible. Take the remainder at each step so numbers stay below `mod²`. (`mod` is at most 10^9.)",
    [("powMod", [("base", "long"), ("exp", "long"), ("mod", "long")], "long")], {"powMod": powmod},
    [("powMod", [2, 10, 1000]), ("powMod", [3, 0, 7]), ("powMod", [5, 3, 13])],
    [("powMod", [2, 1000000000000000000, 1000000007]), ("powMod", [7, 123456789012345678, 998244353]), ("powMod", [10, 1, 7]), ("powMod", [1, 1000000000000000000, 5]), ("powMod", [999999999, 999999999999999999, 1000000000]), ("powMod", [0, 5, 3]), ("powMod", [6, 0, 1])],
    'long powMod(long base, long exp, long mod) {\n    return 0;\n}',
    PM_SOL,
    {"loops-exp-times": 'long powMod(long base, long exp, long mod) {\n    long result = 1 % mod;\n    for (long i = 0; i < exp; i++) {\n        result = result * (base % mod) % mod;\n    }\n    return result;\n}',
     "forgets-the-odd-case": PM_SOL.replace("    if (exp % 2 == 1) {\n        result = result * (base % mod) % mod;\n    }\n", "")},
    ("Base case: exp 0 gives 1 (mod mod). Otherwise compute the power of exp / 2, square it, and multiply by base once more when exp is odd.", "long half = powMod(base, exp / 2, mod); long result = half * half % mod; if (exp % 2 == 1) result = result * (base % mod) % mod;"),
    difficulty=4)
def subsets(s):
    out = []
    for r in range(len(s) + 1):
        for c in itertools.combinations(s, r): out.append("".join(c))
    return sorted(out, key=lambda x: (len(x), x))
SS_SOL = 'List<String> subsets(String letters) {\n    List<String> out = new ArrayList<>();\n    collect(letters, 0, "", out);\n    out.sort(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()));\n    return out;\n}\n\nvoid collect(String letters, int index, String chosen, List<String> out) {\n    if (index == letters.length()) {\n        out.add(chosen);\n        return;\n    }\n    collect(letters, index + 1, chosen, out);\n    collect(letters, index + 1, chosen + letters.charAt(index), out);\n}'
ex.method("write", "j5-l3.1-write-subsets", "Every subset, by backtracking", ["o1"], ["J5.09"], ["IMPL"],
    "Write `subsets(String letters)`: every subset of the letters (all different), including the empty one, each written with its letters in their **original order**. Return them sorted by length, then alphabetically: for `\"abc\"` that's `[\"\", \"a\", \"b\", \"c\", \"ab\", \"ac\", \"bc\", \"abc\"]`. Use recursion: for each letter, try leaving it out and putting it in.",
    [("subsets", [("letters", "String")], "List<String>")], {"subsets": subsets},
    [("subsets", ["abc"]), ("subsets", [""]), ("subsets", ["x"])],
    [("subsets", ["ab"]), ("subsets", ["cba"]), ("subsets", ["abcd"]), ("subsets", ["zy"]), ("subsets", ["hello"])],
    'List<String> subsets(String letters) {\n    return new ArrayList<>();\n}',
    SS_SOL,
    {"forgets-empty-subset": SS_SOL.replace('    collect(letters, 0, "", out);\n', '    collect(letters, 0, "", out);\n    out.remove("");\n'),
     "reorders-letters": SS_SOL.replace("chosen + letters.charAt(index)", "letters.charAt(index) + chosen")},
    ("Base case: when every letter has been decided, record what you chose. Otherwise recurse twice: once without the current letter, once with it.", "collect(letters, index + 1, chosen, out); collect(letters, index + 1, chosen + letters.charAt(index), out);"),
    difficulty=4)
ex.method("debug", "j5-l3.1-debug-base", "The recursion that never stops", ["o3"], ["J5.09"], ["DEBUG"],
    "`sumTo(n)` should return `1 + 2 + ... + n`, and `0` when `n` is 0 or negative. It throws a `StackOverflowError`. Find out why and fix it.",
    [("sumTo", [("n", "int")], "long")], {"sumTo": lambda n: max(n, 0) * (max(n, 0) + 1) // 2},
    [("sumTo", [5]), ("sumTo", [0]), ("sumTo", [1])],
    [("sumTo", [-3]), ("sumTo", [100]), ("sumTo", [1000]), ("sumTo", [2]), ("sumTo", [-1])],
    'long sumTo(int n) {\n    return n + sumTo(n - 1);\n}',
    'long sumTo(int n) {\n    if (n <= 0) {\n        return 0;\n    }\n    return n + sumTo(n - 1);\n}',
    {"base-case-only-at-zero": 'long sumTo(int n) {\n    if (n == 0) {\n        return 0;\n    }\n    return n + sumTo(n - 1);\n}'},
    ("What stops the calls? What happens to n as the calls go on, and what happens if n starts below zero?", "Add a base case: if (n <= 0) return 0;"),
    difficulty=2)
ex.explain("j5-l3.1-explain-stack", "Frames and overflow", ["o3"], ["J5.09"],
    "(a) What two parts must a correct recursive method have? (b) What is a stack frame, and what happens to the frames when the base case is reached? (c) A recursive method that is correct for small inputs throws `StackOverflowError` for an input of 500,000. Why does that happen, and what could you do?",
    "A full answer says a base case and a recursive case that moves toward it; that each call gets a frame holding its own variables, piled up until the base case answers and then unwound with each returning to the one below; and that a very deep recursion needs more frames than the stack allows so it overflows, and you can rewrite it as a loop (or reduce the depth, for example by halving).",
    {2: ("States base case and progress-making recursive case, explains frames pile up with their own variables and unwind after the base case, and explains that depth 500,000 exceeds the stack's limit with a fix such as a loop or a halving approach.",
         ["It needs a base case and a recursive case that makes the problem smaller. Each call gets its own stack frame with its own variables; they pile up until the base case returns, then they unwind one by one. With 500,000 levels there are too many frames for the stack, so it throws StackOverflowError. I could turn it into a loop, or change the algorithm so the depth is smaller, like halving the problem.",
          "A base case and a recursive step towards it. Frames hold each call's locals, stack up, and unwind after the base case. 500,000 deep is more than the stack allows, so use a loop instead."]),
     1: ("Answers two of the three parts well, or gives the right ideas without a fix.",
         ["A base case and a recursive case.", "It overflows because it is too deep."]),
     0: ("Incorrect, for example says the stack frames are deleted by the garbage collector, or that StackOverflowError means the base case was reached.",
         ["A StackOverflowError means it finished.", "You need to add more memory to the loop."])})
reg({"j5-l3.1": ("Recursion", ["J5.09"])},
    {"MC114": (["J5.09"], "I60", "A recursive method works without a base case"),
     "MC115": (["J5.09"], "Platform", "A recursive call on the same argument eventually stops"),
     "MC116": (["J5.09"], "R8", "Statements after a recursive call run before the call returns")})

# ====================================================================== 5.3.2
Lesson("j5-l3.2", "Binary search and sorting", ["J5.10"], [
    ("o1", "Write a binary search that finds the first occurrence in logarithmic time"),
    ("o2", "Write merge sort, and explain why it takes O(n log n)"),
    ("o3", "Fix off-by-one bugs in a binary search, and explain why the data must be sorted"),
], ["j5-l3.1"], 60, ["I57", "I58", "R8"], r'''
## Before you start

You should be comfortable with recursion ([Recursion](j5-l3.1)) and with counting growth rates ([Counting steps and growth rates](j5-l1.1)).

**Quick check.** About how many times can you halve 1,000,000 before reaching 1?

<details><summary>Show the answer</summary>

About 20.

</details>

## Explanation

### Binary search

Searching an unsorted list means checking every item: O(n). If the data is **sorted**, you can do far better. Look at the **middle** item. If it's the one you want, done. If your target is smaller, it can only be in the **left half**; if larger, the **right half**. Throw the other half away and repeat. Each step halves the search space, so about log₂ n steps are needed: 20 for a million items, 30 for a billion.

```java
int indexOf(int[] data, int target) {
    int low = 0;
    int high = data.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (data[mid] == target) return mid;
        if (data[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}
```

Notes that decide whether it works:

- **`low <= high`**: the range `low..high` is *inclusive*, and a range with one element has `low == high`. Using `<` skips that last candidate.
- **`mid = low + (high - low) / 2`** gives the same answer as `(low + high) / 2` but can't overflow `int` for huge arrays.
- **`mid + 1` and `mid - 1`**: the middle has been checked, so exclude it. Writing `low = mid` can loop forever when the range is two items.

### It only works on sorted data

The documentation for `Arrays.binarySearch` says the array **must be sorted**, and that if it isn't, the results are **undefined** `[I57]`. It also says that if the key is present several times, there is **no guarantee which one** is found, and that if the key is absent it returns `-(insertion point) - 1`, where the insertion point is where the key would go to keep the array sorted `[I57]`. So `-1` means "would go at index 0", and the result is negative if and only if the key isn't found.

### Finding the first occurrence

With duplicates (`[1, 2, 2, 2, 3]`), "found a 2" isn't specific enough. To find the **first** one, don't stop when you find the target. **Remember it and keep searching the left half:**

```java
int firstIndex(int[] data, int target) {
    int low = 0, high = data.length - 1, found = -1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (data[mid] == target) {
            found = mid;
            high = mid - 1;               // maybe there's an earlier one
        } else if (data[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return found;
}
```

This "search the left half even after a match" is the core of a **lower bound**, a building block for ranges and insertion points.

### Counting the work

Don't trust a stopwatch here: **count array reads.** For n = 1,000,000, a correct binary search reads at most about 21 elements. A linear scan reads up to a million. The exercises give you an array wrapper that counts reads, so a wrong-complexity answer fails even if it returns the right index.

### Sorting: insertion sort, then merge sort

**Insertion sort** builds a sorted prefix by inserting each next item into place. It's simple, and **O(n²)**: fine for tiny arrays, hopeless at 200,000 items.

**Merge sort** uses divide and conquer:

1. **Split** the array into two halves.
2. **Sort** each half (recursively; an array of 0 or 1 items is already sorted).
3. **Merge** the two sorted halves: repeatedly take the smaller of the two front items.

```java
int[] mergeSort(int[] values) {
    if (values.length <= 1) return values;
    int mid = values.length / 2;
    int[] left = mergeSort(Arrays.copyOfRange(values, 0, mid));
    int[] right = mergeSort(Arrays.copyOfRange(values, mid, values.length));
    int[] merged = new int[values.length];
    int i = 0, j = 0, k = 0;
    while (i < left.length && j < right.length) {
        merged[k++] = left[i] <= right[j] ? left[i++] : right[j++];
    }
    while (i < left.length) merged[k++] = left[i++];
    while (j < right.length) merged[k++] = right[j++];
    return merged;
}
```

**Why O(n log n)?** The halving goes about log₂ n levels deep, and at each level the merging touches every item once, about n steps. So log₂ n levels × n work = **n log n**. For n = 200,000 that's about 3.5 million steps, against insertion sort's roughly 20 billion.

The library sorts for you: `Arrays.sort(int[])` is documented as a Dual-Pivot Quicksort that offers O(n log n) performance on all data sets `[I57]`. And sorting **objects** with `List.sort` or `Arrays.sort(Object[])` is **stable**: equal elements keep their original order `[I57]` `[I58]`. In real code you'll nearly always call the library. You write merge sort to understand it.

### When does sorting pay?

Sort once for O(n log n), then each search is O(log n). One search: just scan (O(n)). A thousand searches over a million items: scanning is about 10⁹ steps, but sorting plus a thousand binary searches is about 2 × 10⁷. The more searches, the better sorting pays.

## Worked examples

### Example 1: first occurrence

*Task: in `[0, 0, 0, 1, 1, 1, 2, 2, 2]`, find the first index of 1.*

| low | high | mid | data[mid] | action |
|---|---|---|---|---|
| 0 | 8 | 4 | 1 | match: `found = 4`, `high = 3` |
| 0 | 3 | 1 | 0 | smaller: `low = 2` |
| 2 | 3 | 2 | 0 | smaller: `low = 3` |
| 3 | 3 | 3 | 1 | match: `found = 3`, `high = 2` |

Now `low > high`, so it stops. `found` is **3**, which is right: that's the first 1. Four reads for nine items.

### Example 2: merging two sorted halves

*Task: merge `[1, 4, 9]` and `[2, 3, 10]`.*

Compare the front items: 1 vs 2 → take 1; 4 vs 2 → take 2; 4 vs 3 → take 3; 4 vs 10 → take 4; 9 vs 10 → take 9; the left is empty, so append the rest: 10. Result: `[1, 2, 3, 4, 9, 10]`.

## Where this is used

- **Anywhere sorted data lives:** database indexes, `TreeMap`, search over sorted logs.
- **`Arrays.binarySearch` and `Collections.binarySearch`** in library code.
- **Merge sort's idea** (sort chunks, merge) is how data too big for memory gets sorted.

## Common mistakes

:::mistake{id=MC117}
**Using `<` instead of `<=` in the loop condition.** The range `low..high` is inclusive, so the last remaining candidate is skipped.
:::

:::mistake{id=MC118}
**Setting `low = mid` or `high = mid`.** The middle is already checked. Without `+ 1` / `- 1` the loop can run forever.
:::

:::mistake{id=MC119}
**Binary searching unsorted data.** The results are undefined. Sort first, or use another structure.
:::

:::mistake{id=MC120}
**Stopping at the first match when you want the first occurrence.** With duplicates the match may be in the middle of a run.
:::

## Practice

::exercise{id=j5-l3.2-write-first}

::exercise{id=j5-l3.2-write-mergesort}

::exercise{id=j5-l3.2-debug-first}

::exercise{id=j5-l3.2-explain-sorted}

## Further reading

- **`java.util.Arrays`** `[I57]` documents `binarySearch`'s preconditions and return value, and the sort's cost and stability.
- **`java.util.List`** `[I58]` documents that `List.sort` is stable.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can write a logarithmic search and a merge sort that handles 200,000 items (*implementation*).
- The **debug** exercise checks that you can fix an off-by-one binary search (*debugging*).
- The **explain** exercise checks that you can say why sorted data is required and when sorting pays (*explanation*).
''' + FOOT)

ex = Exercises("j5-l3.2")
CA = 'class CountingArray {\n    private final int[] data;\n    int reads;\n\n    CountingArray(int[] data) {\n        this.data = data;\n    }\n\n    int size() {\n        return data.length;\n    }\n\n    int get(int index) {\n        reads++;\n        return data[index];\n    }\n}\n\n'
BS_DRV = '\n\nString run(int n, int target) {\n    int[] data = new int[n];\n    for (int i = 0; i < n; i++) {\n        data[i] = i / 3;\n    }\n    CountingArray array = new CountingArray(data);\n    int index = firstIndex(array, target);\n    int limit = 2 * (32 - Integer.numberOfLeadingZeros(Math.max(n, 1))) + 4;\n    return index + " fast=" + (array.reads <= limit);\n}'
BS_SOL = 'int firstIndex(CountingArray array, int target) {\n    int low = 0;\n    int high = array.size() - 1;\n    int found = -1;\n    while (low <= high) {\n        int mid = low + (high - low) / 2;\n        int value = array.get(mid);\n        if (value == target) {\n            found = mid;\n            high = mid - 1;\n        } else if (value < target) {\n            low = mid + 1;\n        } else {\n            high = mid - 1;\n        }\n    }\n    return found;\n}'
def bs_run(n, t):
    first = next((i for i in range(min(n, 3 * (t + 1) + 3)) if i // 3 == t and i < n), -1) if t >= 0 else -1
    # first index with value t is 3*t if it exists
    first = 3 * t if 0 <= t and 3 * t < n else -1
    return f"{first} fast=true"
BS_V = [("run", [10, 1]), ("run", [10, 5]), ("run", [1, 0])]
BS_H = [("run", [1000000, 0]), ("run", [1000000, 333332]), ("run", [1000000, 333333]), ("run", [1000000, 17]), ("run", [999999, 333332]), ("run", [3, 0]), ("run", [3, 1]), ("run", [2000000, 600000])]
ex.method("write", "j5-l3.2-write-first", "A logarithmic search for the first match", ["o1"], ["J5.10"], ["IMPL"],
    "`CountingArray` wraps a sorted `int[]` and counts how many times `get` is called. Write `firstIndex(CountingArray array, int target)`: the index of the **first** occurrence of `target`, or `-1`. The values repeat (the array is `0,0,0,1,1,1,2,2,2,...`). The driver also checks `fast=true`: that you read only about `2 * log2(n)` elements, so a linear scan fails even if its answer is right.",
    [("run", [("n", "int"), ("target", "int")], "String")], {"run": bs_run}, BS_V, BS_H,
    CA + 'int firstIndex(CountingArray array, int target) {\n    for (int i = 0; i < array.size(); i++) {\n        if (array.get(i) == target) {\n            return i;\n        }\n    }\n    return -1;\n}' + BS_DRV,
    CA + BS_SOL + BS_DRV,
    {"any-match": CA + BS_SOL.replace("            found = mid;\n            high = mid - 1;", "            return mid;") + BS_DRV,
     "excludes-last-candidate": CA + BS_SOL.replace("while (low <= high)", "while (low < high)") + BS_DRV},
    ("Keep a low and high index and look at the middle. On a match, remember it but keep searching the left half (high = mid - 1).", "if (value == target) { found = mid; high = mid - 1; }"),
    source_tests=[("doesn't scan every element", None, ["for (int i = 0; i < array.size()"])],
    difficulty=4)
BS_BAD = BS_SOL.replace("    int high = array.size() - 1;\n    int found = -1;\n    while (low <= high) {", "    int high = array.size() - 1;\n    int found = -1;\n    while (low < high) {").replace("            found = mid;\n            high = mid - 1;", "            return mid;")
ex.method("debug", "j5-l3.2-debug-first", "Two off-by-one bugs", ["o3"], ["J5.10"], ["DEBUG"],
    "`firstIndex` should return the **first** index of `target` in a sorted array that contains repeats. It's fast, but it returns wrong answers: sometimes a later copy of the target, and sometimes `-1` for a value that's there. Find the two bugs.",
    [("run", [("n", "int"), ("target", "int")], "String")], {"run": bs_run}, BS_V, BS_H,
    CA + BS_BAD + BS_DRV, CA + BS_SOL + BS_DRV,
    {"fixes-only-the-loop": CA + BS_SOL.replace("            found = mid;\n            high = mid - 1;", "            return mid;") + BS_DRV},
    ("One bug is in the loop condition: is the range low..high inclusive? The other is what happens when the middle value matches: is it necessarily the first match?", "Use while (low <= high), and on a match record found = mid and continue with high = mid - 1."),
    difficulty=3)
def rand_array(n):
    return [(i * 2654435761) % 1000003 for i in range(n)]
def ms_run(n):
    a = sorted(rand_array(n))
    return f"sorted=true sum={sum(a)} first={a[0] if a else 0} last={a[-1] if a else 0}"
MS_DRV = '\n\nString run(int n) {\n    int[] values = new int[n];\n    for (int i = 0; i < n; i++) {\n        values[i] = (int) ((i * 2654435761L) % 1000003);\n    }\n    int[] sorted = mergeSort(values);\n    boolean ok = sorted.length == n;\n    long sum = 0;\n    for (int i = 0; i < sorted.length; i++) {\n        sum += sorted[i];\n        if (i > 0 && sorted[i - 1] > sorted[i]) {\n            ok = false;\n        }\n    }\n    return "sorted=" + ok + " sum=" + sum + " first=" + (n > 0 ? sorted[0] : 0) + " last=" + (n > 0 ? sorted[sorted.length - 1] : 0);\n}'
MS_SOL = 'int[] mergeSort(int[] values) {\n    if (values.length <= 1) {\n        return values;\n    }\n    int mid = values.length / 2;\n    int[] left = mergeSort(Arrays.copyOfRange(values, 0, mid));\n    int[] right = mergeSort(Arrays.copyOfRange(values, mid, values.length));\n    int[] merged = new int[values.length];\n    int i = 0;\n    int j = 0;\n    int k = 0;\n    while (i < left.length && j < right.length) {\n        merged[k++] = left[i] <= right[j] ? left[i++] : right[j++];\n    }\n    while (i < left.length) {\n        merged[k++] = left[i++];\n    }\n    while (j < right.length) {\n        merged[k++] = right[j++];\n    }\n    return merged;\n}'
ex.method("write", "j5-l3.2-write-mergesort", "Merge sort", ["o2"], ["J5.10"], ["IMPL"],
    "Write `mergeSort(int[] values)`: return a **new** sorted array (smallest first), using merge sort: split in half, sort each half recursively, merge. Don't use `Arrays.sort` or `List.sort`. The checks also sort 200,000 values under a 2-second limit, which an O(n²) sort can't do.",
    [("mergeSort", [("values", "int[]")], "int[]"), ("run", [("n", "int")], "String")], {"mergeSort": lambda v: sorted(v), "run": ms_run},
    [("mergeSort", [[5, 2, 9, 1]]), ("mergeSort", [[]]), ("mergeSort", [[3]])],
    [("mergeSort", [[2, 1]]), ("mergeSort", [[4, 4, 4, 1, 1]]), ("mergeSort", [[-5, 3, -1, 0, 7, -9]]), ("mergeSort", [[1, 2, 3, 4, 5]]), ("mergeSort", [[9, 8, 7, 6, 5, 4, 3, 2, 1]]), ("run", [200000]), ("run", [1000])],
    'int[] mergeSort(int[] values) {\n    return values.clone();\n}' + MS_DRV,
    MS_SOL + MS_DRV,
    {"insertion-sort": 'int[] mergeSort(int[] values) {\n    int[] a = values.clone();\n    for (int i = 1; i < a.length; i++) {\n        int x = a[i];\n        int j = i - 1;\n        while (j >= 0 && a[j] > x) {\n            a[j + 1] = a[j];\n            j--;\n        }\n        a[j + 1] = x;\n    }\n    return a;\n}' + MS_DRV,
     "drops-the-tail": MS_SOL.replace("    while (j < right.length) {\n        merged[k++] = right[j++];\n    }\n", "") + MS_DRV},
    ("Base case: 0 or 1 items are already sorted. Otherwise split at the middle, sort both halves, then merge by repeatedly taking the smaller front item, and copy whatever is left.", "int[] left = mergeSort(Arrays.copyOfRange(values, 0, mid)); int[] right = mergeSort(Arrays.copyOfRange(values, mid, values.length));"),
    source_tests=[("no library sort", ["mergeSort("], ["Arrays.sort", ".sort(", "Stream"])],
    difficulty=5)
ex.explain("j5-l3.2-explain-sorted", "Sorted first, then search", ["o3"], ["J5.10"],
    "(a) Why must the data be sorted for binary search, and what does `Arrays.binarySearch` promise if it isn't? (b) What does `Arrays.binarySearch` return when the key is absent, and what does `-4` tell you? (c) You must answer 1,000 membership queries about a list of 1,000,000 numbers. Compare scanning for each query with sorting once and then binary searching, in rough numbers of steps.",
    "A full answer says each step discards half the data on the assumption that the order tells you which half to keep, and the documentation says the results are undefined for unsorted data; that an absent key returns -(insertion point) - 1 so -4 means it would be inserted at index 3; and that scanning costs about 1,000 x 1,000,000 = 10^9 steps whereas sorting about 20 million steps plus 1,000 searches of about 20 steps is far cheaper.",
    {2: ("Says binary search discards half based on the order so unsorted data gives undefined results, says absent returns -(insertion point) - 1 so -4 means index 3, and compares about 10^9 steps for scanning with about 2 x 10^7 for sorting plus searching.",
         ["Binary search throws half the data away by comparing with the middle, which only works if the data is in order, so on unsorted data the result is undefined. For an absent key it returns -(insertion point) - 1, so -4 means the key would go at index 3. Scanning 1,000 times over a million items is about 10^9 steps; sorting once is about 20 million steps and then each of the 1,000 searches is about 20 steps, so sorting is much cheaper.",
          "It relies on the order to know which half to keep, otherwise it's undefined. Absent returns -(ip)-1, so -4 is insertion point 3. 1,000 scans is about a billion steps; sort plus 1,000 binary searches is about 20 million."]),
     1: ("Gets two of the three parts right, or gives them without numbers.",
         ["It has to be sorted, otherwise undefined.", "-4 means it would be inserted at index 3."]),
     0: ("Incorrect, for example says binary search works on any data, or that -1 means index 0 was found.",
         ["Binary search works on any list.", "-4 means the key is at index 4."])})
reg({"j5-l3.2": ("Binary search and sorting", ["J5.10"])},
    {"MC117": (["J5.10"], "Platform", "A binary search loop can use low < high without missing the last candidate"),
     "MC118": (["J5.10"], "Platform", "Setting low = mid is a safe way to move on after checking the middle"),
     "MC119": (["J5.10"], "I57", "Binary search gives a sensible answer on unsorted data"),
     "MC120": (["J5.10"], "I57", "The first match found by binary search is the first occurrence")})

# ====================================================================== 5.3.3
Lesson("j5-l3.3", "Graphs: representation and traversal", ["J5.11"], [
    ("o1", "Represent a graph as an adjacency list built from edge strings"),
    ("o2", "Use breadth-first search to find the fewest hops between two nodes, and count connected components"),
    ("o3", "Explain what BFS and DFS each do, and when to use which"),
], ["j5-l3.2", "j5-l2.3"], 55, ["I55", "R8", "R18"], r'''
## Before you start

You should be comfortable with queues ([Stacks and queues](j5-l2.3)) and recursion ([Recursion](j5-l3.1)).

**Quick check.** Which structure takes items out in the order they went in?

<details><summary>Show the answer</summary>

A queue (first in, first out).

</details>

## Explanation

### What a graph is

A **graph** is a set of **nodes** (also called vertices) joined by **edges**. It models anything made of things and connections: towns and roads, people and friendships, web pages and links, computers and cables.

- An **undirected** edge goes both ways (a road). A **directed** edge goes one way (a link from page A to page B).
- Two nodes are **connected** if some path of edges leads from one to the other.
- A **connected component** is a group of nodes that can all reach each other.

```
0 ─ 1 ─ 2        3 ─ 4        5
```

That graph has three components: `{0, 1, 2}`, `{3, 4}` and `{5}`.

### Representing it: the adjacency list

The usual representation is an **adjacency list**: for each node, the list of its neighbours.

```java
List<List<Integer>> graph = new ArrayList<>();
for (int i = 0; i < n; i++) {
    graph.add(new ArrayList<>());
}
for (String edge : edges) {                       // "1-2"
    String[] parts = edge.split("-");
    int a = Integer.parseInt(parts[0]);
    int b = Integer.parseInt(parts[1]);
    graph.get(a).add(b);                          // undirected: add both ways
    graph.get(b).add(a);
}
```

Memory use is proportional to the nodes plus the edges. Finding a node's neighbours is a direct lookup.

### Breadth-first search (BFS)

**BFS** explores outward in rings: first the start node, then everything one edge away, then everything two edges away, and so on. A **queue** gives that order, plus a record of what's been **visited** (so a loop in the graph doesn't send you round forever):

```java
int hops(int n, String[] edges, int from, int to) {
    List<List<Integer>> graph = buildGraph(n, edges);
    int[] distance = new int[n];
    Arrays.fill(distance, -1);                    // -1 means not visited yet
    Deque<Integer> queue = new ArrayDeque<>();
    distance[from] = 0;
    queue.offer(from);
    while (!queue.isEmpty()) {
        int node = queue.poll();
        for (int next : graph.get(node)) {
            if (distance[next] == -1) {           // first time we reach it
                distance[next] = distance[node] + 1;
                queue.offer(next);
            }
        }
    }
    return distance[to];                          // -1 if never reached
}
```

Because BFS reaches nodes **in order of distance**, the first time it reaches a node is by a **shortest path in number of edges**. That's why BFS answers "fewest hops": the fewest changes on a train map, the fewest clicks between two pages, the degrees of separation between two people.

`distance[next] == -1` is the visited check. Without it, every graph with a cycle makes BFS loop forever, and a graph without cycles still visits some nodes more than once.

### Depth-first search (DFS)

**DFS** goes **as deep as possible** along one path, and only backs up when it's stuck. It uses a **stack**, or recursion, which is the call stack doing that job:

```java
void dfs(List<List<Integer>> graph, int node, boolean[] visited) {
    visited[node] = true;
    for (int next : graph.get(node)) {
        if (!visited[next]) {
            dfs(graph, next, visited);
        }
    }
}
```

DFS doesn't find shortest paths, but it's the natural tool for **"everything reachable from here"**, for exploring structure, and for problems built on backtracking.

### Counting connected components

Start a search from every node you haven't visited yet. Each fresh start finds one whole component:

```java
int components(int n, String[] edges) {
    List<List<Integer>> graph = buildGraph(n, edges);
    boolean[] visited = new boolean[n];
    int count = 0;
    for (int node = 0; node < n; node++) {
        if (!visited[node]) {
            count++;
            dfs(graph, node, visited);
        }
    }
    return count;
}
```

### Cost

Both BFS and DFS visit each node once and look at each edge a constant number of times, so they take time proportional to **V + E** (nodes plus edges). That's linear in the size of the graph.

### Choosing

| You want | Use |
|---|---|
| fewest edges between two nodes | BFS |
| everything reachable, or connected components | DFS or BFS |
| explore all possibilities with backtracking | DFS |

## Worked examples

### Example 1: BFS by hand

*Task: edges `0-1`, `0-2`, `1-3`, `2-3`, `3-4`. How many hops from 0 to 4?*

**Step 1 — Start:** queue `[0]`, `distance[0] = 0`.

**Step 2 — Process 0:** its neighbours 1 and 2 get distance 1. Queue `[1, 2]`.

**Step 3 — Process 1:** neighbour 3 gets distance 2. Process 2: neighbour 3 is already visited. Queue `[3]`.

**Step 4 — Process 3:** neighbour 4 gets distance 3.

**Step 5 — Answer:** `distance[4] = 3`.

### Example 2: components

*Task: 6 nodes (0 to 5), edges `0-1`, `1-2`, `3-4`. How many components?*

Start at 0: reaches 0, 1, 2 (count 1). Node 3 is unvisited: reaches 3, 4 (count 2). Node 5 is unvisited: just itself (count 3). **Three components.**

## Predict, then run

::exercise{id=j5-l3.3-predict-bfs}

## Where this is used

- **Maps and journey planners:** fewest stops or fewest changes is BFS.
- **Social networks:** friends-of-friends and degrees of separation.
- **Build systems and dependency resolvers** traverse graphs to find what depends on what.
- **Network and infrastructure monitoring:** "which machines can still reach each other?" is connected components.

## Common mistakes

:::mistake{id=MC121}
**Forgetting the visited check.** In a graph with a cycle the search never ends, and even without one it repeats work.
:::

:::mistake{id=MC122}
**Using DFS to find the fewest hops.** DFS finds *a* path, not the shortest. Use BFS.
:::

:::mistake{id=MC123}
**Adding an undirected edge in one direction only.** Add it to both nodes' lists.
:::

## Practice

::exercise{id=j5-l3.3-write-hops}

::exercise{id=j5-l3.3-write-components}

::exercise{id=j5-l3.3-explain-bfs-dfs}

## Further reading

- **`java.util.Deque` and `ArrayDeque`** `[I55]` for the queue and stack the searches use.
- **Guo (2013)** `[R18]` describes tools that make traversals visible step by step.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can build an adjacency list, run BFS, and count components (*implementation*).
- The **predict** exercise checks that you can trace BFS order (*identifying mistakes*).
- The **explain** exercise checks that you can say what BFS and DFS find, and when to use which (*explanation*).
''' + FOOT)

ex = Exercises("j5-l3.3")
def build_graph(n, edges):
    g = [[] for _ in range(n)]
    for e in edges:
        a, b = map(int, e.split("-")); g[a].append(b); g[b].append(a)
    return g
def hops(n, edges, frm, to):
    g = build_graph(n, edges); dist = [-1] * n; dist[frm] = 0; q = deque([frm])
    while q:
        u = q.popleft()
        for v in g[u]:
            if dist[v] == -1: dist[v] = dist[u] + 1; q.append(v)
    return dist[to]
def comps(n, edges):
    g = build_graph(n, edges); seen = [False] * n; c = 0
    for s in range(n):
        if not seen[s]:
            c += 1; st = [s]; seen[s] = True
            while st:
                u = st.pop()
                for v in g[u]:
                    if not seen[v]: seen[v] = True; st.append(v)
    return c
GRAPH_HELPER = 'List<List<Integer>> buildGraph(int n, String[] edges) {\n    List<List<Integer>> graph = new ArrayList<>();\n    for (int i = 0; i < n; i++) {\n        graph.add(new ArrayList<>());\n    }\n    for (String edge : edges) {\n        String[] parts = edge.split("-");\n        int a = Integer.parseInt(parts[0]);\n        int b = Integer.parseInt(parts[1]);\n        graph.get(a).add(b);\n        graph.get(b).add(a);\n    }\n    return graph;\n}'
HOPS_SOL = GRAPH_HELPER + '\n\nint hops(int n, String[] edges, int from, int to) {\n    List<List<Integer>> graph = buildGraph(n, edges);\n    int[] distance = new int[n];\n    Arrays.fill(distance, -1);\n    Deque<Integer> queue = new ArrayDeque<>();\n    distance[from] = 0;\n    queue.offer(from);\n    while (!queue.isEmpty()) {\n        int node = queue.poll();\n        for (int next : graph.get(node)) {\n            if (distance[next] == -1) {\n                distance[next] = distance[node] + 1;\n                queue.offer(next);\n            }\n        }\n    }\n    return distance[to];\n}'
G1 = ["0-1", "0-2", "1-3", "2-3", "3-4"]
ex.method("write", "j5-l3.3-write-hops", "Fewest hops", ["o1", "o2"], ["J5.11"], ["IMPL"],
    "Write `hops(n, edges, from, to)`: the **fewest edges** on a path between two nodes in an undirected graph with nodes `0..n-1`; each edge is a string like `\"1-2\"`. It is 0 when `from == to`, and `-1` if `to` can't be reached. `buildGraph` is written for you. Use breadth-first search with a queue and a visited record.",
    [("hops", [("n", "int"), ("edges", "String[]"), ("from", "int"), ("to", "int")], "int")], {"hops": hops},
    [("hops", [5, G1, 0, 4]), ("hops", [3, ["0-1"], 0, 2]), ("hops", [2, [], 1, 1])],
    [("hops", [5, G1, 4, 0]), ("hops", [6, ["0-1", "1-2", "2-3", "3-4", "4-5", "0-5"], 0, 3]), ("hops", [4, ["0-1", "2-3"], 0, 3]), ("hops", [7, ["0-1", "1-2", "2-0", "2-3", "3-4", "5-6"], 0, 4]), ("hops", [4, ["0-1", "1-2", "2-3", "0-3"], 0, 2]), ("hops", [1, [], 0, 0])],
    GRAPH_HELPER + '\n\nint hops(int n, String[] edges, int from, int to) {\n    return -1;\n}',
    HOPS_SOL,
    {"depth-first-not-shortest": GRAPH_HELPER + '\n\nint hops(int n, String[] edges, int from, int to) {\n    List<List<Integer>> graph = buildGraph(n, edges);\n    boolean[] seen = new boolean[n];\n    int[] best = {-1};\n    walk(graph, from, to, 0, seen, best);\n    return best[0];\n}\n\nvoid walk(List<List<Integer>> graph, int node, int to, int depth, boolean[] seen, int[] best) {\n    seen[node] = true;\n    if (node == to) {\n        best[0] = depth;\n        return;\n    }\n    for (int next : graph.get(node)) {\n        if (!seen[next] && best[0] == -1) {\n            walk(graph, next, to, depth + 1, seen, best);\n        }\n    }\n}',
     "no-visited-check-limit": HOPS_SOL.replace("            if (distance[next] == -1) {\n                distance[next] = distance[node] + 1;\n                queue.offer(next);\n            }", "            if (distance[next] == -1 || distance[next] > distance[node] + 1) {\n                distance[next] = distance[node] + 1;\n                if (next != from) queue.offer(next);\n            }").replace("    distance[from] = 0;\n    queue.offer(from);", "    distance[from] = 0;\n    queue.offer(from);\n    if (from == to) return 1;")},
    ("Keep a distance array filled with -1 meaning unvisited, and a queue. When you first reach a neighbour, give it distance + 1 and queue it.", "if (distance[next] == -1) { distance[next] = distance[node] + 1; queue.offer(next); }"),
    difficulty=4)
COMP_SOL = GRAPH_HELPER + '\n\nvoid dfs(List<List<Integer>> graph, int node, boolean[] visited) {\n    visited[node] = true;\n    for (int next : graph.get(node)) {\n        if (!visited[next]) {\n            dfs(graph, next, visited);\n        }\n    }\n}\n\nint components(int n, String[] edges) {\n    List<List<Integer>> graph = buildGraph(n, edges);\n    boolean[] visited = new boolean[n];\n    int count = 0;\n    for (int node = 0; node < n; node++) {\n        if (!visited[node]) {\n            count++;\n            dfs(graph, node, visited);\n        }\n    }\n    return count;\n}'
ex.method("write", "j5-l3.3-write-components", "How many separate groups?", ["o2"], ["J5.11"], ["IMPL"],
    "Write `components(n, edges)`: the number of **connected components** in an undirected graph with nodes `0..n-1` (a node with no edges is a component of its own). `buildGraph` is written for you. Start a search from every node you haven't visited yet, and count the starts.",
    [("components", [("n", "int"), ("edges", "String[]")], "int")], {"components": comps},
    [("components", [6, ["0-1", "1-2", "3-4"]]), ("components", [3, []]), ("components", [4, ["0-1", "1-2", "2-3"]])],
    [("components", [1, []]), ("components", [5, ["0-1", "1-2", "2-0"]]), ("components", [7, ["0-1", "2-3", "4-5"]]), ("components", [4, ["0-3", "3-1", "1-2"]]), ("components", [6, ["0-1", "0-2", "0-3", "0-4", "0-5"]]), ("components", [8, ["0-1", "2-3", "1-2", "5-6"]])],
    GRAPH_HELPER + '\n\nint components(int n, String[] edges) {\n    return 0;\n}',
    COMP_SOL,
    {"counts-edges-groups": COMP_SOL.replace("            count++;\n            dfs(graph, node, visited);", "            dfs(graph, node, visited);\n            count += 2;"),
     "forgets-isolated-nodes": COMP_SOL.replace("for (int node = 0; node < n; node++) {\n        if (!visited[node]) {", "for (int node = 0; node < n; node++) {\n        if (!visited[node] && !graph.get(node).isEmpty()) {")},
    ("Keep a visited array. For each unvisited node, count one component and visit everything reachable from it.", "for each node: if (!visited[node]) { count++; dfs(graph, node, visited); }"),
    difficulty=3)
def bfs_order(n, edges, start):
    g = build_graph(n, edges); seen = [False] * n; seen[start] = True; q = deque([start]); order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in g[u]:
            if not seen[v]: seen[v] = True; q.append(v)
    return order
BFSP_EDGES = ["0-1", "0-2", "1-3", "2-3", "2-4", "3-5", "4-5"]
BFSP = GRAPH_HELPER + '\n\nvoid main() {\n    String[] edges = {"0-1", "0-2", "1-3", "2-3", "2-4", "3-5", "4-5"};\n    List<List<Integer>> graph = buildGraph(6, edges);\n    boolean[] seen = new boolean[6];\n    Deque<Integer> queue = new ArrayDeque<>();\n    List<Integer> order = new ArrayList<>();\n    seen[0] = true;\n    queue.offer(0);\n    while (!queue.isEmpty()) {\n        int node = queue.poll();\n        order.add(node);\n        for (int next : graph.get(node)) {\n            if (!seen[next]) {\n                seen[next] = true;\n                queue.offer(next);\n            }\n        }\n    }\n    IO.println(order);\n    IO.println(graph.get(3));\n}'
ex.predict("j5-l3.3-predict-bfs", "In what order are nodes visited?", ["o2"], ["J5.11"],
    "Work out what this program prints. The first line is the order in which breadth-first search visits the nodes, starting at 0, taking each node's neighbours in the order its edges were listed. The second line is node 3's neighbour list. Draw the graph first.",
    BFSP, str(bfs_order(6, BFSP_EDGES, 0)) + "\n" + str(build_graph(6, BFSP_EDGES)[3]),
    ("Build the adjacency lists in edge order, then process the queue: visit a node, queue its unvisited neighbours.", "From 0: queue 1 and 2. Process 1: queue 3. Process 2: queue 4 (3 is seen). Process 3: queue 5. So the order is 0 1 2 3 4 5."),
    difficulty=3)
ex.explain("j5-l3.3-explain-bfs-dfs", "Which search?", ["o3"], ["J5.11"],
    "(a) Why does breadth-first search find the fewest hops, while depth-first search doesn't have to? (b) What is the visited check for, and what goes wrong without it? (c) Which would you use to answer each: \"what is the fewest number of train changes from A to B?\" and \"are all the computers in this office connected to each other?\"",
    "A full answer says BFS explores outward in rings, reaching nodes in order of their distance, so the first time it reaches a node is by a shortest route, whereas DFS follows one long path as deep as it can and may reach a node by a longer route; the visited check stops the search going round cycles forever and revisiting nodes; and BFS is used for the fewest changes while the connected question needs a traversal (DFS or BFS) from one node and a check that everything was reached.",
    {2: ("Explains that BFS reaches nodes in order of distance (in rings, using a queue) so the first arrival is shortest while DFS goes deep and may find a longer route; says the visited check prevents infinite loops on cycles and repeated work; and chooses BFS for fewest changes and a traversal or component count for connectivity.",
         ["BFS goes outward ring by ring using a queue, so it reaches every node by the fewest edges first. DFS goes as deep as it can along one path and might get to a node the long way round. The visited check stops the search circling forever in a cycle and revisiting nodes. For the fewest train changes I'd use BFS; for whether all the computers are connected I'd run a DFS or BFS from one computer and see whether it reaches them all (or count components).",
          "(a) BFS visits by distance, so the first time it reaches a node is the shortest; DFS can take a longer route. (b) Without it a cycle makes the search loop forever. (c) BFS for the train changes; a traversal or component count for connectivity."]),
     1: ("Answers one or two parts well, or says BFS is shortest without explaining why.",
         ["BFS finds the shortest path.", "You need visited so it stops."]),
     0: ("Incorrect, for example says DFS always finds the shortest path, or that a visited check makes the search slower and isn't needed.",
         ["DFS is always shortest.", "The visited check isn't needed."])})
reg({"j5-l3.3": ("Graphs: representation and traversal", ["J5.11"])},
    {"MC121": (["J5.11"], "Platform", "A graph search needs no visited record"),
     "MC122": (["J5.11"], "Platform", "Depth-first search finds the fewest hops"),
     "MC123": (["J5.11"], "Platform", "An undirected edge only needs adding to one of its two nodes")})

# ====================================================================== 5.3.4
Lesson("j5-l3.4", "Shortest paths", ["J5.12"], [
    ("o1", "Implement Dijkstra's algorithm with a PriorityQueue to find the cheapest path cost in a weighted graph"),
    ("o2", "Recover the route itself from predecessor links"),
    ("o3", "Explain why BFS isn't enough for weighted edges, and why Dijkstra needs non-negative weights"),
], ["j5-l3.3", "j5-l2.6"], 60, ["I56", "R8"], r'''
## Before you start

You should know BFS ([Graphs: representation and traversal](j5-l3.3)) and `PriorityQueue` ([Heaps and priority queues](j5-l2.6)).

**Quick check.** What does `poll()` on a `PriorityQueue` return?

<details><summary>Show the answer</summary>

The head: the least element under the queue's ordering `[I56]`.

</details>

## Explanation

### Edges that cost something

BFS counts **edges**, which is right when every edge costs the same. Roads have lengths, flights have prices, network links have delays: **weighted** edges. The cheapest route isn't necessarily the one with the fewest hops: three short roads can beat one long one.

```
A ─4─ B        A to C directly costs 5 via B? No:
A ─1─ D        A-D-C costs 1 + 1 = 2, with two hops;
D ─1─ C        A-C (weight 5) costs 5, with one hop.
A ─5─ C
```

BFS would pick the one-hop route and be wrong.

### Dijkstra's algorithm

**Dijkstra's algorithm** finds the cheapest cost from a start node to every other node, as long as **no edge weight is negative**. It's BFS's idea with a **priority queue** instead of a plain queue, so it always expands the **cheapest unexplored node next**:

1. `cost[start] = 0`; every other node's cost is "infinity" (unknown).
2. Put `(start, 0)` in a priority queue ordered by cost.
3. Repeat: take the **cheapest** entry `(node, cost)`. If it's **stale** (a cheaper way to this node has already been found), skip it. Otherwise, for each neighbour, compute `cost + weight`; if that beats the neighbour's recorded cost, record it and add `(neighbour, newCost)` to the queue.
4. Stop when the queue is empty (or when you take your target).

Why does it work? When a node is taken from the queue, it has the lowest cost of everything still waiting. Any other route to it would have to go through a node that costs **at least as much already** and then add a **non-negative** weight, so it can't be cheaper. The first time a node is taken, its cost is final.

```java
int shortest(int n, String[] edges, int from, int to) {
    List<List<int[]>> graph = new ArrayList<>();          // each neighbour is {node, weight}
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    for (String edge : edges) {                           // "0-1:4"
        String[] parts = edge.split("[-:]");
        int a = Integer.parseInt(parts[0]), b = Integer.parseInt(parts[1]), w = Integer.parseInt(parts[2]);
        graph.get(a).add(new int[] {b, w});
        graph.get(b).add(new int[] {a, w});
    }

    int[] cost = new int[n];
    Arrays.fill(cost, Integer.MAX_VALUE);
    cost[from] = 0;
    PriorityQueue<int[]> queue = new PriorityQueue<>(Comparator.comparingInt(entry -> entry[1]));
    queue.offer(new int[] {from, 0});

    while (!queue.isEmpty()) {
        int[] current = queue.poll();
        int node = current[0];
        if (current[1] > cost[node]) continue;            // stale entry
        for (int[] edge : graph.get(node)) {
            int next = edge[0];
            int newCost = cost[node] + edge[1];
            if (newCost < cost[next]) {
                cost[next] = newCost;
                queue.offer(new int[] {next, newCost});
            }
        }
    }
    return cost[to] == Integer.MAX_VALUE ? -1 : cost[to];
}
```

`Comparator.comparingInt(entry -> entry[1])` orders the queue entries by their cost. The "stale entry" check matters: a node can be queued several times with different costs, and only the cheapest is worth processing.

### Getting the route, not just the cost

Record **where each node's best cost came from**: a `previous[next] = node` whenever you improve `cost[next]`. To read off a route, start at the target and follow `previous` back to the start, then reverse:

```java
List<Integer> path = new ArrayList<>();
for (int at = to; at != -1; at = previous[at]) path.add(at);
Collections.reverse(path);
```

If the target was never reached, there is no route. When two routes tie for cheapest, which one you get depends on the order things were processed, so only rely on a route when the cheapest is unique.

### What Dijkstra can't do

- **Negative weights.** If an edge can have a negative weight, a node's cost can drop after it was "finalised", and the reasoning above breaks. Dijkstra gives wrong answers there; other algorithms handle that case.
- **Unweighted graphs** are just the case where every weight is 1, where plain BFS is simpler and does the same job.

### Cost

Each edge can add an entry to the priority queue, and each queue operation costs O(log n) `[I56]`, so the total is about **O((V + E) log V)**.

## Worked examples

### Example 1: Dijkstra by hand

*Task: edges `0-1:4`, `0-2:1`, `2-1:2`, `1-3:1`, `2-3:5`. Cheapest cost from 0 to 3?*

| Step | Take | Update |
|---|---|---|
| start | | `cost[0] = 0`, queue `(0, 0)` |
| 1 | `(0, 0)` | `cost[1] = 4`, `cost[2] = 1` |
| 2 | `(2, 1)` | via 2: node 1 would cost 1 + 2 = 3 (better than 4): `cost[1] = 3`; node 3 costs 1 + 5 = 6: `cost[3] = 6` |
| 3 | `(1, 3)` | node 3 costs 3 + 1 = 4 (better than 6): `cost[3] = 4` |
| 4 | `(1, 4)` | stale (cost[1] is already 3), skipped |
| 5 | `(3, 4)` | no neighbours improve |
| 6 | `(3, 6)` | stale, skipped |

The cheapest cost to node 3 is **4**, by 0 → 2 → 1 → 3.

### Example 2: reading the route back

With `previous[3] = 1`, `previous[1] = 2`, `previous[2] = 0`: start at 3 and follow the links to get `3, 1, 2, 0`, then reverse: **0 → 2 → 1 → 3**.

## Where this is used

- **Route planners and navigation** run a version of Dijkstra, with better guesses added, over road networks.
- **Network routing** protocols compute cheapest paths between routers.
- **Games** find the cheapest route across a map where terrain has different costs.

## Common mistakes

:::mistake{id=MC124}
**Using BFS on a weighted graph.** BFS minimises the number of edges, not their total weight.
:::

:::mistake{id=MC125}
**Using Dijkstra with a negative edge weight.** The correctness argument needs every weight to be non-negative.
:::

:::mistake{id=MC126}
**Skipping the stale-entry check.** The code stays correct but does needless repeat work, and in some versions it's what keeps it correct.
:::

## Practice

::exercise{id=j5-l3.4-write-dijkstra}

::exercise{id=j5-l3.4-write-route}

::exercise{id=j5-l3.4-explain-why}

## Further reading

- **`java.util.PriorityQueue`** `[I56]` documents the queue's ordering and the costs that give Dijkstra its running time.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can compute the cheapest cost and reconstruct the route (*implementation*).
- The **explain** exercise checks that you can say why BFS fails on weights and why negative weights break Dijkstra (*explanation*).
''' + FOOT)

ex = Exercises("j5-l3.4")
def dijkstra(n, edges, frm, to, want_route=False):
    g = [[] for _ in range(n)]
    for e in edges:
        ab, w = e.split(":"); a, b = map(int, ab.split("-")); w = int(w)
        g[a].append((b, w)); g[b].append((a, w))
    INF = float("inf"); cost = [INF] * n; cost[frm] = 0; prev = [-1] * n; pq = [(0, frm)]
    while pq:
        c, u = heapq.heappop(pq)
        if c > cost[u]: continue
        for v, w in g[u]:
            if c + w < cost[v]:
                cost[v] = c + w; prev[v] = u; heapq.heappush(pq, (c + w, v))
    return cost, prev
def count_shortest_paths(n, edges, frm, to):
    cost, _ = dijkstra(n, edges, frm, to)
    g = [[] for _ in range(n)]
    for e in edges:
        ab, w = e.split(":"); a, b = map(int, ab.split("-")); w = int(w)
        g[a].append((b, w)); g[b].append((a, w))
    order = sorted(range(n), key=lambda x: cost[x]); ways = [0] * n; ways[frm] = 1
    for u in order:
        if cost[u] == float("inf"): continue
        for v, w in g[u]:
            if cost[u] + w == cost[v] and cost[v] > cost[u] or (w == 0 and cost[u] + w == cost[v]): ways[v] += ways[u]
    return ways[to]
def shortest(n, edges, frm, to):
    c = dijkstra(n, edges, frm, to)[0][to]
    return -1 if c == float("inf") else c
def route(n, edges, frm, to):
    cost, prev = dijkstra(n, edges, frm, to)
    if cost[to] == float("inf"): return "none"
    path, at = [], to
    while at != -1: path.append(at); at = prev[at]
    return ">".join(map(str, reversed(path)))
W1 = ["0-1:4", "0-2:1", "2-1:2", "1-3:1", "2-3:5"]
W2 = ["0-1:7", "0-2:9", "0-5:14", "1-2:10", "1-3:15", "2-3:11", "2-5:2", "3-4:6", "4-5:9"]
W3 = ["0-1:1", "1-2:1", "2-3:1", "0-3:10", "3-4:2"]
for args in [(4, W1, 0, 3), (6, W2, 0, 4), (5, W3, 0, 4)]:
    assert count_shortest_paths(*args) == 1, args      # routes in the tests must be unique
DJ_SOL = 'int shortest(int n, String[] edges, int from, int to) {\n    List<List<int[]>> graph = new ArrayList<>();\n    for (int i = 0; i < n; i++) {\n        graph.add(new ArrayList<>());\n    }\n    for (String edge : edges) {\n        String[] parts = edge.split("[-:]");\n        int a = Integer.parseInt(parts[0]);\n        int b = Integer.parseInt(parts[1]);\n        int w = Integer.parseInt(parts[2]);\n        graph.get(a).add(new int[] {b, w});\n        graph.get(b).add(new int[] {a, w});\n    }\n    int[] cost = new int[n];\n    Arrays.fill(cost, Integer.MAX_VALUE);\n    cost[from] = 0;\n    PriorityQueue<int[]> queue = new PriorityQueue<>(Comparator.comparingInt(entry -> entry[1]));\n    queue.offer(new int[] {from, 0});\n    while (!queue.isEmpty()) {\n        int[] current = queue.poll();\n        int node = current[0];\n        if (current[1] > cost[node]) {\n            continue;\n        }\n        for (int[] edge : graph.get(node)) {\n            int next = edge[0];\n            int newCost = cost[node] + edge[1];\n            if (newCost < cost[next]) {\n                cost[next] = newCost;\n                queue.offer(new int[] {next, newCost});\n            }\n        }\n    }\n    return cost[to] == Integer.MAX_VALUE ? -1 : cost[to];\n}'
DJ_V = [("shortest", [4, W1, 0, 3]), ("shortest", [3, ["0-1:5"], 0, 2]), ("shortest", [2, [], 1, 1])]
DJ_H = [("shortest", [6, W2, 0, 4]), ("shortest", [6, W2, 3, 0]), ("shortest", [5, W3, 0, 4]), ("shortest", [4, ["0-1:1", "2-3:1"], 0, 3]), ("shortest", [3, ["0-1:2", "1-2:2", "0-2:3"], 0, 2]), ("shortest", [3, ["0-1:1", "1-2:1", "0-2:1"], 0, 2]), ("shortest", [5, ["0-1:100", "0-2:1", "2-3:1", "3-1:1", "1-4:1"], 0, 4])]
ex.method("write", "j5-l3.4-write-dijkstra", "The cheapest route cost", ["o1"], ["J5.12"], ["IMPL"],
    "Write `shortest(n, edges, from, to)`: the **lowest total weight** of any path between two nodes in an undirected weighted graph with nodes `0..n-1`. Edges are strings like `\"0-1:4\"` (nodes 0 and 1, weight 4). Weights are never negative. It is 0 when `from == to`, and `-1` if there is no path. Use Dijkstra's algorithm with a `PriorityQueue`.",
    [("shortest", [("n", "int"), ("edges", "String[]"), ("from", "int"), ("to", "int")], "int")], {"shortest": shortest}, DJ_V, DJ_H,
    'int shortest(int n, String[] edges, int from, int to) {\n    return -1;\n}',
    DJ_SOL,
    {"fewest-hops-not-cheapest": 'int shortest(int n, String[] edges, int from, int to) {\n    List<List<Integer>> graph = new ArrayList<>();\n    int[][] w = new int[n][n];\n    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());\n    for (String edge : edges) {\n        String[] p = edge.split("[-:]");\n        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]), c = Integer.parseInt(p[2]);\n        graph.get(a).add(b);\n        graph.get(b).add(a);\n        w[a][b] = c;\n        w[b][a] = c;\n    }\n    int[] hops = new int[n];\n    Arrays.fill(hops, -1);\n    int[] total = new int[n];\n    Deque<Integer> queue = new ArrayDeque<>();\n    hops[from] = 0;\n    queue.offer(from);\n    while (!queue.isEmpty()) {\n        int node = queue.poll();\n        for (int next : graph.get(node)) {\n            if (hops[next] == -1) {\n                hops[next] = hops[node] + 1;\n                total[next] = total[node] + w[node][next];\n                queue.offer(next);\n            }\n        }\n    }\n    return hops[to] == -1 ? -1 : total[to];\n}',
     "forgets-unreachable": DJ_SOL.replace("return cost[to] == Integer.MAX_VALUE ? -1 : cost[to];", "return cost[to];")},
    ("Keep the best known cost for each node. Repeatedly take the cheapest queued node and try to improve its neighbours' costs.", "if (newCost < cost[next]) { cost[next] = newCost; queue.offer(new int[] {next, newCost}); }"),
    source_tests=[("uses a PriorityQueue", ["PriorityQueue"], None)],
    difficulty=5)
RT_SOL = DJ_SOL.replace("int shortest(int n, String[] edges, int from, int to) {", "String route(int n, String[] edges, int from, int to) {").replace("    int[] cost = new int[n];\n", "    int[] cost = new int[n];\n    int[] previous = new int[n];\n    Arrays.fill(previous, -1);\n").replace("                cost[next] = newCost;\n", "                cost[next] = newCost;\n                previous[next] = node;\n").replace("    return cost[to] == Integer.MAX_VALUE ? -1 : cost[to];", "    if (cost[to] == Integer.MAX_VALUE) {\n        return \"none\";\n    }\n    List<Integer> path = new ArrayList<>();\n    for (int at = to; at != -1; at = previous[at]) {\n        path.add(at);\n    }\n    Collections.reverse(path);\n    StringBuilder text = new StringBuilder();\n    for (int node : path) {\n        if (!text.isEmpty()) {\n            text.append(\">\");\n        }\n        text.append(node);\n    }\n    return text.toString();")
RT_V = [("route", [4, W1, 0, 3]), ("route", [3, ["0-1:5"], 0, 2]), ("route", [2, [], 1, 1])]
RT_H = [("route", [6, W2, 0, 4]), ("route", [5, W3, 0, 4]), ("route", [4, ["0-1:1", "2-3:1"], 0, 3]), ("route", [6, W2, 4, 0]), ("route", [4, W1, 3, 0])]
for a in [(4, W1, 3, 0), (6, W2, 4, 0)]:
    assert count_shortest_paths(*a) == 1, a
ex.method("write", "j5-l3.4-write-route", "Which way?", ["o2"], ["J5.12"], ["IMPL"],
    "Write `route(n, edges, from, to)`: the cheapest path itself, as node numbers joined by `>` from `from` to `to`, such as `0>2>1>3`; `none` if the target can't be reached. (The checks only use graphs where the cheapest route is unique.) Extend Dijkstra with a `previous` array: whenever you improve a node's cost, remember which node you came from; then follow it back from the target and reverse.",
    [("route", [("n", "int"), ("edges", "String[]"), ("from", "int"), ("to", "int")], "String")], {"route": route}, RT_V, RT_H,
    'String route(int n, String[] edges, int from, int to) {\n    return "none";\n}',
    RT_SOL,
    {"forgets-to-reverse": RT_SOL.replace("    Collections.reverse(path);\n", ""),
     "records-the-wrong-previous": RT_SOL.replace("previous[next] = node;", "previous[next] = from;")},
    ("When you improve cost[next], also set previous[next] = node. At the end walk from the target back to the start, collecting nodes, and reverse the list.", "previous[next] = node; ... for (int at = to; at != -1; at = previous[at]) path.add(at); Collections.reverse(path);"),
    source_tests=[("uses a PriorityQueue", ["PriorityQueue"], None)],
    difficulty=5)
ex.explain("j5-l3.4-explain-why", "Why Dijkstra?", ["o3"], ["J5.12"],
    "(a) Show with a small example why BFS can give the wrong answer when edges have weights. (b) In one or two sentences, explain why taking the cheapest queued node first lets Dijkstra finalise that node's cost. (c) Why does a negative edge weight break the argument?",
    "A full answer gives an example where the route with fewer edges costs more (for example a direct edge of weight 5 against two edges of weight 1 each, where BFS picks the single edge); explains that when a node is taken from the priority queue every other route to it must go through a node that is already at least as costly and add a non-negative weight, so it cannot be cheaper; and says a negative weight could make a later route cheaper than one already finalised.",
    {2: ("Gives a valid example where fewer edges cost more (such as a single edge of 5 versus two edges of 1 and 1), explains that other routes go through nodes costing at least as much plus a non-negative weight so can't be cheaper, and says a negative edge could later reduce a finalised cost.",
         ["If A to C is one edge of weight 5 but A to D to C is two edges of weight 1 each, BFS picks the one-edge route, which costs 5 instead of 2. When Dijkstra takes the cheapest queued node, any other route to it has to pass through a node that is already at least as expensive and then add a weight that isn't negative, so it can't be cheaper. A negative edge breaks that, because a later step could make the total smaller than a cost we already finalised.",
          "(a) One edge of weight 10 versus three edges of weight 1: BFS takes the one edge. (b) Everything else in the queue costs at least as much, and adding non-negative weights can't lower that. (c) A negative weight could lower a cost after the node was finalised."]),
     1: ("Gets one or two parts right, for example the example but not the reasoning.",
         ["BFS counts edges not weights.", "Negative weights are a problem."]),
     0: ("Incorrect, for example says BFS works on weighted graphs, or that Dijkstra works with negative weights.",
         ["BFS works fine for weights.", "Dijkstra handles negative edges."])})
reg({"j5-l3.4": ("Shortest paths", ["J5.12"])},
    {"MC124": (["J5.12"], "Platform", "BFS finds the cheapest path in a weighted graph"),
     "MC125": (["J5.12"], "Platform", "Dijkstra's algorithm works when some edge weights are negative"),
     "MC126": (["J5.12"], "I56", "A node is only ever queued once in Dijkstra's algorithm")})

# ====================================================================== 5.3.5
Lesson("j5-l3.5", "Dynamic programming", ["J5.13"], [
    ("o1", "Turn an exponential recursion into a fast one by remembering sub-answers, as memoisation or a table"),
    ("o2", "Solve minimum coin change and longest common subsequence length with a table"),
    ("o3", "Explain what overlapping subproblems are, and how they differ from divide and conquer"),
], ["j5-l3.4", "j5-l3.1"], 60, ["R8"], r'''
## Before you start

You should be comfortable with recursion ([Recursion](j5-l3.1)) and with counting calls and growth ([Counting steps and growth rates](j5-l1.1)).

**Quick check.** Roughly how many calls does the recursive `fib(n)` make for large n?

<details><summary>Show the answer</summary>

An exponential number: it recomputes the same values over and over, about 1.6ⁿ calls.

</details>

## Explanation

### The same question, asked again and again

```java
long fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}
```

This is correct, and hopeless. `fib(40)` makes **''' + f"{CALLS_40:,}" + r''' calls**. The reason: `fib(5)` calls `fib(4)` and `fib(3)`; `fib(4)` also calls `fib(3)`, which is computed from scratch a second time, and `fib(2)` is computed over and over.

```
                 fib(5)
               /        \
          fib(4)          fib(3)       <- fib(3) appears twice already
         /     \          /    \
    fib(3)   fib(2)   fib(2)  fib(1)
```

Divide-and-conquer methods like merge sort split a problem into **independent** halves. Here the subproblems **overlap**: the same ones recur. That's the signal for **dynamic programming**: *solve each distinct subproblem once, remember the answer, and reuse it.*

### Way 1: memoisation (top-down)

Keep the recursion, add a **memo**: before computing, look the answer up; after computing, store it.

```java
long fib(int n) {
    return fib(n, new long[n + 1]);
}

long fib(int n, long[] memo) {
    if (n < 2) return n;
    if (memo[n] != 0) return memo[n];                   // already known
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo);      // compute once, remember
    return memo[n];
}
```

Now each value from 0 to n is computed exactly once: about **n** calls, not 331 million. That's a drop from exponential to linear.

### Way 2: a table (bottom-up)

Skip the recursion. Fill in answers from the smallest case upwards:

```java
long fib(int n) {
    if (n < 2) return n;
    long previous = 0, current = 1;
    for (int i = 2; i <= n; i++) {
        long next = previous + current;
        previous = current;
        current = next;
    }
    return current;
}
```

Same answer, no recursion, no depth limit, and (for Fibonacci) it only needs the last two values.

### The recipe

1. **Define the subproblem** precisely: *what does `best[i]` mean?*
2. **Write the recurrence:** how a bigger answer comes from smaller ones.
3. **Set the base cases.**
4. **Choose the order** to fill the table so smaller answers exist first.
5. **Read off the answer.**

### Example: fewest coins

*With coins of 1, 5 and 6 pence, what is the fewest coins making 10p?* Greedy ("take the biggest coin that fits") gives 6 + 1 + 1 + 1 + 1 = five coins, but 5 + 5 is **two**. The right tool is a table.

- **Subproblem:** `best[a]` = fewest coins to make amount `a`.
- **Recurrence:** try each coin `c` as the last one: `best[a] = 1 + min(best[a - c])` over coins with `c <= a`.
- **Base:** `best[0] = 0`. Amounts that can't be made are marked impossible.

```java
int minCoins(int[] coins, int amount) {
    int[] best = new int[amount + 1];
    Arrays.fill(best, Integer.MAX_VALUE);
    best[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int coin : coins) {
            if (coin <= a && best[a - coin] != Integer.MAX_VALUE) {
                best[a] = Math.min(best[a], best[a - coin] + 1);
            }
        }
    }
    return best[amount] == Integer.MAX_VALUE ? -1 : best[amount];
}
```

Cost: `amount × number of coins`, about 10 steps for 10p, and a few million for an amount of 100,000. A plain recursion trying every combination would take longer than you'd wait.

### Example: longest common subsequence

A **subsequence** keeps the order but may skip characters. The longest common subsequence (LCS) of `"ABCBDAB"` and `"BDCABA"` has length 4 (for example `"BCBA"`). It's how file comparison tools find what two versions have in common.

- **Subproblem:** `len[i][j]` = LCS length of the first `i` characters of `a` and the first `j` of `b`.
- **Recurrence:** if `a[i-1] == b[j-1]`, the match extends the best of both shorter strings: `len[i][j] = len[i-1][j-1] + 1`. Otherwise take the better of dropping a character from either: `max(len[i-1][j], len[i][j-1])`.
- **Base:** `len[0][j] = len[i][0] = 0`.

```java
int lcs(String a, String b) {
    int[][] len = new int[a.length() + 1][b.length() + 1];
    for (int i = 1; i <= a.length(); i++) {
        for (int j = 1; j <= b.length(); j++) {
            if (a.charAt(i - 1) == b.charAt(j - 1)) {
                len[i][j] = len[i - 1][j - 1] + 1;
            } else {
                len[i][j] = Math.max(len[i - 1][j], len[i][j - 1]);
            }
        }
    }
    return len[a.length()][b.length()];
}
```

### When does dynamic programming apply?

Two features together:

- **Overlapping subproblems:** the same smaller questions recur (otherwise plain recursion is fine).
- **Optimal substructure:** the best answer is built from best answers to smaller questions.

If a problem has both, a table or memo usually turns exponential into polynomial. If you can't write the recurrence, you don't yet understand the problem; do that first.

## Worked examples

### Example 1: filling the coin table

*Task: coins `{1, 5, 6}`, amount 10.*

| `a` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `best[a]` | 0 | 1 | 2 | 3 | 4 | 1 | 1 | 2 | 3 | 4 | 2 |

For `a = 10`: using coin 1 gives `best[9] + 1 = 5`; coin 5 gives `best[5] + 1 = 2`; coin 6 gives `best[4] + 1 = 5`. The minimum is **2**: 5 + 5.

### Example 2: counting calls

*Task: how many calls does the memoised `fib(40)` make?*

Each value from 2 to 40 is computed once, and each computation makes two further calls, most answered immediately from the memo. So it's about **2 × 40 = 80** calls in total, against ''' + f"{CALLS_40:,}" + r''' for the plain version.

## Where this is used

- **Text comparison and version control:** diff tools use LCS-style tables.
- **Spell checkers and DNA matching** use edit-distance tables.
- **Scheduling and resource planning** (knapsack-style problems) are classic dynamic programming.

## Common mistakes

:::mistake{id=MC127}
**Using a greedy rule for coin change.** Taking the biggest coin first isn't always optimal (1, 5, 6 for 10p). Use the table.
:::

:::mistake{id=MC128}
**Memoising without checking the memo first.** The table is filled but never used, and the recursion is still exponential.
:::

:::mistake{id=MC129}
**Treating the "impossible" case as 0.** A cheap-looking 0 spreads through the table. Mark impossible amounts distinctly.
:::

## Practice

::exercise{id=j5-l3.5-write-fib}

::exercise{id=j5-l3.5-write-coins}

::exercise{id=j5-l3.5-write-lcs}

::exercise{id=j5-l3.5-explain-overlap}

## Further reading

- **Qian & Lehman (2017)** `[R8]` on the reasoning difficulties recursion and tables pose for learners.

## How you'll be assessed

- The **write** exercises check that you can memoise Fibonacci and fill coin and LCS tables (*implementation*).
- The **explain** exercise checks that you can say what overlapping subproblems are and why they matter (*explanation*).
''' + FOOT)

ex = Exercises("j5-l3.5")
ex.method("write", "j5-l3.5-write-fib", "Fibonacci that finishes", ["o1"], ["J5.13"], ["IMPL"],
    "Write `fibonacci(int n)`, returning the n-th Fibonacci number (0, 1, 1, 2, 3, 5, ...; `fibonacci(0)` is 0 and `fibonacci(1)` is 1). The plain recursion makes hundreds of millions of calls by n = 40, and the checks go up to n = 90 (within `long`). Remember sub-answers, with a memo or a loop.",
    [("fibonacci", [("n", "int")], "long")], {"fibonacci": fib},
    [("fibonacci", [10]), ("fibonacci", [0]), ("fibonacci", [1])],
    [("fibonacci", [2]), ("fibonacci", [30]), ("fibonacci", [50]), ("fibonacci", [90]), ("fibonacci", [45]), ("fibonacci", [89])],
    'long fibonacci(int n) {\n    if (n < 2) {\n        return n;\n    }\n    return fibonacci(n - 1) + fibonacci(n - 2);\n}',
    'long fibonacci(int n) {\n    if (n < 2) {\n        return n;\n    }\n    long previous = 0;\n    long current = 1;\n    for (int i = 2; i <= n; i++) {\n        long next = previous + current;\n        previous = current;\n        current = next;\n    }\n    return current;\n}',
    {"off-by-one": 'long fibonacci(int n) {\n    if (n < 2) {\n        return n;\n    }\n    long previous = 0;\n    long current = 1;\n    for (int i = 2; i < n; i++) {\n        long next = previous + current;\n        previous = current;\n        current = next;\n    }\n    return current;\n}'},
    ("Each value is the sum of the two before it. Build up from 0 and 1, keeping only the last two.", "long next = previous + current; previous = current; current = next;"),
    difficulty=3)
def min_coins(coins, amount):
    INF = float("inf"); best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]: best[a] = best[a - c] + 1
    return -1 if best[amount] == INF else best[amount]
MC_SOL = 'int minCoins(int[] coins, int amount) {\n    int[] best = new int[amount + 1];\n    Arrays.fill(best, Integer.MAX_VALUE);\n    best[0] = 0;\n    for (int a = 1; a <= amount; a++) {\n        for (int coin : coins) {\n            if (coin <= a && best[a - coin] != Integer.MAX_VALUE) {\n                best[a] = Math.min(best[a], best[a - coin] + 1);\n            }\n        }\n    }\n    return best[amount] == Integer.MAX_VALUE ? -1 : best[amount];\n}'
ex.method("write", "j5-l3.5-write-coins", "The fewest coins", ["o2"], ["J5.13"], ["IMPL"],
    "Write `minCoins(int[] coins, int amount)`: the **fewest coins** (each kind usable any number of times) that add up to `amount`, or `-1` if it's impossible. With coins `{1, 5, 6}` and amount 10 the answer is 2 (5 + 5), which taking the biggest coin first misses. The checks go up to an amount of 100,000.",
    [("minCoins", [("coins", "int[]"), ("amount", "int")], "int")], {"minCoins": min_coins},
    [("minCoins", [[1, 5, 6], 10]), ("minCoins", [[2], 3]), ("minCoins", [[1], 0])],
    [("minCoins", [[1, 5, 10, 25], 63]), ("minCoins", [[5, 7], 11]), ("minCoins", [[3, 7], 100000]), ("minCoins", [[1, 3, 4], 6]), ("minCoins", [[2, 5, 10], 27]), ("minCoins", [[9, 6, 5, 1], 11])],
    'int minCoins(int[] coins, int amount) {\n    return -1;\n}',
    MC_SOL,
    {"greedy-biggest-first": 'int minCoins(int[] coins, int amount) {\n    int[] sorted = coins.clone();\n    Arrays.sort(sorted);\n    int count = 0;\n    for (int i = sorted.length - 1; i >= 0; i--) {\n        count += amount / sorted[i];\n        amount %= sorted[i];\n    }\n    return amount == 0 ? count : -1;\n}',
     "no-impossible-marker": MC_SOL.replace("    Arrays.fill(best, Integer.MAX_VALUE);\n", "")},
    ("best[a] is the fewest coins for amount a. Try each coin as the last one: 1 + best[a - coin]. best[0] is 0, and unreachable amounts need a marker.", "best[a] = Math.min(best[a], best[a - coin] + 1);"),
    difficulty=4)
def lcs_len(a, b):
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if a[i - 1] == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[len(b)]
LCS_SOL = 'int lcs(String a, String b) {\n    int[][] len = new int[a.length() + 1][b.length() + 1];\n    for (int i = 1; i <= a.length(); i++) {\n        for (int j = 1; j <= b.length(); j++) {\n            if (a.charAt(i - 1) == b.charAt(j - 1)) {\n                len[i][j] = len[i - 1][j - 1] + 1;\n            } else {\n                len[i][j] = Math.max(len[i - 1][j], len[i][j - 1]);\n            }\n        }\n    }\n    return len[a.length()][b.length()];\n}'
LA = "".join(chr(97 + (i * i + 3 * i) % 7) for i in range(1200))
LB = "".join(chr(97 + (i * 5 + i // 3) % 7) for i in range(1200))
ex.method("write", "j5-l3.5-write-lcs", "What two texts have in common", ["o2"], ["J5.13"], ["IMPL"],
    "Write `lcs(String a, String b)`: the **length of the longest common subsequence**: the longest run of characters that appear in both strings **in the same order**, though not necessarily next to each other. For `\"ABCBDAB\"` and `\"BDCABA\"` it is 4. The checks include strings of 1,200 characters, which only a table (not plain recursion) can handle in time.",
    [("lcs", [("a", "String"), ("b", "String")], "int")], {"lcs": lcs_len},
    [("lcs", ["ABCBDAB", "BDCABA"]), ("lcs", ["", "abc"]), ("lcs", ["abc", "abc"])],
    [("lcs", ["abc", "xyz"]), ("lcs", ["AGGTAB", "GXTXAYB"]), ("lcs", ["aaaa", "aa"]), ("lcs", ["abcdef", "fedcba"]), ("lcs", [LA, LB]), ("lcs", ["x", "x"])],
    'int lcs(String a, String b) {\n    return 0;\n}',
    LCS_SOL,
    {"longest-common-substring": 'int lcs(String a, String b) {\n    int best = 0;\n    for (int i = 0; i < a.length(); i++) {\n        for (int j = 0; j < b.length(); j++) {\n            int k = 0;\n            while (i + k < a.length() && j + k < b.length() && a.charAt(i + k) == b.charAt(j + k)) {\n                k++;\n            }\n            best = Math.max(best, k);\n        }\n    }\n    return best;\n}',
     "plain-recursion-too-slow": 'int lcs(String a, String b) {\n    return go(a, b, 0, 0);\n}\n\nint go(String a, String b, int i, int j) {\n    if (i == a.length() || j == b.length()) {\n        return 0;\n    }\n    if (a.charAt(i) == b.charAt(j)) {\n        return 1 + go(a, b, i + 1, j + 1);\n    }\n    return Math.max(go(a, b, i + 1, j), go(a, b, i, j + 1));\n}'},
    ("len[i][j] is the answer for the first i characters of a and the first j of b. If the last characters match, add 1 to len[i-1][j-1]; otherwise take the better of len[i-1][j] and len[i][j-1].", "if (a.charAt(i - 1) == b.charAt(j - 1)) len[i][j] = len[i - 1][j - 1] + 1; else len[i][j] = Math.max(len[i - 1][j], len[i][j - 1]);"),
    difficulty=5)
ex.explain("j5-l3.5-explain-overlap", "Why remember the answers?", ["o3"], ["J5.13"],
    f"The plain recursive `fib(40)` makes {CALLS_40:,} calls; a memoised version makes about 80. (a) Explain why the plain version does so much repeated work. (b) What are \"overlapping subproblems\", and how is that different from merge sort, which also splits a problem? (c) Why does greedy (\"always take the biggest coin\") fail for coins 1, 5 and 6 and amount 10, and what does the table do instead?",
    "A full answer says the plain version recomputes the same smaller Fibonacci values many times because fib(n-1) and fib(n-2) both need the same lower values; that overlapping subproblems are the same subproblem needed again and again, whereas merge sort's halves are independent so nothing is repeated; and that greedy takes 6+1+1+1+1 (five coins) while 5+5 is two, because a locally best choice doesn't give the best total, whereas the table considers every coin as the last one using the best answers to smaller amounts.",
    {2: ("Explains that the plain version recomputes the same values repeatedly, defines overlapping subproblems and contrasts them with merge sort's independent halves, and explains that greedy gives five coins versus two while the table tries every coin using best answers for smaller amounts.",
         ["fib(n-1) and fib(n-2) both call the same smaller values, so the plain version computes them again and again. Overlapping subproblems means the same subproblem is needed many times; merge sort splits into independent halves so nothing is repeated. For 10p with 1, 5 and 6, greedy takes 6+1+1+1+1 which is five coins, but 5+5 is two. The table tries each coin as the last coin and uses the best answers for smaller amounts, so it finds two.",
          "The same Fibonacci numbers are recalculated many times. Overlapping subproblems are repeated questions, unlike merge sort's separate halves. Greedy picks 6 first and ends up with five coins, while 5+5 uses two; the table checks every option from the smaller amounts."]),
     1: ("Answers two parts well, or explains the repetition without the contrast or the coin example.",
         ["It recalculates the same values.", "Greedy gives the wrong answer."]),
     0: ("Incorrect, for example says memoisation makes the computer faster by using a cache, or that greedy is always optimal.",
         ["Memoisation uses the CPU cache.", "Greedy is always best."])})
reg({"j5-l3.5": ("Dynamic programming", ["J5.13"])},
    {"MC127": (["J5.13"], "Platform", "Taking the largest coin that fits always gives the fewest coins"),
     "MC128": (["J5.13"], "Platform", "Filling a memo array speeds up recursion even if it is never read"),
     "MC129": (["J5.13"], "Platform", "In a minimum-coins table an impossible amount can be recorded as 0")})
print("5.3 written")
