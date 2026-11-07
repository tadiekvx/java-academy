from build import *

Lesson("j1-l2.4", "Working with strings", ["J1.04"], [
    ("o1", "Join text and other values with +, and predict the result"),
    ("o2", "Use length, charAt, substring, indexOf, toUpperCase and toLowerCase, counting positions from 0"),
    ("o3", "Compare strings with equals, and explain why == can give the wrong answer"),
    ("o4", "Use the new string a method returns, because a string itself never changes"),
], ["j1-l2.2"], 40, ["R9", "R8", "I4"], r'''
## Before you start

You should be able to create variables and trace their values ([Variables and state](j1-l2.2)).

**Quick check.** After `String a = "cat"; String b = a; a = "dog";`, what is `b`?

<details><summary>Show the answer</summary>

`"cat"`. The line `String b = a;` copied the value at that moment; changing `a` later doesn't affect `b`.

</details>

## Explanation

Text is everywhere in programs: names, messages, passwords, file names. In Java, text is a `String`, and strings come with a toolbox of **methods**: actions you can ask a string to do, by writing a dot after it.

### Joining strings with `+`

`+` between two strings **joins** them (programmers say *concatenates*):

```java runnable
void main() {
    String first = "Ada";
    String last = "Lovelace";
    IO.println(first + " " + last);
}
```

This prints `Ada Lovelace`. Notice the `" "` in the middle: `+` adds nothing between the pieces, not even a space.

When one side of `+` is a string and the other is a number (or a `char` or `boolean`), Java turns the other value into text and joins them. That makes labelled output easy at last:

```java runnable
void main() {
    int score = 42;
    IO.println("Score: " + score);
}
```

### Left to right, so watch the numbers

Java works out `+` from **left to right**, and what happens at each step depends on what's been built so far:

- `"Total: " + 3 + 4` is `"Total: 3"` + `4`, which is `"Total: 34"`. Once the left side is a string, every `+` joins.
- `3 + 4 + " apples"` is `7 + " apples"`, which is `"7 apples"`. The first `+` is between two numbers, so it adds.
- `"Total: " + (3 + 4)` is `"Total: 7"`. The parentheses make the addition happen first.

When you mix text and arithmetic, put the arithmetic in parentheses.

### Positions start at 0

Each character in a string has a position, called its **index**, and **the first index is 0**:

| Character | `J` | `a` | `v` | `a` |
|---|---|---|---|---|
| Index | 0 | 1 | 2 | 3 |

So `"Java"` has length 4, but its last index is 3. Starting at 0 feels strange at first; it's the same in almost every programming language.

### Useful string methods

| Method | What it gives back | Example | Result |
|---|---|---|---|
| `length()` | How many characters | `"Java".length()` | `4` |
| `charAt(i)` | The `char` at index `i` | `"Java".charAt(0)` | `'J'` |
| `substring(a, b)` | Characters from index `a` up to, **but not including**, `b` | `"banana".substring(1, 4)` | `"ana"` |
| `substring(a)` | From index `a` to the end | `"banana".substring(3)` | `"ana"` |
| `indexOf(s)` | Index where `s` first appears, or `-1` if it doesn't | `"banana".indexOf("n")` | `2` |
| `toUpperCase()` | A copy in capitals | `"Java".toUpperCase()` | `"JAVA"` |
| `toLowerCase()` | A copy in lower case | `"Java".toLowerCase()` | `"java"` |
| `strip()` | A copy without spaces at the start and end | `"  hi  ".strip()` | `"hi"` |
| `equals(s)` | `true` if both have exactly the same characters | `"Java".equals("java")` | `false` |

`substring(1, 4)` stopping *before* index 4 means the number of characters you get is `4 - 1 = 3`. Asking for an index that doesn't exist, like `"Java".charAt(4)`, stops the program with an error; you'll learn to read it in [Exceptions and stack traces](j1-l6.4).

### Strings never change

No string method changes the string it's called on. `toUpperCase()` doesn't turn the string into capitals; it gives you **a new string** in capitals. If you don't use or store that new string, it's thrown away:

```java runnable
void main() {
    String name = "ada";
    name.toUpperCase();          // makes "ADA", then throws it away
    IO.println(name);            // still "ada"
    name = name.toUpperCase();   // store the new string
    IO.println(name);            // "ADA"
}
```

### Comparing strings: use `equals`, not `==`

To check whether two strings have the same characters, use `equals`:

```java runnable
void main() {
    String typed = "PARIS".toLowerCase();
    IO.println(typed.equals("paris"));
    IO.println(typed == "paris");
}
```

This prints `true` then `false`, even though both strings are `paris`. `==` asks a different question: *are these the very same string object in memory?* Strings that are built while a program runs, like the result of `toLowerCase()`, are separate objects, so `==` says `false`. Sometimes `==` happens to give `true`, which makes the bug harder to spot. You'll learn exactly why in Stage 2; for now, the rule is simple: **compare strings with `equals`**.

## Worked examples

### Example 1: a username from a name

*Task: build a username from the first letter of the first name and the whole last name, all in lower case. `Ada Lovelace` becomes `alovelace`.*

**Step 1 — Break it into pieces.** The first letter of the first name, then the last name.

**Step 2 — Get each piece with a method.** `first.charAt(0)` gives `'A'`. The last name is `last` itself.

**Step 3 — Join, then convert.** `first.charAt(0) + last` gives `"ALovelace"`: a `char` + a `String` joins into a `String`. Then `.toLowerCase()` on the result.

**Step 4 — Use what the method returns.** `toLowerCase()` gives back a new string, so return that.

```java runnable
String username(String first, String last) {
    return (first.charAt(0) + last).toLowerCase();
}

void main() {
    IO.println(username("Ada", "Lovelace"));
}
```

### Example 2: the domain of an email address

*Task: get everything after the `@` in an email address. `ada@example.com` gives `example.com`.*

**Step 1 — Find the landmark.** `email.indexOf("@")` gives the index of the `@` (here, 3).

**Step 2 — Work out where the answer starts.** One character after the `@`: index + 1.

**Step 3 — Take everything from there.** `email.substring(at + 1)`.

```java runnable
String domain(String email) {
    int at = email.indexOf("@");
    return email.substring(at + 1);
}

void main() {
    IO.println(domain("ada@example.com"));
}
```

**Step 4 — Check an edge case.** With `"x@y"`, `at` is 1, and `substring(2)` gives `"y"`. Correct.

## Predict, then run

::exercise{id=j1-l2.4-predict-strings}

## Where this is used

- **Sign-up forms** check that an email contains `@`, strip stray spaces from what people type, and compare passwords with `equals`.
- **Search** often lower-cases both the query and the text, so that `Java` matches `java`.
- **Labels and messages**: almost every line a program prints for a person is built by joining strings and values.

## Common mistakes

:::mistake{id=MC05}
**Comparing strings with `==`.** `typed == "paris"` can be `false` even when `typed` is `"paris"`, because `==` checks whether they're the same object, not whether they hold the same characters. Use `typed.equals("paris")`.
:::

:::mistake{id=MC06}
**Calling a method and ignoring what it returns.** `name.toUpperCase();` on its own line does nothing useful: the capitalised copy is thrown away. Store it (`name = name.toUpperCase();`) or use it directly (`return name.toUpperCase();`).
:::

### Forgetting that indexes start at 0

The first character is `charAt(0)`, and the last is `charAt(s.length() - 1)`. `charAt(s.length())` is always one past the end.

## Practice

::exercise{id=j1-l2.4-write-initials}

::exercise{id=j1-l2.4-debug-shout}

::exercise{id=j1-l2.4-debug-answer}

::exercise{id=j1-l2.4-modify-badge}

::exercise{id=j1-l2.4-explain-equals}

## Version notes

`strip()` arrived in **Java 11**; in older code you'll see `trim()`, which does nearly the same thing. Everything else here has worked the same way since Java 1.0.

## Further reading

- **Java SE 25 API documentation for `String`** `[I4]`: every method a string has, with examples. Look up `indexOf` and `substring` to see their variations.

## How you'll be assessed

- The **predict** exercise checks that you can work out joined strings and method results (*identifying mistakes*).
- The **write** exercise checks that you can build strings with methods (*implementation*).
- The **debug** exercises check that you can fix the two classic string bugs: an ignored result, and `==` (*debugging*).
- The **modify** and **explain** exercises check that you can change string code and say why `equals` is needed.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''', features=[("String.strip", 11)])

ex = Exercises("j1-l2.4")
ex.predict("j1-l2.4-predict-strings", "Joining and slicing", ["o1", "o2"], ["J1.04"],
    "Predict exactly what this program prints, one line per statement. Remember: `+` works left to right, and indexes start at 0.",
    '''
    void main() {
        IO.println("Total: " + 3 + 4);
        IO.println(3 + 4 + " apples");
        IO.println("Total: " + (3 + 4));
        IO.println("Java".length());
        IO.println("Java".charAt(1));
        IO.println("banana".substring(1, 4));
        IO.println("banana".indexOf("z"));
    }
    ''', '''
    Total: 34
    7 apples
    Total: 7
    4
    a
    ana
    -1
    ''', ("Once the left side of + is a string, every + after it joins text. charAt and substring count from 0.",
          "\"Total: \" + 3 gives \"Total: 3\", then + 4 gives \"Total: 34\". substring(1, 4) takes indexes 1, 2 and 3."),
    difficulty=2)

def initials(first, last):
    return (first[0] + "." + last[0] + ".").upper()
ex.method("write", "j1-l2.4-write-initials", "Initials", ["o1", "o2", "o4"], ["J1.04"], ["IMPL"],
    "Complete `initials` so it returns someone's initials in capitals, each followed by a full stop. For example, `initials(\"ada\", \"Lovelace\")` should be `\"A.L.\"`.",
    [("initials", [("first", "String"), ("last", "String")], "String")], {"initials": initials},
    [(None, ["Ada", "Lovelace"]), (None, ["grace", "hopper"]), (None, ["Alan", "Turing"])],
    [(None, ["x", "y"], "one-letter names"), (None, ["katherine", "Johnson"], "mixed capitals"), (None, ["Tim", "berners-lee"], "hyphenated surname"),
     (None, ["ZOE", "QUINN"], "already capitals"), (None, ["margaret", "hamilton"], "all lower case")],
    '''
    String initials(String first, String last) {
        return ""; // replace "" with your expression
    }

    void main() {
        IO.println(initials("ada", "Lovelace")); // should print A.L.
    }
    ''', '''
    String initials(String first, String last) {
        return (first.charAt(0) + "." + last.charAt(0) + ".").toUpperCase();
    }

    void main() {
        IO.println(initials("ada", "Lovelace")); // should print A.L.
    }
    ''', {
        "no-capitals": 'String initials(String first, String last) {\n    return first.charAt(0) + "." + last.charAt(0) + ".";\n}\n\nvoid main() {\n}\n',
        "ignored-result": 'String initials(String first, String last) {\n    String result = first.charAt(0) + "." + last.charAt(0) + ".";\n    result.toUpperCase();\n    return result;\n}\n\nvoid main() {\n}\n',
    }, ("Which method gives you the first character of a string? Which one makes capitals?",
        "Join first.charAt(0), \".\", last.charAt(0) and \".\", then call toUpperCase() on the whole result and return it."),
    group="string-building")

def short_code(city):
    return city[:3].upper()
ex.method("write", "j1-l2.4-retrieve-code", "Airport-style codes", ["o2", "o4"], ["J1.04"], ["IMPL"],
    "Complete `shortCode` so it returns the first three letters of a city's name, in capitals. For example, `shortCode(\"London\")` should be `\"LON\"`. Every city name has at least three letters.",
    [("shortCode", [("city", "String")], "String")], {"shortCode": short_code},
    [(None, ["London"]), (None, ["paris"]), (None, ["Rome"])],
    [(None, ["Oslo"], "four letters"), (None, ["new york"], "two words"), (None, ["Ely"], "exactly three"), (None, ["MADRID"], "already capitals"), (None, ["cardiff"], "lower case")],
    'String shortCode(String city) {\n    return ""; // replace "" with your expression\n}\n\nvoid main() {\n    IO.println(shortCode("London")); // should print LON\n}\n',
    'String shortCode(String city) {\n    return city.substring(0, 3).toUpperCase();\n}\n\nvoid main() {\n    IO.println(shortCode("London")); // should print LON\n}\n',
    {"no-capitals": 'String shortCode(String city) {\n    return city.substring(0, 3);\n}\n\nvoid main() {\n}\n',
     "off-by-one": 'String shortCode(String city) {\n    return city.substring(1, 4).toUpperCase();\n}\n\nvoid main() {\n}\n'},
    ("substring takes a start index and an end index that isn't included. Which indexes are the first three letters?",
     "city.substring(0, 3) gives the first three letters; call toUpperCase() on that and return it."),
    role="retrieval", group="string-building")

def username(first, last):
    return (first[0] + last).lower()
ex.method("write", "j1-l2.4-retrieve-username", "Usernames", ["o1", "o2"], ["J1.04"], ["IMPL"],
    "Complete `username` so it returns the first letter of the first name followed by the whole last name, all in lower case. For example, `username(\"Grace\", \"Hopper\")` should be `\"ghopper\"`.",
    [("username", [("first", "String"), ("last", "String")], "String")], {"username": username},
    [(None, ["Grace", "Hopper"]), (None, ["ada", "LOVELACE"]), (None, ["Linus", "Torvalds"])],
    [(None, ["A", "B"], "one-letter names"), (None, ["Margaret", "Hamilton"], "long names"), (None, ["kEN", "tHOMPSON"], "odd capitals"),
     (None, ["Barbara", "Liskov"], "another name"), (None, ["Dennis", "Ritchie"], "and another")],
    'String username(String first, String last) {\n    return ""; // replace "" with your expression\n}\n\nvoid main() {\n    IO.println(username("Grace", "Hopper")); // should print ghopper\n}\n',
    'String username(String first, String last) {\n    return (first.charAt(0) + last).toLowerCase();\n}\n\nvoid main() {\n    IO.println(username("Grace", "Hopper")); // should print ghopper\n}\n',
    {"only-last-lowered": 'String username(String first, String last) {\n    return first.charAt(0) + last.toLowerCase();\n}\n\nvoid main() {\n}\n'},
    ("You need the first character of one string, joined to another string, then everything in lower case.",
     "Join first.charAt(0) and last, put that in parentheses, and call toLowerCase() on it."),
    role="retrieval", group="string-building")

def shout(message):
    return message.upper() + "!"
ex.method("debug", "j1-l2.4-debug-shout", "The quiet shout", ["o4"], ["J1.04"], ["DEBUG"],
    "`shout` should return the message in capitals with an exclamation mark, so `shout(\"hello\")` gives `\"HELLO!\"`. It returns `\"hello!\"` instead. Find and fix the bug.",
    [("shout", [("message", "String")], "String")], {"shout": shout},
    [(None, ["hello"]), (None, ["stop"]), (None, ["Watch Out"])],
    [(None, ["a"], "one letter"), (None, ["already LOUD"], "some capitals already"), (None, ["fire drill"], "two words"), (None, ["go go go"], "repeated words"), (None, [""], "empty message")],
    'String shout(String message) {\n    message.toUpperCase();\n    return message + "!";\n}\n\nvoid main() {\n    IO.println(shout("hello")); // should print HELLO!\n}\n',
    'String shout(String message) {\n    return message.toUpperCase() + "!";\n}\n\nvoid main() {\n    IO.println(shout("hello")); // should print HELLO!\n}\n',
    {"still-ignored": 'String shout(String message) {\n    String loud = message;\n    loud.toUpperCase();\n    return loud + "!";\n}\n\nvoid main() {\n}\n'},
    ("Does toUpperCase() change message, or give you something back?",
     "toUpperCase() returns a new string and leaves message unchanged. Use what it returns: return message.toUpperCase() + \"!\";"),
    misconceptions=["MC06"], notes="Bug: the result of `toUpperCase()` is ignored (MC06). Strings are immutable; the fix uses the returned string.")

def correct(answer):
    return answer.strip().lower() == "paris"
ex.method("debug", "j1-l2.4-debug-answer", "Capital of France", ["o3"], ["J1.04"], ["DEBUG"],
    "A quiz accepts `paris` as the answer in any capitals and with stray spaces around it, so `\"Paris\"` and `\"  PARIS \"` should both be correct. Learners who type `Paris` are being told they're wrong. Find and fix the bug.",
    [("isCorrect", [("answer", "String")], "boolean")], {"isCorrect": correct},
    [(None, ["paris"]), (None, ["Paris"]), (None, ["London"])],
    [(None, ["  PARIS "], "capitals and spaces"), (None, ["pAris"], "odd capitals"), (None, ["Rome"], "wrong city"), (None, ["par is"], "space in the middle"), (None, [""], "no answer")],
    'boolean isCorrect(String answer) {\n    String cleaned = answer.strip().toLowerCase();\n    return cleaned == "paris";\n}\n\nvoid main() {\n    IO.println(isCorrect("Paris")); // should print true\n}\n',
    'boolean isCorrect(String answer) {\n    String cleaned = answer.strip().toLowerCase();\n    return cleaned.equals("paris");\n}\n\nvoid main() {\n    IO.println(isCorrect("Paris")); // should print true\n}\n',
    {"case-sensitive": 'boolean isCorrect(String answer) {\n    return answer.strip().equals("paris");\n}\n\nvoid main() {\n}\n'},
    ("The cleaning looks right. Look at how the cleaned answer is compared with \"paris\".",
     "== checks whether two strings are the same object, not whether they hold the same characters. Use cleaned.equals(\"paris\")."),
    misconceptions=["MC05"], difficulty=2,
    notes="Bug: `==` compares object identity (MC05). The literal \"paris\" input passes by coincidence (interning), which is exactly why the bug survives casual testing.")

def badge(name, level):
    return f"{name.upper()} (level {level})"
ex.method("modify", "j1-l2.4-modify-badge", "New name badges", ["o1", "o2"], ["J1.04"], ["MOD"],
    "A game prints name badges like `Ada - 3`. The designers want a new style: the name in capitals, then the level in brackets, like `ADA (level 3)`. Change `badge` to produce the new style.",
    [("badge", [("name", "String"), ("level", "int")], "String")], {"badge": badge},
    [(None, ["Ada", 3]), (None, ["grace", 10]), (None, ["Linus", 1])],
    [(None, ["x", 0], "level zero"), (None, ["Margaret", 99], "high level"), (None, ["ZOE", 7], "already capitals"), (None, ["tim", 42], "lower case"), (None, ["Bo", 5], "short name")],
    'String badge(String name, int level) {\n    return name + " - " + level;\n}\n\nvoid main() {\n    IO.println(badge("Ada", 3));\n}\n',
    'String badge(String name, int level) {\n    return name.toUpperCase() + " (level " + level + ")";\n}\n\nvoid main() {\n    IO.println(badge("Ada", 3));\n}\n',
    {"forgot-capitals": 'String badge(String name, int level) {\n    return name + " (level " + level + ")";\n}\n\nvoid main() {\n}\n'},
    ("Compare the old output and the new output piece by piece. What text goes around the level now?",
     "Return name.toUpperCase() + \" (level \" + level + \")\". Mind the spaces inside the quotes."))

ex.explain("j1-l2.4-explain-equals", "Why equals?", ["o3"], ["J1.04"],
    "A learner's program compares a typed password with `typed == \"open sesame\"`. Sometimes it works and sometimes it says the password is wrong even when it's right. Explain what `==` is really checking for strings, and what to use instead.",
    "A full answer says that == checks whether the two strings are the same object, not whether they contain the same characters; strings built while the program runs are separate objects, so == can be false; equals compares the characters and should be used.",
    {2: ("Explains that == compares whether they are the same object (not the characters), so equal text can still give false, and recommends equals, which compares the characters.",
         ["== checks if it's the very same string object in memory. A password the user typed is a different object from the one in the code, even with the same letters, so == can be false. equals compares the actual characters, so use typed.equals(\"open sesame\").",
          "With strings, == asks 'same object?' not 'same text?'. Sometimes Java reuses an object so it happens to work, which is why it's only sometimes wrong. Use equals to compare the text."]),
     1: ("Says to use equals instead of ==, but the explanation of what == checks is missing or vague.",
         ["You should use .equals for strings, not ==.", "== doesn't work properly with strings, equals does."]),
     0: ("Incorrect, for example says == is fine, or that the problem is capital letters or spaces.",
         ["The problem is that passwords are case-sensitive.", "== is right, the user must have typed it wrong."])},
    misconceptions=["MC05"])
print("2.4 written")
