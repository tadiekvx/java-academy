import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-3"
from build import *
import outline, re
from collections import Counter
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'

# ====================================================================== 3.3.1
Lesson("j3-l3.1", "Lambdas and functional interfaces", ["J3.05"], [
    ("o1", "Write lambda expressions and method references for the common functional interfaces"),
    ("o2", "Predict the result of code that uses lambdas, including captured variables"),
    ("o3", "Explain what a functional interface is and why a lambda can be passed where one is expected"),
], ["j3-l2.1"], 45, ["I53", "I36", "R8"], r'''
## Before you start

You should know how interfaces work ([Interfaces and polymorphism](j2-l3.1)) and have seen `Comparator.comparing(String::length)` and `removeIf(v -> v < 0)` in the collections lessons.

**Quick check.** What does `list.sort(Comparator.comparing(String::length))` sort by?

<details><summary>Show the answer</summary>

By the length of each string, shortest first.

</details>

## Explanation

### Passing behaviour as a value

So far you've passed data to methods: numbers, strings, lists. Sometimes you want to pass **a piece of behaviour**: *"remove the items that satisfy this condition"*, *"sort by this rule"*. Java does that with **lambda expressions**.

```java
copy.removeIf(v -> v < 0);
```

`v -> v < 0` is a lambda: a small, nameless method. Read it as *"given `v`, the answer is `v < 0`"*.

### Functional interfaces

A lambda has to be given to something that can accept it. That something is an object of a **functional interface**: an interface with **exactly one abstract method** `[I53]`. The lambda supplies the body of that one method, and the compiler works out which interface from the context.

The standard library has a set of ready-made ones in `java.util.function`:

| Interface | Its one method | Meaning | Example |
|---|---|---|---|
| `Predicate<T>` | `boolean test(T t)` | a yes/no question | `s -> s.isEmpty()` |
| `Function<T, R>` | `R apply(T t)` | turn a `T` into an `R` | `s -> s.length()` |
| `Consumer<T>` | `void accept(T t)` | do something with a `T` | `s -> IO.println(s)` |
| `Supplier<T>` | `T get()` | produce a `T` from nothing | `() -> "hi"` |
| `BiFunction<T, U, R>` | `R apply(T t, U u)` | two inputs, one result | `(a, b) -> a * b` |
| `Comparator<T>` | `int compare(T a, T b)` | order two things | `(a, b) -> a.length() - b.length()` |
| `Runnable` | `void run()` | an action with no input or output | `() -> IO.println("go")` |

`Function` and `Predicate` both come with useful helper methods: `negate()`, `and(...)`, `or(...)` on a `Predicate`, and `andThen(...)` on a `Function` `[I53]`.

### Lambda syntax

```java
x -> x * 2                      // one parameter: brackets optional
(a, b) -> a + b                 // several parameters: brackets needed
() -> "hello"                   // none
(String s) -> s.length()        // you can write the type if you like
s -> {                          // several statements: use a block and return
    String t = s.strip();
    return t.length();
}
```

A lambda used where a `Predicate<String>` is expected must take a `String` and return a `boolean`. The types come from the target; you usually don't write them.

```java runnable
void main() {
    Function<Integer, Integer> doubler = x -> x * 2;
    Predicate<String> isEmpty = s -> s.isEmpty();
    BiFunction<Integer, Integer, Integer> add = (a, b) -> a + b;

    IO.println(doubler.apply(21));
    IO.println(isEmpty.test(""));
    IO.println(add.apply(3, 4));
}
```

It prints `42`, `true`, `7`.

### Method references

When a lambda only calls one existing method, a **method reference** says the same more briefly:

| Method reference | Same as the lambda |
|---|---|
| `String::length` | `s -> s.length()` |
| `String::toUpperCase` | `s -> s.toUpperCase()` |
| `Integer::sum` | `(a, b) -> Integer.sum(a, b)` |
| `ArrayList::new` | `() -> new ArrayList<>()` |
| `IO::println` | `x -> IO.println(x)` |

`Type::method` can mean "call this method on the argument" (`String::length`) or "call this static method with the arguments" (`Integer::sum`). Use whichever reads more clearly.

### Capturing variables

A lambda can use variables from the method around it, but only if they never change after they're set (they're **effectively final**):

```java
int base = 10;
Function<Integer, Integer> addBase = x -> x + base;     // fine
```

```java
int count = 0;
Runnable r = () -> count++;     // error: local variables referenced from a lambda
                                //        expression must be final or effectively final
```

The lambda gets a **copy** of the value at that moment, so a later change to the variable couldn't be seen. Java forbids the confusion. If you need to accumulate, use an object (such as a list, or an `AtomicInteger`), or restructure with a stream.

## Worked examples

### Example 1: choosing a rule by name

*Task: given a rule name, return the matching `Predicate<String>`.*

**Step 1 — Each rule is a yes/no question about one string.**

**Step 2 — Return a lambda per rule:**

```java
Predicate<String> ruleFor(String rule) {
    return switch (rule) {
        case "long" -> s -> s.length() > 5;
        case "short" -> s -> s.length() <= 3;
        default -> s -> !s.isEmpty();
    };
}
```

**Step 3 — Use it:** `ruleFor("long").test("banana")` is `true`.

### Example 2: chaining functions

*Task: "double, then add one" as a single function.*

**Step 1 — Two small functions:** `x -> x * 2` and `x -> x + 1`.

**Step 2 — Join them with `andThen`:**

```java
Function<Integer, Integer> doubler = x -> x * 2;
Function<Integer, Integer> plusOne = x -> x + 1;
Function<Integer, Integer> both = doubler.andThen(plusOne);
// both.apply(5) is 11
```

## Predict, then run

::exercise{id=j3-l3.1-predict-lambda}

## Where this is used

- **Collections and streams:** `removeIf`, `sort`, `forEach`, `computeIfAbsent` and every stream operation take lambdas.
- **Callbacks:** "when this happens, run that" is the standard way to plug behaviour into frameworks.
- **Strategy selection:** choosing a rule, a fee or a formatter at run time.

## Common mistakes

:::mistake{id=MC72}
**Changing a local variable from inside a lambda.** The lambda sees a copy, so Java requires the variable to be effectively final. Use a mutable object or restructure.
:::

:::mistake{id=MC73}
**Using a lambda where the target isn't a functional interface.** A lambda needs a target type with exactly one abstract method. `Object o = x -> x;` doesn't compile.
:::

## Practice

::exercise{id=j3-l3.1-write-rules}

::exercise{id=j3-l3.1-write-steps}

::exercise{id=j3-l3.1-explain-functional}

## Further reading

- **`java.lang.FunctionalInterface`, `Function` and `Predicate`** `[I53]` define functional interfaces and these two types.
- **`java.util.Comparator`** `[I36]`.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can write lambdas for predicates and functions (*implementation*).
- The **predict** exercise checks that you can trace lambdas and method references (*identifying mistakes*).
- The **explain** exercise checks that you can say what a functional interface is and why captured variables must not change (*explanation*).
''' + FOOT, features=[("lambda expressions", 8), ("method references", 8)])

ex = Exercises("j3-l3.1")
def rule(r, s):
    if r == "long": return len(s) > 5
    if r == "short": return len(s) <= 3
    if r == "capital": return len(s) > 0 and s[0].isupper() and s[0].isascii()
    return len(s) > 0
RULE_DRV = '\n\nList<String> filterBy(List<String> items, String rule) {\n    Predicate<String> p = ruleFor(rule);\n    List<String> out = new ArrayList<>();\n    for (String s : items) {\n        if (p.test(s)) {\n            out.add(s);\n        }\n    }\n    return out;\n}'
RULE_SOL = 'Predicate<String> ruleFor(String rule) {\n    return switch (rule) {\n        case "long" -> s -> s.length() > 5;\n        case "short" -> s -> s.length() <= 3;\n        case "capital" -> s -> !s.isEmpty() && Character.isUpperCase(s.charAt(0));\n        default -> s -> !s.isEmpty();\n    };\n}'
ex.method("write", "j3-l3.1-write-rules", "A rule as a lambda", ["o1"], ["J3.05"], ["IMPL"],
    "`filterBy` keeps the items that a rule accepts, and it is written. You write `ruleFor(String rule)`, which returns a `Predicate<String>` as a lambda for each rule: `\"long\"` (more than 5 characters), `\"short\"` (3 characters or fewer), `\"capital\"` (starts with an upper-case letter; an empty string doesn't), and anything else means `\"nonempty\"` (not empty).",
    [("filterBy", [("items", "List<String>"), ("rule", "String")], "List<String>")], {"filterBy": lambda items, r: [s for s in items if rule(r, s)]},
    [("filterBy", [["banana", "fig", "Kiwi"], "long"]), ("filterBy", [["a", "abcd", "ab"], "short"]), ("filterBy", [["Ada", "bo", ""], "capital"])],
    [("filterBy", [["", "x"], "nonempty"]), ("filterBy", [["sixsix", "five5"], "long"]), ("filterBy", [["abc", "abcd"], "short"]), ("filterBy", [["Zed", "zed", "", "Q"], "capital"]), ("filterBy", [[], "long"]), ("filterBy", [["a", ""], "other"])],
    'Predicate<String> ruleFor(String rule) {\n    return s -> true;\n}' + RULE_DRV,
    RULE_SOL + RULE_DRV,
    {"long-is-at-least-five": RULE_SOL.replace("s.length() > 5", "s.length() >= 5") + RULE_DRV,
     "capital-crashes-on-empty": RULE_SOL.replace("!s.isEmpty() && Character.isUpperCase", "Character.isUpperCase") + RULE_DRV},
    ("Each rule is a lambda taking a String s and returning a boolean. A switch on the rule name can return a different lambda for each case.", "case \"long\" -> s -> s.length() > 5;"),
    source_tests=[("uses lambdas", ["->"], None)],
    difficulty=3)
def steps(s, start):
    x = start
    for name in ([] if s == "" else s.split(",")):
        x = {"double": lambda v: v * 2, "inc": lambda v: v + 1, "square": lambda v: v * v, "negate": lambda v: -v}[name](x)
    return x
STEP_DRV = '\n\nint applySteps(String steps, int start) {\n    Function<Integer, Integer> all = x -> x;\n    if (!steps.isEmpty()) {\n        for (String name : steps.split(",")) {\n            all = all.andThen(stepFor(name));\n        }\n    }\n    return all.apply(start);\n}'
STEP_SOL = 'Function<Integer, Integer> stepFor(String name) {\n    return switch (name) {\n        case "double" -> x -> x * 2;\n        case "inc" -> x -> x + 1;\n        case "square" -> x -> x * x;\n        default -> x -> -x;\n    };\n}'
ex.method("write", "j3-l3.1-write-steps", "Steps as functions", ["o1"], ["J3.05"], ["IMPL"],
    "`applySteps` chains steps such as `\"double,inc,square\"` with `andThen`, and it is written. You write `stepFor(String name)`, which returns a `Function<Integer, Integer>` as a lambda: `\"double\"` multiplies by 2, `\"inc\"` adds 1, `\"square\"` multiplies the number by itself, and `\"negate\"` flips the sign.",
    [("applySteps", [("steps", "String"), ("start", "int")], "int")], {"applySteps": steps},
    [("applySteps", ["double,inc", 5]), ("applySteps", ["square", 7]), ("applySteps", ["", 3])],
    [("applySteps", ["negate", 4]), ("applySteps", ["inc,inc,inc", 0]), ("applySteps", ["double,double,double", 1]), ("applySteps", ["inc,square", 2]), ("applySteps", ["square,negate", 3]), ("applySteps", ["negate,negate", -8])],
    'Function<Integer, Integer> stepFor(String name) {\n    return x -> x;\n}' + STEP_DRV,
    STEP_SOL + STEP_DRV,
    {"square-doubles": STEP_SOL.replace("x -> x * x", "x -> x * 2") + STEP_DRV,
     "inc-adds-two": STEP_SOL.replace("x -> x + 1", "x -> x + 2") + STEP_DRV},
    ("Return a different lambda for each step name. They take an Integer and return an Integer.", "case \"square\" -> x -> x * x;"),
    source_tests=[("uses lambdas", ["->"], None)],
    difficulty=2)
ex.predict("j3-l3.1-predict-lambda", "Read the lambdas", ["o2"], ["J3.05"],
    "Work out what this program prints.",
    '''void main() {
    int base = 10;
    Function<Integer, Integer> addBase = x -> x + base;
    Predicate<String> isEmpty = String::isEmpty;
    BiFunction<Integer, Integer, Integer> mul = (a, b) -> a * b;
    Supplier<String> hello = () -> "hi";

    IO.println(addBase.apply(5));
    IO.println(isEmpty.test(""));
    IO.println(isEmpty.negate().test(""));
    IO.println(mul.apply(3, 4));
    IO.println(hello.get());

    List<String> words = new ArrayList<>(List.of("pear", "fig", "apple"));
    words.sort((a, b) -> a.length() - b.length());
    IO.println(words);
}''', "15\ntrue\nfalse\n12\nhi\n[fig, pear, apple]",
    ("Work out each lambda's job. isEmpty.negate() is the opposite question. The sort compares lengths.", "addBase adds the captured 10. negate flips true to false. The words sort by length: fig (3), pear (4), apple (5)."),
    difficulty=3)
ex.explain("j3-l3.1-explain-functional", "What can a lambda become?", ["o3"], ["J3.05"],
    "(a) What is a **functional interface**, and why can `(a, b) -> a.length() - b.length()` be passed to `list.sort(...)`? (b) Why does this not compile, and how would you fix it? `int count = 0; list.forEach(x -> count++);`",
    "A full answer says a functional interface has exactly one abstract method, and Comparator is one, so the lambda provides the body of that method (compare) for the compiler to treat as a Comparator; and the second does not compile because a lambda can only use local variables that are effectively final and count changes, so use a mutable holder such as an AtomicInteger or an array, or use a stream's count().",
    {2: ("Says a functional interface has exactly one abstract method, that Comparator is one so the lambda supplies compare, and that the lambda cannot change the captured local count (must be effectively final) with a fix such as an AtomicInteger, a one-element array, or counting another way.",
         ["A functional interface has exactly one abstract method. Comparator is one, with compare(a, b), so the lambda provides that method's body and sort accepts it. The second example doesn't compile because count is a local variable that's changed, and lambdas can only capture variables that are effectively final. I'd use an AtomicInteger, or just use list.size() or a stream's count().",
          "(a) An interface with exactly one abstract method; Comparator has compare, and the lambda is its implementation, so it can be passed to sort. (b) count++ changes a captured local variable, which isn't allowed. Use a mutable object like an AtomicInteger instead."]),
     1: ("Answers one part well, or both parts only partly.",
         ["A functional interface has one abstract method.", "count can't be changed in a lambda."]),
     0: ("Incorrect, for example says any interface works, or that lambdas can change locals freely.",
         ["Any interface can take a lambda.", "Lambdas can change locals."])})
reg({"j3-l3.1": ("Lambdas and functional interfaces", ["J3.05"])},
    {"MC72": (["J3.05"], "Platform", "A lambda can change a local variable of the method around it"),
     "MC73": (["J3.05"], "I53", "A lambda can be assigned to any type, such as Object")})

# ====================================================================== 3.3.2
Lesson("j3-l3.2", "Stream pipelines", ["J3.06"], [
    ("o1", "Write a stream pipeline with filter, map, sorted and a collecting step"),
    ("o2", "Rewrite a loop as a stream, keeping its behaviour"),
    ("o3", "Find and fix a stream bug: reusing a stream, or expecting an operation to run without a terminal one"),
], ["j3-l3.1"], 50, ["I36", "I43", "I50", "R16"], r'''
## Before you start

You should be able to write lambdas and method references ([Lambdas and functional interfaces](j3-l3.1)).

**Quick check.** What does `x -> x * x` do, as a `Function<Integer, Integer>`?

<details><summary>Show the answer</summary>

It takes a number and returns its square.

</details>

## Explanation

### A pipeline instead of a loop

Much code has the same shape: take some items, **filter** the ones you want, **transform** them, and **collect** the results. A **stream** expresses that as a pipeline `[I36]`:

```java
List<String> result = words.stream()
        .filter(w -> w.length() >= 4)
        .map(String::toUpperCase)
        .sorted()
        .toList();
```

A pipeline has three parts:

1. **A source:** `words.stream()` (also `Arrays.stream(array)`, `Stream.of(...)`, `IntStream.range(0, 10)`).
2. **Intermediate operations:** each one turns a stream into another stream: `filter` (keep some), `map` (transform each), `sorted`, `distinct`, `limit(n)`.
3. **A terminal operation:** produces the final result: `toList()`, `collect(...)`, `count()`, `findFirst()`, `anyMatch(...)`, `sum()`.

Streams don't change the original collection; they produce new results.

### Streams are lazy

Nothing happens until the **terminal operation** runs: the computation on the source is only performed when it is initiated `[I50]`. This line does **nothing**:

```java
words.stream().filter(w -> w.length() >= 4).map(String::toUpperCase);   // no terminal operation
```

It builds a pipeline and throws it away. Forgetting the terminal operation is a classic bug: the code compiles and silently does nothing.

### A stream can be used once

A stream should be operated on **only once** `[I50]`:

```java
Stream<String> shortWords = words.stream().filter(w -> w.length() < 4);
long count = shortWords.count();      // uses up the stream
List<String> list = shortWords.toList();   // IllegalStateException: stream has already been operated upon or closed
```

If you need two results, collect once into a list, then ask the list for both:

```java
List<String> list = words.stream().filter(w -> w.length() < 4).toList();
int count = list.size();
```

### Collecting

`toList()` gathers the elements into a list. For more, `collect(...)` with a **collector** from `Collectors` `[I43]`:

```java
words.stream().collect(Collectors.joining(", "));                       // "a, b, c"
words.stream().collect(Collectors.groupingBy(String::length));           // Map<Integer, List<String>>
words.stream().collect(Collectors.groupingBy(String::length, Collectors.counting()));   // Map<Integer, Long>
words.stream().collect(Collectors.groupingBy(String::length, TreeMap::new, Collectors.counting()));  // sorted by length
```

The third form gives `groupingBy` a **map supplier** (`TreeMap::new`) so you control the kind of map (here, sorted by key) `[I43]`. Without it you get a `HashMap`, whose order isn't guaranteed.

### Numbers: `IntStream` and friends

Streams of `int` avoid boxing:

```java
values.stream().mapToInt(v -> v * v).sum();      // from a List<Integer> to an IntStream, then add up
IntStream.rangeClosed(1, 5).sum();                // 15
```

`mapToInt` turns a stream of objects into an `IntStream`, which has `sum()`, `max()`, `average()` and so on.

### Loop to stream, and back

A loop that filters, transforms and accumulates is usually a pipeline in disguise:

```java
int total = 0;
for (int v : values) {
    if (v % 2 == 0) {
        total += v * v;
    }
}
```

is:

```java
int total = values.stream().filter(v -> v % 2 == 0).mapToInt(v -> v * v).sum();
```

The stream version says *what* (even numbers, squared, added up); the loop says *how*. Lesson 3.3.3 covers when the loop is clearer.

Don't use side effects in the middle of a pipeline (changing an outside variable inside `map` or `filter`). It makes the result depend on when and how often the operation runs.

## Worked examples

### Example 1: long words, shouted and sorted

*Task: from a list of words, keep those with at least `min` letters, in upper case, sorted.*

**Step 1 — Filter:** `w.length() >= min`.

**Step 2 — Transform:** `String::toUpperCase`.

**Step 3 — Order, then collect:** `sorted()` and `toList()`.

```java
List<String> longUpper(List<String> words, int min) {
    return words.stream()
            .filter(w -> w.length() >= min)
            .map(String::toUpperCase)
            .sorted()
            .toList();
}
```

**Step 4 — Check.** `["pear", "fig", "apple"]` with `min = 4` gives `[APPLE, PEAR]`.

### Example 2: counting by length

*Task: produce `3=2,5=1` from `["fig", "kiwi"...]`-style data: how many words of each length, sorted by length.*

**Step 1 — Group by length and count, in a sorted map:**

```java
Map<Integer, Long> counts = words.stream()
        .collect(Collectors.groupingBy(String::length, TreeMap::new, Collectors.counting()));
```

**Step 2 — Turn each entry into text and join:**

```java
return counts.entrySet().stream()
        .map(e -> e.getKey() + "=" + e.getValue())
        .collect(Collectors.joining(","));
```

## Where this is used

- **Reports and data processing:** filter, group, count and total are the daily tasks of back-end code.
- **Reading code:** most modern Java uses streams, so you must be able to read them.
- **Collections APIs:** newer library methods return streams.

## Common mistakes

:::mistake{id=MC74}
**Using a stream twice.** A stream is used up by its terminal operation. Collect into a list first and use the list.
:::

:::mistake{id=MC75}
**Expecting `filter` or `map` to run without a terminal operation.** Nothing runs until a terminal operation such as `toList()` or `count()` is called.
:::

## Practice

::exercise{id=j3-l3.2-write-pipeline}

::exercise{id=j3-l3.2-write-grouping}

::exercise{id=j3-l3.2-modify-loop}

::exercise{id=j3-l3.2-debug-reuse}

## Further reading

- **`java.util.stream.Stream`** `[I50]` describes the pipeline, laziness and single use.
- **`java.util.stream.Collectors`** `[I43]` lists the ready-made collectors.
- **McCauley et al. (2008)** `[R16]` on debugging: an exception message such as "stream has already been operated upon" is a clue to read, not an obstacle.

## How you'll be assessed

- The **write** exercises check that you can build filter-map-collect pipelines and group and count (*implementation*).
- The **modify** exercise checks that you can turn a loop into a stream with the same behaviour (*modification*).
- The **debug** exercise checks that you can fix a stream reuse bug (*debugging*).
''' + FOOT, features=[("streams", 8), ("Stream.toList()", 16)])

ex = Exercises("j3-l3.2")
PIPE_SOL = 'List<String> longUpper(List<String> words, int minLength) {\n    return words.stream()\n            .filter(w -> w.length() >= minLength)\n            .map(String::toUpperCase)\n            .sorted()\n            .toList();\n}'
ex.method("write", "j3-l3.2-write-pipeline", "Filter, map, sort", ["o1"], ["J3.06"], ["IMPL"],
    "Write `longUpper(List<String> words, int minLength)` as a **stream pipeline**: keep the words with at least `minLength` letters, turn them to upper case, sort them, and return the list.",
    [("longUpper", [("words", "List<String>"), ("minLength", "int")], "List<String>")],
    {"longUpper": lambda ws, m: sorted(w.upper() for w in ws if len(w) >= m)},
    [("longUpper", [["pear", "fig", "apple"], 4]), ("longUpper", [[], 1]), ("longUpper", [["a", "bb"], 5])],
    [("longUpper", [["a", "B", "cc"], 1]), ("longUpper", [["a", "B"], 1]), ("longUpper", [["kiwi", "plum", "lime"], 4]), ("longUpper", [["zeta", "Alpha", "beta"], 4]), ("longUpper", [["x"], 1]), ("longUpper", [["abc", "abcd"], 4])],
    'List<String> longUpper(List<String> words, int minLength) {\n    return new ArrayList<>(words);\n}',
    PIPE_SOL,
    {"sorts-before-upper": PIPE_SOL.replace(".map(String::toUpperCase)\n            .sorted()", ".sorted()\n            .map(String::toUpperCase)"),
     "min-exclusive": PIPE_SOL.replace("w.length() >= minLength", "w.length() > minLength")},
    ("Chain filter, map, sorted and toList on words.stream(). The order of map and sorted matters for mixed case.", "words.stream().filter(w -> w.length() >= minLength).map(String::toUpperCase).sorted().toList();"),
    source_tests=[("uses a stream", ["stream()"], ["for ("])],
    difficulty=3)
GRP_SOL = 'String countByLength(List<String> words) {\n    Map<Integer, Long> counts = words.stream()\n            .collect(Collectors.groupingBy(String::length, TreeMap::new, Collectors.counting()));\n    return counts.entrySet().stream()\n            .map(e -> e.getKey() + "=" + e.getValue())\n            .collect(Collectors.joining(","));\n}'
def by_len(ws):
    c = Counter(len(w) for w in ws)
    return ",".join(f"{k}={c[k]}" for k in sorted(c))
ex.method("write", "j3-l3.2-write-grouping", "How many of each length?", ["o1"], ["J3.06"], ["IMPL"],
    "Write `countByLength(List<String> words)`: group the words by their length, count each group, and return the counts as `length=count` pairs, **shortest length first**, joined with commas, e.g. `3=2,5=1`. Use `Collectors.groupingBy` with a `TreeMap` and `Collectors.counting()`.",
    [("countByLength", [("words", "List<String>")], "String")], {"countByLength": by_len},
    [("countByLength", [["fig", "pear", "kiwi", "apple", "plum"]]), ("countByLength", [[]]), ("countByLength", [["a", "b"]])],
    [("countByLength", [["abc", "de", "fgh", "i"]]), ("countByLength", [["same", "size", "four"]]), ("countByLength", [["x"]]), ("countByLength", [["long", "longer", "longest", "a"]]), ("countByLength", [["", "a", ""]])],
    'String countByLength(List<String> words) {\n    return "";\n}',
    GRP_SOL,
    {"sums-lengths": GRP_SOL.replace("Collectors.counting()", "Collectors.summingLong(String::length)"),
     "counts-words-per-first-letter": GRP_SOL.replace("String::length", "w -> w.length() % 2")},
    ("Group with groupingBy(String::length, TreeMap::new, Collectors.counting()), then stream the entries and join.", "counts.entrySet().stream().map(e -> e.getKey() + \"=\" + e.getValue()).collect(Collectors.joining(\",\"));"),
    source_tests=[("uses groupingBy", ["groupingBy"], None)],
    difficulty=4)
LOOP_BAD = 'int sumOfSquaresOfEvens(List<Integer> values) {\n    int total = 0;\n    for (int v : values) {\n        if (v % 2 == 0) {\n            total += v * v;\n        }\n    }\n    return total;\n}'
LOOP_OK = 'int sumOfSquaresOfEvens(List<Integer> values) {\n    return values.stream()\n            .filter(v -> v % 2 == 0)\n            .mapToInt(v -> v * v)\n            .sum();\n}'
ex.method("modify", "j3-l3.2-modify-loop", "Loop to stream", ["o2"], ["J3.06"], ["MOD"],
    "`sumOfSquaresOfEvens` works, but it's a loop. **Rewrite it as a stream pipeline** with exactly the same behaviour: keep the even numbers (negative ones too), square each, and add them up. Don't use a `for` loop.",
    [("sumOfSquaresOfEvens", [("values", "List<Integer>")], "int")], {"sumOfSquaresOfEvens": lambda vs: sum(v * v for v in vs if v % 2 == 0)},
    [("sumOfSquaresOfEvens", [[1, 2, 3, 4]]), ("sumOfSquaresOfEvens", [[]]), ("sumOfSquaresOfEvens", [[-2, 3]])],
    [("sumOfSquaresOfEvens", [[1, 3, 5]]), ("sumOfSquaresOfEvens", [[0, 0]]), ("sumOfSquaresOfEvens", [[10, -10, 7]]), ("sumOfSquaresOfEvens", [[6]]), ("sumOfSquaresOfEvens", [[-4, -3, -2, -1]])],
    LOOP_BAD, LOOP_OK,
    {"odd-numbers": LOOP_OK.replace("v % 2 == 0", "v % 2 != 0"),
     "forgets-to-square": LOOP_OK.replace("v -> v * v", "v -> v")},
    ("filter keeps the even numbers; mapToInt squares them; sum adds them.", "values.stream().filter(v -> v % 2 == 0).mapToInt(v -> v * v).sum();"),
    source_tests=[("it is a stream", ["stream()"], ["for ("])],
    difficulty=3)
REUSE_BAD = 'String summary(List<String> words) {\n    Stream<String> shortWords = words.stream().filter(w -> w.length() < 4);\n    long count = shortWords.count();\n    List<String> list = shortWords.toList();\n    return count + ":" + String.join("+", list);\n}'
REUSE_OK = 'String summary(List<String> words) {\n    List<String> list = words.stream().filter(w -> w.length() < 4).toList();\n    return list.size() + ":" + String.join("+", list);\n}'
ex.method("debug", "j3-l3.2-debug-reuse", "The stream that was already used", ["o3"], ["J3.06"], ["DEBUG"],
    "`summary` should return the number of short words (fewer than 4 letters), a colon, and the short words joined by `+`, e.g. `2:fig+ax`. It throws an `IllegalStateException`. Read the message, find why, and fix it.",
    [("summary", [("words", "List<String>")], "String")],
    {"summary": lambda ws: f"{len([w for w in ws if len(w) < 4])}:{'+'.join(w for w in ws if len(w) < 4)}"},
    [("summary", [["fig", "pear", "ax"]]), ("summary", [[]]), ("summary", [["banana"]])],
    [("summary", [["a", "b", "c"]]), ("summary", [["abc", "abcd"]]), ("summary", [["x", "longword", "yz"]]), ("summary", [["fig"]]), ("summary", [["", "pear"]])],
    REUSE_BAD, REUSE_OK,
    {"filters-at-most-four": REUSE_OK.replace("w.length() < 4", "w.length() <= 4"),
     "count-only": 'String summary(List<String> words) {\n    long n = words.stream().filter(w -> w.length() < 4).count();\n    return n + ":";\n}'},
    ("What does the message say about the stream? How many times is it used?", "Collect into a list once, then use list.size() and the list itself."),
    difficulty=3)
reg({"j3-l3.2": ("Stream pipelines", ["J3.06"])},
    {"MC74": (["J3.06"], "I50", "A stream can be used again after a terminal operation"),
     "MC75": (["J3.06"], "I50", "filter and map run as soon as they are written, without a terminal operation")})

# ====================================================================== 3.3.3
Lesson("j3-l3.3", "Optional, and choosing loops or streams", ["J3.07"], [
    ("o1", "Return and use an Optional for a result that might not exist"),
    ("o2", "Chain findFirst, map and orElse in one expression"),
    ("o3", "Explain when a loop is clearer than a stream, and when a stream is clearer"),
], ["j3-l3.2"], 45, ["I35", "I50", "R8"], r'''
## Before you start

You should be able to write stream pipelines ([Stream pipelines](j3-l3.2)).

**Quick check.** What does `list.stream().filter(...).findFirst()` look for?

<details><summary>Show the answer</summary>

The first element matching the condition. It might not find one.

</details>

## Explanation

### A result that might not exist

"Find the first long name" has no answer when no name is long. Returning `null` for "nothing" is the old way, and it moves the failure to whoever forgets to check. **`Optional<T>`** is a container that **may or may not hold a value** `[I35]`. A method that returns `Optional<String>` tells the caller, in its type, that there might be nothing.

```java
Optional<String> findLong(List<String> names, int min) {
    return names.stream()
            .filter(n -> n.length() >= min)
            .findFirst();
}
```

`findFirst()` itself returns an `Optional`.

### Using an Optional

Never just grab the value; say what to do in each case:

```java
Optional<String> found = findLong(names, 6);

String name = found.orElse("none");                  // the value, or a default
String upper = found.map(String::toUpperCase).orElse("?");   // transform if present
found.ifPresent(n -> IO.println("Found " + n));      // do something only if present
String must = found.orElseThrow();                   // the value, or an exception if empty
```

| Method | Meaning |
|---|---|
| `orElse(x)` | the value, or `x` if empty |
| `map(f)` | if present, apply `f` and wrap the result; if empty, stay empty |
| `ifPresent(action)` | run `action` only if there's a value |
| `isPresent()` | `true` if there's a value |
| `orElseThrow()` | the value, or throw `NoSuchElementException` |
| `Optional.of(x)` / `Optional.empty()` / `Optional.ofNullable(x)` | make one |

`Optional.of(null)` throws, and `ofNullable(x)` gives an empty one when `x` is null `[I35]`.

### Using `get()` safely

`get()` exists, but calling it on an empty Optional throws. A common bad habit is `if (opt.isPresent()) { use(opt.get()); }` everywhere, which is just a null check wearing a coat. Prefer `map`, `orElse` and `ifPresent`, which handle both cases in the code's shape.

### Where Optional belongs

Use it for **return values** where "no result" is normal. Don't use it for fields or method parameters (it adds clutter without benefit there), and never return `null` from a method that returns an `Optional`.

### Loop or stream?

Streams are a good tool, not the best one for everything. Compare:

**A stream reads well when** the job is *filter, transform, collect* in a row, with no state shared between steps:

```java
List<String> shouted = names.stream().filter(n -> !n.isEmpty()).map(String::toUpperCase).toList();
```

**A loop reads better when** you need:

- **early exit** with several conditions;
- **several accumulators** updated together (a total, a count and a maximum);
- **index access** or work on two positions at once;
- **checked exceptions** inside the body;
- steps whose order and side effects matter.

```java
int best = 0;
String bestName = "";
for (String name : names) {
    int score = score(name);
    if (score > best) {
        best = score;
        bestName = name;
    }
}
```

The same logic as a stream would need a cleverly built collector and would be harder to read. Choose the one a **colleague would understand fastest**. A sign you've gone too far: a stream with several lambdas that each span several lines, or one that modifies outside variables.

## Worked examples

### Example 1: first match, transformed

*Task: the upper-case initial of the first name that starts with `prefix`, or `?` if none.*

**Step 1 — Find the first match:** `filter(n -> n.startsWith(prefix)).findFirst()`.

**Step 2 — If found, take its first letter in capitals:** `map(n -> n.substring(0, 1).toUpperCase())`.

**Step 3 — If not found, use `?`:** `orElse("?")`.

```java
String initialOf(List<String> names, String prefix) {
    return names.stream()
            .filter(n -> n.startsWith(prefix))
            .findFirst()
            .map(n -> n.substring(0, 1).toUpperCase())
            .orElse("?");
}
```

**Step 4 — Check.** With names `[ada, bo, bea]` and prefix `b`, the result is `B`; with prefix `z`, it's `?`.

### Example 2: choosing

*Task: find the name with the highest score, and also count how many scored above 10. Loop or stream?*

**Step 1 — What state is shared?** The best so far, its name, and a counter: three things updated together.

**Step 2 — Which reads better?** One loop updating three variables. A stream would need two passes or a custom collector.

**Step 3 — Choose the loop.** A clear loop is a good answer.

## Predict, then run

::exercise{id=j3-l3.3-predict-optional}

## Where this is used

- **Search methods** (`findById`, `findByEmail`) return `Optional` throughout modern Java libraries and Spring.
- **Code review:** "this stream is too clever; use a loop" and "this `get()` is unsafe" are both common comments.
- **Readability** matters more than cleverness once other people maintain your code.

## Common mistakes

:::mistake{id=MC76}
**Calling `get()` on an Optional without checking.** An empty Optional throws `NoSuchElementException`. Use `orElse`, `map`, or `orElseThrow` (with a message that makes the failure clear).
:::

:::mistake{id=MC77}
**Using a stream for everything.** A stream that updates several variables, or whose lambdas span many lines, is harder to read than a loop.
:::

## Practice

::exercise{id=j3-l3.3-write-find}

::exercise{id=j3-l3.3-write-initial}

::exercise{id=j3-l3.3-explain-loop-or-stream}

## Further reading

- **`java.util.Optional`** `[I35]` documents every method above.
- **`java.util.stream.Stream`** `[I50]`.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can return an `Optional` and chain `findFirst`, `map` and `orElse` (*implementation*).
- The **predict** exercise checks that you know how `Optional` behaves when empty and when present (*identifying mistakes*).
- The **explain** exercise checks that you can choose between a loop and a stream and justify it (*explanation*).
''' + FOOT)

ex = Exercises("j3-l3.3")
FIND_DRV = '\n\nString firstLong(List<String> names, int min) {\n    return findLong(names, min).orElse("none");\n}'
FIND_SOL = 'Optional<String> findLong(List<String> names, int min) {\n    return names.stream()\n            .filter(n -> n.length() >= min)\n            .findFirst();\n}'
ex.method("write", "j3-l3.3-write-find", "Return an Optional", ["o1"], ["J3.07"], ["IMPL"],
    "Write `findLong(List<String> names, int min)`, which returns an `Optional<String>`: the **first** name with at least `min` letters, or an empty `Optional` if there isn't one. (The driver `firstLong` turns that into text, using `\"none\"` for empty.)",
    [("firstLong", [("names", "List<String>"), ("min", "int")], "String")],
    {"firstLong": lambda ns, m: next((n for n in ns if len(n) >= m), "none")},
    [("firstLong", [["ada", "grace", "bo"], 5]), ("firstLong", [["ada", "bo"], 5]), ("firstLong", [[], 1])],
    [("firstLong", [["abcd", "abcde"], 4]), ("firstLong", [["x", "yy", "zzz"], 2]), ("firstLong", [["same", "size"], 4]), ("firstLong", [["a"], 2]), ("firstLong", [["", "q"], 1])],
    'Optional<String> findLong(List<String> names, int min) {\n    return Optional.empty();\n}' + FIND_DRV,
    FIND_SOL + FIND_DRV,
    {"last-match": FIND_SOL.replace(".findFirst()", ".reduce((a, b) -> b)"),
     "min-exclusive": FIND_SOL.replace("n.length() >= min", "n.length() > min")},
    ("Stream the names, keep those that are long enough, and ask for the first one with findFirst().", "names.stream().filter(n -> n.length() >= min).findFirst();"),
    source_tests=[("returns an Optional", ["Optional<String> findLong"], None)],
    difficulty=2)
def initial(ns, p):
    for n in ns:
        if n.startswith(p): return n[0].upper()
    return "?"
INIT_SOL = 'String initialOf(List<String> names, String prefix) {\n    return names.stream()\n            .filter(n -> n.startsWith(prefix))\n            .findFirst()\n            .map(n -> n.substring(0, 1).toUpperCase())\n            .orElse("?");\n}'
ex.method("write", "j3-l3.3-write-initial", "An Optional chain", ["o2"], ["J3.07"], ["IMPL"],
    "Write `initialOf(List<String> names, String prefix)`: find the **first** name that starts with `prefix`, and return its first letter in **upper case**; if no name starts with the prefix, return `\"?\"`. Do it as one chain using `findFirst`, `map` and `orElse`. (All the names are non-empty.)",
    [("initialOf", [("names", "List<String>"), ("prefix", "String")], "String")], {"initialOf": initial},
    [("initialOf", [["ada", "bo", "bea"], "b"]), ("initialOf", [["ada", "bo"], "z"]), ("initialOf", [[], "a"])],
    [("initialOf", [["grace", "ada"], "gr"]), ("initialOf", [["Ada", "ada"], "a"]), ("initialOf", [["x"], ""]), ("initialOf", [["bob", "bill"], "bi"]), ("initialOf", [["zed"], "zed"])],
    'String initialOf(List<String> names, String prefix) {\n    return "?";\n}',
    INIT_SOL,
    {"not-capitalised": INIT_SOL.replace(".toUpperCase()", ""),
     "last-match": INIT_SOL.replace(".findFirst()", ".reduce((a, b) -> b)")},
    ("filter by startsWith, findFirst gives an Optional, map takes its first letter in capitals, orElse supplies the question mark.", "...findFirst().map(n -> n.substring(0, 1).toUpperCase()).orElse(\"?\");"),
    source_tests=[("uses an Optional chain", ["findFirst()", "orElse"], None)],
    difficulty=3)
ex.predict("j3-l3.3-predict-optional", "Present or empty?", ["o1"], ["J3.07"],
    "Work out what this program prints.",
    '''void main() {
    Optional<String> some = Optional.of("kiwi");
    Optional<String> none = Optional.empty();
    String missing = null;

    IO.println(some.map(String::toUpperCase).orElse("?"));
    IO.println(none.map(String::toUpperCase).orElse("?"));
    IO.println(none.isPresent());
    IO.println(Optional.ofNullable(missing).isPresent());
    some.ifPresent(s -> IO.println("has " + s));
    none.ifPresent(s -> IO.println("has " + s));
    IO.println(some.map(String::length).orElse(0));
}''', "KIWI\n?\nfalse\nfalse\nhas kiwi\n4",
    ("map only does something when there's a value. ifPresent only runs its action then.", "some becomes KIWI; none stays empty so orElse gives ?. ofNullable(null) is empty. Only some prints \"has kiwi\". length of kiwi is 4."),
    difficulty=2)
ex.explain("j3-l3.3-explain-loop-or-stream", "Which is clearer?", ["o3"], ["J3.07"],
    "A colleague rewrites this loop as a stream and says \"streams are always better\":\n\n```java\nint best = 0;\nString bestName = \"\";\nint over10 = 0;\nfor (String name : names) {\n    int score = score(name);\n    if (score > 10) over10++;\n    if (score > best) { best = score; bestName = name; }\n}\n```\n\nSay (a) whether you'd accept the rewrite and why, and (b) give one situation in the same codebase where a stream *would* be the clearer choice, with a one-line example.",
    "A full answer says the loop updates three variables together (best, bestName, over10) so a stream would need several passes or an awkward collector and would be harder to read; and gives a case where a stream is clearer, such as filtering and transforming a list into another list (names.stream().filter(...).map(...).toList()).",
    {2: ("Says the loop keeps several pieces of state together so the stream would need multiple passes or a custom collector and be less readable, and gives a good stream case such as a simple filter-map-collect with an example.",
         ["I wouldn't accept it. The loop updates three things in one pass (best score, best name and the over-ten count), and a stream would need several passes or an awkward collector, which is harder to read. A stream is clearer for something like names.stream().filter(n -> !n.isEmpty()).map(String::toUpperCase).toList(), which just filters and transforms.",
          "I'd keep the loop because it's one clear pass with three accumulators. Streams are better when it's a simple pipeline, like turning a list of names into a list of their lengths with map and toList."]),
     1: ("Gives a sensible view without a reason, or reasons without a stream example.",
         ["Keep the loop.", "Streams are good for filtering."]),
     0: ("Incorrect or one-sided, for example says streams are always better or loops are always better.",
         ["Streams are always better.", "Never use streams."])})
reg({"j3-l3.3": ("Optional, and choosing loops or streams", ["J3.07"])},
    {"MC76": (["J3.07"], "I35", "Calling get() on an Optional is always safe"),
     "MC77": (["J3.07"], "Platform", "A stream is always clearer than a loop")})
print("3.3 written")
