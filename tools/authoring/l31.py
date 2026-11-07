from build import *

Lesson("j1-l3.1", "Reading input", ["J1.05"], [
    ("o1", "Read a line the user types with IO.readln, showing a prompt"),
    ("o2", "Convert typed text into a number with Integer.parseInt or Double.parseDouble"),
    ("o3", "Explain why text from the keyboard must be converted before you do arithmetic with it"),
    ("o4", "Recognise NumberFormatException as the error you get when the text isn't a number"),
], ["j1-l2.4"], 30, ["I4", "R6"], r'''
## Before you start

You should be able to join strings and values with `+` ([Working with strings](j1-l2.4)).

**Quick check.** What does `"Total: " + 2 + 3` give?

<details><summary>Show the answer</summary>

`"Total: 23"`. Once the left side is a string, every `+` joins text.

</details>

## Explanation

Until now, every value your programs used was written into the code. Real programs respond to **input**: what someone types.

### Reading a line with `IO.readln`

`IO.readln` shows a **prompt**, waits for the person to type a line and press Enter, and gives back what they typed as a `String`:

```java
void main() {
    String name = IO.readln("What's your name? ");
    IO.println("Hello, " + name + "!");
}
```

A run looks like this (what the person typed is `Ada`):

```
What's your name? Ada
Hello, Ada!
```

The prompt doesn't end the line, so put a space at its end: it keeps the typing from touching the question.

**Trying it here:** programs in this course can't pause for you to type. In the code exercises, open **Input for Run** and type your input there first, one line for each `IO.readln`, before you press Run. The tests give your program input the same way.

### Typed numbers arrive as text

Everything `IO.readln` returns is a `String`, even if the person typed digits. `"12"` is text, not a number, so `+` would join it rather than add it:

| Expression | Result |
|---|---|
| `"12" + 1` | `"121"` |
| `12 + 1` | `13` |

To do arithmetic, **convert** the text to a number first:

| Method | Turns | Into |
|---|---|---|
| `Integer.parseInt(text)` | `"12"` | the `int` `12` |
| `Double.parseDouble(text)` | `"2.5"` | the `double` `2.5` |

```java
void main() {
    String typed = IO.readln("How old are you? ");
    int age = Integer.parseInt(typed);
    IO.println("Next year you will be " + (age + 1) + ".");
}
```

Notice the parentheses around `age + 1`: without them, `+` would join the 1 onto the text.

### When the text isn't a number

If someone types `twelve`, `Integer.parseInt` can't convert it, and the program stops with a runtime error:

```
Exception in thread "main" java.lang.NumberFormatException: For input string: "twelve"
```

The message even quotes the text it couldn't convert. `Integer.parseInt` also rejects `"12.5"` (not a whole number) and `" 12"` (it doesn't ignore spaces; use `strip()` first). Later lessons show how to check input before converting it, so a typo doesn't crash your program.

## Worked examples

### Example 1: area of a rectangle

*Task: ask for a width and a height in metres (whole numbers) and print the area.*

**Step 1 — One `IO.readln` per value**, each with a clear prompt.

**Step 2 — Convert each to an `int`** straight away, so the rest of the program works with numbers.

**Step 3 — Calculate, then print with a label.** Put the calculation in parentheses, or work it out into a variable first.

```java
void main() {
    int width = Integer.parseInt(IO.readln("Width (m): "));
    int height = Integer.parseInt(IO.readln("Height (m): "));
    int area = width * height;
    IO.println("Area: " + area + " square metres");
}
```

With the input `4` and `3`:

```
Width (m): 4
Height (m): 3
Area: 12 square metres
```

**Step 4 — Think about bad input.** If someone types `4m`, `parseInt` fails. That's acceptable for now; you'll handle it in [Input validation loops](j1-l4.5).

### Example 2: a price with pence

*Task: ask for a price like `2.50` and print the price of three.*

**Step 1 — Choose the type.** Prices have a decimal point, so use `Double.parseDouble`.

**Step 2 — Convert, calculate, print.**

```java
void main() {
    double price = Double.parseDouble(IO.readln("Price: "));
    IO.println("Three cost " + (price * 3));
}
```

With `2.50`, this prints `Three cost 7.5`. Remember from [Arithmetic](j1-l2.3) that doubles can print long decimal tails for some values; programs that handle real money store whole pence as `int`s instead.

## Predict, then run

::exercise{id=j1-l3.1-predict-parse}

## Where this is used

- **Command-line tools** ask questions like `Overwrite existing file? (y/n)` and act on the answer.
- **Every form on the web** sends text to a server, which converts the parts that are numbers, dates or yes/no answers, exactly as you're doing here.
- **Converting carefully matters**: a huge number of real bugs come from text that was assumed to be a number.

## Common mistakes

### Doing arithmetic on the text

`IO.readln("Number: ") + 1` joins `1` onto the text. Convert first with `Integer.parseInt`.

### Forgetting parentheses in the output

`"Next year: " + age + 1` prints `Next year: 341` when `age` is 34. Write `"Next year: " + (age + 1)`.

### Expecting `parseInt` to understand anything number-like

`"12.5"`, `"1,000"` and `" 7"` all cause `NumberFormatException` with `Integer.parseInt`. Strip spaces first, and use `Double.parseDouble` for decimals.

## Practice

::exercise{id=j1-l3.1-write-greeting}

::exercise{id=j1-l3.1-write-next-age}

::exercise{id=j1-l3.1-debug-join}

::exercise{id=j1-l3.1-explain-convert}

## Version notes

`IO.readln` arrived in **Java 25**. Older code reads input with `new Scanner(System.in)` and `scanner.nextLine()`, which does the same job with more set-up.

## Further reading

- **Java SE 25 API documentation for `Integer.parseInt`** `[I4]`: the exact rules for which strings it accepts, including signs like `-12` and `+12`.

## How you'll be assessed

- The **write** exercises check that you can read input and convert it (*implementation*).
- The **debug** exercise checks that you can fix text being joined instead of added (*debugging*).
- The **predict** and **explain** exercises check that you understand why conversion is needed, and what happens when it fails.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l3.1")
ex.predict("j1-l3.1-predict-parse", "Text or number?", ["o2", "o3"], ["J1.05"],
    "Predict exactly what this program prints. Which values are text, and which are numbers?",
    '''
    void main() {
        String typed = "12";
        int number = Integer.parseInt(typed);
        IO.println(typed + 1);
        IO.println(number + 1);
        IO.println(typed + number);
        IO.println(number + number);
    }
    ''', '''
    121
    13
    1212
    24
    ''', ("typed is a String; number is an int. What does + do with each?",
          "Text + anything joins, so typed + 1 is \"121\". number + 1 adds. typed + number joins \"12\" and 12."), difficulty=2)

ex.io("write", "j1-l3.1-write-greeting", "A friendly greeting", ["o1"], ["J1.05"], ["IMPL"],
    "Write a program that asks `What's your name? ` and then prints `Hello, NAME!` with the name the person typed. For example, if they type `Ada`, it prints `Hello, Ada!`.",
    lambda stdin: [f"Hello, {stdin.strip()}!\n"],
    [("Ada", "Ada\n"), ("Grace", "Grace\n"), ("two words", "Mary Jane\n")],
    [("short name", "Bo\n"), ("lower case", "linus\n"), ("long name", "Bartholomew\n"), ("hyphenated", "Jean-Luc\n"), ("capitals", "ZOE\n")],
    'void main() {\n    // Ask for a name with IO.readln, then print the greeting.\n}\n',
    'void main() {\n    String name = IO.readln("What\'s your name? ");\n    IO.println("Hello, " + name + "!");\n}\n',
    {"no-exclamation": 'void main() {\n    String name = IO.readln("What\'s your name? ");\n    IO.println("Hello, " + name);\n}\n'},
    ("IO.readln shows the prompt and gives back what was typed. Store it in a String variable.",
     "String name = IO.readln(\"What's your name? \"); then IO.println(\"Hello, \" + name + \"!\");"),
    contains=True, difficulty=1)

def next_age(stdin):
    return [f"Next year you will be {int(stdin.strip()) + 1}.\n"]
ex.io("write", "j1-l3.1-write-next-age", "Next birthday", ["o2"], ["J1.05"], ["IMPL"],
    "Write a program that asks `How old are you? ` and prints `Next year you will be N.`, where N is one more than the age typed. For example, with `34` it prints `Next year you will be 35.`",
    next_age, [("34", "34\n"), ("9", "9\n"), ("0", "0\n")],
    [("teenager", "15\n"), ("very old", "104\n"), ("twenties", "29\n"), ("one", "1\n"), ("fifty", "50\n")],
    'void main() {\n    // Ask for the age, convert it to an int, then print the message.\n}\n',
    'void main() {\n    int age = Integer.parseInt(IO.readln("How old are you? "));\n    IO.println("Next year you will be " + (age + 1) + ".");\n}\n',
    {"joined-not-added": 'void main() {\n    int age = Integer.parseInt(IO.readln("How old are you? "));\n    IO.println("Next year you will be " + age + 1 + ".");\n}\n'},
    ("What type does IO.readln give back? What do you need before you can add 1?",
     "Convert with Integer.parseInt, then print \"Next year you will be \" + (age + 1) + \".\" with the brackets."),
    contains=True, group="read-convert")

def seconds(stdin):
    return [f"That's {int(stdin.strip()) * 60} seconds.\n"]
ex.io("write", "j1-l3.1-retrieve-seconds", "Minutes to seconds", ["o1", "o2"], ["J1.05"], ["IMPL"],
    "Write a program that asks `Minutes: ` and prints `That's N seconds.` For example, with `3` it prints `That's 180 seconds.`",
    seconds, [("3", "3\n"), ("1", "1\n"), ("0", "0\n")],
    [("ten", "10\n"), ("an hour", "60\n"), ("a day", "1440\n"), ("seven", "7\n"), ("two", "2\n")],
    'void main() {\n    // Ask for minutes, convert, then print the seconds.\n}\n',
    'void main() {\n    int minutes = Integer.parseInt(IO.readln("Minutes: "));\n    IO.println("That\'s " + (minutes * 60) + " seconds.");\n}\n',
    {"not-multiplied": 'void main() {\n    int minutes = Integer.parseInt(IO.readln("Minutes: "));\n    IO.println("That\'s " + minutes + " seconds.");\n}\n'},
    ("Read the text, convert it to an int, then multiply.",
     "int minutes = Integer.parseInt(IO.readln(\"Minutes: \")); then print \"That's \" + (minutes * 60) + \" seconds.\""),
    contains=True, role="retrieval", group="read-convert")

def total_pence(stdin):
    price, qty = (int(x) for x in stdin.split())
    return [f"Total: {price * qty} pence\n"]
ex.io("write", "j1-l3.1-retrieve-total", "Shopping total", ["o1", "o2"], ["J1.05"], ["IMPL"],
    "Write a program that asks `Price in pence: ` and then `How many? `, and prints `Total: N pence`. For example, with `45` and `3` it prints `Total: 135 pence`.",
    total_pence, [("45 x 3", "45\n3\n"), ("100 x 1", "100\n1\n"), ("nothing bought", "99\n0\n")],
    [("a dozen", "30\n12\n"), ("free item", "0\n5\n"), ("big order", "250\n40\n"), ("two", "75\n2\n"), ("pound coins", "100\n7\n")],
    'void main() {\n    // Ask for both values, convert them, then print the total.\n}\n',
    'void main() {\n    int price = Integer.parseInt(IO.readln("Price in pence: "));\n    int quantity = Integer.parseInt(IO.readln("How many? "));\n    IO.println("Total: " + (price * quantity) + " pence");\n}\n',
    {"joined": 'void main() {\n    String price = IO.readln("Price in pence: ");\n    String quantity = IO.readln("How many? ");\n    IO.println("Total: " + price + quantity + " pence");\n}\n'},
    ("Two IO.readln calls, two conversions, one multiplication.",
     "Convert both with Integer.parseInt, then print \"Total: \" + (price * quantity) + \" pence\"."),
    contains=True, role="retrieval", group="read-convert")

def sum_two(stdin):
    a, b = (int(x) for x in stdin.split())
    return [f"Sum: {a + b}\n"]
ex.io("debug", "j1-l3.1-debug-join", "The sum that isn't", ["o2", "o3"], ["J1.05"], ["DEBUG"],
    "This program should ask for two whole numbers and print their sum. With `2` and `3` it should print `Sum: 5`, but it prints `Sum: 23`. Find and fix the bug.",
    sum_two, [("2 and 3", "2\n3\n"), ("10 and 5", "10\n5\n"), ("zeros", "0\n0\n")],
    [("negative", "-4\n10\n"), ("large", "1000\n2345\n"), ("both negative", "-3\n-3\n"), ("one zero", "0\n7\n"), ("big and small", "99\n1\n")],
    'void main() {\n    String first = IO.readln("First number: ");\n    String second = IO.readln("Second number: ");\n    IO.println("Sum: " + first + second);\n}\n',
    'void main() {\n    int first = Integer.parseInt(IO.readln("First number: "));\n    int second = Integer.parseInt(IO.readln("Second number: "));\n    IO.println("Sum: " + (first + second));\n}\n',
    {"converted-but-joined": 'void main() {\n    int first = Integer.parseInt(IO.readln("First number: "));\n    int second = Integer.parseInt(IO.readln("Second number: "));\n    IO.println("Sum: " + first + second);\n}\n'},
    ("What type are first and second? What does + do with that type?",
     "They're Strings, so + joins them. Convert both with Integer.parseInt, and put the addition in parentheses when you print."),
    contains=True,
    notes="Two layers: the inputs must be converted, and the addition must be parenthesised in the output (the wrong solution converts but still joins).")

ex.explain("j1-l3.1-explain-convert", "Why convert?", ["o3", "o4"], ["J1.05"],
    "Explain why a program has to call `Integer.parseInt` on what `IO.readln` returns before it can do arithmetic with it. What happens if the person types `ten` instead of `10`?",
    "A full answer says IO.readln always returns a String (text), so + would join rather than add; parseInt converts the text to an int; if the text isn't a whole number, such as ten, parseInt fails with a NumberFormatException and the program stops.",
    {2: ("Says readln returns text (a String) so arithmetic like + would join or wouldn't work, parseInt turns it into an int, and typing ten causes a NumberFormatException (the program crashes).",
         ["IO.readln always gives you a String, even if you typed digits, so \"10\" + 1 would be \"101\". parseInt turns \"10\" into the number 10. If you type ten it can't convert it and you get a NumberFormatException, so the program stops.",
          "Input is text. To add you need a number, which is what Integer.parseInt makes. With 'ten' it throws NumberFormatException because ten isn't digits."]),
     1: ("Gets one half: either why conversion is needed or what happens with ten, but not both, or is vague.",
         ["Because readln gives a String and you can't do maths with Strings.", "If you type ten the program crashes."]),
     0: ("Incorrect, for example says parseInt understands words, or that conversion isn't needed.",
         ["parseInt would turn ten into 10.", "You only need parseInt for decimals."])})
print("3.1 written")
