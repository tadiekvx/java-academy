from build import *

Lesson("j1-l6.3", "ArrayList", ["J1.11"], [
    ("o1", "Create an ArrayList and use add, get, set, remove, size and contains"),
    ("o2", "Loop over a list with an index loop and an enhanced for loop"),
    ("o3", "Choose between an array and an ArrayList for a problem"),
    ("o4", "Avoid the remove(index) versus remove(value) trap on a list of ints"),
], ["j1-l6.2"], 40, ["R8", "I4"], r'''
## Before you start

You should be able to create arrays and loop over them ([Arrays](j1-l6.1)).

**Quick check.** Can you add a fifth element to an array created with four?

<details><summary>Show the answer</summary>

No. An array's size is fixed when it's created.

</details>

## Explanation

Arrays have a fixed size. Often you don't know in advance how many items you'll have: the words a user types, the orders in a queue. An **`ArrayList`** is a list that grows and shrinks as you add and remove items.

### Creating a list

```java
ArrayList<Integer> scores = new ArrayList<>();
ArrayList<String> names = new ArrayList<>();
```

The type in the angle brackets says what the list holds. Lists hold **objects**, so for whole numbers you write `Integer` (not `int`), and for decimals `Double`. Java converts between `int` and `Integer` automatically, so you can mostly ignore the difference. The empty `<>` on the right tells Java to use the same type.

### The main methods

| Method | What it does |
|---|---|
| `add(item)` | Adds to the end |
| `get(i)` | The item at index `i` (starting at 0) |
| `set(i, item)` | Replaces the item at index `i` |
| `remove(i)` | Removes the item at index `i`; later items shuffle down |
| `size()` | How many items are in the list |
| `isEmpty()` | `true` if there are none |
| `contains(item)` | `true` if the item is in the list |

```java runnable
void main() {
    ArrayList<String> queue = new ArrayList<>();
    queue.add("Ada");
    queue.add("Grace");
    queue.add("Alan");
    IO.println(queue);
    queue.remove(0);
    queue.set(0, "Hopper");
    IO.println(queue + " has " + queue.size());
    IO.println(queue.contains("Alan"));
}
```

This prints `[Ada, Grace, Alan]`, then `[Hopper, Alan] has 2`, then `true`. Unlike an array, a list prints sensibly all by itself.

Notice the size is a method, `size()`, with brackets; arrays use `length`, strings use `length()`, and lists use `size()`. The compiler tells you which one you got wrong.

### Looping over a list

```java runnable
void main() {
    ArrayList<Integer> scores = new ArrayList<>();
    scores.add(40);
    scores.add(70);
    scores.add(55);

    int total = 0;
    for (int score : scores) {
        total += score;
    }
    IO.println(total);

    for (int i = 0; i < scores.size(); i++) {
        IO.print(scores.get(i) + " ");
    }
    IO.println();
}
```

Both loop styles from arrays work, with `get(i)` and `size()` replacing `[i]` and `length`.

### The remove trap

For a list of `Integer`, `remove` is ambiguous: *remove the item at this index*, or *remove this value*? Java picks based on the type you give it:

```java runnable
void main() {
    ArrayList<Integer> nums = new ArrayList<>();
    nums.add(5);
    nums.add(10);
    nums.add(15);
    nums.remove(Integer.valueOf(10));   // removes the VALUE 10
    IO.println(nums);
    nums.remove(0);                      // removes the item at INDEX 0
    IO.println(nums);
}
```

This prints `[5, 15]` and then `[15]`. A plain `int` argument means an **index**. So `nums.remove(10)` on this list would look for index 10, which doesn't exist, and crash with `IndexOutOfBoundsException`. To remove by value, wrap it: `Integer.valueOf(10)`.

### Array or ArrayList?

| | Array | ArrayList |
|---|---|---|
| Size | Fixed when created | Grows and shrinks |
| Holds | `int`, `double`, … or objects | Objects (`Integer`, `String`, …) |
| Size check | `values.length` | `list.size()` |
| Read / write | `values[i]` | `list.get(i)` / `list.set(i, x)` |

Use an array when the size is known and fixed. Use an `ArrayList` when items come and go. In day-to-day Java, lists are far more common.

## Worked examples

### Example 1: keep the passes

*Task: return a new list holding only the marks of 50 or more.*

**Step 1 — Which pattern?** Filter: look at each item, add the ones you want to a new list.

**Step 2 — Make an empty result list, and add to it.**

```java runnable
ArrayList<Integer> passes(ArrayList<Integer> marks) {
    ArrayList<Integer> result = new ArrayList<>();
    for (int mark : marks) {
        if (mark >= 50) {
            result.add(mark);
        }
    }
    return result;
}

void main() {
    ArrayList<Integer> marks = new ArrayList<>();
    marks.add(40);
    marks.add(70);
    marks.add(55);
    IO.println(passes(marks));
}
```

This prints `[70, 55]`. Building a new list leaves the original unchanged.

### Example 2: collecting what the user types

*Task: read words until the person types `done`, then print how many they typed.*

**Step 1 — You don't know how many.** That's exactly what a list is for.

**Step 2 — A loop that reads, then stops at `done`.**

```java
void main() {
    ArrayList<String> words = new ArrayList<>();
    String typed = IO.readln("Word (or done): ").strip();
    while (!typed.equals("done")) {
        words.add(typed);
        typed = IO.readln("Word (or done): ").strip();
    }
    IO.println("You typed " + words.size() + " words: " + words);
}
```

With the input `cat`, `dog`, `done`, this prints `You typed 2 words: [cat, dog]`.

## Predict, then run

::exercise{id=j1-l6.3-predict-list}

## Where this is used

- **Almost every program**: lists of users, orders, messages, products.
- **Collecting results**: add to a list as you go, then process or print the whole list.
- **Reading data**: lines from a file, rows from a database.

## Common mistakes

### Using `remove(int)` when you meant to remove a value

`list.remove(10)` removes the item at index 10. To remove the value 10 from a list of `Integer`, use `list.remove(Integer.valueOf(10))`.

### `length` or `length()` instead of `size()`

Arrays have `length`, strings have `length()`, lists have `size()`.

### Forgetting the type in the angle brackets

`new ArrayList<>()` needs the list's declared type on the left (`ArrayList<String>`), so Java knows what it holds.

## Practice

::exercise{id=j1-l6.3-write-evens}

::exercise{id=j1-l6.3-debug-remove}

::exercise{id=j1-l6.3-modify-names}

::exercise{id=j1-l6.3-explain-choice}

## Version notes

`ArrayList` is in `java.util`, which compact source files import automatically. In ordinary Java files you'd write `import java.util.ArrayList;`.

## Further reading

- **Java SE 25 API documentation for `ArrayList`** `[I4]`: every method, with notes on how fast each one is.

## How you'll be assessed

- The **predict** exercise checks that you can follow list code.
- The **write**, **debug** and **modify** exercises check that you can build, fix and change list code (*implementation, debugging, modification*).
- The **explain** exercise checks that you can choose between an array and a list.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l6.3")
ex.predict("j1-l6.3-predict-list", "What's in the list?", ["o1", "o2", "o4"], ["J1.11"],
    "Predict exactly what this program prints.",
    '''
    void main() {
        ArrayList<Integer> nums = new ArrayList<>();
        nums.add(30);
        nums.add(10);
        nums.add(20);
        nums.set(1, 99);
        IO.println(nums);
        nums.remove(0);
        IO.println(nums);
        nums.remove(Integer.valueOf(20));
        IO.println(nums + " " + nums.size());
        IO.println(nums.contains(99));
    }
    ''', '''
    [30, 99, 20]
    [99, 20]
    [99] 1
    true
    ''', ("set replaces; remove(0) is an index; remove(Integer.valueOf(20)) is a value.",
          "After set: [30, 99, 20]. remove(0) takes off 30. Then the value 20 is removed, leaving [99]."),
    misconceptions=[], difficulty=2)

def evens(v): return [x for x in v if x % 2 == 0]
ex.method("write", "j1-l6.3-write-evens", "Keep the evens", ["o1", "o2"], ["J1.11"], ["IMPL"],
    "Write a method called `evens` that is given an `ArrayList<Integer>` called `numbers` and returns a **new** `ArrayList<Integer>` containing only the even numbers, in the same order. The original list must not change.",
    [("evens", [("numbers", "ArrayList<Integer>")], "ArrayList<Integer>")], {"evens": evens},
    [(None, [[1, 2, 3, 4, 5, 6]]), (None, [[]]), (None, [[7, 9]])],
    [(None, [[2]], "one even"), (None, [[0, -2, -3]], "zero and negatives"), (None, [[8, 8, 8]], "repeats"), (None, [[1, 3, 5, 7, 9]], "all odd"), (None, [[10, 11, 12, 13, 14]], "alternating")],
    '// Write the evens method here.\n\nvoid main() {\n    ArrayList<Integer> numbers = new ArrayList<>();\n    numbers.add(1);\n    numbers.add(2);\n    numbers.add(4);\n    IO.println(evens(numbers)); // should print [2, 4]\n}\n',
    'ArrayList<Integer> evens(ArrayList<Integer> numbers) {\n    ArrayList<Integer> result = new ArrayList<>();\n    for (int number : numbers) {\n        if (number % 2 == 0) {\n            result.add(number);\n        }\n    }\n    return result;\n}\n\nvoid main() {\n    ArrayList<Integer> numbers = new ArrayList<>();\n    numbers.add(1);\n    numbers.add(2);\n    numbers.add(4);\n    IO.println(evens(numbers)); // should print [2, 4]\n}\n',
    {"odds": 'ArrayList<Integer> evens(ArrayList<Integer> numbers) {\n    ArrayList<Integer> result = new ArrayList<>();\n    for (int number : numbers) {\n        if (number % 2 != 0) {\n            result.add(number);\n        }\n    }\n    return result;\n}\n\nvoid main() {\n}\n'},
    ("Filter: make an empty result list and add each even number to it.", "if (number % 2 == 0) result.add(number);"),
    starter_compiles=False, group="list-filter")

def positives(v): return [x for x in v if x > 0]
ex.method("write", "j1-l6.3-retrieve-positives", "Keep the positives", ["o1", "o2"], ["J1.11"], ["IMPL"],
    "Write a method called `positives` that is given an `ArrayList<Integer>` called `numbers` and returns a **new** `ArrayList<Integer>` containing only the numbers greater than zero, in the same order.",
    [("positives", [("numbers", "ArrayList<Integer>")], "ArrayList<Integer>")], {"positives": positives},
    [(None, [[3, -1, 0, 8]]), (None, [[]]), (None, [[-5, -6]])],
    [(None, [[1]], "one"), (None, [[0]], "just zero"), (None, [[5, 5, -5, 5]], "repeats"), (None, [[-1, 1, -1, 1]], "alternating"), (None, [[100, 200, 300]], "all positive")],
    '// Write the positives method here.\n\nvoid main() {\n}\n',
    'ArrayList<Integer> positives(ArrayList<Integer> numbers) {\n    ArrayList<Integer> result = new ArrayList<>();\n    for (int number : numbers) {\n        if (number > 0) {\n            result.add(number);\n        }\n    }\n    return result;\n}\n\nvoid main() {\n}\n',
    {"keeps-zero": 'ArrayList<Integer> positives(ArrayList<Integer> numbers) {\n    ArrayList<Integer> result = new ArrayList<>();\n    for (int number : numbers) {\n        if (number >= 0) {\n            result.add(number);\n        }\n    }\n    return result;\n}\n\nvoid main() {\n}\n'},
    ("Filter again, with a different condition.", "if (number > 0) result.add(number);"), starter_compiles=False, role="retrieval", group="list-filter")

def long_words(v, n): return [w for w in v if len(w) > n]
ex.method("write", "j1-l6.3-retrieve-longwords", "Keep the long words", ["o1", "o2"], ["J1.11"], ["IMPL"],
    "Write a method called `longWords` that is given an `ArrayList<String>` called `words` and an `int` called `minLength` (in that order), and returns a **new** `ArrayList<String>` containing the words with **more than** `minLength` characters, in the same order.",
    [("longWords", [("words", "ArrayList<String>"), ("minLength", "int")], "ArrayList<String>")], {"longWords": long_words},
    [(None, [["cat", "elephant", "dog", "giraffe"], 3]), (None, [[], 3]), (None, [["a", "bb"], 5])],
    [(None, [["abc", "abcd"], 3], "boundary"), (None, [["x"], 0], "min zero"), (None, [["", "a"], 0], "empty word"), (None, [["Java", "is", "fun"], 2], "short list"), (None, [["same", "same", "same"], 3], "repeats")],
    '// Write the longWords method here.\n\nvoid main() {\n}\n',
    'ArrayList<String> longWords(ArrayList<String> words, int minLength) {\n    ArrayList<String> result = new ArrayList<>();\n    for (String word : words) {\n        if (word.length() > minLength) {\n            result.add(word);\n        }\n    }\n    return result;\n}\n\nvoid main() {\n}\n',
    {"at-least": 'ArrayList<String> longWords(ArrayList<String> words, int minLength) {\n    ArrayList<String> result = new ArrayList<>();\n    for (String word : words) {\n        if (word.length() >= minLength) {\n            result.add(word);\n        }\n    }\n    return result;\n}\n\nvoid main() {\n}\n'},
    ("Filter: strings use length() with brackets.", "if (word.length() > minLength) result.add(word);"), starter_compiles=False, role="retrieval", group="list-filter")

def remove_value(v, x):
    out = list(v)
    if x in out:
        out.remove(x)
    return out
ex.method("debug", "j1-l6.3-debug-remove", "Remove the value", ["o4"], ["J1.11"], ["DEBUG"],
    "`removeValue` should remove the **first item equal to** `value` from a list of ints, and return the list. If the value isn't there, the list is returned unchanged. It crashes for some inputs. Find and fix the bug.",
    [("removeValue", [("numbers", "ArrayList<Integer>"), ("value", "int")], "ArrayList<Integer>")], {"removeValue": remove_value},
    [(None, [[5, 10, 15], 10]), (None, [[1, 2, 3], 3]), (None, [[4, 5], 9])],
    [(None, [[], 1], "empty list"), (None, [[7, 7, 7], 7], "removes only the first"), (None, [[100, 200], 100], "first"), (None, [[0, 1, 2], 2], "index equals value"), (None, [[10, 20, 30, 40, 50], 30], "middle")],
    'ArrayList<Integer> removeValue(ArrayList<Integer> numbers, int value) {\n    numbers.remove(value);\n    return numbers;\n}\n\nvoid main() {\n    ArrayList<Integer> numbers = new ArrayList<>();\n    numbers.add(5);\n    numbers.add(10);\n    numbers.add(15);\n    IO.println(removeValue(numbers, 10)); // should print [5, 15]\n}\n',
    'ArrayList<Integer> removeValue(ArrayList<Integer> numbers, int value) {\n    numbers.remove(Integer.valueOf(value));\n    return numbers;\n}\n\nvoid main() {\n    ArrayList<Integer> numbers = new ArrayList<>();\n    numbers.add(5);\n    numbers.add(10);\n    numbers.add(15);\n    IO.println(removeValue(numbers, 10)); // should print [5, 15]\n}\n',
    {"removes-nothing": 'ArrayList<Integer> removeValue(ArrayList<Integer> numbers, int value) {\n    return numbers;\n}\n\nvoid main() {\n}\n'},
    ("What does remove do when it's given a plain int?", "A plain int means an index. Wrap the value: numbers.remove(Integer.valueOf(value))."),
    notes="Bug: remove(int) removes by index. The 'index equals value' test shows the wrong element removed rather than a crash.")

def upper(v): return [w.upper() for w in v if w.strip() != ""]
ex.method("modify", "j1-l6.3-modify-names", "Skip the blanks", ["o1", "o2"], ["J1.11"], ["MOD"],
    "`shout` returns a new list with every name in capitals. Some of the names are blank (empty, or just spaces); change `shout` so those are **left out** of the result. Keep the order of the rest.",
    [("shout", [("names", "ArrayList<String>")], "ArrayList<String>")], {"shout": upper},
    [(None, [["ada", "", "grace"]]), (None, [[]]), (None, [["alan"]])],
    [(None, [[" ", "x"]], "spaces only"), (None, [["", "", ""]], "all blank"), (None, [["a", "b", "c"]], "none blank"), (None, [["  padded  ", "ok"]], "padded name"), (None, [["Zed", " ", "Amy", ""]], "mixed")],
    'ArrayList<String> shout(ArrayList<String> names) {\n    ArrayList<String> result = new ArrayList<>();\n    for (String name : names) {\n        result.add(name.toUpperCase());\n    }\n    return result;\n}\n\nvoid main() {\n}\n',
    'ArrayList<String> shout(ArrayList<String> names) {\n    ArrayList<String> result = new ArrayList<>();\n    for (String name : names) {\n        if (!name.strip().isEmpty()) {\n            result.add(name.toUpperCase());\n        }\n    }\n    return result;\n}\n\nvoid main() {\n}\n',
    {"only-empty": 'ArrayList<String> shout(ArrayList<String> names) {\n    ArrayList<String> result = new ArrayList<>();\n    for (String name : names) {\n        if (!name.isEmpty()) {\n            result.add(name.toUpperCase());\n        }\n    }\n    return result;\n}\n\nvoid main() {\n}\n'},
    ("Which names should be added, and which skipped? What does strip() do to a name made of spaces?", "Only add when !name.strip().isEmpty()."))

ex.explain("j1-l6.3-explain-choice", "Array or ArrayList?", ["o3"], ["J1.11"],
    "A program collects the words a player types in a word game, until they type `done`. Would you store them in an array or an ArrayList? Explain why.",
    "A full answer chooses an ArrayList, because you don't know in advance how many words there'll be and an ArrayList grows as you add, while an array has a fixed size that must be chosen when it's created.",
    {2: ("Chooses an ArrayList and explains that the number of words isn't known in advance, a list can grow while an array's size is fixed when created.",
         ["An ArrayList, because I don't know how many words the player will type. It grows as I add, but an array has a fixed size set when it's created.",
          "ArrayList. The array would need a size up front, and I can't know how many words there'll be."]),
     1: ("Chooses an ArrayList but the reason is vague or missing.",
         ["ArrayList because it's easier.", "ArrayList is better for words."]),
     0: ("Chooses an array, or gives an incorrect reason.",
         ["An array, because arrays are faster.", "Either works the same way."])})
print("6.3 written")
