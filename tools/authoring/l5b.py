import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-5"
from build import *
import outline, re, heapq
from collections import deque
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'
def jtrunc_div(a, b): return int(a / b)
def jhash(s):
    h = 0
    for ch in s: h = (31 * h + ord(ch)) & 0xFFFFFFFF
    return h - (1 << 32) if h >= (1 << 31) else h

# ====================================================================== 5.2.3
Lesson("j5-l2.3", "Stacks and queues", ["J5.05"], [
    ("o1", "Explain the difference between a stack (last in, first out) and a queue (first in, first out), and name the Deque methods for each"),
    ("o2", "Use a Deque to check balanced brackets and to evaluate a postfix expression"),
    ("o3", "Implement a fixed-capacity queue on a circular array"),
], ["j5-l2.2"], 50, ["I55", "R8"], r'''
## Before you start

You should know how arrays and linked lists differ ([Dynamic arrays](j5-l2.1), [Linked lists](j5-l2.2)), and how collections are declared by their interface ([Lists and sets](j3-l1.1)).

**Quick check.** What does the call stack in a stack trace show you?

<details><summary>Show the answer</summary>

The chain of method calls that were active, with the most recent call at the top.

</details>

## Explanation

### Two ways of waiting

A **stack** and a **queue** both hold items and hand them back later. They differ in *which* item comes back first.

- A **stack** is **last in, first out** (LIFO): a pile of plates. You add to the top and take from the top. Undo history, the call stack, and "go back" in a browser work this way.
- A **queue** is **first in, first out** (FIFO): a line at a shop. You join at the back and are served from the front. Print jobs, messages waiting to be processed, and breadth-first search (lesson 5.3.3) work this way.

| | Add | Remove | Look |
|---|---|---|---|
| **Stack** | `push` | `pop` | `peek` |
| **Queue** | `offer` (or `addLast`) | `poll` (or `pollFirst`) | `peek` |

### Java's tool: `Deque`

A **`Deque`** ("double-ended queue", pronounced "deck") supports insertion and removal at **both ends** `[I55]`. It can serve as either a stack or a queue. The Java documentation says to use it **in preference to the legacy `Stack` class**, and that when used as a stack, elements are pushed and popped at the **front** `[I55]`.

```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1);
stack.push(2);
stack.peek();      // 2   (the most recent)
stack.pop();       // 2
stack.pop();       // 1

Deque<Integer> queue = new ArrayDeque<>();
queue.offer(1);    // join at the back
queue.offer(2);
queue.poll();      // 1   (the one who has waited longest)
```

`ArrayDeque` is a resizable-array implementation with no capacity limit. It **prohibits `null`** elements. Most of its operations run in amortised constant time (but `contains` and `remove(Object)` are linear), and the documentation says it's likely to be faster than `Stack` as a stack and faster than `LinkedList` as a queue `[I55]`.

`pop` and `poll` differ when the structure is empty: `pop()` throws `NoSuchElementException`, while `poll()` returns `null`. Check `isEmpty()` first when empty is possible.

### Use 1: matching brackets

Is `"([]{})"` balanced, and `"(]"` not? Every closing bracket must match the **most recent unclosed** opener, which is exactly what a stack gives you:

1. Go through the characters. On an **opener** (`( [ {`), push it.
2. On a **closer**, the stack must not be empty, and its top must be the matching opener; pop it. Otherwise it's unbalanced.
3. At the end, the stack must be **empty**, or some opener was never closed.

```java
boolean balanced(String text) {
    Deque<Character> open = new ArrayDeque<>();
    for (char c : text.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') {
            open.push(c);
        } else if (c == ')' || c == ']' || c == '}') {
            if (open.isEmpty()) return false;
            char top = open.pop();
            if ((c == ')' && top != '(') || (c == ']' && top != '[') || (c == '}' && top != '{')) return false;
        }
    }
    return open.isEmpty();
}
```

### Use 2: postfix expressions

In **postfix** notation the operator comes after its operands: `3 4 +` means 3 + 4, and `3 4 + 2 *` means (3 + 4) × 2. No brackets are needed. A stack evaluates it: on a number, **push**; on an operator, **pop two numbers**, apply it, **push the result**.

For `-` and `/` the order matters: the number popped **second** is the left operand. For `7 2 -`, you pop 2 first and 7 second, and compute 7 − 2.

```java
int evalPostfix(String expr) {
    Deque<Integer> stack = new ArrayDeque<>();
    for (String token : expr.split(" ")) {
        switch (token) {
            case "+" -> stack.push(stack.pop() + stack.pop());
            case "*" -> stack.push(stack.pop() * stack.pop());
            case "-" -> { int right = stack.pop(); stack.push(stack.pop() - right); }
            case "/" -> { int right = stack.pop(); stack.push(stack.pop() / right); }
            default -> stack.push(Integer.parseInt(token));
        }
    }
    return stack.pop();
}
```

### Building a queue on a circular array

A queue on a plain array has a problem: removing from the front leaves a gap that moves along the array. The fix is a **circular buffer**: treat the array as a ring. Keep:

- `head`: the index of the front item;
- `size`: how many items are stored;
- the next free slot is `(head + size) % capacity`.

```java
class RingQueue {
    private final int[] items;
    private int head;
    private int size;

    RingQueue(int capacity) { items = new int[capacity]; }

    boolean offer(int value) {
        if (size == items.length) return false;              // full
        items[(head + size) % items.length] = value;         // wraps around
        size++;
        return true;
    }

    int poll() {
        if (size == 0) throw new NoSuchElementException();
        int value = items[head];
        head = (head + 1) % items.length;                    // wraps around
        size--;
        return value;
    }

    int size() { return size; }
}
```

The `%` is what makes the array a ring: after the last slot, index 0 comes next. Both operations are O(1), with no shifting and no growth.

## Worked examples

### Example 1: evaluating `5 1 2 + 4 * + 3 -`

| Token | Action | Stack (top on the right) |
|---|---|---|
| 5 | push | 5 |
| 1 | push | 5 1 |
| 2 | push | 5 1 2 |
| + | pop 2, 1; push 3 | 5 3 |
| 4 | push | 5 3 4 |
| * | pop 4, 3; push 12 | 5 12 |
| + | pop 12, 5; push 17 | 17 |
| 3 | push | 17 3 |
| - | pop 3, 17; push 17 − 3 | 14 |

The answer is `14`.

### Example 2: a ring that wraps

*Task: capacity 3. `offer 1, 2, 3`, `poll`, `offer 4`: where does 4 go?*

**Step 1 — After three offers:** `items = [1, 2, 3]`, `head = 0`, `size = 3`.

**Step 2 — `poll`:** returns 1, `head = 1`, `size = 2`.

**Step 3 — `offer 4`:** slot `(1 + 2) % 3 = 0`, so `items = [4, 2, 3]`. The new item reused the slot freed at the front.

## Where this is used

- **Parsers and compilers** use stacks to match brackets and evaluate expressions.
- **Undo/redo, navigation history and the call stack** are stacks.
- **Message queues, schedulers and print spoolers** are queues; a ring buffer is a standard fixed-size queue in drivers and networking code.

## Common mistakes

:::mistake{id=MC102}
**Using the old `Stack` class or a `LinkedList` for a stack or queue.** The documentation recommends `Deque`, and `ArrayDeque` is the usual implementation.
:::

:::mistake{id=MC103}
**Forgetting to check that the stack is empty at the end** of a bracket check, so `"(("` passes.
:::

:::mistake{id=MC104}
**Getting the operand order wrong for `-` and `/`.** The first value popped is the right-hand operand.
:::

## Practice

::exercise{id=j5-l2.3-write-balanced}

::exercise{id=j5-l2.3-write-postfix}

::exercise{id=j5-l2.3-write-ring}

::exercise{id=j5-l2.3-explain-uses}

## Further reading

- **`java.util.Deque` and `ArrayDeque`** `[I55]` document the stack and queue methods and the recommendation over `Stack`.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can use a `Deque` for two classic problems and build a circular queue (*implementation*).
- The **explain** exercise checks that you can say which structure fits a task (*explanation*).
''' + FOOT)

ex = Exercises("j5-l2.3")
def balanced(t):
    st = []
    pair = {')': '(', ']': '[', '}': '{'}
    for c in t:
        if c in '([{': st.append(c)
        elif c in ')]}':
            if not st or st.pop() != pair[c]: return False
    return not st
BAL_SOL = 'boolean balanced(String text) {\n    Deque<Character> open = new ArrayDeque<>();\n    for (char c : text.toCharArray()) {\n        if (c == \'(\' || c == \'[\' || c == \'{\') {\n            open.push(c);\n        } else if (c == \')\' || c == \']\' || c == \'}\') {\n            if (open.isEmpty()) {\n                return false;\n            }\n            char top = open.pop();\n            if ((c == \')\' && top != \'(\') || (c == \']\' && top != \'[\') || (c == \'}\' && top != \'{\')) {\n                return false;\n            }\n        }\n    }\n    return open.isEmpty();\n}'
ex.method("write", "j5-l2.3-write-balanced", "Matching brackets", ["o2"], ["J5.05"], ["IMPL"],
    "Write `balanced(String text)`: `true` if every `(`, `[` and `{` is closed by the right kind of bracket in the right order, ignoring all other characters. `\"([]{})\"` and `\"a(b)c\"` are balanced; `\"(]\"`, `\"((\"` and `\"][\"` are not. Use a `Deque` as a stack.",
    [("balanced", [("text", "String")], "boolean")], {"balanced": balanced},
    [("balanced", ["([]{})"]), ("balanced", ["(]"]), ("balanced", [""])],
    [("balanced", ["(("]), ("balanced", ["]["]), ("balanced", ["a(b)c"]), ("balanced", ["{[()]}"]), ("balanced", ["{[(])}"]), ("balanced", [")"]), ("balanced", ["no brackets at all"])],
    'boolean balanced(String text) {\n    return true;\n}',
    BAL_SOL,
    {"ignores-bracket-kind": 'boolean balanced(String text) {\n    int depth = 0;\n    for (char c : text.toCharArray()) {\n        if (c == \'(\' || c == \'[\' || c == \'{\') depth++;\n        else if (c == \')\' || c == \']\' || c == \'}\') {\n            depth--;\n            if (depth < 0) return false;\n        }\n    }\n    return depth == 0;\n}',
     "forgets-leftover-openers": BAL_SOL.replace("return open.isEmpty();\n}", "return true;\n}")},
    ("Push openers. On a closer, the stack must be non-empty and its top must match. At the end, nothing should be left open.", "open.push(c); ... char top = open.pop(); ... return open.isEmpty();"),
    source_tests=[("uses a Deque", ["Deque"], None)],
    difficulty=3)
def postfix(expr):
    st = []
    for tok in expr.split(" "):
        if tok in "+-*/" and len(tok) == 1:
            b = st.pop(); a = st.pop()
            st.append(a + b if tok == "+" else a - b if tok == "-" else a * b if tok == "*" else jtrunc_div(a, b))
        else: st.append(int(tok))
    return st.pop()
PF_SOL = 'int evalPostfix(String expr) {\n    Deque<Integer> stack = new ArrayDeque<>();\n    for (String token : expr.split(" ")) {\n        switch (token) {\n            case "+" -> stack.push(stack.pop() + stack.pop());\n            case "*" -> stack.push(stack.pop() * stack.pop());\n            case "-" -> {\n                int right = stack.pop();\n                stack.push(stack.pop() - right);\n            }\n            case "/" -> {\n                int right = stack.pop();\n                stack.push(stack.pop() / right);\n            }\n            default -> stack.push(Integer.parseInt(token));\n        }\n    }\n    return stack.pop();\n}'
ex.method("write", "j5-l2.3-write-postfix", "Evaluate postfix", ["o2"], ["J5.05"], ["IMPL"],
    "Write `evalPostfix(String expr)`: evaluate a postfix expression whose tokens are whole numbers (possibly negative, like `-3`) and the operators `+ - * /`, separated by single spaces. `3 4 + 2 *` is `14`. Division is whole-number division, as in Java. The expression is always valid.",
    [("evalPostfix", [("expr", "String")], "int")], {"evalPostfix": postfix},
    [("evalPostfix", ["3 4 + 2 *"]), ("evalPostfix", ["7 2 -"]), ("evalPostfix", ["42"])],
    [("evalPostfix", ["5 1 2 + 4 * + 3 -"]), ("evalPostfix", ["10 2 /"]), ("evalPostfix", ["2 3 -"]), ("evalPostfix", ["9 -3 /"]), ("evalPostfix", ["7 2 /"]), ("evalPostfix", ["-7 2 /"]), ("evalPostfix", ["1 2 3 * +"])],
    'int evalPostfix(String expr) {\n    return 0;\n}',
    PF_SOL,
    {"operands-reversed": PF_SOL.replace("stack.push(stack.pop() - right);", "stack.push(right - stack.pop());"),
     "treats-minus-as-number": PF_SOL.replace('default -> stack.push(Integer.parseInt(token));', 'default -> stack.push(token.length() > 1 ? -Math.abs(Integer.parseInt(token)) : Integer.parseInt(token));')},
    ("On a number, push it. On an operator, pop the right operand first, then the left, apply, and push the result.", "int right = stack.pop(); stack.push(stack.pop() - right);"),
    source_tests=[("uses a Deque", ["Deque"], None)],
    difficulty=3)
RING_DRV = '\n\nString run(int capacity, String[] ops) {\n    RingQueue q = new RingQueue(capacity);\n    StringBuilder out = new StringBuilder();\n    for (String op : ops) {\n        if (op.startsWith("offer:")) {\n            out.append(q.offer(Integer.parseInt(op.substring(6))) ? "T" : "F");\n        } else {\n            try {\n                out.append(q.poll());\n            } catch (NoSuchElementException e) {\n                out.append("E");\n            }\n        }\n        out.append(" ");\n    }\n    return out + "size=" + q.size();\n}'
RING_SOL = 'class RingQueue {\n    private final int[] items;\n    private int head;\n    private int size;\n\n    RingQueue(int capacity) {\n        items = new int[capacity];\n    }\n\n    boolean offer(int value) {\n        if (size == items.length) {\n            return false;\n        }\n        items[(head + size) % items.length] = value;\n        size++;\n        return true;\n    }\n\n    int poll() {\n        if (size == 0) {\n            throw new NoSuchElementException();\n        }\n        int value = items[head];\n        head = (head + 1) % items.length;\n        size--;\n        return value;\n    }\n\n    int size() {\n        return size;\n    }\n}'
def ring(cap, ops):
    q, out = deque(), []
    for op in ops:
        if op.startswith("offer:"):
            if len(q) == cap: out.append("F")
            else: q.append(int(op[6:])); out.append("T")
        else: out.append(str(q.popleft()) if q else "E")
    return "".join(o + " " for o in out) + f"size={len(q)}"
ex.method("write", "j5-l2.3-write-ring", "A circular queue", ["o3"], ["J5.05"], ["IMPL"],
    "Write `RingQueue`: a queue of `int`s with a **fixed capacity**, built on an `int[]` used as a ring. `offer(int)` returns `false` if the queue is full, otherwise adds at the back and returns `true`. `poll()` removes and returns the front item, and throws `NoSuchElementException` if it's empty. `size()` says how many items are stored. No shifting: use a head index and `%`. The driver prints `T`/`F` for offers, the value or `E` for polls, then the final size.",
    [("run", [("capacity", "int"), ("ops", "String[]")], "String")], {"run": ring},
    [("run", [3, ["offer:1", "offer:2", "poll"]]), ("run", [2, ["poll"]]), ("run", [2, ["offer:1", "offer:2", "offer:3"]])],
    [("run", [3, ["offer:1", "offer:2", "offer:3", "poll", "offer:4", "poll", "poll", "poll", "poll"]]), ("run", [1, ["offer:5", "offer:6", "poll", "offer:7", "poll"]]), ("run", [4, ["offer:1", "poll", "offer:2", "poll", "offer:3", "poll", "offer:4", "poll", "offer:5", "poll"]]), ("run", [2, []]), ("run", [3, ["offer:1", "offer:2", "poll", "poll", "offer:3", "offer:4", "offer:5", "offer:6"]])],
    'class RingQueue {\n    RingQueue(int capacity) {\n    }\n\n    boolean offer(int value) {\n        return false;\n    }\n\n    int poll() {\n        return 0;\n    }\n\n    int size() {\n        return 0;\n    }\n}' + RING_DRV,
    RING_SOL + RING_DRV,
    {"no-wraparound": RING_SOL.replace("items[(head + size) % items.length] = value;", "if (head + size >= items.length) return false;\n        items[head + size] = value;"),
     "poll-does-not-wrap": RING_SOL.replace("head = (head + 1) % items.length;", "head = head + 1;")},
    ("Keep a head index and a size. The next free slot is (head + size) % capacity. After polling, move head forward with % capacity.", "items[(head + size) % items.length] = value;   head = (head + 1) % items.length;"),
    source_tests=[("built on an int array", ["int[]"], ["new ArrayDeque", "new LinkedList", "new ArrayList"])],
    difficulty=4)
ex.explain("j5-l2.3-explain-uses", "Stack or queue?", ["o1"], ["J5.05"],
    "For each, say whether you'd use a **stack** or a **queue**, and why: (a) the undo history in a text editor; (b) customers waiting to be served in the order they arrived; (c) checking that the brackets in a formula match. Then (d) say what you would declare and create in Java for either one, and why not the old `Stack` class.",
    "A full answer chooses a stack for (a) (the most recent change is undone first, last in first out), a queue for (b) (first come first served, first in first out), and a stack for (c) (a closer must match the most recent opener); and for (d) a Deque created as an ArrayDeque, because the documentation recommends Deque over the legacy Stack class and ArrayDeque is likely to be faster.",
    {2: ("Chooses stack for (a), queue for (b), stack for (c) with the LIFO or FIFO reason, and says Deque implemented by ArrayDeque, preferred over the legacy Stack class.",
         ["(a) A stack, because the most recent change is undone first (last in, first out). (b) A queue: first come, first served. (c) A stack, since each closing bracket has to match the most recent opening one. In Java I'd use a Deque created as new ArrayDeque<>(), because the documentation recommends it instead of the legacy Stack class.",
          "Stack for undo (LIFO), queue for the customers (FIFO), stack for brackets (match the latest opener). I'd declare Deque<T> and create an ArrayDeque, which is recommended over Stack and is likely faster."]),
     1: ("Chooses the structures correctly without reasons, or gets the Java part but not the choices.",
         ["(a) stack (b) queue (c) stack.", "Use ArrayDeque."]),
     0: ("Incorrect, for example reverses stack and queue, or says to use the Stack class.",
         ["(a) queue (b) stack.", "Use the Stack class."])})
reg({"j5-l2.3": ("Stacks and queues", ["J5.05"])},
    {"MC102": (["J5.05"], "I55", "Stack and LinkedList are the right classes for a stack and a queue"),
     "MC103": (["J5.05"], "Platform", "A bracket check is finished when the last character has been read, even if openers remain"),
     "MC104": (["J5.05"], "Platform", "In postfix, the first value popped is the left operand of - and /")})

# ====================================================================== 5.2.4
Lesson("j5-l2.4", "Hash tables", ["J5.06"], [
    ("o1", "Implement a hash table with chaining that handles collisions and resizes as it fills"),
    ("o2", "Explain what a collision is, and why equal keys must have equal hash codes"),
    ("o3", "Find and fix a bug where keys with the same hash code are treated as the same key"),
], ["j5-l2.3", "j3-l1.2"], 55, ["I59", "I30", "I38", "R8"], r'''
## Before you start

You should know how maps are used ([Maps](j3-l1.2)), the `equals` and `hashCode` contract ([static, toString and equals](j2-l1.4)), and how linked chains work ([Linked lists](j5-l2.2)).

**Quick check.** If two objects are equal by `equals`, what must be true of their `hashCode`s?

<details><summary>Show the answer</summary>

They must be the same `[I38]`.

</details>

## Explanation

### The idea: turn the key into an array index

Looking up a key in a list means scanning, O(n). A **hash table** gets to the right place almost directly. It keeps an array of **buckets**, and uses the key's **hash code** to choose a bucket:

```
index = Math.floorMod(key.hashCode(), buckets.length)
```

`hashCode()` gives an `int` (possibly negative or huge), and `floorMod` folds it into `0..buckets.length-1` (the plain `%` can give a negative result for a negative hash). To store or find a key, compute its bucket and look only there. That's why `HashMap`'s `get` and `put` are constant time, **provided the hash function spreads the keys among the buckets** `[I59]`.

### Collisions

Different keys can land in the same bucket: that's a **collision**. Two ways to get one:

- **Different hash codes, same index**: with 8 buckets, hash codes 5 and 13 both give index 5.
- **The same hash code**: unequal strings can share one. `"Aa"` and `"BB"` both have hash code 2112, and so do `"AaAa"`, `"AaBB"`, `"BBAa"` and `"BBBB"`.

Collisions are unavoidable, so a hash table needs a plan. The simplest is **chaining**: each bucket holds a small linked chain of entries. To find a key, go to its bucket and walk the chain, comparing keys with **`equals`**.

```
buckets:  0: ─▶ [Aa=1] ─▶ [BB=2]
          1: (empty)
          2: ─▶ [pear=5]
```

### The key point: `equals`, not the hash

Once you're in a bucket, you must decide which entry is **your** key. Comparing hash codes isn't enough: `"Aa"` and `"BB"` have the same hash code but are different keys. The hash only narrows the search; **`equals` decides.** And since the bucket is chosen from the hash, equal keys must give the same hash `[I38]`, or you'd look in the wrong bucket and miss the entry. That's the whole reason for the `equals`/`hashCode` contract.

### Writing it

```java
class StringIntMap {
    private static class Entry {
        final String key;
        int value;
        Entry next;
        Entry(String key, int value, Entry next) { this.key = key; this.value = value; this.next = next; }
    }

    private Entry[] buckets = new Entry[8];
    private int size;

    private int indexFor(String key, int capacity) {
        return Math.floorMod(key.hashCode(), capacity);
    }

    void put(String key, int value) {
        int i = indexFor(key, buckets.length);
        for (Entry e = buckets[i]; e != null; e = e.next) {
            if (e.key.equals(key)) {          // equals decides
                e.value = value;              // replace
                return;
            }
        }
        buckets[i] = new Entry(key, value, buckets[i]);   // add at the front of the chain
        size++;
        if (size > buckets.length * 3 / 4) {
            resize();
        }
    }
}
```

`get` walks the same chain and returns the value (or a fallback); `remove` walks the chain and unlinks the entry, as in the linked-list lesson.

### Resizing

As entries pile up, chains get long and lookups slow down. The **load factor** is entries divided by buckets, and `HashMap` has both an initial capacity and a load factor as tuning parameters `[I59]`. When the table is too full (here, more than 75% of the buckets' count), **double the bucket array and re-insert every entry**:

```java
private void resize() {
    Entry[] old = buckets;
    buckets = new Entry[old.length * 2];
    for (Entry head : old) {
        for (Entry e = head; e != null; e = e.next) {
            int i = indexFor(e.key, buckets.length);
            buckets[i] = new Entry(e.key, e.value, buckets[i]);
        }
    }
}
```

You must **recompute every index**: the index depends on the array's length, which just changed. Copying chains across unchanged would put entries in the wrong buckets. Doubling gives amortised constant cost, just as for the dynamic array.

### When it goes wrong

- **A bad `hashCode`** (say, always 42) puts every key in one bucket: one long chain, O(n) lookups. The documentation warns that many keys with the same hash code slow a hash table `[I30]`.
- **Mutating a key** after inserting it changes its hash code, so it can't be found (lesson 3.1.2).
- **Order is unspecified.** The position of an entry depends on hash codes and the table size, which is why `HashMap` makes no promise about iteration order `[I30]`.

## Worked examples

### Example 1: where do keys go?

*Task: with 8 buckets, which bucket do `"Aa"` and `"BB"` use?*

**Step 1 — Their hash code** is 2112 for both.

**Step 2 — `Math.floorMod(2112, 8)`:** 2112 = 264 × 8, so the remainder is 0.

**Step 3 — Both go in bucket 0:** a collision from equal hash codes. The chain holds both, told apart by `equals`.

### Example 2: the bug that compares hashes

*Task: `get("BB")` returns the value stored under `"Aa"`. Why?*

**Step 1 — Look at the comparison in the chain walk.** It reads `e.key.hashCode() == key.hashCode()`.

**Step 2 — For `"Aa"` and `"BB"` that's true,** so the first entry in the chain is returned.

**Step 3 — Fix:** compare keys with `e.key.equals(key)`.

## Predict, then run

::exercise{id=j5-l2.4-predict-buckets}

## Where this is used

- **`HashMap`, `HashSet` and `Collectors.groupingBy`** all rest on this structure.
- **Caches, indexes and deduplication** depend on its constant-time lookup.
- **Security:** attackers can deliberately cause hash collisions to slow a service down, so real libraries defend against long chains.

## Common mistakes

:::mistake{id=MC105}
**Treating equal hash codes as equal keys.** The hash only chooses a bucket. Use `equals` to compare keys within it.
:::

:::mistake{id=MC106}
**Not recomputing bucket indexes when resizing.** The index depends on the array length, so every entry must be re-inserted.
:::

:::mistake{id=MC107}
**Using `%` on a hash code.** A negative hash gives a negative result. Use `Math.floorMod`.
:::

## Practice

::exercise{id=j5-l2.4-write-map}

::exercise{id=j5-l2.4-debug-compare}

::exercise{id=j5-l2.4-explain-hash}

## Further reading

- **`java.util.HashMap`** `[I59]` `[I30]` documents the constant-time claim, capacity and load factor, and the unspecified order.
- **`java.lang.Object`** `[I38]` gives the `equals` and `hashCode` contract.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercise checks that you can build a chained, resizing hash table (*implementation*).
- The **predict** exercise checks that you can compute bucket indexes (*identifying mistakes*).
- The **debug** exercise checks that you can fix a table that compares hashes instead of keys (*debugging*).
- The **explain** exercise checks that you can say why `equals` and `hashCode` must agree (*explanation*).
''' + FOOT)

ex = Exercises("j5-l2.4")
HM_DRV = '\n\nString run(String[] ops) {\n    StringIntMap map = new StringIntMap();\n    StringBuilder out = new StringBuilder();\n    for (String op : ops) {\n        if (op.startsWith("put:")) {\n            String[] kv = op.substring(4).split("=");\n            map.put(kv[0], Integer.parseInt(kv[1]));\n        } else if (op.startsWith("get:")) {\n            out.append(map.getOrDefault(op.substring(4), -1)).append(" ");\n        } else if (op.startsWith("remove:")) {\n            out.append(map.remove(op.substring(7)) ? "T" : "F").append(" ");\n        }\n    }\n    return out + "size=" + map.size();\n}'
HM_SOL = 'class StringIntMap {\n    private static class Entry {\n        final String key;\n        int value;\n        Entry next;\n\n        Entry(String key, int value, Entry next) {\n            this.key = key;\n            this.value = value;\n            this.next = next;\n        }\n    }\n\n    private Entry[] buckets = new Entry[8];\n    private int size;\n\n    private int indexFor(String key, int capacity) {\n        return Math.floorMod(key.hashCode(), capacity);\n    }\n\n    void put(String key, int value) {\n        int i = indexFor(key, buckets.length);\n        for (Entry e = buckets[i]; e != null; e = e.next) {\n            if (e.key.equals(key)) {\n                e.value = value;\n                return;\n            }\n        }\n        buckets[i] = new Entry(key, value, buckets[i]);\n        size++;\n        if (size > buckets.length * 3 / 4) {\n            resize();\n        }\n    }\n\n    int getOrDefault(String key, int fallback) {\n        for (Entry e = buckets[indexFor(key, buckets.length)]; e != null; e = e.next) {\n            if (e.key.equals(key)) {\n                return e.value;\n            }\n        }\n        return fallback;\n    }\n\n    boolean remove(String key) {\n        int i = indexFor(key, buckets.length);\n        Entry previous = null;\n        for (Entry e = buckets[i]; e != null; e = e.next) {\n            if (e.key.equals(key)) {\n                if (previous == null) {\n                    buckets[i] = e.next;\n                } else {\n                    previous.next = e.next;\n                }\n                size--;\n                return true;\n            }\n            previous = e;\n        }\n        return false;\n    }\n\n    int size() {\n        return size;\n    }\n\n    private void resize() {\n        Entry[] old = buckets;\n        buckets = new Entry[old.length * 2];\n        for (Entry head : old) {\n            for (Entry e = head; e != null; e = e.next) {\n                int i = indexFor(e.key, buckets.length);\n                buckets[i] = new Entry(e.key, e.value, buckets[i]);\n            }\n        }\n    }\n}'
def hm_run(ops):
    d, out = {}, []
    for op in ops:
        if op.startswith("put:"):
            k, v = op[4:].split("="); d[k] = int(v)
        elif op.startswith("get:"): out.append(str(d.get(op[4:], -1)) + " ")
        elif op.startswith("remove:"):
            k = op[7:]; out.append(("T" if k in d else "F") + " "); d.pop(k, None)
    return "".join(out) + f"size={len(d)}"
many = [f"put:k{i}={i}" for i in range(60)] + [f"get:k{i}" for i in (0, 17, 59, 60)]
many_rm = [f"put:k{i}={i}" for i in range(40)] + [f"remove:k{i}" for i in range(0, 40, 3)] + ["get:k3", "get:k4"]
COLL = ["put:Aa=1", "put:BB=2", "get:Aa", "get:BB", "put:AaAa=3", "put:BBBB=4", "get:AaAa", "get:BBBB", "get:AaBB"]
HM_V = [("run", [["put:a=1", "put:b=2", "get:a", "get:z"]]), ("run", [COLL]), ("run", [[]])]
HM_H = [("run", [["put:a=1", "put:a=9", "get:a"]]), ("run", [many]), ("run", [many_rm]), ("run", [["put:Aa=1", "put:BB=2", "remove:Aa", "get:BB", "get:Aa", "remove:Aa"]]), ("run", [["remove:x", "get:x"]]), ("run", [["put:AaBB=5", "put:BBAa=6", "put:AaAa=7", "remove:BBAa", "get:AaBB", "get:AaAa", "get:BBAa"]])]
ex.method("write", "j5-l2.4-write-map", "A hash table from scratch", ["o1", "o2"], ["J5.06"], ["IMPL"],
    "Write `StringIntMap`, a hash table from `String` to `int` using **chaining** (an array of buckets, each a chain of entries) and **no library map**. Start with 8 buckets; choose a bucket with `Math.floorMod(key.hashCode(), buckets.length)`; compare keys with `equals`; **double** the buckets and re-insert everything when `size` goes above three quarters of the bucket count. It needs `put` (replacing an existing key), `getOrDefault(key, fallback)`, `remove(key)` (returns whether it was there) and `size()`. Keys such as `\"Aa\"` and `\"BB\"` share a hash code, so your chaining has to work.",
    [("run", [("ops", "String[]")], "String")], {"run": hm_run}, HM_V, HM_H,
    'class StringIntMap {\n    void put(String key, int value) {\n    }\n\n    int getOrDefault(String key, int fallback) {\n        return fallback;\n    }\n\n    boolean remove(String key) {\n        return false;\n    }\n\n    int size() {\n        return 0;\n    }\n}' + HM_DRV,
    HM_SOL + HM_DRV,
    {"one-entry-per-bucket": HM_SOL.replace("        buckets[i] = new Entry(key, value, buckets[i]);\n        size++;\n        if (size > buckets.length * 3 / 4) {\n            resize();\n        }", "        buckets[i] = new Entry(key, value, null);\n        size++;"),
     "resize-copies-chains-unchanged": HM_SOL.replace("                int i = indexFor(e.key, buckets.length);\n                buckets[i] = new Entry(e.key, e.value, buckets[i]);", "                int i = indexFor(e.key, old.length) % buckets.length;\n                buckets[i] = new Entry(e.key, e.value, buckets[i]);").replace("Math.floorMod(key.hashCode(), capacity)", "Math.abs(key.hashCode() % capacity)")},
    ("Buckets are an Entry[] of chains. put: find the key in its chain with equals, else add a new entry and maybe resize. resize: a bigger array, and re-insert every entry using its new index.", "int i = Math.floorMod(key.hashCode(), buckets.length); for (Entry e = buckets[i]; e != null; e = e.next) if (e.key.equals(key)) ..."),
    source_tests=[("no library map", None, ["new HashMap", "new TreeMap", "new LinkedHashMap", "Hashtable"])],
    difficulty=5)
HM_BAD = HM_SOL.replace("            if (e.key.equals(key)) {\n                return e.value;\n            }", "            if (e.key.hashCode() == key.hashCode()) {\n                return e.value;\n            }").replace("            if (e.key.equals(key)) {\n                if (previous == null) {", "            if (e.key.hashCode() == key.hashCode()) {\n                if (previous == null) {")
ex.method("debug", "j5-l2.4-debug-compare", "Same hash, different key", ["o3"], ["J5.06"], ["DEBUG"],
    "This table works until two different keys share a hash code: `get(\"BB\")` returns the value stored under `\"Aa\"`, and `remove` can delete the wrong entry. Find the faulty comparison (there are two copies of it) and fix them.",
    [("run", [("ops", "String[]")], "String")], {"run": hm_run}, HM_V, HM_H,
    HM_BAD + HM_DRV, HM_SOL + HM_DRV,
    {"fixes-get-only": HM_SOL.replace("            if (e.key.equals(key)) {\n                if (previous == null) {", "            if (e.key.hashCode() == key.hashCode()) {\n                if (previous == null) {")},
    ("Which comparison tells you the entries are the same key: equal hash codes, or equal keys?", "Replace e.key.hashCode() == key.hashCode() with e.key.equals(key) in get and in remove."),
    difficulty=3)
def bucket_lines(keys, cap):
    out = []
    for k in keys:
        out.append(f"{k} {jhash(k)} {(jhash(k) % cap)}")
    return out
BK_KEYS = ["Aa", "BB", "pear", "fig", "apple"]
BK_OUT = "\n".join(bucket_lines(BK_KEYS, 8) + [f"{k} {(jhash(k) % 16)}" for k in BK_KEYS[:3]])
ex.predict("j5-l2.4-predict-buckets", "Which bucket?", ["o2"], ["J5.06"],
    "`String.hashCode` is a fixed formula, so you can compute these by hand or by careful reasoning about collisions. Work out what this program prints (for each key: the key, its hash code, and its bucket among 8). Then it prints the bucket among 16 for the first three keys.",
    '''void main() {
    String[] keys = {"Aa", "BB", "pear", "fig", "apple"};
    for (String key : keys) {
        IO.println(key + " " + key.hashCode() + " " + Math.floorMod(key.hashCode(), 8));
    }
    for (int i = 0; i < 3; i++) {
        IO.println(keys[i] + " " + Math.floorMod(keys[i].hashCode(), 16));
    }
}''', BK_OUT,
    ("The hash code of a String is s[0]*31^(n-1) + ... + s[n-1]. \"Aa\" is 65*31 + 97, and \"BB\" is 66*31 + 66.", "Aa and BB both give 2112, so they share a bucket. floorMod by 8 keeps the last three bits of the hash code."),
    difficulty=4)
ex.explain("j5-l2.4-explain-hash", "Why does hashCode matter?", ["o2"], ["J5.06"],
    "(a) What is a **collision** in a hash table, and give one example in Java? (b) Within a bucket, why must a lookup compare keys with `equals` and not just their hash codes? (c) Why must two keys that are `equals` have the same `hashCode`? (d) Why does the iteration order of a `HashMap` carry no guarantee?",
    "A full answer says a collision is two keys going to the same bucket (for example \"Aa\" and \"BB\", which have the same hash code 2112); that different keys can share a hash code so only equals can tell them apart; that the bucket is chosen from the hash code so equal keys with different hash codes would be looked for in the wrong bucket and missed; and that entry positions depend on hash codes and table size, so the order isn't defined.",
    {2: ("Defines a collision with a valid example, says only equals can distinguish keys that share a hash code, says equal keys with different hash codes would be searched for in the wrong bucket, and says iteration order depends on hash codes and table size so is unspecified.",
         ["A collision is two different keys ending up in the same bucket, like \"Aa\" and \"BB\" which both have hash code 2112. The hash code only picks the bucket, and different keys can share it, so equals has to decide which entry is the key. Equal keys must have the same hash code or they'd be looked up in the wrong bucket and not found. Iteration order depends on the hash codes and the table size, which is why HashMap doesn't promise any order.",
          "(a) Two keys hashing to the same bucket, e.g. Aa and BB. (b) Same hash doesn't mean same key; equals does. (c) Otherwise the lookup goes to a different bucket and misses the entry. (d) Position depends on hashes and capacity, so it's unspecified."]),
     1: ("Answers two or three parts well, or gives the right ideas without the example.",
         ["A collision is when two keys go to the same bucket.", "equals decides."]),
     0: ("Incorrect, for example says equal hash codes mean equal keys, or that order is insertion order.",
         ["Same hash code means same key.", "HashMap keeps insertion order."])})
reg({"j5-l2.4": ("Hash tables", ["J5.06"])},
    {"MC105": (["J5.06"], "I38", "Two keys with equal hash codes are equal keys"),
     "MC106": (["J5.06"], "Platform", "When a hash table resizes, entries can stay in the same bucket indexes"),
     "MC107": (["J5.06"], "Platform", "hashCode % length is always a valid bucket index")})

# ====================================================================== 5.2.5
Lesson("j5-l2.5", "Binary search trees", ["J5.07"], [
    ("o1", "Implement insert, contains, size, height and in-order traversal for a binary search tree of ints"),
    ("o2", "Trace insertions to predict a tree's shape and in-order output"),
    ("o3", "Find and fix an insertion bug that loses part of the tree, and explain why sorted input makes a tree degenerate"),
], ["j5-l2.4", "j5-l1.1"], 55, ["I42", "R8", "R18"], r'''
## Before you start

You should be comfortable with node-and-link structures ([Linked lists](j5-l2.2)) and with recursion at a basic level (a method calling itself on a smaller problem; the next section of this stage covers it fully).

**Quick check.** A method keeps halving a range of n items until one is left. About how many halvings?

<details><summary>Show the answer</summary>

About log₂ n. For a million items, about 20.

</details>

## Explanation

### A tree of nodes

A **binary tree** is a node structure where each node has up to two children, a **left** and a **right**. The top node is the **root**; a node with no children is a **leaf**.

A **binary search tree** (BST) adds one rule that makes searching fast:

> For every node, **everything in its left subtree is smaller**, and **everything in its right subtree is larger**.

```
        5
       / \
      3   8
     / \   \
    1   4   9
```

To find a value, start at the root and **go left if the value is smaller, right if it's larger**. Each step discards a whole subtree, like binary search.

### Writing it

```java
class IntBst {
    private static class Node {
        int value;
        Node left, right;
        Node(int value) { this.value = value; }
    }

    private Node root;
    private int size;

    boolean contains(int value) {
        Node current = root;
        while (current != null) {
            if (value == current.value) return true;
            current = value < current.value ? current.left : current.right;
        }
        return false;
    }

    void insert(int value) {
        if (!contains(value)) {          // duplicates are ignored
            root = insert(root, value);
            size++;
        }
    }

    private Node insert(Node node, int value) {
        if (node == null) return new Node(value);                  // found the empty spot
        if (value < node.value) node.left = insert(node.left, value);
        else node.right = insert(node.right, value);
        return node;                                               // keep the existing links
    }
}
```

`insert(node, value)` is **recursive**: it asks the left or right subtree to insert the value, and hands back the (unchanged) node. The line `return node` matters: the result is assigned back (`node.left = insert(node.left, value)`), so the **existing** subtree stays attached. A tempting wrong version, `node.left = new Node(value)`, replaces whatever was there and silently drops a whole subtree.

### In-order traversal: sorted output for free

Visit the **left subtree, then the node, then the right subtree**:

```java
private void inOrder(Node node, List<Integer> out) {
    if (node == null) return;
    inOrder(node.left, out);
    out.add(node.value);
    inOrder(node.right, out);
}
```

For the tree above that gives `[1, 3, 4, 5, 8, 9]`: **sorted**. That's a property of every BST, and a quick test: an in-order list that isn't sorted means the BST rule is broken.

### Height

The **height** is the number of nodes on the longest path from the root to a leaf (0 for an empty tree, 1 for a single node):

```java
private int height(Node node) {
    if (node == null) return 0;
    return 1 + Math.max(height(node.left), height(node.right));
}
```

### Why the shape matters

Searching costs about the **height** of the tree. In a **balanced** tree of n nodes, the height is about log₂ n: for a million values, about 20. But the shape depends on the insertion order. Insert `1, 2, 3, 4, 5` in order, and every value goes to the right of the previous one:

```
1
 \
  2
   \
    3     (a linked list in disguise: height n, search O(n))
```

A tree built from already-sorted data is **degenerate**. That's why real libraries use **self-balancing** trees: Java's `TreeMap` guarantees log(n) time for `containsKey`, `get`, `put` and `remove` `[I42]`. A plain BST is the clearest way to learn the idea, and it is a poor choice for data that might arrive sorted.

## Worked examples

### Example 1: building a tree

*Task: insert 5, 3, 8, 1, 4, 7, 9, 2 into an empty BST. What is the in-order list and the height?*

| Insert | Where it goes |
|---|---|
| 5 | root |
| 3 | left of 5 |
| 8 | right of 5 |
| 1 | left of 3 |
| 4 | right of 3 |
| 7 | left of 8 |
| 9 | right of 8 |
| 2 | right of 1 (2 < 5, 2 < 3, 2 > 1) |

**In-order:** `[1, 2, 3, 4, 5, 7, 8, 9]`. **Height:** the longest path is 5 → 3 → 1 → 2, which is 4 nodes, so 4.

### Example 2: spotting a lost subtree

*Task: after inserting 5, 3, 1, `contains(1)` is false. Why?*

**Step 1 — Inserting 3:** left of 5. **Inserting 1:** compare with 5 (go left), then with 3 (go left).

**Step 2 — With the buggy code,** the step at 5 does `node.left = new Node(1)`, replacing the left child (3) instead of going down into it.

**Step 3 — So 3 disappears and 1 takes its place.** The fix is to recurse: `node.left = insert(node.left, value)`.

## Predict, then run

::exercise{id=j5-l2.5-predict-shape}

## Where this is used

- **`TreeMap` and `TreeSet`** are balanced search trees: sorted keys with fast lookup.
- **Databases** keep indexes in tree structures so that a lookup doesn't scan the whole table.
- **Parsers and compilers** build trees from source code, and walk them with the same recursive pattern.

## Common mistakes

:::mistake{id=MC108}
**Replacing a child instead of recursing into it.** `node.left = new Node(v)` throws away the existing left subtree.
:::

:::mistake{id=MC109}
**Assuming a BST is always fast.** Insert sorted data and it becomes a linked list with O(n) searches.
:::

:::mistake{id=MC110}
**Forgetting the empty tree.** `root` is `null`, so code that reads `root.value` fails.
:::

## Practice

::exercise{id=j5-l2.5-write-bst}

::exercise{id=j5-l2.5-debug-insert}

::exercise{id=j5-l2.5-explain-balance}

## Further reading

- **`java.util.TreeMap`** `[I42]` states the guaranteed log(n) cost of its balanced tree.
- **Guo (2013)** `[R18]` describes tools that draw tree and pointer structures.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercise checks that you can implement the tree operations (*implementation*).
- The **predict** exercise checks that you can trace insertions (*identifying mistakes*).
- The **debug** exercise checks that you can fix an insert that loses nodes (*debugging*).
- The **explain** exercise checks that you can say why input order affects a plain tree's shape (*explanation*).
''' + FOOT)

ex = Exercises("j5-l2.5")
def bst_run(values, probe):
    root, size = None, 0
    # a node is [value, left, right]
    def insert(node, v):
        if node is None: return [v, None, None], True
        if v == node[0]: return node, False
        if v < node[0]: node[1], added = insert(node[1], v)
        else: node[2], added = insert(node[2], v)
        return node, added
    for v in values:
        root, added = insert(root, v)
        size += added
    def inorder(n): return [] if n is None else inorder(n[1]) + [n[0]] + inorder(n[2])
    def height(n): return 0 if n is None else 1 + max(height(n[1]), height(n[2]))
    contains = probe in inorder(root)
    return f"inorder={inorder(root)} size={size} height={height(root)} contains={str(contains).lower()}"
def py_list(xs): return "[" + ", ".join(map(str, xs)) + "]"
def bst_run_fmt(values, probe):
    return bst_run(values, probe).replace("inorder=[", "inorder=[")
BST_DRV = '\n\nString run(int[] values, int probe) {\n    IntBst tree = new IntBst();\n    for (int v : values) {\n        tree.insert(v);\n    }\n    return "inorder=" + tree.inOrder() + " size=" + tree.size() + " height=" + tree.height() + " contains=" + tree.contains(probe);\n}'
BST_SOL = 'class IntBst {\n    private static class Node {\n        int value;\n        Node left;\n        Node right;\n\n        Node(int value) {\n            this.value = value;\n        }\n    }\n\n    private Node root;\n    private int size;\n\n    boolean contains(int value) {\n        Node current = root;\n        while (current != null) {\n            if (value == current.value) {\n                return true;\n            }\n            current = value < current.value ? current.left : current.right;\n        }\n        return false;\n    }\n\n    void insert(int value) {\n        if (!contains(value)) {\n            root = insert(root, value);\n            size++;\n        }\n    }\n\n    private Node insert(Node node, int value) {\n        if (node == null) {\n            return new Node(value);\n        }\n        if (value < node.value) {\n            node.left = insert(node.left, value);\n        } else {\n            node.right = insert(node.right, value);\n        }\n        return node;\n    }\n\n    int size() {\n        return size;\n    }\n\n    int height() {\n        return height(root);\n    }\n\n    private int height(Node node) {\n        if (node == null) {\n            return 0;\n        }\n        return 1 + Math.max(height(node.left), height(node.right));\n    }\n\n    List<Integer> inOrder() {\n        List<Integer> out = new ArrayList<>();\n        inOrder(root, out);\n        return out;\n    }\n\n    private void inOrder(Node node, List<Integer> out) {\n        if (node == null) {\n            return;\n        }\n        inOrder(node.left, out);\n        out.add(node.value);\n        inOrder(node.right, out);\n    }\n}'
BST_V = [("run", [[5, 3, 8, 1, 4], 4]), ("run", [[], 1]), ("run", [[2, 1, 3], 9])]
BST_H = [("run", [[5, 3, 8, 1, 4, 7, 9, 2], 6]), ("run", [[1, 2, 3, 4, 5], 5]), ("run", [[5, 5, 5], 5]), ("run", [[9, 7, 5, 3, 1], 3]), ("run", [[10, 5, 15, 3, 7, 12, 18, 1], 12]), ("run", [[-3, 0, -7, 4, -1], -7]), ("run", [[7], 8])]
ex.method("write", "j5-l2.5-write-bst", "A binary search tree", ["o1"], ["J5.07"], ["IMPL"],
    "Write `IntBst`, a binary search tree of `int`s **built from your own nodes** (no `TreeSet` or `TreeMap`, no sorting). `insert(int)` ignores a value that's already in the tree. It needs `contains`, `size()`, `height()` (the number of nodes on the longest path; 0 for an empty tree) and `inOrder()`, which returns the values as a `List<Integer>` in sorted order. The driver inserts the values and reports the results.",
    [("run", [("values", "int[]"), ("probe", "int")], "String")], {"run": bst_run}, BST_V, BST_H,
    'class IntBst {\n    void insert(int value) {\n    }\n\n    boolean contains(int value) {\n        return false;\n    }\n\n    int size() {\n        return 0;\n    }\n\n    int height() {\n        return 0;\n    }\n\n    List<Integer> inOrder() {\n        return new ArrayList<>();\n    }\n}' + BST_DRV,
    BST_SOL + BST_DRV,
    {"duplicates-counted": BST_SOL.replace("        if (!contains(value)) {\n            root = insert(root, value);\n            size++;\n        }", "        root = insert(root, value);\n        size++;"),
     "height-counts-edges": BST_SOL.replace("            return 0;\n        }\n        return 1 + Math.max(height(node.left)", "            return -1;\n        }\n        return 1 + Math.max(height(node.left)").replace("    int height() {\n        return height(root);", "    int height() {\n        return height(root) + 1;")},
    ("Each node holds a value and left/right children. insert goes left if smaller and right if larger, recursing until it finds an empty spot. inOrder is left, then node, then right.", "node.left = insert(node.left, value);  ...  inOrder(node.left, out); out.add(node.value); inOrder(node.right, out);"),
    source_tests=[("built from nodes, not library trees", ["Node"], ["TreeSet", "TreeMap", "sort("])],
    difficulty=4)
BST_BAD = BST_SOL.replace("        if (value < node.value) {\n            node.left = insert(node.left, value);\n        } else {\n            node.right = insert(node.right, value);\n        }\n        return node;", "        if (value < node.value) {\n            node.left = new Node(value);\n        } else {\n            node.right = new Node(value);\n        }\n        return node;")
ex.method("debug", "j5-l2.5-debug-insert", "The subtree that disappears", ["o3"], ["J5.07"], ["DEBUG"],
    "This `IntBst` works for a root and its two children, but inserting a third level loses values: after inserting `5, 3, 1`, the tree doesn't contain 3. Find the bug in the private `insert` and fix it.",
    [("run", [("values", "int[]"), ("probe", "int")], "String")], {"run": bst_run}, BST_V, BST_H,
    BST_BAD + BST_DRV, BST_SOL + BST_DRV,
    {"always-goes-right": BST_SOL.replace("        if (value < node.value) {\n            node.left = insert(node.left, value);", "        if (false) {\n            node.left = insert(node.left, value);")},
    ("Compare node.left = new Node(value) with what the node.left already holds. What happens to an existing left child?", "Recurse: node.left = insert(node.left, value) and node.right = insert(node.right, value)."),
    difficulty=3)
tree_inorder = bst_run([5, 3, 8, 1, 4, 7, 9, 2], 4)
BSTP_PROG = BST_SOL.replace("class IntBst {", "class IntBst {", 1) + '\n\nvoid main() {\n    IntBst tree = new IntBst();\n    int[] values = {5, 3, 8, 1, 4, 7, 9, 2};\n    for (int v : values) {\n        tree.insert(v);\n    }\n    IO.println(tree.inOrder());\n    IO.println(tree.height());\n    IO.println(tree.contains(4));\n    IO.println(tree.contains(6));\n    IntBst sorted = new IntBst();\n    for (int v = 1; v <= 6; v++) {\n        sorted.insert(v);\n    }\n    IO.println(sorted.height());\n}'
ex.predict("j5-l2.5-predict-shape", "Shape and order", ["o2"], ["J5.07"],
    "Work out what this program prints. The `IntBst` class is complete. Trace the insertions on paper: where does each value go, and what is the longest path?",
    BSTP_PROG, "[1, 2, 3, 4, 5, 7, 8, 9]\n4\ntrue\nfalse\n6",
    ("Draw the tree as you insert. The in-order list is always sorted. Height is the longest root-to-leaf path in nodes. What does inserting 1, 2, 3, 4, 5, 6 in order build?", "Eight values, longest path 5-3-1-2 is 4 nodes. 4 is in the tree and 6 isn't. Sorted insertion makes a chain, so six values give height 6."),
    difficulty=4)
ex.explain("j5-l2.5-explain-balance", "Why did the tree become a list?", ["o3"], ["J5.07"],
    "A developer builds a BST by inserting 1,000,000 customer ids read from a file in ascending order, and lookups are very slow. (a) Describe the shape of the tree and the cost of a lookup. (b) About how tall would a balanced tree of a million values be, and what does that mean for lookups? (c) Name a Java class that avoids the problem, and what it promises.",
    "A full answer says that inserting in ascending order puts every value to the right of the previous one so the tree is a chain of height about 1,000,000 and a lookup is O(n); a balanced tree of a million values is about 20 levels tall so a lookup takes about 20 steps; and TreeMap (or TreeSet) is a balanced tree that guarantees log(n) time for get, put, containsKey and remove.",
    {2: ("Says ascending insertion builds a chain of height about a million with O(n) lookups, a balanced tree has about 20 levels so about 20 steps, and names TreeMap or TreeSet which guarantees log(n) operations.",
         ["Every new id is larger than the last so it goes to the right each time, making a chain with height about a million, and a lookup walks up to a million nodes. A balanced tree of a million values is only about 20 levels tall, so a lookup takes about 20 steps. TreeMap uses a self-balancing tree and guarantees log(n) time for get, put, containsKey and remove.",
          "The tree is degenerate: a linked list to the right, height about 1,000,000 and O(n) lookup. Balanced would be around 20 deep. Use TreeMap, which is guaranteed O(log n)."]),
     1: ("Gets the degenerate shape or the balanced height or the Java class, but not all three.",
         ["It becomes a linked list.", "Use TreeMap."]),
     0: ("Incorrect, for example says the tree is balanced or the problem is the file read.",
         ["The tree is balanced because it is sorted.", "The disk is slow."])})
reg({"j5-l2.5": ("Binary search trees", ["J5.07"])},
    {"MC108": (["J5.07"], "Platform", "Setting node.left = new Node(v) inserts the value into the tree"),
     "MC109": (["J5.07"], "I42", "A binary search tree always gives O(log n) lookups"),
     "MC110": (["J5.07"], "Platform", "A tree always has a root node, so root.value is safe")})

# ====================================================================== 5.2.6
Lesson("j5-l2.6", "Heaps and priority queues", ["J5.08"], [
    ("o1", "Implement a min-heap on an array with add and poll"),
    ("o2", "Explain the heap property and why add and poll cost O(log n) while peek is constant"),
    ("o3", "Use PriorityQueue to keep the k smallest items of a stream"),
], ["j5-l2.5"], 55, ["I56", "R8"], r'''
## Before you start

You should know how a binary tree is shaped ([Binary search trees](j5-l2.5)) and how an array holds values by position ([Dynamic arrays](j5-l2.1)).

**Quick check.** What does `queue.poll()` return on an empty `ArrayDeque`?

<details><summary>Show the answer</summary>

`null`.

</details>

## Explanation

### Always serving the smallest first

A queue serves items in arrival order. A **priority queue** serves the **most important** one first, whatever order they arrived in: an emergency ward, a scheduler picking the next job, a route planner picking the cheapest unexplored road. In Java the "most important" is the **least** element under the natural ordering or a `Comparator`: the head of a `PriorityQueue` is its smallest element `[I56]`.

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(5);
pq.offer(1);
pq.offer(3);
pq.peek();     // 1   (look at the smallest)
pq.poll();     // 1   (remove and return the smallest)
pq.poll();     // 3
```

The documentation gives its costs: `offer`, `add`, `poll` and `remove()` take **O(log n)**, `peek` and `size` take constant time, and `contains` and `remove(Object)` take linear time `[I56]`. It doesn't permit `null` elements, and ties are broken arbitrarily `[I56]`.

### A heap: a tree stored in an array

`PriorityQueue` is "based on a priority heap" `[I56]`. A **min-heap** is a binary tree with two properties:

1. **Shape:** it is *complete*: every level is full except possibly the last, which fills from the left.
2. **Heap property:** every node is **less than or equal to its children**. So the root is the smallest of all.

Because it's complete, there are no gaps, and the tree fits in a plain array by position:

```
index:   0   1   2   3   4   5
value: [ 1 | 3 | 2 | 7 | 4 | 5 ]

        1
      /   \
     3     2
    / \   /
   7   4 5
```

For the node at index `i`:

- **parent:** `(i - 1) / 2`
- **left child:** `2 * i + 1`
- **right child:** `2 * i + 2`

No node objects and no links, only index arithmetic.

### Adding: sift up

To add a value, put it in the **next free slot** (end of the array), then **swap it upward** while it's smaller than its parent:

```java
void add(int value) {
    if (size == data.length) data = Arrays.copyOf(data, data.length * 2);
    data[size] = value;
    int i = size;
    size++;
    while (i > 0 && data[i] < data[(i - 1) / 2]) {
        swap(i, (i - 1) / 2);
        i = (i - 1) / 2;
    }
}
```

The value rises at most one level per swap, and the tree has about log₂ n levels, so `add` is O(log n).

### Removing the smallest: sift down

The smallest is at index 0. To remove it, **move the last element to the root**, shrink the size, then **swap it downward** with its **smaller child** while a child is smaller:

```java
int poll() {
    if (size == 0) throw new NoSuchElementException();
    int min = data[0];
    size--;
    data[0] = data[size];
    int i = 0;
    while (true) {
        int left = 2 * i + 1, right = 2 * i + 2, smallest = i;
        if (left < size && data[left] < data[smallest]) smallest = left;
        if (right < size && data[right] < data[smallest]) smallest = right;
        if (smallest == i) break;
        swap(i, smallest);
        i = smallest;
    }
    return min;
}
```

Again at most one swap per level: O(log n). `peek` is just `data[0]`: constant.

### A heap is not sorted

A heap only guarantees that **each parent is below its children**, not that the array is in order. The array above, `[1, 3, 2, 7, 4, 5]`, isn't sorted. The Java documentation says exactly this about `PriorityQueue`: its iterator is **not guaranteed to traverse the elements in any particular order**, and for ordered traversal you should sort a copy, such as `Arrays.sort(pq.toArray())` `[I56]`. The way to get items in order is to **poll repeatedly**.

### A classic use: the k smallest

To keep the **k smallest** values seen so far from a long stream, keep a **max**-heap of size k: its head is the *largest of the kept ones*. For each new value, add it; if the heap is now bigger than k, **poll** the largest. At the end the heap holds the k smallest. Cost: O(n log k), and memory for only k items.

```java
PriorityQueue<Integer> biggestKept = new PriorityQueue<>(Comparator.reverseOrder());
for (int v : values) {
    biggestKept.offer(v);
    if (biggestKept.size() > k) {
        biggestKept.poll();            // drop the largest, which can't be among the k smallest
    }
}
```

`Comparator.reverseOrder()` flips the ordering so the head becomes the largest.

## Worked examples

### Example 1: adding to a heap

*Task: heap `[2, 5, 4]`; add 1.*

**Step 1 — Append:** `[2, 5, 4, 1]`, with 1 at index 3. Its parent is `(3-1)/2 = 1`, holding 5.

**Step 2 — 1 < 5, swap:** `[2, 1, 4, 5]`. Now 1 is at index 1, with parent index 0 holding 2.

**Step 3 — 1 < 2, swap:** `[1, 2, 4, 5]`. At index 0 there's no parent, so it stops.

### Example 2: polling

*Task: poll from `[1, 2, 4, 5]`.*

**Step 1 — The result is 1.** Move the last element (5) to the root: `[5, 2, 4]`.

**Step 2 — Compare 5 with its children 2 and 4;** the smaller is 2. Swap: `[2, 5, 4]`.

**Step 3 — 5 at index 1 has no children now** (index 3 is beyond the size), so it stops. The heap is `[2, 5, 4]`.

## Where this is used

- **Schedulers and event simulations** pick the next earliest event with a priority queue.
- **Dijkstra's shortest-path algorithm** (lesson 5.3.4) repeatedly takes the cheapest unexplored node.
- **Top-k and streaming statistics** use a bounded heap, so they need memory for k items, not n.

## Common mistakes

:::mistake{id=MC111}
**Expecting a `PriorityQueue` to iterate in order.** Only `poll` yields the smallest first. Iteration order isn't sorted.
:::

:::mistake{id=MC112}
**Treating the heap array as sorted.** It's only partially ordered: each parent is no larger than its children.
:::

:::mistake{id=MC113}
**Sifting down against the larger child.** Swap with the **smaller** child, or the heap property breaks.
:::

## Practice

::exercise{id=j5-l2.6-write-heap}

::exercise{id=j5-l2.6-write-topk}

::exercise{id=j5-l2.6-explain-heap}

## Further reading

- **`java.util.PriorityQueue`** `[I56]` documents ordering, costs, null handling and the unordered iterator.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can implement a min-heap, and use `PriorityQueue` for the k smallest (*implementation*).
- The **explain** exercise checks that you can say why the costs are logarithmic and why iteration isn't sorted (*explanation*).
''' + FOOT)

ex = Exercises("j5-l2.6")
HEAP_DRV = '\n\nString run(String[] ops) {\n    MinHeap heap = new MinHeap();\n    StringBuilder out = new StringBuilder();\n    for (String op : ops) {\n        if (op.startsWith("add:")) {\n            heap.add(Integer.parseInt(op.substring(4)));\n        } else {\n            try {\n                out.append(heap.poll());\n            } catch (NoSuchElementException e) {\n                out.append("E");\n            }\n            out.append(" ");\n        }\n    }\n    return out + "size=" + heap.size() + (heap.size() > 0 ? " peek=" + heap.peek() : "");\n}'
HEAP_SOL = 'class MinHeap {\n    private int[] data = new int[4];\n    private int size;\n\n    void add(int value) {\n        if (size == data.length) {\n            data = Arrays.copyOf(data, data.length * 2);\n        }\n        data[size] = value;\n        int i = size;\n        size++;\n        while (i > 0 && data[i] < data[(i - 1) / 2]) {\n            swap(i, (i - 1) / 2);\n            i = (i - 1) / 2;\n        }\n    }\n\n    int poll() {\n        if (size == 0) {\n            throw new NoSuchElementException();\n        }\n        int min = data[0];\n        size--;\n        data[0] = data[size];\n        int i = 0;\n        while (true) {\n            int left = 2 * i + 1;\n            int right = 2 * i + 2;\n            int smallest = i;\n            if (left < size && data[left] < data[smallest]) {\n                smallest = left;\n            }\n            if (right < size && data[right] < data[smallest]) {\n                smallest = right;\n            }\n            if (smallest == i) {\n                break;\n            }\n            swap(i, smallest);\n            i = smallest;\n        }\n        return min;\n    }\n\n    int peek() {\n        if (size == 0) {\n            throw new NoSuchElementException();\n        }\n        return data[0];\n    }\n\n    int size() {\n        return size;\n    }\n\n    private void swap(int a, int b) {\n        int t = data[a];\n        data[a] = data[b];\n        data[b] = t;\n    }\n}'
def heap_run(ops):
    h, out = [], []
    for op in ops:
        if op.startswith("add:"): heapq.heappush(h, int(op[4:]))
        else: out.append(str(heapq.heappop(h)) if h else "E"); out[-1] += " "
    return "".join(out) + f"size={len(h)}" + (f" peek={h[0]}" if h else "")
HEAP_V = [("run", [["add:5", "add:1", "add:3", "poll", "poll"]]), ("run", [["poll"]]), ("run", [[]])]
HEAP_H = [("run", [["add:2", "add:2", "add:2", "poll", "poll", "poll", "poll"]]), ("run", [["add:9", "add:8", "add:7", "add:6", "add:5", "add:4", "add:3", "add:2", "add:1", "poll", "poll", "poll"]]), ("run", [["add:-5", "add:0", "add:-10", "poll", "add:-7", "poll", "poll"]]), ("run", [["add:1", "add:2", "add:3", "add:4", "add:5", "add:6", "poll", "add:0", "poll", "poll"]]), ("run", [["add:42"]]), ("run", [["add:3", "add:1", "add:2", "poll", "add:0", "poll", "poll", "poll", "poll"]])]
ex.method("write", "j5-l2.6-write-heap", "A min-heap on an array", ["o1"], ["J5.08"], ["IMPL"],
    "Write `MinHeap`: a min-heap of `int`s **stored in an `int[]`** (no `PriorityQueue`, `TreeSet` or sorting). `add(int)` puts the value at the end and sifts it up; `poll()` removes and returns the smallest, moving the last value to the root and sifting it down (it throws `NoSuchElementException` if empty); `peek()` returns the smallest without removing it (same exception if empty); `size()`. The array should grow when full. The driver prints each polled value (or `E`), then the final size and, if any remain, the smallest.",
    [("run", [("ops", "String[]")], "String")], {"run": heap_run}, HEAP_V, HEAP_H,
    'class MinHeap {\n    void add(int value) {\n    }\n\n    int poll() {\n        return 0;\n    }\n\n    int peek() {\n        return 0;\n    }\n\n    int size() {\n        return 0;\n    }\n}' + HEAP_DRV,
    HEAP_SOL + HEAP_DRV,
    {"sift-down-with-larger-child": HEAP_SOL.replace("if (right < size && data[right] < data[smallest]) {\n                smallest = right;\n            }", "if (right < size && data[right] > data[left]) {\n                smallest = right;\n            }"),
     "poll-forgets-sift-down": HEAP_SOL.replace("            swap(i, smallest);\n            i = smallest;\n        }\n        return min;", "            break;\n        }\n        return min;")},
    ("Parent of i is (i-1)/2; children are 2i+1 and 2i+2. add: put at the end, swap up while smaller than the parent. poll: move the last to the root, swap down with the smaller child.", "while (i > 0 && data[i] < data[(i - 1) / 2]) { swap(i, (i - 1) / 2); i = (i - 1) / 2; }"),
    source_tests=[("stored in an int array, no library queue", ["int[]"], ["new PriorityQueue", "new TreeSet", "sort("])],
    difficulty=5)
def k_smallest(values, k):
    return sorted(values)[:k]
KS_SOL = 'List<Integer> kSmallest(int[] values, int k) {\n    PriorityQueue<Integer> kept = new PriorityQueue<>(Comparator.reverseOrder());\n    for (int v : values) {\n        kept.offer(v);\n        if (kept.size() > k) {\n            kept.poll();\n        }\n    }\n    List<Integer> result = new ArrayList<>(kept);\n    Collections.sort(result);\n    return result;\n}'
ex.method("write", "j5-l2.6-write-topk", "The k smallest of a stream", ["o3"], ["J5.08"], ["IMPL"],
    "Write `kSmallest(int[] values, int k)`: the `k` smallest values, in ascending order (all of them if there are fewer than `k`). Use a `PriorityQueue` that keeps at most `k` items: a **max**-heap (`Comparator.reverseOrder()`), so the head is the largest kept value and is the one to drop when the queue grows past `k`. Remember: iterating a `PriorityQueue` isn't sorted, so sort the result at the end.",
    [("kSmallest", [("values", "int[]"), ("k", "int")], "List<Integer>")], {"kSmallest": k_smallest},
    [("kSmallest", [[5, 1, 9, 3, 7], 3]), ("kSmallest", [[], 2]), ("kSmallest", [[4, 4, 4], 2])],
    [("kSmallest", [[10, 20], 5]), ("kSmallest", [[3, 1, 2], 0]), ("kSmallest", [[-1, -5, 4, 0, -3], 2]), ("kSmallest", [[9, 8, 7, 6, 5, 4, 3, 2, 1], 4]), ("kSmallest", [[1], 1]), ("kSmallest", [[2, 2, 1, 1, 3, 3], 3])],
    'List<Integer> kSmallest(int[] values, int k) {\n    return new ArrayList<>();\n}',
    KS_SOL,
    {"keeps-the-largest": KS_SOL.replace("Comparator.reverseOrder()", "Comparator.naturalOrder()"),
     "unsorted-result": KS_SOL.replace("    Collections.sort(result);\n", "")},
    ("A max-heap of size k holds the k smallest so far. Its head is the largest kept value: poll it whenever the size exceeds k.", "new PriorityQueue<>(Comparator.reverseOrder()); if (kept.size() > k) kept.poll();"),
    source_tests=[("uses a PriorityQueue", ["PriorityQueue"], None)],
    difficulty=4)
ex.explain("j5-l2.6-explain-heap", "Why logarithmic, and why not sorted?", ["o2"], ["J5.08"],
    "(a) State the two properties of a min-heap. (b) Explain why `add` and `poll` cost O(log n) while `peek` costs O(1). (c) A learner prints a `PriorityQueue` of 5, 1, 3, 4, 2 with `for (int x : pq)` and the order isn't sorted. Is that a bug? How do you get the values out in order?",
    "A full answer states that a min-heap is a complete binary tree where every parent is no larger than its children; that add and poll move one value up or down a single path through about log2 n levels, whereas peek just reads the root; and that it's not a bug because only the parent-child ordering is guaranteed (the documentation says the iterator has no particular order), so you poll repeatedly or sort a copy.",
    {2: ("States the complete shape and the parent-no-larger-than-children property, explains that add and poll walk one path of about log n levels while peek reads the root, and says iteration order isn't guaranteed so poll repeatedly or sort a copy.",
         ["A min-heap is a complete binary tree, and each parent is less than or equal to its children, so the smallest is at the root. add and poll only move one value up or down a single path, which has about log2 n levels, so they're O(log n); peek just reads the root so it's O(1). The unsorted printing isn't a bug: the heap only orders parents against children and the iterator makes no promise of order, so you poll repeatedly, or sort a copy, to get sorted values.",
          "(a) Complete tree, parent <= children. (b) Sifting moves along one root-to-leaf path of about log n levels; peek reads index 0. (c) Not a bug: iteration isn't sorted. Use poll in a loop to get them in order."]),
     1: ("Answers some parts correctly, for example the properties and the costs but not the iteration point.",
         ["Parents are smaller than children.", "It isn't a bug, poll them in order."]),
     0: ("Incorrect, for example says the array of a heap is sorted, or that the iteration order is a bug in PriorityQueue.",
         ["A heap is a sorted array.", "It's a bug in PriorityQueue."])})
reg({"j5-l2.6": ("Heaps and priority queues", ["J5.08"])},
    {"MC111": (["J5.08"], "I56", "A for-each loop over a PriorityQueue visits items in sorted order"),
     "MC112": (["J5.08"], "Platform", "The array behind a heap is sorted"),
     "MC113": (["J5.08"], "Platform", "When sifting down, a value swaps with either child")})
print("5.2 (stacks, hash tables, trees, heaps) written")
