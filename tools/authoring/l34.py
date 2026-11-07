from build import *

Lesson("j1-l3.4", "switch expressions", ["J1.06"], [
    ("o1", "Write a switch expression that picks a value for each case, with a default"),
    ("o2", "Group several values into one case with commas"),
    ("o3", "Choose between switch and an else-if chain for a problem"),
], ["j1-l3.3"], 30, ["I5"], r'''
## Before you start

You should be able to write else-if chains ([Making decisions](j1-l3.3)).

**Quick check.** In an else-if chain, how many branches run?

<details><summary>Show the answer</summary>

At most one: the first one whose condition is true (or the `else` if none are).

</details>

## Explanation

Some decisions compare one value against a list of exact possibilities: *1 means Monday, 2 means Tuesday, …*. An else-if chain works, but it repeats `day ==` on every line. A **switch expression** says it more directly.

### A switch expression

```java runnable
String dayName(int day) {
    return switch (day) {
        case 1 -> "Monday";
        case 2 -> "Tuesday";
        case 3 -> "Wednesday";
        case 4 -> "Thursday";
        case 5 -> "Friday";
        case 6 -> "Saturday";
        case 7 -> "Sunday";
        default -> "Unknown";
    };
}

void main() {
    IO.println(dayName(3));
    IO.println(dayName(9));
}
```

Read it as: *look at `day`; if it's 1, the value is `"Monday"`; if it's 2, …; for anything else, `"Unknown"`*.

- `switch (day)` names the value being checked.
- Each `case value -> result;` gives the result for one value.
- `default ->` covers every value not listed.
- The whole switch **is a value**, so you can `return` it or store it in a variable. Notice the semicolon after the closing brace: it ends the `return` statement.

### `default` is required

A switch expression must produce a value for **every** possible input. For an `int`, you can't list them all, so you need `default`. Without it, Java won't compile the program:

```
error: the switch expression does not cover all possible input values
```

### Several values in one case

Separate values with commas when they share a result:

```java
String dayType(int day) {
    return switch (day) {
        case 1, 2, 3, 4, 5 -> "weekday";
        case 6, 7 -> "weekend";
        default -> "unknown";
    };
}
```

### Switching on strings and characters

You can switch on a `String` or a `char` as well. Unlike `==`, a switch on strings compares the **characters**, so it behaves like `equals`:

```java runnable
int menuPrice(String item) {
    return switch (item) {
        case "tea", "coffee" -> 3;
        case "cake" -> 4;
        default -> 0;
    };
}

void main() {
    IO.println(menuPrice("coffee"));
    IO.println(menuPrice("soup"));
}
```

### switch or else-if?

Use a **switch** when you compare one value against **exact** values (1, 2, 3 or `"tea"`, `"cake"`). Use an **else-if chain** when the conditions are **ranges** or combinations, like `score >= 70` or `age < 12 || age >= 65`: a `case` can't say "70 or more".

## Worked examples

### Example 1: days in a month

*Task: return how many days a month has (ignore leap years). Months are numbered 1 to 12.*

**Step 1 — Group the months by answer.** 31 days: 1, 3, 5, 7, 8, 10, 12. 30 days: 4, 6, 9, 11. 28 days: 2.

**Step 2 — One case per group,** with commas.

**Step 3 — Decide what `default` means.** Any other number isn't a month; return 0.

```java runnable
int daysInMonth(int month) {
    return switch (month) {
        case 1, 3, 5, 7, 8, 10, 12 -> 31;
        case 4, 6, 9, 11 -> 30;
        case 2 -> 28;
        default -> 0;
    };
}

void main() {
    IO.println(daysInMonth(2) + " " + daysInMonth(9) + " " + daysInMonth(12));
}
```

This prints `28 30 31`.

### Example 2: vowel or consonant

*Task: for a lower-case letter, return `"vowel"` or `"consonant"`.*

**Step 1 — The exact values are the vowels:** `'a'`, `'e'`, `'i'`, `'o'`, `'u'`.

**Step 2 — Everything else is a consonant,** so that's the `default`.

```java runnable
String letterType(char letter) {
    return switch (letter) {
        case 'a', 'e', 'i', 'o', 'u' -> "vowel";
        default -> "consonant";
    };
}

void main() {
    IO.println(letterType('e') + " " + letterType('z'));
}
```

## Predict, then run

::exercise{id=j1-l3.4-predict-switch}

## Where this is used

- **Menus and commands**: `"save"`, `"open"` and `"quit"` each map to an action.
- **Codes and statuses**: shipping codes, error codes and file types are usually looked up with a switch.
- **Games**: a pressed key (`'w'`, `'a'`, `'s'`, `'d'`) maps to a direction.

## Common mistakes

### Forgetting `default`

A switch expression on an `int` or `String` must have a `default`, or it won't compile.

### Trying to use a range in a case

`case >= 70` isn't allowed. Ranges need an else-if chain.

### Forgetting the semicolon after the closing brace

`return switch (x) { … };` ends with `};` because the whole switch is part of a `return` statement.

## Practice

::exercise{id=j1-l3.4-write-day}

::exercise{id=j1-l3.4-debug-default}

::exercise{id=j1-l3.4-modify-closed}

::exercise{id=j1-l3.4-explain-choice}

## Version notes

The arrow form of `switch` (`case 1 ->`) became a standard part of Java in **Java 14**. Older code uses a different form, with `case 1:` and `break;` after each case. That form lets execution "fall through" into the next case if you forget `break`, which causes bugs. If you meet it, the ideas are the same; the arrow form is just safer.

## Further reading

- **The Java Language Specification, §15.28 "switch Expressions"** `[I5]`: the precise rules, including why `default` is needed.

## How you'll be assessed

- The **predict** exercise checks that you can follow a switch (*identifying mistakes*).
- The **write** exercise checks that you can write one (*implementation*).
- The **debug**, **modify** and **explain** exercises check that you can fix a missing `default`, change the cases, and choose between switch and else-if.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''', features=[("switch expressions", 14)])

ex = Exercises("j1-l3.4")
ex.predict("j1-l3.4-predict-switch", "Which case?", ["o1", "o2"], ["J1.06"],
    "Predict exactly what this program prints.",
    '''
    String sizeOf(int code) {
        return switch (code) {
            case 1, 2 -> "small";
            case 3 -> "medium";
            case 4, 5, 6 -> "large";
            default -> "unknown";
        };
    }

    void main() {
        IO.println(sizeOf(2));
        IO.println(sizeOf(5));
        IO.println(sizeOf(0));
        IO.println(sizeOf(3) + "!");
    }
    ''', '''
    small
    large
    unknown
    medium!
    ''', ("Find the case that lists the value. If none does, it's the default.",
          "2 is in the first case, 5 in the third, and 0 isn't listed anywhere, so it's the default."))

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
def day_name(d): return DAYS[d - 1] if 1 <= d <= 7 else "Unknown"
switch_days = 'String dayName(int day) {\n    return switch (day) {\n' + ''.join(f'        case {i + 1} -> "{n}";\n' for i, n in enumerate(DAYS)) + '        default -> "Unknown";\n    };\n}\n'
ex.method("write", "j1-l3.4-write-day", "Day names", ["o1"], ["J1.06"], ["IMPL"],
    "Complete `dayName` with a switch expression: 1 is `\"Monday\"` through to 7, `\"Sunday\"`. Any other number gives `\"Unknown\"`.",
    [("dayName", [("day", "int")], "String")], {"dayName": day_name},
    [(None, [1]), (None, [5]), (None, [0])],
    [(None, [7], "Sunday"), (None, [2], "Tuesday"), (None, [6], "Saturday"), (None, [8], "too big"), (None, [-1], "negative")],
    'String dayName(int day) {\n    return ""; // replace this with a switch expression\n}\n\nvoid main() {\n    IO.println(dayName(1)); // should print Monday\n}\n',
    switch_days + '\nvoid main() {\n    IO.println(dayName(1)); // should print Monday\n}\n',
    {"starts-at-zero": 'String dayName(int day) {\n    return switch (day) {\n' + ''.join(f'        case {i} -> "{n}";\n' for i, n in enumerate(DAYS)) + '        default -> "Unknown";\n    };\n}\n\nvoid main() {\n}\n'},
    ("One case per day, and a default for everything else.", "return switch (day) { case 1 -> \"Monday\"; … case 7 -> \"Sunday\"; default -> \"Unknown\"; };"),
    group="switch-mapping")

def dim(m): return 31 if m in (1, 3, 5, 7, 8, 10, 12) else 30 if m in (4, 6, 9, 11) else 28 if m == 2 else 0
ex.method("write", "j1-l3.4-retrieve-days", "Days in a month", ["o1", "o2"], ["J1.06"], ["IMPL"],
    "Complete `daysInMonth` with a switch expression. Ignore leap years: February has 28 days. April, June, September and November have 30; the other months have 31. Any number that isn't a month (1 to 12) gives 0.",
    [("daysInMonth", [("month", "int")], "int")], {"daysInMonth": dim},
    [(None, [1]), (None, [4]), (None, [2])],
    [(None, [12], "December"), (None, [11], "November"), (None, [8], "August"), (None, [13], "not a month"), (None, [0], "zero")],
    'int daysInMonth(int month) {\n    return 0; // replace this with a switch expression\n}\n\nvoid main() {\n    IO.println(daysInMonth(2)); // should print 28\n}\n',
    'int daysInMonth(int month) {\n    return switch (month) {\n        case 1, 3, 5, 7, 8, 10, 12 -> 31;\n        case 4, 6, 9, 11 -> 30;\n        case 2 -> 28;\n        default -> 0;\n    };\n}\n\nvoid main() {\n    IO.println(daysInMonth(2)); // should print 28\n}\n',
    {"august-30": 'int daysInMonth(int month) {\n    return switch (month) {\n        case 1, 3, 5, 7, 10, 12 -> 31;\n        case 4, 6, 8, 9, 11 -> 30;\n        case 2 -> 28;\n        default -> 0;\n    };\n}\n\nvoid main() {\n}\n'},
    ("Group the months by how many days they have, one case per group.", "case 1, 3, 5, 7, 8, 10, 12 -> 31; case 4, 6, 9, 11 -> 30; case 2 -> 28; default -> 0;"),
    role="retrieval", group="switch-mapping")

def letter_type(c): return "vowel" if c in "aeiou" else "consonant"
ex.method("write", "j1-l3.4-retrieve-letters", "Vowel or consonant", ["o1", "o2"], ["J1.06"], ["IMPL"],
    "Complete `letterType` with a switch expression. For a lower-case letter, return `\"vowel\"` for a, e, i, o and u, and `\"consonant\"` for any other letter.",
    [("letterType", [("letter", "char")], "String")], {"letterType": letter_type},
    [(None, ["a"]), (None, ["b"]), (None, ["u"])],
    [(None, ["e"], "e"), (None, ["i"], "i"), (None, ["o"], "o"), (None, ["z"], "z"), (None, ["y"], "y")],
    'String letterType(char letter) {\n    return ""; // replace this with a switch expression\n}\n\nvoid main() {\n    IO.println(letterType(\'a\')); // should print vowel\n}\n',
    "String letterType(char letter) {\n    return switch (letter) {\n        case 'a', 'e', 'i', 'o', 'u' -> \"vowel\";\n        default -> \"consonant\";\n    };\n}\n\nvoid main() {\n    IO.println(letterType('a')); // should print vowel\n}\n",
    {"missing-u": "String letterType(char letter) {\n    return switch (letter) {\n        case 'a', 'e', 'i', 'o' -> \"vowel\";\n        default -> \"consonant\";\n    };\n}\n\nvoid main() {\n}\n"},
    ("The vowels share one case; everything else is the default.", "case 'a', 'e', 'i', 'o', 'u' -> \"vowel\"; default -> \"consonant\";"),
    role="retrieval", group="switch-mapping")

def medal(p): return {1: "gold", 2: "silver", 3: "bronze"}.get(p, "none")
ex.method("debug", "j1-l3.4-debug-default", "The missing medal", ["o1"], ["J1.06"], ["DEBUG"],
    "`medal` should return `\"gold\"`, `\"silver\"` or `\"bronze\"` for places 1, 2 and 3, and `\"none\"` for any other place. It doesn't compile. Read the error and fix it.",
    [("medal", [("place", "int")], "String")], {"medal": medal},
    [(None, [1]), (None, [3]), (None, [4])],
    [(None, [2], "second"), (None, [0], "zero"), (None, [10], "tenth"), (None, [-1], "negative"), (None, [5], "fifth")],
    'String medal(int place) {\n    return switch (place) {\n        case 1 -> "gold";\n        case 2 -> "silver";\n        case 3 -> "bronze";\n    };\n}\n\nvoid main() {\n    IO.println(medal(4)); // should print none\n}\n',
    'String medal(int place) {\n    return switch (place) {\n        case 1 -> "gold";\n        case 2 -> "silver";\n        case 3 -> "bronze";\n        default -> "none";\n    };\n}\n\nvoid main() {\n    IO.println(medal(4)); // should print none\n}\n',
    {"default-empty": 'String medal(int place) {\n    return switch (place) {\n        case 1 -> "gold";\n        case 2 -> "silver";\n        case 3 -> "bronze";\n        default -> "";\n    };\n}\n\nvoid main() {\n}\n'},
    ("Read the error: what does Java say the switch doesn't do?", "Add default -> \"none\"; as the last case."),
    starter_compiles=False)

def day_type(d): return "closed" if d == 3 else "weekday" if d in (1, 2, 4, 5) else "weekend" if d in (6, 7) else "unknown"
ex.method("modify", "j1-l3.4-modify-closed", "Closed on Wednesdays", ["o2"], ["J1.06"], ["MOD"],
    "A shop's app labels each day (1 = Monday … 7 = Sunday). The shop now closes on Wednesdays, so day 3 should give `\"closed\"`. Every other day keeps its label.",
    [("dayType", [("day", "int")], "String")], {"dayType": day_type},
    [(None, [3]), (None, [1]), (None, [6])],
    [(None, [2], "Tuesday"), (None, [4], "Thursday"), (None, [5], "Friday"), (None, [7], "Sunday"), (None, [0], "not a day")],
    'String dayType(int day) {\n    return switch (day) {\n        case 1, 2, 3, 4, 5 -> "weekday";\n        case 6, 7 -> "weekend";\n        default -> "unknown";\n    };\n}\n\nvoid main() {\n    IO.println(dayType(3));\n}\n',
    'String dayType(int day) {\n    return switch (day) {\n        case 1, 2, 4, 5 -> "weekday";\n        case 3 -> "closed";\n        case 6, 7 -> "weekend";\n        default -> "unknown";\n    };\n}\n\nvoid main() {\n    IO.println(dayType(3));\n}\n',
    {"all-weekdays-closed": 'String dayType(int day) {\n    return switch (day) {\n        case 1, 2, 3, 4, 5 -> "closed";\n        case 6, 7 -> "weekend";\n        default -> "unknown";\n    };\n}\n\nvoid main() {\n}\n'},
    ("Day 3 needs its own case. What else must change so 3 isn't listed twice?",
     "Remove 3 from the weekday case and add case 3 -> \"closed\";"))

ex.explain("j1-l3.4-explain-choice", "switch or else-if?", ["o3"], ["J1.06"],
    "A shop gives 10% off orders of £50 or more and 20% off orders of £100 or more. Would you write this with a switch or an else-if chain? Explain why.",
    "A full answer chooses an else-if chain, because the rule depends on ranges (50 or more, 100 or more), and switch cases can only match exact values.",
    {2: ("Chooses else-if and explains that the conditions are ranges, which switch cases can't express because they match exact values.",
         ["An else-if chain, because the discounts depend on ranges like 'at least 50'. A switch can only match exact values, like case 50, so it can't say 'or more'.",
          "else-if. switch is for exact values, and you can't list every possible order total. Ranges like >= 100 need if conditions."]),
     1: ("Chooses else-if but the reason is vague or missing, or mentions ranges without saying switch only handles exact values.",
         ["else-if, because it's easier.", "An if chain because there are only two discounts."]),
     0: ("Chooses switch, or gives an incorrect reason.",
         ["A switch, with case 50 and case 100.", "switch, because it's always better than if."])})
print("3.4 written")
