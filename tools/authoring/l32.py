from build import *

Lesson("j1-l3.2", "Boolean expressions", ["J1.06"], [
    ("o1", "Write comparisons with <, >, <=, >=, == and !=, and predict whether they are true or false"),
    ("o2", "Combine conditions with && (and), || (or) and ! (not)"),
    ("o3", "Explain short-circuiting: && stops at the first false, || stops at the first true"),
], ["j1-l3.1"], 30, ["R9", "I5"], r'''
## Before you start

You should know the `boolean` type ([Values and types](j1-l2.1)) and how to compare strings with `equals` ([Working with strings](j1-l2.4)).

**Quick check.** What type is `true`, and what type is `"true"`?

<details><summary>Show the answer</summary>

`true` is a `boolean`; `"true"`, in quotes, is a `String`.

</details>

## Explanation

Programs make decisions: *is the password right? is the player old enough? is the basket empty?* Each question has a yes/no answer, a `boolean`. An expression that produces a `boolean` is a **boolean expression**, or **condition**.

### Comparing numbers

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `<` | less than | `3 < 5` | `true` |
| `>` | greater than | `3 > 5` | `false` |
| `<=` | less than or equal to | `5 <= 5` | `true` |
| `>=` | greater than or equal to | `4 >= 5` | `false` |
| `==` | equal to | `5 == 5` | `true` |
| `!=` | not equal to | `5 != 5` | `false` |

Equality is `==`, two equals signs. A single `=` stores a value ([Variables and state](j1-l2.2)). For strings, remember to use `equals`, not `==`.

```java runnable
void main() {
    int age = 17;
    IO.println(age >= 18);
    IO.println(age != 18);
}
```

This prints `false` then `true`.

### Combining conditions

| Operator | Name | True when |
|---|---|---|
| `a && b` | and | **both** `a` and `b` are true |
| `a \|\| b` | or | **at least one** of `a` and `b` is true |
| `!a` | not | `a` is false |

A teenager is someone aged 13 **and** at most 19:

```java
age >= 13 && age <= 19
```

You can't shorten this to `13 <= age <= 19` as in maths: Java works out `13 <= age` first, getting a `boolean`, and then can't compare a `boolean` with 19.

When you mix `&&` and `||`, `&&` is worked out first, like `*` before `+`. Use parentheses to make your meaning clear: `isMember || (age >= 65 && hasCard)`.

### Short-circuiting

Java works out `&&` and `||` from left to right and **stops as soon as it knows the answer**:

- `a && b`: if `a` is false, the whole thing is false, so `b` is never checked.
- `a || b`: if `a` is true, the whole thing is true, so `b` is never checked.

This matters when the second part is only safe if the first part is true:

```java runnable
boolean startsWithA(String word) {
    return word.length() > 0 && word.charAt(0) == 'A';
}

void main() {
    IO.println(startsWithA("Apple"));
    IO.println(startsWithA(""));
}
```

For the empty string, `word.length() > 0` is false, so `charAt(0)`, which would crash on an empty string, never runs. The single-character operators `&` and `|` also mean and/or for booleans, but they **always** check both sides, so they don't protect you this way. Use `&&` and `||` for conditions.

## Worked examples

### Example 1: free entry

*Task: a museum is free for children under 5 and for adults aged 65 and over. Write `isFree(int age)`.*

**Step 1 — Split the rule into simple comparisons.** "Under 5" is `age < 5`. "65 and over" is `age >= 65`.

**Step 2 — Decide how they combine.** Either one makes entry free, so join them with `||`.

**Step 3 — Test the boundaries.** 4 and 5, 64 and 65: those are where mistakes like `<=` instead of `<` show up.

```java runnable
boolean isFree(int age) {
    return age < 5 || age >= 65;
}

void main() {
    IO.println(isFree(4));
    IO.println(isFree(5));
    IO.println(isFree(65));
}
```

This prints `true`, `false`, `true`.

### Example 2: a valid PIN

*Task: a PIN is valid if it has exactly 4 characters and isn't `"0000"`.*

**Step 1 — Write each condition.** `pin.length() == 4`, and `!pin.equals("0000")`.

**Step 2 — Both must hold, so use `&&`.**

```java runnable
boolean isValidPin(String pin) {
    return pin.length() == 4 && !pin.equals("0000");
}

void main() {
    IO.println(isValidPin("1234"));
    IO.println(isValidPin("0000"));
    IO.println(isValidPin("12345"));
}
```

## Predict, then run

::exercise{id=j1-l3.2-predict-conditions}

## Where this is used

- **Sign-up rules**: a password must be at least 8 characters **and** not equal the username.
- **Feature switches**: show the new design if the user is a tester **or** the date is after launch day.
- **Safety checks**: short-circuiting is used everywhere to check that something exists before using it.

## Common mistakes

:::mistake{id=MC14}
**Using `&` or `|` for conditions.** They compute the same true/false result, but always evaluate both sides, so `word.length() > 0 & word.charAt(0) == 'A'` crashes on an empty string. Use `&&` and `||`.
:::

### Off-by-one boundaries

"At least 18" is `>= 18`, not `> 18`. Always test the values right on the boundary.

### Chaining comparisons like maths

`13 <= age <= 19` doesn't compile. Write `age >= 13 && age <= 19`.

## Practice

::exercise{id=j1-l3.2-write-teenager}

::exercise{id=j1-l3.2-write-ride}

::exercise{id=j1-l3.2-debug-month}

::exercise{id=j1-l3.2-debug-initial}

::exercise{id=j1-l3.2-explain-short-circuit}

## Further reading

- **The Java Language Specification, §15.23 "Conditional-And Operator &&"** `[I5]`: the official one-paragraph rule for short-circuiting.

## How you'll be assessed

- The **predict** exercise checks that you can work out conditions (*identifying mistakes*).
- The **write** exercises check that you can turn rules into conditions (*implementation*).
- The **debug** exercises check that you can fix a boundary mistake and an `&` that should be `&&` (*debugging*).
- The **explain** exercise checks that you understand short-circuiting (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l3.2")
ex.predict("j1-l3.2-predict-conditions", "True or false?", ["o1", "o2"], ["J1.06"],
    "Predict whether each line prints `true` or `false`. Work out the comparisons first, then the `&&`, `||` and `!`.",
    '''
    void main() {
        int x = 7;
        IO.println(x > 5);
        IO.println(x >= 7 && x < 7);
        IO.println(x == 3 || x != 3);
        IO.println(!(x > 10));
        IO.println(x % 2 == 0);
    }
    ''', '''
    true
    false
    true
    true
    false
    ''', ("Work out each comparison on its own first, then combine them.",
          "x >= 7 is true but x < 7 is false, so && gives false. x % 2 is 1, so x % 2 == 0 is false."), difficulty=2)

def teen(age): return 13 <= age <= 19
ex.method("write", "j1-l3.2-write-teenager", "Is it a teenager?", ["o1", "o2"], ["J1.06"], ["IMPL"],
    "Complete `isTeenager` so it returns `true` for ages 13 to 19, including both 13 and 19, and `false` otherwise.",
    [("isTeenager", [("age", "int")], "boolean")], {"isTeenager": teen},
    [(None, [15]), (None, [10]), (None, [25])],
    [(None, [13], "exactly 13"), (None, [19], "exactly 19"), (None, [12], "just too young"), (None, [20], "just too old"), (None, [0], "a baby")],
    'boolean isTeenager(int age) {\n    return false; // replace false with your condition\n}\n\nvoid main() {\n    IO.println(isTeenager(15)); // should print true\n}\n',
    'boolean isTeenager(int age) {\n    return age >= 13 && age <= 19;\n}\n\nvoid main() {\n    IO.println(isTeenager(15)); // should print true\n}\n',
    {"exclusive": 'boolean isTeenager(int age) {\n    return age > 13 && age < 19;\n}\n\nvoid main() {\n}\n',
     "or-instead": 'boolean isTeenager(int age) {\n    return age >= 13 || age <= 19;\n}\n\nvoid main() {\n}\n'},
    ("Two conditions must both be true. Which comparison includes the boundary value itself?",
     "age >= 13 && age <= 19"), group="boolean-ranges")

def valid_pct(p): return 0 <= p <= 100
ex.method("write", "j1-l3.2-retrieve-percentage", "A valid percentage", ["o1", "o2"], ["J1.06"], ["IMPL"],
    "Complete `isValidPercentage` so it returns `true` for whole numbers from 0 to 100, including both, and `false` otherwise.",
    [("isValidPercentage", [("value", "int")], "boolean")], {"isValidPercentage": valid_pct},
    [(None, [50]), (None, [-5]), (None, [150])],
    [(None, [0], "exactly 0"), (None, [100], "exactly 100"), (None, [101], "just over"), (None, [-1], "just under"), (None, [1], "one")],
    'boolean isValidPercentage(int value) {\n    return false; // replace false with your condition\n}\n\nvoid main() {\n    IO.println(isValidPercentage(50)); // should print true\n}\n',
    'boolean isValidPercentage(int value) {\n    return value >= 0 && value <= 100;\n}\n\nvoid main() {\n    IO.println(isValidPercentage(50)); // should print true\n}\n',
    {"exclusive": 'boolean isValidPercentage(int value) {\n    return value > 0 && value < 100;\n}\n\nvoid main() {\n}\n'},
    ("Both limits are allowed. Which operators include the boundary?", "value >= 0 && value <= 100"),
    role="retrieval", group="boolean-ranges")

def working(age): return 16 <= age <= 66
ex.method("write", "j1-l3.2-retrieve-working-age", "Working age", ["o1", "o2"], ["J1.06"], ["IMPL"],
    "Complete `isWorkingAge` so it returns `true` for ages 16 to 66, including both, and `false` otherwise.",
    [("isWorkingAge", [("age", "int")], "boolean")], {"isWorkingAge": working},
    [(None, [30]), (None, [10]), (None, [70])],
    [(None, [16], "exactly 16"), (None, [66], "exactly 66"), (None, [15], "just too young"), (None, [67], "just too old"), (None, [40], "middle")],
    'boolean isWorkingAge(int age) {\n    return false; // replace false with your condition\n}\n\nvoid main() {\n    IO.println(isWorkingAge(30)); // should print true\n}\n',
    'boolean isWorkingAge(int age) {\n    return age >= 16 && age <= 66;\n}\n\nvoid main() {\n    IO.println(isWorkingAge(30)); // should print true\n}\n',
    {"exclusive": 'boolean isWorkingAge(int age) {\n    return age > 16 && age < 66;\n}\n\nvoid main() {\n}\n'},
    ("Both limits are allowed. Which operators include the boundary?", "age >= 16 && age <= 66"),
    role="retrieval", group="boolean-ranges")

def can_ride(height, with_adult): return height >= 120 or (height >= 100 and with_adult)
ex.method("write", "j1-l3.2-write-ride", "The rollercoaster rule", ["o2"], ["J1.06"], ["IMPL"],
    "A rollercoaster lets you ride if you're at least 120 cm tall, **or** if you're at least 100 cm tall **and** riding with an adult. Complete `canRide`.",
    [("canRide", [("heightCm", "int"), ("withAdult", "boolean")], "boolean")], {"canRide": can_ride},
    [(None, [130, False]), (None, [110, True]), (None, [110, False])],
    [(None, [120, False], "exactly 120 alone"), (None, [100, True], "exactly 100 with an adult"), (None, [99, True], "too short even with an adult"),
     (None, [150, True], "tall with an adult"), (None, [119, False], "just too short alone")],
    'boolean canRide(int heightCm, boolean withAdult) {\n    return false; // replace false with your condition\n}\n\nvoid main() {\n    IO.println(canRide(110, true)); // should print true\n}\n',
    'boolean canRide(int heightCm, boolean withAdult) {\n    return heightCm >= 120 || (heightCm >= 100 && withAdult);\n}\n\nvoid main() {\n    IO.println(canRide(110, true)); // should print true\n}\n',
    {"forgot-adult": 'boolean canRide(int heightCm, boolean withAdult) {\n    return heightCm >= 100;\n}\n\nvoid main() {\n}\n',
     "and-instead": 'boolean canRide(int heightCm, boolean withAdult) {\n    return heightCm >= 120 && heightCm >= 100 && withAdult;\n}\n\nvoid main() {\n}\n'},
    ("There are two ways to be allowed on. Write each as a condition, then join them.",
     "heightCm >= 120 || (heightCm >= 100 && withAdult)"))

def valid_month(m): return 1 <= m <= 12
ex.method("debug", "j1-l3.2-debug-month", "January and December", ["o1"], ["J1.06"], ["DEBUG"],
    "`isValidMonth` should accept month numbers 1 to 12. Users report that January and December are rejected. Find and fix the bug.",
    [("isValidMonth", [("month", "int")], "boolean")], {"isValidMonth": valid_month},
    [(None, [6]), (None, [1]), (None, [12])],
    [(None, [0], "zero"), (None, [13], "thirteen"), (None, [2], "February"), (None, [11], "November"), (None, [-1], "negative")],
    'boolean isValidMonth(int month) {\n    return month > 1 && month < 12;\n}\n\nvoid main() {\n    IO.println(isValidMonth(1)); // should print true\n}\n',
    'boolean isValidMonth(int month) {\n    return month >= 1 && month <= 12;\n}\n\nvoid main() {\n    IO.println(isValidMonth(1)); // should print true\n}\n',
    {"half-fixed": 'boolean isValidMonth(int month) {\n    return month >= 1 && month < 12;\n}\n\nvoid main() {\n}\n'},
    ("Try the boundary values 1 and 12 by hand. Is 1 > 1?", "Use >= 1 and <= 12 so the boundary months are included."))

def starts_a(word): return len(word) > 0 and word[0] == "A"
ex.method("debug", "j1-l3.2-debug-initial", "The empty name crash", ["o3"], ["J1.06"], ["DEBUG"],
    "`startsWithA` should return `true` if a word begins with a capital A, and `false` otherwise, including for an empty word. It crashes when given `\"\"`. Find and fix the bug.",
    [("startsWithA", [("word", "String")], "boolean")], {"startsWithA": starts_a},
    [(None, ["Apple"]), (None, ["banana"]), (None, [""])],
    [(None, ["A"], "just A"), (None, ["apple"], "lower-case a"), (None, ["Zebra"], "another letter"), (None, ["Aardvark"], "double A"), (None, [" A"], "space first")],
    "boolean startsWithA(String word) {\n    return word.length() > 0 & word.charAt(0) == 'A';\n}\n\nvoid main() {\n    IO.println(startsWithA(\"\")); // should print false\n}\n",
    "boolean startsWithA(String word) {\n    return word.length() > 0 && word.charAt(0) == 'A';\n}\n\nvoid main() {\n    IO.println(startsWithA(\"\")); // should print false\n}\n",
    {"swapped-order": "boolean startsWithA(String word) {\n    return word.charAt(0) == 'A' && word.length() > 0;\n}\n\nvoid main() {\n}\n"},
    ("For an empty word, which part of the condition crashes? Should it ever run?",
     "& always checks both sides. && stops when the left side is false, so charAt(0) never runs on an empty word."),
    misconceptions=["MC14"])

ex.explain("j1-l3.2-explain-short-circuit", "Order matters", ["o3"], ["J1.06"],
    "These two conditions look the same, but the second one crashes for an empty word. Explain why.\n\n```java\nword.length() > 0 && word.charAt(0) == 'A'\nword.charAt(0) == 'A' && word.length() > 0\n```",
    "A full answer says && is checked left to right and stops at the first false (short-circuit); in the first version an empty word makes the length check false so charAt(0) is never run; in the second, charAt(0) runs first on an empty word and crashes because there's no character at index 0.",
    {2: ("Explains short-circuiting (&& stops at the first false, left to right) and why the order means charAt(0) runs on an empty word only in the second version, causing the crash.",
         ["&& goes left to right and stops when it finds false. In the first one, an empty word fails the length check so charAt(0) is skipped. In the second, charAt(0) runs first, and there is no index 0 in an empty string, so it crashes.",
          "Short-circuiting: if the left of && is false, the right is never checked. Putting the length check first protects charAt; putting it second means charAt runs on \"\" and throws an error."]),
     1: ("Says the second one checks charAt first, or that charAt fails on an empty word, but doesn't explain that && skips the right side when the left is false.",
         ["Because charAt(0) doesn't work on an empty word.", "The second one checks the character before the length."]),
     0: ("Incorrect, for example says the conditions are identical, or blames the capital A.",
         ["They're the same, the crash must be somewhere else.", "It crashes because 'A' should be in double quotes."])})
print("3.2 written")
