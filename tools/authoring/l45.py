from build import *

Lesson("j1-l4.5", "Input validation loops", ["J1.05", "J1.07"], [
    ("o1", "Repeat a prompt in a loop until the person types something acceptable"),
    ("o2", "Check that text is made of digits before converting it with Integer.parseInt"),
    ("o3", "Combine a digit check and a range check, in the right order"),
], ["j1-l4.4"], 35, ["R8", "I4"], r'''
## Before you start

You should be able to read and convert input ([Reading input](j1-l3.1)) and write loops over the characters of a string ([Loop patterns](j1-l4.4)).

**Quick check.** What happens if a program calls `Integer.parseInt("ten")`?

<details><summary>Show the answer</summary>

It stops with a `NumberFormatException`, because `"ten"` isn't a whole number.

</details>

## Explanation

People mistype. A program that crashes on `4m` instead of `4` isn't much use. **Validation** means checking input before you trust it, and a loop lets you ask again until you get something acceptable.

### Ask again until it's valid

```java
void main() {
    String name = "";
    while (name.isEmpty()) {
        name = IO.readln("Your name: ").strip();
        if (name.isEmpty()) {
            IO.println("Please type something.");
        }
    }
    IO.println("Hello, " + name + "!");
}
```

The pattern: start with a value that fails the check, loop **while** the value is bad, and read a new one inside the loop. When the person types something acceptable, the condition becomes false and the loop ends.

`strip()` removes spaces at both ends, so a line of only spaces counts as empty.

### Checking that text is a number

You can't check a number by calling `Integer.parseInt` and hoping: that crashes on bad text. Instead, check the **characters first**, using the loop pattern from the last lesson. `Character.isDigit(c)` is true for `'0'` to `'9'`:

```java runnable
boolean isWholeNumber(String text) {
    if (text.isEmpty()) {
        return false;
    }
    for (int i = 0; i < text.length(); i++) {
        if (!Character.isDigit(text.charAt(i))) {
            return false;
        }
    }
    return true;
}

void main() {
    IO.println(isWholeNumber("4071"));
    IO.println(isWholeNumber("4m"));
    IO.println(isWholeNumber(""));
}
```

This prints `true`, `false`, `false`. It's the find-the-first pattern turned round: *return false as soon as one character isn't a digit*. The empty-text check matters, because an empty string has no characters to fail on and would otherwise count as a number.

This check accepts digits only, so `-5` and `2.5` are rejected. That's fine for ages and counts.

### Order matters: digits, then range

To accept ages from 0 to 120, check in this order:

1. Is it digits only? (If not, don't even try to convert it.)
2. Is it short enough to convert safely? A text of 20 digits is too big for an `int`, so limit the length.
3. Is the number in range?

With `&&`, Java stops at the first false ([Boolean expressions](j1-l3.2)), so `Integer.parseInt` only runs on safe text:

```java
isWholeNumber(typed) && typed.length() <= 3 && Integer.parseInt(typed) <= 120
```

### When the input ends

`IO.readln` returns `null` when there's no more input at all. In this course's tests, the input always contains a valid answer eventually, so you don't need to handle that.

## Worked examples

### Example 1: a number from 1 to 10

*Task: keep asking `Pick 1-10: ` until the person types a whole number from 1 to 10, then print `You picked N`.*

**Step 1 — Start with a value that fails.** `int pick = 0;` isn't in range, so the loop runs at least once.

**Step 2 — Loop while it's still invalid.** `while (pick == 0)`.

**Step 3 — Inside, read, check in order, and either accept or complain.**

```java
void main() {
    int pick = 0;
    while (pick == 0) {
        String typed = IO.readln("Pick 1-10: ").strip();
        if (isWholeNumber(typed) && typed.length() <= 2 && Integer.parseInt(typed) >= 1 && Integer.parseInt(typed) <= 10) {
            pick = Integer.parseInt(typed);
        } else {
            IO.println("That's not a whole number from 1 to 10.");
        }
    }
    IO.println("You picked " + pick);
}
```

(`isWholeNumber` is the method from above.) With the typed lines `eleven`, `11`, `7`, the program complains twice and then prints `You picked 7`.

**Step 4 — Test the edges.** `0`, `1`, `10` and `11`.

## Predict, then run

::exercise{id=j1-l4.5-predict-check}

## Where this is used

- **Every form on the web** checks input before using it: email addresses, card numbers, dates.
- **Security**: unchecked input is behind a huge share of real-world attacks, so checking it is a core professional habit.
- **Friendly programs**: asking again is much kinder than crashing.

## Common mistakes

### Converting before checking

`Integer.parseInt(typed)` on unchecked text crashes the program. Always check the text is digits first.

### Forgetting the empty text

Without the `isEmpty()` check, `""` passes the digit loop, and `parseInt("")` then crashes.

### A loop that can never exit

If the start value already passes the condition, the loop never runs; if the body never changes it, the loop never ends. Trace the first pass.

## Practice

::exercise{id=j1-l4.5-write-age}

::exercise{id=j1-l4.5-debug-limit}

::exercise{id=j1-l4.5-explain-order}

## Further reading

- **Java SE 25 API documentation for `Character.isDigit`** `[I4]`: what it accepts, including digits from other alphabets, which is why this course says "digits" rather than "0 to 9".

## How you'll be assessed

- The **predict** exercise checks that you can follow a digit check.
- The **write** exercises check that you can build a validation loop on your own (*implementation*).
- The **debug** exercise checks that you can fix a boundary (*debugging*), and **explain** that you know why the checks come in that order.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

HELPER = '''boolean isWholeNumber(String text) {
    if (text.isEmpty()) {
        return false;
    }
    for (int i = 0; i < text.length(); i++) {
        if (!Character.isDigit(text.charAt(i))) {
            return false;
        }
    }
    return true;
}
'''

ex = Exercises("j1-l4.5")
ex.predict("j1-l4.5-predict-check", "Is it a number?", ["o2"], ["J1.05"],
    "Predict exactly what this program prints. Think about which texts pass the digit check.",
    HELPER + '''
void main() {
    IO.println(isWholeNumber("120"));
    IO.println(isWholeNumber("12 0"));
    IO.println(isWholeNumber("-5"));
    IO.println(isWholeNumber(""));
    IO.println(isWholeNumber("007"));
}
''', '''
true
false
false
false
true
''', ("A text passes only if it's not empty and every character is a digit.",
      "A space and a minus sign aren't digits. \"007\" is all digits, so it passes."), difficulty=2)

def make(lo, hi, prompt, ok_label, id_, title, role, group, maxlen):
    def fn(stdin):
        bad = False
        for line in stdin.split("\n")[:-1]:
            t = line.strip()
            if t.isascii() and t.isdigit() and len(t) <= maxlen and lo <= int(t) <= hi:
                frags = [f"{ok_label}{int(t)}"]
                if bad:
                    frags.append(f"Please enter a whole number from {lo} to {hi}.")
                return frags
            bad = True
        raise ValueError("no valid line")
    visible = [("valid first time", f"{(lo + hi) // 2}\n"), ("one bad then good", f"abc\n{hi}\n"), ("range edge", f"{hi + 1}\n{lo}\n")]
    hidden = [("empty line first", f"\n{lo}\n"), ("negative then good", f"-3\n{lo}\n"), ("decimal then good", f"2.5\n{hi}\n"),
              ("several bad", f"x\n{hi + 50}\n 7 7\n{hi}\n"), ("spaces around", f"  {lo}  \n"), ("huge number", f"99999999999999999999\n{hi}\n")]
    starter = HELPER + f'\nvoid main() {{\n    // Keep asking "{prompt}" until the input is valid, then print the result.\n}}\n'
    solution = HELPER + f'''
void main() {{
    int value = -1;
    while (value < 0) {{
        String typed = IO.readln("{prompt}").strip();
        if (isWholeNumber(typed) && typed.length() <= {maxlen} && Integer.parseInt(typed) >= {lo} && Integer.parseInt(typed) <= {hi}) {{
            value = Integer.parseInt(typed);
        }} else {{
            IO.println("Please enter a whole number from {lo} to {hi}.");
        }}
    }}
    IO.println("{ok_label}" + value);
}}
'''
    no_check = HELPER + f'\nvoid main() {{\n    int value = Integer.parseInt(IO.readln("{prompt}").strip());\n    IO.println("{ok_label}" + value);\n}}\n'
    no_range = HELPER + f'''
void main() {{
    String typed = "";
    while (!isWholeNumber(typed) || typed.length() > {maxlen}) {{
        typed = IO.readln("{prompt}").strip();
        if (!isWholeNumber(typed) || typed.length() > {maxlen}) {{
            IO.println("Please enter a whole number from {lo} to {hi}.");
        }}
    }}
    IO.println("{ok_label}" + Integer.parseInt(typed));
}}
'''
    return dict(program_fn=fn, visible=visible, hidden=hidden, starter=starter, solution=solution,
                wrongs={"no-validation": no_check, "no-range-check": no_range})

a = make(0, 120, "Age (0-120): ", "Age accepted: ", "j1-l4.5-write-age", "Ask for an age", "ladder", "validation-loop", 3)
ex.io("write", "j1-l4.5-write-age", "Ask for an age", ["o1", "o2", "o3"], ["J1.05", "J1.07"], ["IMPL"],
    "Write `main` so it keeps asking `Age (0-120): ` until the person types a whole number from 0 to 120. Each time the input is bad, print `Please enter a whole number from 0 to 120.` When it's good, print `Age accepted: N`.\n\nThe `isWholeNumber` method is already there for you. Check the text is a number **before** converting it.",
    a["program_fn"], a["visible"], a["hidden"], a["starter"], a["solution"], a["wrongs"],
    ("Loop while you don't yet have a valid value, and check the text before converting it.",
     "Start with int value = -1; while (value < 0) { read, strip; if isWholeNumber && short && in range → convert, else print the message }."),
    contains=True, difficulty=3, group="validation-loop")

p = make(0, 100, "Percentage: ", "Percentage accepted: ", "", "", "", "", 3)
ex.io("write", "j1-l4.5-retrieve-percentage", "Ask for a percentage", ["o1", "o2", "o3"], ["J1.05", "J1.07"], ["IMPL"],
    "Write `main` so it keeps asking `Percentage: ` until the person types a whole number from 0 to 100. Each time the input is bad, print `Please enter a whole number from 0 to 100.` When it's good, print `Percentage accepted: N`. `isWholeNumber` is provided.",
    p["program_fn"], p["visible"], p["hidden"], p["starter"], p["solution"], p["wrongs"],
    ("Loop until valid; check the digits before converting.", "Same shape as asking for an age, with a different range and messages."),
    contains=True, difficulty=3, role="retrieval", group="validation-loop")

q = make(2, 6, "Players (2-6): ", "Players accepted: ", "", "", "", "", 1)
ex.io("write", "j1-l4.5-retrieve-players", "Ask for the players", ["o1", "o2", "o3"], ["J1.05", "J1.07"], ["IMPL"],
    "Write `main` so it keeps asking `Players (2-6): ` until the person types a whole number from 2 to 6. Each time the input is bad, print `Please enter a whole number from 2 to 6.` When it's good, print `Players accepted: N`. `isWholeNumber` is provided.",
    q["program_fn"], q["visible"], q["hidden"], q["starter"], q["solution"], q["wrongs"],
    ("Loop until valid; check the digits before converting.", "Same shape as asking for an age, with the range 2 to 6."),
    contains=True, difficulty=3, role="retrieval", group="validation-loop")

def debug_fn(stdin):
    for line in stdin.split("\n")[:-1]:
        t = line.strip()
        if t.isascii() and t.isdigit() and len(t) <= 3 and 1 <= int(t) <= 31:
            return [f"Day accepted: {int(t)}"]
    raise ValueError
ex.io("debug", "j1-l4.5-debug-limit", "Days of the month", ["o3"], ["J1.07"], ["DEBUG"],
    "This program asks for a day of the month (1 to 31). People report that it won't accept 31. Find and fix the bug.",
    debug_fn, [("middle", "15\n"), ("first day", "1\n"), ("last day", "31\n")],
    [("too big then good", "32\n31\n"), ("zero then good", "0\n1\n"), ("text then good", "x\n30\n"), ("empty then good", "\n2\n"), ("spaces", " 31 \n")],
    HELPER + '''
void main() {
    int day = 0;
    while (day == 0) {
        String typed = IO.readln("Day (1-31): ").strip();
        if (isWholeNumber(typed) && typed.length() <= 3 && Integer.parseInt(typed) >= 1 && Integer.parseInt(typed) < 31) {
            day = Integer.parseInt(typed);
        } else {
            IO.println("Please enter a whole number from 1 to 31.");
        }
    }
    IO.println("Day accepted: " + day);
}
''', HELPER + '''
void main() {
    int day = 0;
    while (day == 0) {
        String typed = IO.readln("Day (1-31): ").strip();
        if (isWholeNumber(typed) && typed.length() <= 3 && Integer.parseInt(typed) >= 1 && Integer.parseInt(typed) <= 31) {
            day = Integer.parseInt(typed);
        } else {
            IO.println("Please enter a whole number from 1 to 31.");
        }
    }
    IO.println("Day accepted: " + day);
}
''', {"accepts-too-much": HELPER + '''
void main() {
    int day = 0;
    while (day == 0) {
        String typed = IO.readln("Day (1-31): ").strip();
        if (isWholeNumber(typed) && typed.length() <= 3 && Integer.parseInt(typed) >= 1) {
            day = Integer.parseInt(typed);
        } else {
            IO.println("Please enter a whole number from 1 to 31.");
        }
    }
    IO.println("Day accepted: " + day);
}
'''},
    ("Try the boundary value 31 by hand. Is 31 < 31?", "Use <= 31 so the last day is included."), contains=True)

ex.explain("j1-l4.5-explain-order", "Digits before parseInt", ["o2", "o3"], ["J1.05", "J1.07"],
    "In a validation check like `isWholeNumber(typed) && Integer.parseInt(typed) <= 120`, why must the digit check come first? What would happen the other way round if someone typed `abc`?",
    "A full answer says Integer.parseInt crashes (NumberFormatException) on text that isn't a number, and && stops at the first false, so putting the digit check first means parseInt only runs on safe text; the other way round, abc would reach parseInt and crash.",
    {2: ("Explains that parseInt crashes on non-numeric text and that && short-circuits, so the digit check first stops parseInt from running on abc; the other way round it would crash with NumberFormatException.",
         ["parseInt throws NumberFormatException on abc. && stops at the first false, so with the digit check first, abc fails there and parseInt never runs. Reversed, parseInt would run on abc and crash.",
          "The digit check protects parseInt. If abc is checked by parseInt first, the program crashes before it can say the input is bad."]),
     1: ("Says the check should come first to avoid a crash, but doesn't explain short-circuiting or what crashes.",
         ["To stop it crashing.", "Because you need to check it's a number first."]),
     0: ("Incorrect, for example says order doesn't matter, or that parseInt can handle letters.",
         ["The order doesn't matter, && checks both.", "parseInt would just return 0 for abc."])})
print("4.5 written")
