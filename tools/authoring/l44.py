from build import *

Lesson("j1-l4.4", "Loop patterns", ["J1.07", "J1.09"], [
    ("o1", "Use the counting, summing, find-the-first and track-the-largest patterns"),
    ("o2", "Choose the right pattern for a new problem"),
    ("o3", "Loop over the characters of a string with charAt"),
], ["j1-l4.3"], 40, ["R4", "R3"], r'''
## Before you start

You should be able to write for loops over a range and over a string ([for loops and boundaries](j1-l4.3)).

**Quick check.** Write the header of a for loop that visits every index of `word`.

<details><summary>Show the answer</summary>

`for (int i = 0; i < word.length(); i++)`

</details>

## Explanation

Experienced programmers rarely invent a loop from nothing. Most loops are one of a handful of **patterns**, and recognising which one a problem needs gets you most of the way. This lesson covers four.

### Pattern 1: count

*How many …?* Start a counter at 0; add 1 whenever an item matches.

```java
int count = 0;
for (int i = 0; i < word.length(); i++) {
    if (word.charAt(i) == 'e') {
        count++;
    }
}
```

### Pattern 2: sum

*What's the total of …?* Start a total at 0; add each item.

```java
int total = 0;
for (int i = 1; i <= n; i++) {
    total += i;
}
```

### Pattern 3: find the first

*Where is the first …?* Look at each item; as soon as one matches, `return` it. If the loop finishes without finding one, return a value that means *not found*, often `-1`.

```java
int firstSpace(String text) {
    for (int i = 0; i < text.length(); i++) {
        if (text.charAt(i) == ' ') {
            return i;
        }
    }
    return -1;
}
```

`return` inside the loop stops the loop **and** the method immediately. That's what makes it the *first* match.

### Pattern 4: track the largest

*What's the biggest …?* Keep the best seen so far; replace it whenever a bigger one comes along.

```java
int best = number at the start;
for (each item) {
    if (item > best) {
        best = item;
    }
}
```

The starting value matters. Start with the first item, or with a value you know every item is at least as big as. For digits, that's 0.

### Working through the digits of a number

`n % 10` is the last digit of `n`, and `n / 10` removes it. A while loop that repeats this visits every digit:

```java runnable
void main() {
    int n = 4071;
    while (n > 0) {
        IO.println(n % 10);
        n = n / 10;
    }
}
```

This prints 1, 7, 0, 4: the digits from last to first.

## Worked examples

### Example 1: counting vowels

*Task: count the vowels (a, e, i, o, u, in any capitals) in a word.*

**Step 1 — Which pattern?** "How many" means **count**.

**Step 2 — What counts as a match?** Lower-case the character first, then check the five vowels. `"aeiou".indexOf(c)` is a neat trick: it's `-1` when `c` isn't a vowel.

```java runnable
int countVowels(String word) {
    String lower = word.toLowerCase();
    int count = 0;
    for (int i = 0; i < lower.length(); i++) {
        if ("aeiou".indexOf(lower.charAt(i)) != -1) {
            count++;
        }
    }
    return count;
}

void main() {
    IO.println(countVowels("Education"));
}
```

This prints `5`.

### Example 2: the largest digit

*Task: return the largest digit in a non-negative whole number. For 4071 that's 7.*

**Step 1 — Which pattern?** "Biggest" means **track the largest**, combined with the digit loop.

**Step 2 — Starting value.** Digits are never negative, so `best = 0` is safe.

**Step 3 — Edge case.** For `n = 0`, the loop doesn't run, and the answer is 0. Correct.

```java runnable
int largestDigit(int n) {
    int best = 0;
    while (n > 0) {
        int digit = n % 10;
        if (digit > best) {
            best = digit;
        }
        n = n / 10;
    }
    return best;
}

void main() {
    IO.println(largestDigit(4071));
}
```

## Predict, then run

::exercise{id=j1-l4.4-predict-patterns}

## Where this is used

- **Count**: unread messages, failed logins, words in a document.
- **Sum**: basket totals, scores, distances.
- **Find the first**: the first error in a log, the first free seat.
- **Largest or smallest**: the highest score, the cheapest flight, the hottest day.

## Common mistakes

### Returning "not found" inside the loop

```java
if (text.charAt(i) == ' ') {
    return i;
} else {
    return -1;   // gives up after looking at only the first character
}
```

The `return -1` belongs **after** the loop, once every item has been checked.

### Starting the largest-so-far badly

Starting `best` at a value larger than every item (like `best = 100` for marks out of 100) means it's never replaced. Start with the first item, or the smallest possible value.

### Using the wrong pattern

"Is there any …?" is find-the-first (return `true` as soon as you find one). "Are they all …?" is the opposite: return `false` as soon as one fails.

## Practice

::exercise{id=j1-l4.4-write-vowels}

::exercise{id=j1-l4.4-debug-first}

::exercise{id=j1-l4.4-write-palindrome}

::exercise{id=j1-l4.4-explain-pattern}

## Further reading

- **"Subgoals, context, and worked examples in learning computing problem solving"** (Morrison, Margulieux & Guzdial, 2015) `[R4]`: why naming the steps of a pattern, as this lesson does, helps learners reuse it.

## How you'll be assessed

- The **predict** exercise checks that you can follow the patterns.
- The **write** exercises check that you can use a pattern, and apply one to a new problem (*applying to a new problem*).
- The **debug** exercise checks that you can fix a find-the-first loop (*debugging*).
- The **explain** exercise checks that you can choose a pattern and say why.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l4.4")
ex.predict("j1-l4.4-predict-patterns", "Which pattern?", ["o1", "o3"], ["J1.07"],
    "Predict exactly what this program prints. Name the pattern each loop uses.",
    '''
    int firstDigit(String text) {
        for (int i = 0; i < text.length(); i++) {
            if (Character.isDigit(text.charAt(i))) {
                return i;
            }
        }
        return -1;
    }

    void main() {
        String text = "Room 42B";
        int count = 0;
        for (int i = 0; i < text.length(); i++) {
            if (text.charAt(i) == 'o') {
                count++;
            }
        }
        IO.println(count);
        IO.println(firstDigit(text));
        IO.println(firstDigit("none"));
    }
    ''', '''
    2
    5
    -1
    ''', ("The first loop counts; firstDigit finds the first. Character.isDigit is true for '0' to '9'.",
          "\"Room\" has two o's. The first digit, 4, is at index 5. \"none\" has no digits, so -1."), difficulty=2)

def vowels(w): return sum(1 for c in w.lower() if c in "aeiou")
ex.method("write", "j1-l4.4-write-vowels", "Counting vowels", ["o1", "o3"], ["J1.07"], ["IMPL"],
    "Complete `countVowels` so it returns how many vowels (a, e, i, o, u, in any capitals) a word contains.",
    [("countVowels", [("word", "String")], "int")], {"countVowels": vowels},
    [(None, ["Education"]), (None, ["rhythm"]), (None, ["AEIOU"])],
    [(None, [""], "empty"), (None, ["a"], "one vowel"), (None, ["Programming"], "a longer word"), (None, ["queue"], "repeated vowels"), (None, ["Hello World"], "two words")],
    'int countVowels(String word) {\n    return 0; // replace this with a loop\n}\n\nvoid main() {\n    IO.println(countVowels("Education")); // should print 5\n}\n',
    'int countVowels(String word) {\n    String lower = word.toLowerCase();\n    int count = 0;\n    for (int i = 0; i < lower.length(); i++) {\n        if ("aeiou".indexOf(lower.charAt(i)) != -1) {\n            count++;\n        }\n    }\n    return count;\n}\n\nvoid main() {\n    IO.println(countVowels("Education")); // should print 5\n}\n',
    {"lower-case-only": 'int countVowels(String word) {\n    int count = 0;\n    for (int i = 0; i < word.length(); i++) {\n        if ("aeiou".indexOf(word.charAt(i)) != -1) {\n            count++;\n        }\n    }\n    return count;\n}\n\nvoid main() {\n}\n'},
    ("Which pattern is 'how many'? How will you deal with capital letters?",
     "Lower-case the word first, then count characters for which \"aeiou\".indexOf(c) != -1."), group="loop-patterns")

def largest(n): return max(int(d) for d in str(n))
ex.method("write", "j1-l4.4-retrieve-largest", "The largest digit", ["o1"], ["J1.07"], ["IMPL"],
    "Complete `largestDigit` so it returns the largest digit of a non-negative whole number. For example, `largestDigit(4071)` is 7. Hint: `n % 10` is the last digit and `n / 10` removes it.",
    [("largestDigit", [("n", "int")], "int")], {"largestDigit": largest},
    [(None, [4071]), (None, [5]), (None, [0])],
    [(None, [999], "all nines"), (None, [10], "ten"), (None, [123456], "increasing"), (None, [907], "middle zero"), (None, [800000], "big first digit")],
    'int largestDigit(int n) {\n    return 0; // replace this with a loop\n}\n\nvoid main() {\n    IO.println(largestDigit(4071)); // should print 7\n}\n',
    'int largestDigit(int n) {\n    int best = 0;\n    while (n > 0) {\n        int digit = n % 10;\n        if (digit > best) {\n            best = digit;\n        }\n        n = n / 10;\n    }\n    return best;\n}\n\nvoid main() {\n    IO.println(largestDigit(4071)); // should print 7\n}\n',
    {"last-digit-only": 'int largestDigit(int n) {\n    return n % 10;\n}\n\nvoid main() {\n}\n'},
    ("Track the largest digit seen so far, taking digits off the end one at a time.",
     "best = 0; while (n > 0) { digit = n % 10; if (digit > best) best = digit; n = n / 10; }"),
    role="retrieval", group="loop-patterns")

def first_space(t):
    return t.find(" ")
ex.method("write", "j1-l4.4-retrieve-space", "The first space", ["o1", "o3"], ["J1.07"], ["IMPL"],
    "Complete `firstSpace` using a loop (not `indexOf`) so it returns the index of the first space in some text, or -1 if there isn't one.",
    [("firstSpace", [("text", "String")], "int")], {"firstSpace": first_space},
    [(None, ["hello world"]), (None, ["nospace"]), (None, [" start"])],
    [(None, [""], "empty"), (None, ["a b c"], "several spaces"), (None, ["end "], "space at the end"), (None, ["two  spaces"], "double space"), (None, ["x"], "one letter")],
    'int firstSpace(String text) {\n    return 0; // replace this with a loop\n}\n\nvoid main() {\n    IO.println(firstSpace("hello world")); // should print 5\n}\n',
    "int firstSpace(String text) {\n    for (int i = 0; i < text.length(); i++) {\n        if (text.charAt(i) == ' ') {\n            return i;\n        }\n    }\n    return -1;\n}\n\nvoid main() {\n    IO.println(firstSpace(\"hello world\")); // should print 5\n}\n",
    {"gives-up-early": "int firstSpace(String text) {\n    for (int i = 0; i < text.length(); i++) {\n        if (text.charAt(i) == ' ') {\n            return i;\n        } else {\n            return -1;\n        }\n    }\n    return -1;\n}\n\nvoid main() {\n}\n"},
    ("Find the first: return as soon as you find a match. What do you return if you never find one?",
     "Loop over the indexes; if charAt(i) == ' ' return i. After the loop, return -1."),
    role="retrieval", group="loop-patterns")

def first_vowel(s):
    for i, c in enumerate(s.lower()):
        if c in "aeiou":
            return i
    return -1
ex.method("debug", "j1-l4.4-debug-first", "First or last?", ["o1"], ["J1.07"], ["DEBUG"],
    "`firstVowel` should return the index of the **first** vowel in a word, or -1 if it has none. For `\"Banana\"` it returns 5 instead of 1. Find and fix the bug.",
    [("firstVowel", [("word", "String")], "int")], {"firstVowel": first_vowel},
    [(None, ["Banana"]), (None, ["sky"]), (None, ["Apple"])],
    [(None, [""], "empty"), (None, ["strength"], "one vowel late"), (None, ["queue"], "vowels together"), (None, ["Rhythm"], "no vowels"), (None, ["xyzE"], "capital vowel last")],
    'int firstVowel(String word) {\n    String lower = word.toLowerCase();\n    int found = -1;\n    for (int i = 0; i < lower.length(); i++) {\n        if ("aeiou".indexOf(lower.charAt(i)) != -1) {\n            found = i;\n        }\n    }\n    return found;\n}\n\nvoid main() {\n    IO.println(firstVowel("Banana")); // should print 1\n}\n',
    'int firstVowel(String word) {\n    String lower = word.toLowerCase();\n    for (int i = 0; i < lower.length(); i++) {\n        if ("aeiou".indexOf(lower.charAt(i)) != -1) {\n            return i;\n        }\n    }\n    return -1;\n}\n\nvoid main() {\n    IO.println(firstVowel("Banana")); // should print 1\n}\n',
    {"case-sensitive": 'int firstVowel(String word) {\n    for (int i = 0; i < word.length(); i++) {\n        if ("aeiou".indexOf(word.charAt(i)) != -1) {\n            return i;\n        }\n    }\n    return -1;\n}\n\nvoid main() {\n}\n'},
    ("Trace Banana. What happens to found each time another vowel turns up?",
     "found is overwritten by every later vowel. Return i as soon as you find the first one, and return -1 after the loop."))

def palindrome(s):
    t = s.lower()
    return t == t[::-1]
ex.method("write", "j1-l4.4-write-palindrome", "Palindromes", ["o2", "o3"], ["J1.07", "J1.09"], ["XFER"],
    "A palindrome reads the same forwards and backwards, like `level` or `Noon` (ignore capitals). Complete `isPalindrome`. Think about which pattern fits before you write any code.",
    [("isPalindrome", [("word", "String")], "boolean")], {"isPalindrome": palindrome},
    [(None, ["level"]), (None, ["Noon"]), (None, ["java"])],
    [(None, [""], "empty"), (None, ["a"], "one letter"), (None, ["ab"], "two different"), (None, ["Racecar"], "racecar"), (None, ["abca"], "almost")],
    'boolean isPalindrome(String word) {\n    return false; // replace this with a loop\n}\n\nvoid main() {\n    IO.println(isPalindrome("level")); // should print true\n}\n',
    'boolean isPalindrome(String word) {\n    String lower = word.toLowerCase();\n    int last = lower.length() - 1;\n    for (int i = 0; i < lower.length() / 2; i++) {\n        if (lower.charAt(i) != lower.charAt(last - i)) {\n            return false;\n        }\n    }\n    return true;\n}\n\nvoid main() {\n    IO.println(isPalindrome("level")); // should print true\n}\n',
    {"case-sensitive": 'boolean isPalindrome(String word) {\n    int last = word.length() - 1;\n    for (int i = 0; i < word.length() / 2; i++) {\n        if (word.charAt(i) != word.charAt(last - i)) {\n            return false;\n        }\n    }\n    return true;\n}\n\nvoid main() {\n}\n',
     "first-and-last-only": 'boolean isPalindrome(String word) {\n    String lower = word.toLowerCase();\n    return lower.length() == 0 || lower.charAt(0) == lower.charAt(lower.length() - 1);\n}\n\nvoid main() {\n}\n'},
    ("It's an 'are they all …?' question: every pair of characters from opposite ends must match. Return false as soon as one pair doesn't.",
     "Compare charAt(i) with charAt(length - 1 - i) for i from 0 to half the length; return false on a mismatch, true after the loop."),
    difficulty=3)

ex.explain("j1-l4.4-explain-pattern", "Choosing a pattern", ["o2"], ["J1.09"],
    "You're asked: *does a password contain at least one digit?* Which loop pattern would you use, and why? Say what the loop returns, and when.",
    "A full answer chooses find-the-first: loop over the characters, return true as soon as a digit is found, and return false after the loop if none was found; there's no need to keep looking after the first digit.",
    {2: ("Chooses find-the-first (or 'any'), and says to return true as soon as a digit is found and false only after checking every character.",
         ["Find the first. Loop over each character, and as soon as one is a digit, return true. If the loop gets to the end without finding one, return false.",
          "It's an 'is there any' question, so stop at the first digit and return true; return false after the loop."]),
     1: ("Picks a workable pattern, such as counting digits and checking the count is above 0, or find-the-first without explaining when each value is returned.",
         ["Count the digits and check if the count is more than 0.", "Find the first digit."]),
     0: ("Incorrect, for example returns false at the first non-digit, or uses track-the-largest.",
         ["Loop through and return false as soon as you see a letter.", "Track the largest digit."])})
print("4.4 written")
