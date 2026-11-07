import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-3"
from build import *
import outline, re
from collections import Counter
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'

# ====================================================================== 3.1.1
Lesson("j3-l1.1", "Lists and sets", ["J3.01"], [
    ("o1", "Choose between a List and a Set, and between the kinds of Set, for a given need"),
    ("o2", "Use add, remove, contains and size on lists and sets, and predict the results, including remove on a List of Integer"),
    ("o3", "Explain which collection fits a scenario and why"),
], ["j2-l5.3", "j1-l6.3"], 45, ["I41", "I47", "I29", "I2"], r'''
## Before you start

You should be comfortable with `ArrayList` ([ArrayList](j1-l6.3)) and with interfaces ([Interfaces and polymorphism](j2-l3.1)).

**Quick check.** Why is a variable usually declared as `List<String> names = new ArrayList<>();` and not `ArrayList<String> names = ...`?

<details><summary>Show the answer</summary>

The code then depends only on the `List` interface, so the implementation can be swapped without changing the rest.

</details>

## Explanation

Stage 3 is about the standard library you'll use every day. The first part is **collections**: objects that hold other objects. They live in `java.util`. In a traditional source file you'd start with `import java.util.*;`. In a compact source file, as in this course, the public types of the `java.base` module (which includes `java.util`) are available without any import `[I2]`.

### The collection family

The main interfaces are:

| Interface | Idea |
|---|---|
| `List` | an ordered sequence; allows duplicates; items have a position |
| `Set` | a group with **no duplicates** |
| `Map` | keys that lead to values (next lesson) |

You almost always declare the **interface** type and choose the implementation when you create it.

### List and ArrayList

```java
List<String> names = new ArrayList<>();
names.add("Ada");
names.add("Bo");
names.add("Ada");          // duplicates are fine
names.size();              // 3
names.get(0);              // "Ada"
names.contains("Bo");      // true
```

`ArrayList` is a resizable array `[I47]`, the usual choice for a `List`.

**A trap with `remove`.** `List` has two methods called `remove`: `remove(int index)` removes the item **at a position**, and `remove(Object o)` removes the **first matching** item. With a `List<Integer>`, the argument type decides:

```java
List<Integer> nums = new ArrayList<>(List.of(10, 20, 30));
nums.remove(1);                    // index 1  -> [10, 30]
nums.remove(Integer.valueOf(10));  // the value 10 -> [30]
```

`remove(1)` removed the item at position 1 (the 20), not the value 1.

### Set: no duplicates

A set silently ignores an `add` of something it already has, and `add` tells you whether it changed anything:

```java
Set<String> seen = new HashSet<>();
seen.add("a");     // true
seen.add("a");     // false: already there
seen.size();       // 1
```

There are three common implementations, and they differ in **order**:

| Class | Iteration order |
|---|---|
| `HashSet` | **no guarantee**, and it can change `[I41]` |
| `LinkedHashSet` | the order items were first added `[I41]` |
| `TreeSet` | sorted, by natural ordering or a `Comparator` `[I41]` |

Never rely on `HashSet`'s order. If you print one and it looks sorted today, that is luck.

### Useful tricks

- **Remove duplicates, keeping order:** `new ArrayList<>(new LinkedHashSet<>(list))`.
- **Sorted unique items:** `new TreeSet<>(list)`.
- **Intersection (items in both):** copy one set, then `retainAll(other)`.
- **Unmodifiable list:** `List.of(...)` creates one that can't be changed `[I29]` (more in lesson 3.1.3).

### Choosing

Ask what you need:

- **Position matters, or duplicates matter** (a to-do list, the last five transactions): `List`.
- **Only "is it in there?" matters, and duplicates are meaningless** (visited pages, banned words): `Set`.
- **Unique, in the order they arrived:** `LinkedHashSet`. **Unique and sorted:** `TreeSet`. **Unique, order irrelevant:** `HashSet`.

## Worked examples

### Example 1: unique names, in order

*Task: `["b", "a", "b", "c"]` should become `["b", "a", "c"]`.*

**Step 1 — What do I need?** No duplicates, and the first-seen order kept.

**Step 2 — `LinkedHashSet`** does exactly that.

**Step 3 — Code:**

```java runnable
void main() {
    List<String> names = List.of("b", "a", "b", "c");
    List<String> unique = new ArrayList<>(new LinkedHashSet<>(names));
    IO.println(unique);
}
```

It prints `[b, a, c]`. A plain `HashSet` could print them in any order.

### Example 2: how many in common?

*Task: how many different items appear in both of two lists?*

**Step 1 — Duplicates shouldn't count twice,** so sets are the natural fit.

**Step 2 — Copy the first list into a set, keep only what's also in the second:**

```java
int commonCount(List<String> a, List<String> b) {
    Set<String> common = new HashSet<>(a);
    common.retainAll(new HashSet<>(b));
    return common.size();
}
```

**Step 3 — Check.** `["x", "x", "y"]` and `["x", "z"]` share just `x`, so 1.

## Predict, then run

::exercise{id=j3-l1.1-predict-sets}

::exercise{id=j3-l1.1-predict-remove}

## Where this is used

- **Deduplicating** user input, ids, and log lines is a daily task.
- **Membership checks** (`allowed.contains(user)`) are sets in almost every codebase.
- **Choosing the right collection** is a standard question in code review and interviews.

## Common mistakes

:::mistake{id=MC62}
**Expecting a `HashSet` to keep the order items were added.** It makes no promise about order. Use `LinkedHashSet` for insertion order or `TreeSet` for sorted.
:::

:::mistake{id=MC63}
**Calling `list.remove(1)` on a `List<Integer>` to remove the value 1.** It removes the item at index 1. To remove a value, use `remove(Integer.valueOf(1))`.
:::

## Practice

::exercise{id=j3-l1.1-write-unique}

::exercise{id=j3-l1.1-write-common}

::exercise{id=j3-l1.1-explain-choose}

## Further reading

- **`java.util.HashSet`, `LinkedHashSet` and `TreeSet`** `[I41]` describe each class's ordering.
- **`java.util.ArrayList`** `[I47]` and **`java.util.List`** `[I29]`.
- **JEP 512** `[I2]` explains why compact source files need no imports for these classes.

## How you'll be assessed

- The **write** exercises check that you can use a set to remove duplicates in order and to find common items (*implementation*).
- The **predict** exercises check that you know set ordering and the two `remove` methods (*identifying mistakes*).
- The **explain** exercise checks that you can choose a collection for a scenario (*explanation*).
''' + FOOT)

ex = Exercises("j3-l1.1")
def uniq(a):
    seen, out = set(), []
    for x in a:
        if x not in seen: seen.add(x); out.append(x)
    return out
ex.method("write", "j3-l1.1-write-unique", "Unique, in order", ["o1"], ["J3.01"], ["IMPL"],
    "Write `unique(List<String> names)`: return a new list with the duplicates removed, keeping each name's **first** position. `[b, a, b, c]` becomes `[b, a, c]`.",
    [("unique", [("names", "List<String>")], "List<String>")], {"unique": uniq},
    [("unique", [["b", "a", "b", "c"]]), ("unique", [[]]), ("unique", [["x", "x", "x"]])],
    [("unique", [["b", "a"]]), ("unique", [["pear", "apple", "pear", "fig", "apple"]]), ("unique", [["z", "y", "x"]]), ("unique", [["a"]]), ("unique", [["c", "b", "a", "b", "c"]])],
    'List<String> unique(List<String> names) {\n    return names;\n}',
    'List<String> unique(List<String> names) {\n    return new ArrayList<>(new LinkedHashSet<>(names));\n}',
    {"hash-order": 'List<String> unique(List<String> names) {\n    return new ArrayList<>(new HashSet<>(names));\n}',
     "sorted": 'List<String> unique(List<String> names) {\n    return new ArrayList<>(new TreeSet<>(names));\n}'},
    ("Which Set keeps the order that things were first added?", "new ArrayList<>(new LinkedHashSet<>(names))"),
    difficulty=2)
ex.method("write", "j3-l1.1-write-common", "Items in both lists", ["o1", "o2"], ["J3.01"], ["IMPL"],
    "Write `commonCount(List<String> a, List<String> b)`: the number of **different** items that appear in both lists. `[x, x, y]` and `[x, z]` have one in common.",
    [("commonCount", [("a", "List<String>"), ("b", "List<String>")], "int")], {"commonCount": lambda a, b: len(set(a) & set(b))},
    [("commonCount", [["x", "x", "y"], ["x", "z"]]), ("commonCount", [[], ["a"]]), ("commonCount", [["a", "b"], ["b", "a"]])],
    [("commonCount", [["a", "a", "a"], ["a", "a"]]), ("commonCount", [["p", "q", "r"], ["x", "y"]]), ("commonCount", [["a", "b", "c", "d"], ["d", "c", "e"]]), ("commonCount", [["m"], ["m"]]), ("commonCount", [["k", "k", "j"], ["j", "j", "k", "k"]])],
    'int commonCount(List<String> a, List<String> b) {\n    return 0;\n}',
    'int commonCount(List<String> a, List<String> b) {\n    Set<String> common = new HashSet<>(a);\n    common.retainAll(new HashSet<>(b));\n    return common.size();\n}',
    {"counts-duplicates": 'int commonCount(List<String> a, List<String> b) {\n    int n = 0;\n    for (String s : a) {\n        if (b.contains(s)) n++;\n    }\n    return n;\n}',
     "union-size": 'int commonCount(List<String> a, List<String> b) {\n    Set<String> all = new HashSet<>(a);\n    all.addAll(b);\n    return all.size();\n}'},
    ("Duplicates shouldn't count twice, so use sets. Keep only the items of one set that are also in the other.", "Set<String> common = new HashSet<>(a); common.retainAll(new HashSet<>(b)); return common.size();"),
    difficulty=3)
ex.predict("j3-l1.1-predict-sets", "Three kinds of collection", ["o2"], ["J3.01"],
    "Work out what this program prints. (Only collections whose order is guaranteed are printed.)",
    '''void main() {
    List<String> list = new ArrayList<>(List.of("b", "a", "b", "c"));
    Set<String> set = new HashSet<>(list);
    Set<String> sorted = new TreeSet<>(list);
    Set<String> ordered = new LinkedHashSet<>(list);
    IO.println(list.size());
    IO.println(set.size());
    IO.println(sorted);
    IO.println(ordered);
    IO.println(list.remove("b"));
    IO.println(list);
}''', "4\n3\n[a, b, c]\n[b, a, c]\ntrue\n[a, b, c]",
    ("Which of these collections drop duplicates? What does each do about order? remove(Object) removes only the first match.", "The list keeps all four. The three sets keep b, a, c. After removing the first \"b\" from the list, [a, b, c] is left."),
    difficulty=2)
ex.predict("j3-l1.1-predict-remove", "remove: index or value?", ["o2"], ["J3.01"],
    "Work out what this program prints.",
    '''void main() {
    List<Integer> nums = new ArrayList<>(List.of(10, 20, 30, 20));
    nums.remove(1);
    IO.println(nums);
    nums.remove(Integer.valueOf(20));
    IO.println(nums);
    nums.remove(Integer.valueOf(99));
    IO.println(nums);
    IO.println(nums.contains(30));
}''', "[10, 30, 20]\n[10, 30]\n[10, 30]\ntrue",
    ("remove(1) with an int removes the item at that position. remove(Integer.valueOf(x)) removes a matching value.", "Index 1 is the first 20, so [10, 30, 20]. Then the value 20 is removed, leaving [10, 30]. Removing 99 changes nothing."),
    difficulty=3)
ex.explain("j3-l1.1-explain-choose", "Which collection?", ["o3"], ["J3.01"],
    "Choose a collection for each of these, and say why: (a) the last ten pages a user visited, newest last, where visiting the same page twice counts twice; (b) the set of user ids that have already claimed a coupon, where only \"has this id claimed it?\" matters; (c) a list of tags with no repeats, shown in the order the author typed them; (d) the unique words in a text, shown alphabetically.",
    "A full answer chooses List/ArrayList for (a) because order and duplicates matter, a HashSet (or any Set) for (b) because only membership matters, LinkedHashSet for (c) for no duplicates in insertion order, and TreeSet for (d) for unique and sorted.",
    {2: ("Gives List for (a), a Set such as HashSet for (b), LinkedHashSet for (c) and TreeSet for (d), each with a correct reason about order, duplicates or membership.",
         ["(a) an ArrayList, because order and repeats matter. (b) a HashSet, because I only need to ask whether an id is in it. (c) a LinkedHashSet, which drops repeats and keeps insertion order. (d) a TreeSet, which keeps unique items sorted.",
          "(a) List. (b) HashSet for fast membership. (c) LinkedHashSet for no duplicates in the order typed. (d) TreeSet for sorted unique words."]),
     1: ("Gets two or three right, or names collections without reasons.",
         ["(a) List (b) Set (c) List (d) Set", "Use a Set for all of them."]),
     0: ("Incorrect, for example uses a HashSet for the ordered or sorted cases.",
         ["HashSet for everything.", "A list for (b) and (d)."])})
reg({"j3-l1.1": ("Lists and sets", ["J3.01"])},
    {"MC62": (["J3.01"], "I41", "A HashSet keeps items in the order they were added"),
     "MC63": (["J3.01"], "R8", "list.remove(1) on a List of Integer removes the value 1")})

# ====================================================================== 3.1.2
Lesson("j3-l1.2", "Maps", ["J3.02"], [
    ("o1", "Use a Map to store and look up values by key, including getOrDefault, merge and containsKey"),
    ("o2", "Count things with a Map, and choose HashMap, LinkedHashMap or TreeMap by the order needed"),
    ("o3", "Explain why a map key needs equals and hashCode, and fix the null-from-get bug"),
], ["j3-l1.1"], 45, ["I30", "I42", "I38", "R8"], r'''
## Before you start

You should know how lists and sets differ ([Lists and sets](j3-l1.1)) and the `equals`/`hashCode` contract ([static, toString and equals](j2-l1.4)).

**Quick check.** Which collection would you use to hold "the words I've seen so far, with no repeats"?

<details><summary>Show the answer</summary>

A `Set`.

</details>

## Explanation

### Looking things up by key

A **`Map`** connects **keys** to **values**: a word to its count, a customer id to a customer, a country code to a name. Keys are unique; looking up a key is the whole point.

```java
Map<String, Integer> stock = new HashMap<>();
stock.put("apple", 3);
stock.put("pear", 1);
stock.get("apple");              // 3
stock.get("kiwi");               // null  (no such key)
stock.containsKey("pear");       // true
stock.put("apple", 5);           // replaces the old value
stock.size();                    // 2
```

`Map<String, Integer>` has two type parameters: the key type and the value type. Both must be object types, so you use `Integer`, not `int`. Java converts between them automatically (*boxing*), which is exactly where the first trap hides.

### The null trap

`get` returns `null` for a missing key. If the value type is `Integer` and you do arithmetic on the result, Java tries to unbox `null` into an `int` and throws a `NullPointerException`:

```java
counts.put(word, counts.get(word) + 1);    // crashes the first time a word is seen
```

Safer ways:

```java
counts.put(word, counts.getOrDefault(word, 0) + 1);   // 0 if absent
counts.merge(word, 1, Integer::sum);                  // add 1, or set 1 if absent
```

`merge(key, value, how)` says: *put this value if there is none, otherwise combine the old and new with this function*. `Integer::sum` is a ready-made way to add two numbers; lesson 3.3.1 explains the `::` notation. There's also `putIfAbsent(key, value)`, which only puts if the key isn't there.

### Counting is the classic job for a map

```java runnable
void main() {
    String text = "to be or not to be";
    Map<String, Integer> counts = new TreeMap<>();
    for (String word : text.split(" ")) {
        counts.merge(word, 1, Integer::sum);
    }
    IO.println(counts);
}
```

It prints `{be=2, not=1, or=1, to=2}`.

### Going through a map

```java
for (Map.Entry<String, Integer> entry : counts.entrySet()) {
    IO.println(entry.getKey() + " -> " + entry.getValue());
}
```

You can also loop over `counts.keySet()` or `counts.values()`.

### Three kinds of map, three orders

| Class | Iteration order |
|---|---|
| `HashMap` | **no guarantee**; permits a null key and null values `[I30]` |
| `LinkedHashMap` | the order keys were first inserted `[I42]` |
| `TreeMap` | sorted by key, by natural ordering or a `Comparator` `[I42]` |

As with sets, never rely on `HashMap`'s order. For predictable output (and for tests), use `TreeMap` or `LinkedHashMap`.

### Keys need `equals` and `hashCode`

A `HashMap` uses a key's `hashCode()` to find where to look, then `equals` to confirm. So a class used as a key must follow the contract: equal objects have equal hash codes `[I38]`. And many keys sharing the same hash code make the map slow `[I30]`.

Two more rules for keys:

- **Make keys immutable.** If a key's fields change after it's been put in a map, its hash code changes, and the map can no longer find it. `String`, `Integer` and records are good keys.
- Records get correct `equals` and `hashCode` for free, which makes them excellent keys.

## Worked examples

### Example 1: the most common word

*Task: return the most frequent word, and the alphabetically first if there's a tie.*

**Step 1 — Count the words,** in a `TreeMap` so iteration is alphabetical.

**Step 2 — Walk the entries,** remembering the best so far, and replace it only when a count is **strictly greater**. A tie keeps the earlier (alphabetically first) word.

```java
String topWord(String text) {
    Map<String, Integer> counts = new TreeMap<>();
    for (String w : text.toLowerCase().strip().split("\\s+")) {
        if (!w.isEmpty()) counts.merge(w, 1, Integer::sum);
    }
    String best = "";
    int bestCount = 0;
    for (Map.Entry<String, Integer> e : counts.entrySet()) {
        if (e.getValue() > bestCount) {
            best = e.getKey();
            bestCount = e.getValue();
        }
    }
    return best;
}
```

**Step 3 — Check.** `"b a b a"` has a tie at 2, and gives `a`.

### Example 2: the NullPointerException

*Task: `counts.put(w, counts.get(w) + 1)` throws on the first word. Fix it.*

**Step 1 — What does `get` return for an unseen word?** `null`.

**Step 2 — And `null + 1`?** Java unboxes `null` into an `int`, and that throws.

**Step 3 — Use `counts.merge(w, 1, Integer::sum)`.**

## Predict, then run

::exercise{id=j3-l1.2-predict-map}

## Where this is used

- **Counting and grouping** (word counts, errors per code, sales per region) is a map in nearly every report.
- **Lookups:** caches, configuration, indexes from id to object.
- **JSON and configuration** are maps of keys to values at their core.

## Common mistakes

:::mistake{id=MC64}
**Assuming `map.get(key)` returns 0 for a missing key.** It returns `null`, and arithmetic on that throws a `NullPointerException`. Use `getOrDefault` or `merge`.
:::

:::mistake{id=MC65}
**Relying on `HashMap` order.** It's unspecified. Use `LinkedHashMap` or `TreeMap` when order matters.
:::

:::mistake{id=MC66}
**Using a mutable object as a key and then changing it.** The map can't find it any more, because its hash code changed.
:::

## Practice

::exercise{id=j3-l1.2-write-counts}

::exercise{id=j3-l1.2-write-topword}

::exercise{id=j3-l1.2-debug-null}

::exercise{id=j3-l1.2-explain-keys}

## Further reading

- **`java.util.HashMap`** `[I30]`, **`TreeMap` and `LinkedHashMap`** `[I42]`.
- **`java.lang.Object`** `[I38]` for the `equals` and `hashCode` contract.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can count with a map and get a deterministic result (*implementation*).
- The **predict** exercise checks that you know `put`, `merge`, `putIfAbsent`, `get` and `getOrDefault` (*identifying mistakes*).
- The **debug** exercise checks that you can fix the null-unboxing bug (*debugging*).
- The **explain** exercise checks that you can say what a key needs and why map order isn't something to rely on (*explanation*).
''' + FOOT)

ex = Exercises("j3-l1.2")
def words(text): return text.lower().split()
def counts_str(text):
    c = Counter(words(text))
    return ",".join(f"{w}={c[w]}" for w in sorted(c))
COUNTS_SOL = 'String counts(String text) {\n    Map<String, Integer> counts = new TreeMap<>();\n    for (String w : text.toLowerCase().strip().split("\\\\s+")) {\n        if (!w.isEmpty()) {\n            counts.merge(w, 1, Integer::sum);\n        }\n    }\n    StringBuilder out = new StringBuilder();\n    for (Map.Entry<String, Integer> e : counts.entrySet()) {\n        if (!out.isEmpty()) out.append(",");\n        out.append(e.getKey()).append("=").append(e.getValue());\n    }\n    return out.toString();\n}'
ex.method("write", "j3-l1.2-write-counts", "Word counts", ["o1", "o2"], ["J3.02"], ["IMPL"],
    "Write `counts(String text)`. Split the text into words (separated by spaces, ignoring upper/lower case), count each word, and return the counts as `word=count` pairs **sorted alphabetically** and joined with commas, e.g. `be=2,not=1,or=1,to=2` for `\"To be or not to be\"`. An empty text gives an empty string.",
    [("counts", [("text", "String")], "String")], {"counts": counts_str},
    [("counts", ["To be or not to be"]), ("counts", [""]), ("counts", ["a a a"])],
    [("counts", ["pear apple pear fig"]), ("counts", ["Hello hello HELLO"]), ("counts", ["zebra yak"]), ("counts", ["one"]), ("counts", ["b a c b a b"]), ("counts", ["  spaced   out  "])],
    'String counts(String text) {\n    return "";\n}',
    COUNTS_SOL,
    {"insertion-order": COUNTS_SOL.replace("new TreeMap<>()", "new LinkedHashMap<>()"),
     "case-sensitive": COUNTS_SOL.replace("text.toLowerCase().strip()", "text.strip()")},
    ("Use a TreeMap so the keys come out sorted, and merge(word, 1, Integer::sum) to count.", "counts.merge(w, 1, Integer::sum); then loop over entrySet()."),
    difficulty=3)
def top_word(text):
    c = Counter(words(text))
    if not c: return ""
    return sorted(c, key=lambda w: (-c[w], w))[0]
TOP_SOL = 'String topWord(String text) {\n    Map<String, Integer> counts = new TreeMap<>();\n    for (String w : text.toLowerCase().strip().split("\\\\s+")) {\n        if (!w.isEmpty()) {\n            counts.merge(w, 1, Integer::sum);\n        }\n    }\n    String best = "";\n    int bestCount = 0;\n    for (Map.Entry<String, Integer> e : counts.entrySet()) {\n        if (e.getValue() > bestCount) {\n            best = e.getKey();\n            bestCount = e.getValue();\n        }\n    }\n    return best;\n}'
ex.method("write", "j3-l1.2-write-topword", "The most common word", ["o2"], ["J3.02"], ["IMPL"],
    "Write `topWord(String text)`: the word that appears most often (ignoring upper/lower case). If two words tie, return the one that comes **first alphabetically**. An empty text gives an empty string.",
    [("topWord", [("text", "String")], "String")], {"topWord": top_word},
    [("topWord", ["to be or not to be"]), ("topWord", ["b a b a"]), ("topWord", [""])],
    [("topWord", ["one"]), ("topWord", ["x y z"]), ("topWord", ["The the THE cat"]), ("topWord", ["pear fig fig pear apple"]), ("topWord", ["  a  "]), ("topWord", ["z z y y x"])],
    'String topWord(String text) {\n    return "";\n}',
    TOP_SOL,
    {"ties-pick-last": TOP_SOL.replace("e.getValue() > bestCount", "e.getValue() >= bestCount"),
     "case-sensitive": TOP_SOL.replace("text.toLowerCase().strip()", "text.strip()")},
    ("Count in a TreeMap, then keep the best so far. Replace it only when a count is strictly greater.", "if (e.getValue() > bestCount) { best = e.getKey(); bestCount = e.getValue(); }"),
    difficulty=3)
MOST_BAD = 'int mostRepeated(List<String> items) {\n    Map<String, Integer> counts = new HashMap<>();\n    for (String item : items) {\n        counts.put(item, counts.get(item) + 1);\n    }\n    int best = 0;\n    for (int n : counts.values()) {\n        if (n > best) {\n            best = n;\n        }\n    }\n    return best;\n}'
MOST_OK = MOST_BAD.replace("counts.put(item, counts.get(item) + 1);", "counts.merge(item, 1, Integer::sum);")
ex.method("debug", "j3-l1.2-debug-null", "The first one always crashes", ["o3"], ["J3.02"], ["DEBUG"],
    "`mostRepeated` should return how many times the most repeated item occurs (0 for an empty list). It throws a `NullPointerException` on the first item. Find out why, and fix it.",
    [("mostRepeated", [("items", "List<String>")], "int")],
    {"mostRepeated": lambda items: max(Counter(items).values()) if items else 0},
    [("mostRepeated", [["a", "b", "a"]]), ("mostRepeated", [[]]), ("mostRepeated", [["x"]])],
    [("mostRepeated", [["a", "a", "a"]]), ("mostRepeated", [["p", "q", "r"]]), ("mostRepeated", [["k", "j", "k", "j", "k"]]), ("mostRepeated", [["z", "z"]]), ("mostRepeated", [["m", "n", "m", "o", "o", "o"]])],
    MOST_BAD, MOST_OK,
    {"counts-distinct": MOST_OK.replace("int best = 0;\n    for (int n : counts.values()) {\n        if (n > best) {\n            best = n;\n        }\n    }\n    return best;", "return counts.size();")},
    ("What does counts.get(item) return the first time an item is seen? What happens to null + 1?", "Use counts.merge(item, 1, Integer::sum), or getOrDefault(item, 0) + 1."),
    source_tests=[("no get(item) + 1", None, ["counts.get(item) + 1"])],
    difficulty=2)
ex.predict("j3-l1.2-predict-map", "put, merge and get", ["o1"], ["J3.02"],
    "Work out what this program prints. The map is a `TreeMap`, so its order is sorted by key.",
    '''void main() {
    Map<String, Integer> stock = new TreeMap<>();
    stock.put("apple", 3);
    stock.put("pear", 1);
    stock.put("apple", 5);
    stock.merge("pear", 2, Integer::sum);
    stock.putIfAbsent("fig", 9);
    stock.putIfAbsent("fig", 1);
    IO.println(stock);
    IO.println(stock.get("kiwi"));
    IO.println(stock.getOrDefault("kiwi", 0));
    IO.println(stock.containsKey("fig"));
    IO.println(stock.size());
}''', "{apple=5, fig=9, pear=3}\nnull\n0\ntrue\n3",
    ("put replaces an existing value. merge adds when the key exists. putIfAbsent only puts when the key is missing.", "apple becomes 5; pear is 1 + 2 = 3; fig is added once with 9. kiwi isn't there."),
    difficulty=3)
ex.explain("j3-l1.2-explain-keys", "A key that gets lost", ["o3"], ["J3.02"],
    "A developer uses their own mutable class `Point` (with `equals` but **no** `hashCode`) as a key in a `HashMap<Point, String>`, puts a value under `new Point(1, 2)`, and then `map.get(new Point(1, 2))` returns `null`. Explain (a) why the lookup fails, (b) what the fix is, and (c) what could go wrong if a key's fields are changed after it has been put in the map.",
    "A full answer says HashMap uses hashCode to find where to look, and without a matching hashCode the equal point hashes elsewhere so it isn't found; the fix is to override hashCode consistently with equals (or use a record); and if a key is mutated after insertion its hash code changes, so the map looks in the wrong place and can no longer find it.",
    {2: ("Explains that the map uses hashCode to find the entry and equal points without equal hash codes are looked up in the wrong place; fixes it with hashCode consistent with equals or a record; and says mutating a key changes its hash code so it can't be found.",
         ["HashMap uses the key's hashCode to decide where to look. Point has equals but no hashCode, so the new Point(1, 2) has a different hash code and the map looks in the wrong place. Fix: override hashCode from the same fields, or make Point a record. If you change a key's fields after putting it in, its hash code changes and the map can't find it any more.",
          "The lookup goes by hash code first, and the two equal points have different ones. Add a hashCode that matches equals. Mutating a key afterwards is also bad because the hash code changes and the entry gets lost."]),
     1: ("Explains one or two of the parts, for example the hashCode fix without saying why the lookup failed, or without the mutation point.",
         ["You need hashCode too.", "Make it a record."]),
     0: ("Incorrect, for example blames the map being empty or says equals should fix it.",
         ["equals is enough.", "HashMap can't hold objects."])})
reg({"j3-l1.2": ("Maps", ["J3.02"])},
    {"MC64": (["J3.02"], "Platform", "map.get(key) returns 0 for a missing key"),
     "MC65": (["J3.02"], "I30", "A HashMap iterates in the order keys were put"),
     "MC66": (["J3.02"], "I38", "A key object can be changed after it has been put in a HashMap")})

# ====================================================================== 3.1.3
Lesson("j3-l1.3", "Ordering and safe iteration", ["J3.03"], [
    ("o1", "Sort a list with a Comparator, and give a class a natural order with Comparable"),
    ("o2", "Remove items from a collection while looping without causing a ConcurrentModificationException"),
    ("o3", "Explain what an unmodifiable collection is, and why an API might return one"),
], ["j3-l1.2"], 45, ["I36", "I31", "I29", "R16"], r'''
## Before you start

You should know how to use lists and maps ([Lists and sets](j3-l1.1), [Maps](j3-l1.2)).

**Quick check.** What do `TreeSet` and `TreeMap` use to keep their contents sorted?

<details><summary>Show the answer</summary>

The natural ordering of the elements or keys, or a `Comparator` given when they're created.

</details>

## Explanation

### Natural order: `Comparable`

Some types know how to put themselves in order: numbers by value, strings alphabetically. They implement `Comparable`, whose one method `compareTo(other)` returns a **negative number** if this comes first, **zero** if they're equal in order, and a **positive number** if this comes later. You can give your own class a natural order:

```java
class Version implements Comparable<Version> {
    private final int major;
    private final int minor;

    Version(int major, int minor) { this.major = major; this.minor = minor; }

    @Override
    public int compareTo(Version other) {
        int byMajor = Integer.compare(major, other.major);
        return byMajor != 0 ? byMajor : Integer.compare(minor, other.minor);
    }
}
```

(`<Version>` says *compares against other `Version`s*; lesson 3.2.1 explains the angle brackets.) Now `Collections.sort(versions)`, `Collections.max(versions)` and a `TreeSet<Version>` all work. Use `Integer.compare`, rather than subtracting numbers, so that very large values can't overflow.

Compare **numbers as numbers**: as text, `"1.10"` sorts before `"1.9"`.

### Other orders: `Comparator`

A **`Comparator`** is a separate object that defines an order, so you can sort by something that isn't the natural order, or sort a type you can't change. The `Comparator` interface has helper methods for building one `[I36]`:

```java
List<String> words = new ArrayList<>(List.of("pear", "fig", "banana", "kiwi"));

words.sort(Comparator.comparing(String::length));                  // by length
words.sort(Comparator.comparing(String::length)
                     .thenComparing(Comparator.naturalOrder()));    // by length, ties alphabetical
words.sort(Comparator.comparing(String::length).reversed());        // longest first
```

`String::length` means *the length method of a String*. It's a method reference, which lesson 3.3.1 explains properly; for now, read `Comparator.comparing(String::length)` as "compare by length". `thenComparing` breaks ties, and `reversed()` flips the order. `list.sort(comparator)` sorts a list in place (it modifies the list).

`sort` is **stable** for lists: items that compare equal keep their original relative order. So if you sort by length only, two words of the same length stay in the order they had.

### Removing while looping

This looks fine and isn't:

```java
for (Integer v : copy) {
    if (v < 0) copy.remove(v);       // changes the list while the loop is using it
}
```

The enhanced `for` loop uses an iterator that notices if the list is **structurally modified** behind its back, and throws a `ConcurrentModificationException` `[I31]`. Not always: with `[1, -2, 3]` the removal happens just before the loop would end, and the loop happens to finish without noticing. With `[-1, 2, 3]` it throws. "Sometimes works" is what makes this bug nasty.

Safe ways to remove while processing:

```java
copy.removeIf(v -> v < 0);                 // the simplest: remove everything that matches

Iterator<Integer> it = copy.iterator();    // or use the iterator's own remove
while (it.hasNext()) {
    if (it.next() < 0) it.remove();
}
```

Or build a **new** list of what you want to keep. Removing by index in a counting loop avoids the exception, but skips the item that slides into the removed slot unless you adjust the index, so prefer the other ways.

`removeIf(v -> v < 0)` uses a lambda, an inline condition; lesson 3.3.1 covers lambdas, but you can already read it as "remove each `v` where `v < 0`".

### Unmodifiable collections

`List.of(...)` creates a list that **can't be changed**: adding, removing or replacing throws an `UnsupportedOperationException` `[I29]`. `Set.of` and `Map.of` are the same. `List.copyOf(other)` makes an unmodifiable copy.

Why return one from a method? So callers can read your data but can't change it (as with the defensive copies from lesson 2.2.2). Why is it *not* a copy by default? Some library code returns a **view**: an object that looks like a list but still reflects the original. Be clear in your own code which you're giving out.

`new ArrayList<>(List.of(1, 2, 3))` makes an ordinary changeable copy.

## Worked examples

### Example 1: sort by length, ties alphabetical

*Task: sort words by length, and alphabetically among words of the same length.*

**Step 1 — Primary key:** length. **Secondary key:** the word itself.

**Step 2 — Build the comparator,** and sort a copy:

```java
List<String> sortedByLength(List<String> words) {
    List<String> copy = new ArrayList<>(words);
    copy.sort(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()));
    return copy;
}
```

**Step 3 — Check.** `[pear, fig, kiwi, ax]` becomes `[ax, fig, kiwi, pear]`.

### Example 2: removing safely

*Task: drop the negative numbers from a list of numbers.*

**Step 1 — Don't remove inside a for-each.**

**Step 2 — Copy, then `removeIf`:**

```java
List<Integer> removeNegatives(List<Integer> values) {
    List<Integer> copy = new ArrayList<>(values);
    copy.removeIf(v -> v < 0);
    return copy;
}
```

**Step 3 — Check.** `[-1, 2, -3, 0]` becomes `[2, 0]`: zero isn't negative.

## Where this is used

- **Sorted output** is needed in every report and every list screen.
- **Cleaning data in place** (dropping expired items, filtering bad rows) is routine.
- **Immutable results** from APIs are standard practice in library design.

## Common mistakes

:::mistake{id=MC67}
**Removing from a list inside a for-each over that same list.** It throws `ConcurrentModificationException`, or sometimes silently misbehaves. Use `removeIf`, an iterator, or build a new list.
:::

:::mistake{id=MC68}
**Trying to modify a `List.of(...)`.** It's unmodifiable. Copy it into an `ArrayList` first if you need to change it.
:::

:::mistake{id=MC69}
**Comparing version numbers (or any numbers) as text.** `"1.10"` sorts before `"1.9"`. Compare the numeric parts.
:::

## Practice

::exercise{id=j3-l1.3-write-sort}

::exercise{id=j3-l1.3-write-comparable}

::exercise{id=j3-l1.3-debug-cme}

::exercise{id=j3-l1.3-explain-immutable}

## Further reading

- **`java.util.Comparator`** `[I36]` lists the factory methods for building comparators.
- **`java.util.ConcurrentModificationException`** `[I31]` and **`java.util.List`** `[I29]`.
- **McCauley et al. (2008)** `[R16]` on debugging: a bug that only sometimes shows up needs a deliberately chosen test case to reproduce.

## How you'll be assessed

- The **write** exercises check that you can sort with a comparator and give a class a natural order (*implementation*).
- The **debug** exercise checks that you can remove items while iterating safely (*debugging*).
- The **explain** exercise checks that you understand unmodifiable collections (*explanation*).
''' + FOOT)

ex = Exercises("j3-l1.3")
SORT_SOL = 'List<String> sortedByLength(List<String> words) {\n    List<String> copy = new ArrayList<>(words);\n    copy.sort(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()));\n    return copy;\n}'
ex.method("write", "j3-l1.3-write-sort", "Sort by length, then alphabetically", ["o1"], ["J3.03"], ["IMPL"],
    "Write `sortedByLength(List<String> words)`: return a **new** sorted list: shortest words first, and words of the same length in alphabetical order. Don't change the list you were given.",
    [("sortedByLength", [("words", "List<String>")], "List<String>")], {"sortedByLength": lambda ws: sorted(ws, key=lambda w: (len(w), w))},
    [("sortedByLength", [["pear", "fig", "kiwi", "ax"]]), ("sortedByLength", [[]]), ("sortedByLength", [["b", "a"]])],
    [("sortedByLength", [["banana", "apple", "cherry", "fig"]]), ("sortedByLength", [["zz", "aa", "m", "bb"]]), ("sortedByLength", [["one"]]), ("sortedByLength", [["dd", "cc", "bb", "aa"]]), ("sortedByLength", [["xyz", "ab", "abc", "a"]])],
    'List<String> sortedByLength(List<String> words) {\n    return new ArrayList<>(words);\n}',
    SORT_SOL,
    {"length-only": SORT_SOL.replace(".thenComparing(Comparator.naturalOrder())", ""),
     "alphabetical-only": SORT_SOL.replace("Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder())", "Comparator.naturalOrder()")},
    ("Use Comparator.comparing(String::length) for the first key, and thenComparing to break ties.", "copy.sort(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()));"),
    difficulty=3)
VER = 'class Version implements Comparable<Version> {\n    private final int major;\n    private final int minor;\n\n    Version(String text) {\n        String[] parts = text.split("\\\\.");\n        this.major = Integer.parseInt(parts[0]);\n        this.minor = Integer.parseInt(parts[1]);\n    }\n\n'
VER_END = '\n    @Override\n    public String toString() {\n        return major + "." + minor;\n    }\n}\n\nString newest(List<String> versions) {\n    List<Version> list = new ArrayList<>();\n    for (String v : versions) {\n        list.add(new Version(v));\n    }\n    return Collections.max(list).toString();\n}'
VER_OK = '    @Override\n    public int compareTo(Version other) {\n        int byMajor = Integer.compare(major, other.major);\n        return byMajor != 0 ? byMajor : Integer.compare(minor, other.minor);\n    }\n'
def newest(vs):
    return max(vs, key=lambda v: tuple(int(x) for x in v.split(".")))
ex.method("write", "j3-l1.3-write-comparable", "Versions in order", ["o1"], ["J3.03"], ["IMPL"],
    "`Version` should have a natural order: by major number, then by minor number, **as numbers** (so `1.10` is newer than `1.9`). Write its `compareTo`. `newest` uses `Collections.max`, which relies on it.",
    [("newest", [("versions", "List<String>")], "String")], {"newest": newest},
    [("newest", [["1.4", "1.10", "1.9"]]), ("newest", [["2.0", "1.99"]]), ("newest", [["3.1"]])],
    [("newest", [["1.9", "1.10"]]), ("newest", [["0.1", "0.2", "0.11"]]), ("newest", [["10.0", "9.9"]]), ("newest", [["1.0", "1.0"]]), ("newest", [["4.5", "4.5", "4.6", "3.9"]])],
    VER + '    @Override\n    public int compareTo(Version other) {\n        return 0;\n    }\n' + VER_END,
    VER + VER_OK + VER_END,
    {"compares-as-text": VER + '    @Override\n    public int compareTo(Version other) {\n        return toString().compareTo(other.toString());\n    }\n' + VER_END,
     "minor-first": VER + VER_OK.replace("Integer.compare(major, other.major)", "Integer.compare(minor, other.minor)").replace("Integer.compare(minor, other.minor);\n    }", "Integer.compare(major, other.major);\n    }") + VER_END},
    ("Compare the major numbers first; only if they're equal compare the minor numbers. Use Integer.compare.", "int byMajor = Integer.compare(major, other.major); return byMajor != 0 ? byMajor : Integer.compare(minor, other.minor);"),
    difficulty=3)
CME_BAD = 'List<Integer> removeNegatives(List<Integer> values) {\n    List<Integer> copy = new ArrayList<>(values);\n    for (Integer v : copy) {\n        if (v < 0) {\n            copy.remove(v);\n        }\n    }\n    return copy;\n}'
CME_OK = 'List<Integer> removeNegatives(List<Integer> values) {\n    List<Integer> copy = new ArrayList<>(values);\n    copy.removeIf(v -> v < 0);\n    return copy;\n}'
ex.method("debug", "j3-l1.3-debug-cme", "Removing while looping", ["o2"], ["J3.03"], ["DEBUG"],
    "`removeNegatives` should return the list without its negative numbers (zero stays). It throws a `ConcurrentModificationException` for some inputs, and appears to work for others. Find a failing input, explain to yourself why, and fix it **without** removing inside the for-each loop.",
    [("removeNegatives", [("values", "List<Integer>")], "List<Integer>")], {"removeNegatives": lambda vs: [v for v in vs if v >= 0]},
    [("removeNegatives", [[1, -2, 3]]), ("removeNegatives", [[-1, 2, 3]]), ("removeNegatives", [[]])],
    [("removeNegatives", [[-1, -2, 3]]), ("removeNegatives", [[0, -5, 0]]), ("removeNegatives", [[-1, -2, -3]]), ("removeNegatives", [[4, 5]]), ("removeNegatives", [[-9, 1, -8, 2, -7]])],
    CME_BAD, CME_OK,
    {"removes-zero-too": CME_OK.replace("v < 0", "v <= 0"),
     "index-loop-skips": 'List<Integer> removeNegatives(List<Integer> values) {\n    List<Integer> copy = new ArrayList<>(values);\n    for (int i = 0; i < copy.size(); i++) {\n        if (copy.get(i) < 0) {\n            copy.remove(i);\n        }\n    }\n    return copy;\n}'},
    ("The enhanced for loop notices when the list changes under it. What can you use instead?", "copy.removeIf(v -> v < 0); or build a new list of the values to keep."),
    source_tests=[("no remove inside the for-each", None, ["copy.remove(v)"])],
    difficulty=3)
ex.explain("j3-l1.3-explain-immutable", "Why return List.of?", ["o3"], ["J3.03"],
    "A method `List<String> roles()` returns `List.of(\"admin\", \"user\")`. A caller does `roles().add(\"guest\")`. (a) What happens, and why does `List.of` behave that way? (b) Give one reason an API author might return an unmodifiable list. (c) If the caller wants a list they can change, what should they do?",
    "A full answer says the call throws UnsupportedOperationException because List.of creates an unmodifiable list; an API returns one so callers can read but not change its internal data (protecting invariants, like a defensive copy); and the caller should copy it into a new ArrayList.",
    {2: ("Says the add throws UnsupportedOperationException because List.of is unmodifiable, gives a reason such as stopping callers changing the owner's data, and says to copy into new ArrayList<>(...).",
         ["It throws an UnsupportedOperationException, because List.of creates a list that can't be added to, removed from or replaced in. An author returns one so callers can read the data but not change it, which protects the class's own state. The caller can write new ArrayList<>(roles()) to get a list they can change.",
          "UnsupportedOperationException: List.of makes an unmodifiable list. It protects the owner's data from outside changes. If you need a changeable one, make a copy with new ArrayList<>(...)."]),
     1: ("Gets the exception or the reason or the copy, but not all three.",
         ["It throws an exception.", "Copy it first."]),
     0: ("Incorrect, for example says the guest is added, or that List.of lists are faster for no reason.",
         ["It adds guest.", "It silently ignores it."])})
reg({"j3-l1.3": ("Ordering and safe iteration", ["J3.03"])},
    {"MC67": (["J3.03"], "I31", "Removing from a list inside a for-each over it is fine"),
     "MC68": (["J3.03"], "I29", "A list made with List.of can be added to"),
     "MC69": (["J3.03"], "Platform", "Version numbers can be compared as text")})

# ====================================================================== 3.2.1
Lesson("j3-l2.1", "Generics", ["J3.04"], [
    ("o1", "Write a generic class with a type parameter, and replace duplicated classes with one"),
    ("o2", "Write a generic method with a bound such as T extends Comparable<T>"),
    ("o3", "Explain why List<int> isn't allowed, and what type erasure means"),
], ["j3-l1.3"], 45, ["I52", "R8"], r'''
## Before you start

You've been using generic types such as `List<String>` and `Map<String, Integer>`. This lesson is about writing your own.

**Quick check.** What does the `<String>` in `List<String>` do for you?

<details><summary>Show the answer</summary>

It tells the compiler that the list holds `String`s, so `add(5)` is an error and `get(0)` is already a `String`.

</details>

## Explanation

### The problem generics solve

Suppose you write a box that holds one value:

```java
class IntBox    { private int value;    /* ... */ }
class StringBox { private String value; /* ... */ }
```

The two classes are identical except for the type. Every new type means a new copy. The old fix, a box of `Object`, loses type safety: you'd have to cast on the way out, and the compiler can't stop you putting a number in a box of names.

A **generic class** declares a **type parameter**, a stand-in name for "whichever type the user picks":

```java
class Box<T> {
    private T value;

    Box(T value) { this.value = value; }
    T get() { return value; }
    void set(T value) { this.value = value; }
}
```

`T` is a name for the type (a single capital letter is the convention). When you use the class, you say which type:

```java
Box<Integer> count = new Box<>(5);
Box<String> name = new Box<>("Ada");
int n = count.get();          // already an Integer; no cast
name.set("Bo");
// name.set(42);              // compile error: 42 is not a String
```

The compiler checks the types everywhere, and writes the casts for you. `new Box<>(...)`, with empty angle brackets, lets the compiler work out the type argument (the *diamond*).

A class can have several type parameters:

```java
class Pair<A, B> {
    private final A first;
    private final B second;
    Pair(A first, B second) { this.first = first; this.second = second; }
    A first() { return first; }
    B second() { return second; }
    Pair<B, A> swap() { return new Pair<>(second, first); }
}
```

### Generic methods

A method can have its own type parameter, written before the return type:

```java
<T> List<T> repeat(T item, int times) {
    List<T> result = new ArrayList<>();
    for (int i = 0; i < times; i++) result.add(item);
    return result;
}
```

The compiler works out `T` from the arguments: `repeat("hi", 3)` gives a `List<String>`.

### Bounded types

Sometimes the method needs the type to **do** something. To find the biggest item in a list it must be able to compare two of them. Say so with a **bound**:

```java
<T extends Comparable<T>> T biggest(List<T> items) {
    T best = items.get(0);
    for (T item : items) {
        if (item.compareTo(best) > 0) {
            best = item;
        }
    }
    return best;
}
```

`T extends Comparable<T>` reads *T is any type that can be compared to its own kind*. (Here `extends` also covers interfaces.) `String` and `Integer` qualify; a class without `compareTo` doesn't, and the compiler says so. Inside the method you can call `compareTo` because the bound guarantees it.

### Why `List<int>` isn't allowed

A type argument must be a **reference type**: a class, interface or array, not a primitive `[I52]`. So you write `List<Integer>`, `Map<String, Double>`. Java converts between `int` and `Integer` automatically (*boxing* and *unboxing*), which is convenient but has two costs: each `Integer` is a separate object (more memory than an `int` in an `int[]`), and unboxing a `null` throws a `NullPointerException` (as in the map lesson).

### Type erasure

The compiler checks generic types, and then **erases** them: after compilation, a `List<String>` and a `List<Integer>` are both just a `List`, and `T` becomes its bound (or `Object`) `[I52]`. Consequences you'll meet:

- You can't ask at run time "is this a `List<String>`?" (`x instanceof List<String>` is an error); only "is it a `List`?".
- You can't write `new T()` or `new T[10]`, because at run time there's no `T`.
- Mixing generic and old *raw* types (a plain `List` with no argument) turns off the checking and gives compiler warnings. Treat those warnings as real problems.

### Wildcards (a first look)

A method that only **reads** a list of numbers can accept lists of any number type with a wildcard:

```java
double sum(List<? extends Number> numbers) { ... }
```

`List<? extends Number>` means *a list of some type that is a `Number`*. You can read from it but not add to it. You'll rarely need to write wildcards yet, but you'll see them in library signatures.

## Worked examples

### Example 1: replacing two classes with one

*Task: `IntBox` and `StringBox` are the same code with different types. Replace both.*

**Step 1 — Find what differs:** only the type of `value`.

**Step 2 — Make that a type parameter:** `class Box<T>`.

**Step 3 — Replace the two uses:** `Box<Integer>` and `Box<String>`.

**Step 4 — Delete the old classes.** One class now serves every type, and the compiler still checks them.

### Example 2: swapping a pair

*Task: `new Pair<>("a", 1).swap()` should be a `Pair<Integer, String>` holding `1` and `"a"`.*

**Step 1 — Type of the result:** the parameters swap places: `Pair<B, A>`.

**Step 2 — Build it from the fields in the opposite order:** `new Pair<>(second, first)`.

**Step 3 — Check.** `swap().first()` is `1`.

## Where this is used

- **Every collection and many APIs** are generic, so you'll read generic signatures constantly (`Map<K, V>`, `Optional<T>`, `Comparable<T>`).
- **Your own utilities** (a result wrapper, a cache, a pair) become reusable when generic.
- **Frameworks** use generics to give you typed results from untyped sources.

## Common mistakes

:::mistake{id=MC70}
**Trying to use a primitive as a type argument** (`List<int>`). Use the wrapper type (`List<Integer>`).
:::

:::mistake{id=MC71}
**Expecting generic types to exist at run time.** After erasure a `List<String>` is just a `List`, so you can't test for `List<String>` or create a `T`.
:::

## Practice

::exercise{id=j3-l2.1-write-pair}

::exercise{id=j3-l2.1-modify-box}

::exercise{id=j3-l2.1-write-biggest}

::exercise{id=j3-l2.1-explain-erasure}

## Further reading

- **The Java Language Specification, chapter 4** `[I52]` defines type arguments (§4.5.1) and type erasure (§4.6).
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** and **modify** exercises check that you can write generic classes and a bounded generic method (*implementation*).
- The **explain** exercise checks that you can say why primitives aren't allowed and what erasure means (*explanation*).
''' + FOOT)

ex = Exercises("j3-l2.1")
PAIR_SOL = 'class Pair<A, B> {\n    private final A first;\n    private final B second;\n\n    Pair(A first, B second) {\n        this.first = first;\n        this.second = second;\n    }\n\n    A first() {\n        return first;\n    }\n\n    B second() {\n        return second;\n    }\n\n    Pair<B, A> swap() {\n        return new Pair<>(second, first);\n    }\n}\n\n'
PAIR_DRV = 'String run(String a, int b) {\n    Pair<String, Integer> p = new Pair<>(a, b);\n    Pair<Integer, String> s = p.swap();\n    return s.first() + ":" + s.second();\n}'
ex.method("write", "j3-l2.1-write-pair", "A generic pair", ["o1"], ["J3.04"], ["IMPL"],
    "Finish the generic class `Pair<A, B>`: a constructor taking the two values, accessors `first()` and `second()`, and `swap()`, which returns a **new** `Pair<B, A>` with the two values in the opposite order.",
    [("run", [("a", "String"), ("b", "int")], "String")], {"run": lambda a, b: f"{b}:{a}"},
    [("run", ["x", 1]), ("run", ["", 0]), ("run", ["hello", -5])],
    [("run", ["a", 99]), ("run", ["pair", 7]), ("run", ["z", 1000]), ("run", ["q", 2]), ("run", ["long text here", 42])],
    'class Pair<A, B> {\n    Pair(A first, B second) {\n    }\n\n    A first() {\n        return null;\n    }\n\n    B second() {\n        return null;\n    }\n\n    Pair<B, A> swap() {\n        return new Pair<>(null, null);\n    }\n}\n\n' + PAIR_DRV,
    PAIR_SOL + PAIR_DRV,
    {"swap-returns-same-order": PAIR_SOL.replace("return new Pair<>(second, first);", "return new Pair<>(null, null);") + PAIR_DRV},
    ("Store the two values in fields. swap builds a Pair with the arguments in the other order.", "return new Pair<>(second, first);"),
    difficulty=3)
BOX_DRV = 'String run(int n, String s) {\n    Box<Integer> a = new Box<>(n);\n    Box<String> b = new Box<>(s);\n    a.set(a.get() + 1);\n    return a.get() + b.get();\n}'
BOX_SOL = 'class Box<T> {\n    private T value;\n\n    Box(T value) {\n        this.value = value;\n    }\n\n    T get() {\n        return value;\n    }\n\n    void set(T value) {\n        this.value = value;\n    }\n}\n\n'
ex.method("modify", "j3-l2.1-modify-box", "One Box instead of two", ["o1"], ["J3.04"], ["MOD"],
    "`IntBox` and `StringBox` are the same code with a different type. The driver `run` has already been changed to use a generic `Box<T>`. Replace both classes with one generic class `Box<T>` (a constructor taking the value, `get()` and `set(...)`), and delete the two old ones.",
    [("run", [("n", "int"), ("s", "String")], "String")], {"run": lambda n, s: f"{n + 1}{s}"},
    [("run", [1, "a"]), ("run", [0, ""]), ("run", [-3, "x"])],
    [("run", [10, "ten"]), ("run", [99, "!"]), ("run", [5, "five"]), ("run", [0, "zero"]), ("run", [-1, "neg"])],
    'class IntBox {\n    private int value;\n    IntBox(int value) { this.value = value; }\n    int get() { return value; }\n    void set(int value) { this.value = value; }\n}\n\nclass StringBox {\n    private String value;\n    StringBox(String value) { this.value = value; }\n    String get() { return value; }\n    void set(String value) { this.value = value; }\n}\n\n' + BOX_DRV,
    BOX_SOL + BOX_DRV,
    {"set-does-nothing": BOX_SOL.replace("this.value = value;\n    }\n}", "}\n}") + BOX_DRV},
    ("Make the field's type a type parameter T on the class: class Box<T>. Then get returns T and set takes T.", "class Box<T> { private T value; Box(T value) {...} T get() {...} void set(T value) {...} }"),
    source_tests=[("one generic class", ["class Box<T>"], ["class IntBox", "class StringBox"])],
    starter_compiles=False, difficulty=2)
BIG_DRV = '\n\nString run(List<String> words, List<Integer> numbers) {\n    return biggest(words) + "," + biggest(numbers);\n}'
BIG_SOL = '<T extends Comparable<T>> T biggest(List<T> items) {\n    T best = items.get(0);\n    for (T item : items) {\n        if (item.compareTo(best) > 0) {\n            best = item;\n        }\n    }\n    return best;\n}'
ex.method("write", "j3-l2.1-write-biggest", "The biggest of anything comparable", ["o2"], ["J3.04"], ["IMPL"],
    "Write the generic method `biggest(List<T> items)`: it returns the largest item, for **any** type that can be compared with its own kind (`T extends Comparable<T>`). The driver uses it on a list of strings and a list of numbers. The lists are never empty.",
    [("run", [("words", "List<String>"), ("numbers", "List<Integer>")], "String")], {"run": lambda w, n: f"{max(w)},{max(n)}"},
    [("run", [["pear", "apple", "fig"], [3, 9, 4]]), ("run", [["a"], [1]]), ("run", [["b", "c", "a"], [-5, -2, -9]])],
    [("run", [["x", "y"], [10, 20]]), ("run", [["zebra", "zoo"], [0, 0]]), ("run", [["m", "n", "o", "p"], [5, 4, 3, 2]]), ("run", [["only"], [100]]), ("run", [["Beta", "alpha"], [7, 7, 8]])],
    '<T> T biggest(List<T> items) {\n    return items.get(0);\n}' + BIG_DRV,
    BIG_SOL + BIG_DRV,
    {"smallest": BIG_SOL.replace("item.compareTo(best) > 0", "item.compareTo(best) < 0") + BIG_DRV},
    ("The method needs to compare items, so say the type can be compared: <T extends Comparable<T>>.", "if (item.compareTo(best) > 0) { best = item; }"),
    source_tests=[("the type is bounded", ["T extends Comparable<T>"], None)],
    difficulty=3)
ex.explain("j3-l2.1-explain-erasure", "Why no List<int>?", ["o3"], ["J3.04"],
    "A learner writes `List<int> scores = new ArrayList<>();` and gets a compile error. (a) Explain why Java doesn't allow it and what to write instead. (b) Name one cost of what you wrote instead. (c) In one or two sentences, explain what \"type erasure\" means, and give one thing it stops you doing.",
    "A full answer says type arguments must be reference types so primitives aren't allowed and you write List<Integer> using the wrapper type; a cost is boxing (separate Integer objects use more memory, or unboxing null throws NullPointerException); and type erasure means the compiler checks generic types and then removes them so at run time a List<String> is just a List, which stops you testing for List<String> with instanceof or creating a new T.",
    {2: ("Says type arguments must be reference types and the fix is List<Integer>; gives a cost of boxing; and explains that erasure removes generic type information after compilation, with a consequence such as no instanceof List<String> or no new T().",
         ["Type arguments have to be reference types, not primitives, so I'd write List<Integer>. A cost is boxing: every Integer is an object, so it uses more memory than int values and unboxing a null throws a NullPointerException. Type erasure means the compiler checks the generics and then removes them, so at run time a List<String> is just a List. That's why you can't test x instanceof List<String> or create a new T().",
          "List<int> is not allowed because a generic type argument must be a class or interface type; use List<Integer>. Boxing has a cost in memory and a null unboxing risk. Erasure means the generic types disappear at run time, so you can't ask what the element type of a list is."]),
     1: ("Gets two of the three parts right, for example the fix and erasure but not a cost.",
         ["Use List<Integer> instead.", "Erasure removes the generics."]),
     0: ("Incorrect, for example says generics are only a runtime feature, or that primitives are too slow to be used.",
         ["Generics don't exist in Java.", "Primitives can't be used with lists because they are too slow."])})
reg({"j3-l2.1": ("Generics", ["J3.04"])},
    {"MC70": (["J3.04"], "I52", "A primitive such as int can be used as a type argument"),
     "MC71": (["J3.04"], "I52", "Generic type arguments are still known at run time")})
print("3.1 and 3.2 written")
