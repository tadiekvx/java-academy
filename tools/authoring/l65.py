from build import *

Lesson("j1-l6.5", "Debugging systematically", ["J1.13"], [
    ("o1", "Follow the cycle: reproduce, hypothesise, test, fix, verify"),
    ("o2", "Find several bugs in the same method by checking one case at a time"),
    ("o3", "Explain why you change one thing at a time and check after each change"),
], ["j1-l6.4"], 40, ["R16", "R8"], r'''
## Before you start

You should be able to read compiler errors and stack traces ([Errors are feedback](j1-l1.2), [Exceptions and stack traces](j1-l6.4)).

**Quick check.** Where is the first place to look in a stack trace?

<details><summary>Show the answer</summary>

The first `at` line that names your own file: that's where your code was running when the problem showed up.

</details>

## Explanation

Sometimes there's no error message at all: the program runs and gives the **wrong answer**. Finding out why is **debugging**, and it's a skill you can practise, not a talent you either have or don't. Research on how people debug finds that the people who are best at it don't have better instincts; they follow a method.

### The method

1. **Reproduce it.** Find a specific input that gives the wrong answer, and write down what you expected and what you got. If you can't make it happen reliably, you can't tell whether you've fixed it.
2. **Make a hypothesis.** Think about *why* it might happen, and write down one specific guess: "I think the loop skips the first element."
3. **Test the hypothesis.** Don't change the code yet. Check whether your guess is true: trace by hand, or print values while the program runs.
4. **Fix it.** Make the **smallest** change that fixes that one cause.
5. **Verify.** Run the original failing case, **and** the cases that used to pass. A fix can break something else.

Then repeat for the next problem.

### Reproduce: the smallest failing case

Shrink the input until only the essential part is left. A bug that shows up on `{3, 1, 2}` is easier to study than one on a list of 50 numbers. Ask: *what's the smallest input that still goes wrong?*

### Hypothesise and test: look at the values

Don't stare at code and hope. **Make the program show you what it's doing.** The simplest way is to print:

```java runnable
int largest(int[] values) {
    int best = 0;
    for (int value : values) {
        IO.println("looking at " + value + ", best so far " + best);
        if (value > best) {
            best = value;
        }
    }
    return best;
}

void main() {
    IO.println(largest(new int[] {-4, -2, -9}));
}
```

This returns `0`, not `-2`. The printed lines show `best so far 0` at every step: `best` started at 0, and none of the values beats it. Hypothesis confirmed: starting `best` at 0 is wrong when every value is negative. The fix is to start with the first element.

Printing is a perfectly professional technique. (Real programmers also use a tool called a **debugger** to pause a running program and look at its variables; you'll meet one later.) Remember to take the prints out when you're done.

### One change at a time

If you change three things and the program works, you don't know which change mattered, and you may have added a new bug. If it still fails, you don't know whether any of your changes helped. **Change one thing, check, then change the next.**

### Several bugs at once

One method can have more than one bug. After you fix one, the failing tests may not all go away, and that's normal: the remaining failures belong to the next bug. Use each failing case as a clue: *which kind of input still fails? What do they have in common?*

### When you're stuck

- **Explain it out loud** (to a friend, or to a rubber duck): saying it step by step often reveals the gap.
- **Take a break**: fresh eyes spot things tired ones miss.
- **Check your assumptions**: the thing you're *sure* is right is often the thing that's wrong.
- **Ask for help well**: say what you expected, what happened, what you've tried. (The mentor in this course will ask for exactly that.)

## Worked examples

### Example 1: one bug, the full method

*Task: `countWords` should count the words in a sentence. For `"hello big world"` it returns 2 instead of 3.*

**Step 1 — Reproduce.** `countWords("hello big world")` → expected 3, got 2. Smaller: `countWords("hi there")` → expected 2.

```java
int countWords(String text) {
    int spaces = 0;
    for (int i = 0; i < text.length(); i++) {
        if (text.charAt(i) == ' ') {
            spaces++;
        }
    }
    return spaces;
}
```

**Step 2 — Hypothesis.** The code counts *spaces*, and there's one fewer space than words.

**Step 3 — Test it.** `"hi there"` has 1 space: the method returns 1, expected 2. One short, as guessed. What about `""`? There are no spaces, and the answer should be 0, not 1. So "add 1" alone isn't the whole story: a hypothesis can be partly right.

**Step 4 — Fix, carefully.** Return `spaces + 1`, unless the text is empty.

**Step 5 — Verify every case:** `"hello big world"` → 3; `"hi there"` → 2; `""` → 0; and `"one"` → 1.

### Example 2: two bugs hiding together

*Task: `sumOfSquares(n)` should return 1² + 2² + … + n². It returns the wrong answer for every n.*

```java
int sumOfSquares(int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += i * 2;
    }
    return total;
}
```

**Step 1 — Reproduce.** `sumOfSquares(3)` → expected 14 (1 + 4 + 9), got 2 (0 + 2 + 4).

**Step 2 — First hypothesis: the loop range is wrong.** It starts at 0 and stops before `n`, but we want 1 to `n`. Fix only that: `for (int i = 1; i <= n; i++)`.

**Step 3 — Re-run.** Now `sumOfSquares(3)` gives 2 + 4 + 6 = 12. Still wrong, but different: the first fix helped, and a second bug remains.

**Step 4 — Second hypothesis: `i * 2` doubles instead of squaring.** Change it to `i * i`. Now `sumOfSquares(3)` is 14. ✓

Because we changed one thing at a time, we know both changes were needed.

## Predict, then run

::exercise{id=j1-l6.5-predict-trace}

## Where this is used

- **All of software engineering.** Developers spend more time finding and fixing problems than writing new code.
- **Bug reports**: a good one gives a minimal way to reproduce the problem, exactly step 1 of the method.
- **Incident response**: when a live system misbehaves, teams follow this same cycle under pressure.

## Common mistakes

### Changing code at random

"Try something and see" can accidentally work, but you won't know why, and it often hides the real bug. Form a hypothesis first.

### Changing several things at once

You lose the ability to tell which change helped, or which one broke something.

### Not re-checking old cases

A fix for the new failing case can break a case that worked. Always run the old cases too.

### Stopping when the one failing case passes

Check the edges too: empty, zero, one item, the largest and smallest values.

## Practice

::exercise{id=j1-l6.5-debug-stats}

::exercise{id=j1-l6.5-debug-wordcount}

::exercise{id=j1-l6.5-explain-method}

## Further reading

- **"Debugging: a review of the literature from an educational perspective"** (McCauley et al., 2008) `[R16]`: what research says about how people debug, and which habits help most.

## How you'll be assessed

- The **predict** exercise checks that you can follow a trace of values.
- The **debug** exercises check that you can find and fix several bugs in one method (*debugging*).
- The **explain** exercise checks that you can describe the debugging cycle and why you change one thing at a time (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l6.5")
ex.predict("j1-l6.5-predict-trace", "Follow the printed values", ["o1", "o2"], ["J1.13"],
    "This program prints its working as it goes. Predict exactly what it prints.",
    '''
    int countWords(String text) {
        if (text.isEmpty()) {
            return 0;
        }
        int spaces = 0;
        for (int i = 0; i < text.length(); i++) {
            if (text.charAt(i) == ' ') {
                spaces++;
            }
        }
        IO.println("spaces: " + spaces);
        return spaces + 1;
    }

    void main() {
        IO.println(countWords("hello big world"));
        IO.println(countWords(""));
        IO.println(countWords("one"));
    }
    ''', '''
    spaces: 2
    3
    0
    spaces: 0
    1
    ''', ("Each call to countWords prints its 'spaces' line before it returns, unless the text is empty.",
          "\"hello big world\" has 2 spaces, so it prints spaces: 2 and returns 3. The empty text returns 0 straight away. \"one\" has no spaces."),
    difficulty=2)

def stats(v): return [min(v), max(v), sum(v)]
ex.method("debug", "j1-l6.5-debug-stats", "Three bugs in one method", ["o1", "o2"], ["J1.13"], ["DEBUG"],
    "`stats` is given a non-empty array and should return a new array of three ints: the **smallest** element, the **largest** element and the **sum** of all elements. For `{3, 1, 2}` it should return `{1, 3, 6}`. This version has **three separate bugs**. Use the method from the lesson: find a small failing case, form a hypothesis, fix **one** thing, and check again.",
    [("stats", [("values", "int[]")], "int[]")], {"stats": stats},
    [(None, [[3, 1, 2]]), (None, [[5]]), (None, [[-4, -2, -9]])],
    [(None, [[1, 2, 3]], "ascending"), (None, [[9, 8, 7]], "descending"), (None, [[0, 0, 0]], "zeros"), (None, [[10, -10]], "balanced"), (None, [[100, 5, 50, 1, 75]], "scrambled")],
    'int[] stats(int[] values) {\n    int smallest = 0;\n    int largest = values[0];\n    int sum = 0;\n    for (int i = 1; i < values.length; i++) {\n        int value = values[i];\n        if (value < smallest) {\n            smallest = value;\n        }\n        if (value < largest) {\n            largest = value;\n        }\n        sum += value;\n    }\n    return new int[] {smallest, largest, sum};\n}\n\nvoid main() {\n    IO.println(Arrays.toString(stats(new int[] {3, 1, 2}))); // should print [1, 3, 6]\n}\n',
    'int[] stats(int[] values) {\n    int smallest = values[0];\n    int largest = values[0];\n    int sum = 0;\n    for (int i = 0; i < values.length; i++) {\n        int value = values[i];\n        if (value < smallest) {\n            smallest = value;\n        }\n        if (value > largest) {\n            largest = value;\n        }\n        sum += value;\n    }\n    return new int[] {smallest, largest, sum};\n}\n\nvoid main() {\n    IO.println(Arrays.toString(stats(new int[] {3, 1, 2}))); // should print [1, 3, 6]\n}\n',
    {"two-of-three": 'int[] stats(int[] values) {\n    int smallest = values[0];\n    int largest = values[0];\n    int sum = 0;\n    for (int i = 1; i < values.length; i++) {\n        int value = values[i];\n        if (value < smallest) {\n            smallest = value;\n        }\n        if (value > largest) {\n            largest = value;\n        }\n        sum += value;\n    }\n    return new int[] {smallest, largest, sum};\n}\n\nvoid main() {\n}\n'},
    ("Start with the smallest input that fails, {5}. Which of the three results is wrong, and why?",
     "The bugs: smallest starts at 0 (should be values[0]); largest uses < (should be >); the loop starts at index 1 (should start at 0), so the first element is left out of the sum."),
    notes="Three bugs: smallest initialised to 0 (fails for all-positive or negative arrays); largest uses `<` (finds the smallest); loop starts at 1 so the first element is missed in the sum. The `two-of-three` solution fixes the first two but not the loop start, so it must still fail.", difficulty=3)

def count_words(t):
    return len(t.split()) if t.strip() else 0
ex.method("debug", "j1-l6.5-debug-wordcount", "Counting words", ["o1", "o2"], ["J1.13"], ["DEBUG"],
    "`countWords` should count the words in some text, where words are separated by one or more spaces. `\"hello big world\"` is 3, `\"\"` is 0 and `\"  \"` (only spaces) is 0. Texts can start or end with spaces, and have more than one space in a row. This version gets some cases wrong. Reproduce a failing case, form a hypothesis, fix it, then check the other cases again.",
    [("countWords", [("text", "String")], "int")], {"countWords": count_words},
    [(None, ["hello big world"]), (None, [""]), (None, ["one"])],
    [(None, ["  "], "only spaces"), (None, [" leading"], "leading space"), (None, ["trailing "], "trailing space"), (None, ["a  b"], "double space"), (None, ["  many   spaces  here "], "messy")],
    'int countWords(String text) {\n    int spaces = 0;\n    for (int i = 0; i < text.length(); i++) {\n        if (text.charAt(i) == \' \') {\n            spaces++;\n        }\n    }\n    return spaces + 1;\n}\n\nvoid main() {\n    IO.println(countWords("hello big world")); // should print 3\n}\n',
    'int countWords(String text) {\n    int words = 0;\n    boolean inWord = false;\n    for (int i = 0; i < text.length(); i++) {\n        if (text.charAt(i) == \' \') {\n            inWord = false;\n        } else if (!inWord) {\n            inWord = true;\n            words++;\n        }\n    }\n    return words;\n}\n\nvoid main() {\n    IO.println(countWords("hello big world")); // should print 3\n}\n',
    {"spaces-plus-one": 'int countWords(String text) {\n    int spaces = 0;\n    for (int i = 0; i < text.length(); i++) {\n        if (text.charAt(i) == \' \') {\n            spaces++;\n        }\n    }\n    return spaces + 1;\n}\n\nvoid main() {\n}\n'},
    ("Which inputs fail, and what do they have in common? Spaces don't always mean 'one more word'.",
     "Count the start of each word instead: a non-space character that follows a space (or the start of the text). A boolean 'inWord' remembers which state you're in."),
    difficulty=3, notes="Spaces-plus-one fails on empty, only-spaces, leading, trailing and doubled spaces. A word is counted at each transition from a space (or the start) to a non-space.")

ex.explain("j1-l6.5-explain-method", "Why one change at a time?", ["o1", "o3"], ["J1.13"],
    "A friend's program gives wrong answers. They change five lines at once, and now it works for one test but fails on another. Describe the steps you'd suggest instead, and explain why changing one thing at a time is better.",
    "A full answer lists the cycle (reproduce with a small failing case, form a hypothesis, test it, make one small fix, verify old and new cases) and explains that changing several things at once hides which change helped or broke something.",
    {2: ("Describes reproducing a small failing case, a hypothesis, a single small fix, and re-checking, and says that changing many things at once makes it impossible to know which change fixed or broke what.",
         ["First find the smallest input that fails, then guess what the cause is and check that guess, then change just one thing and test again, including the cases that used to work. If you change five lines at once you can't tell which one fixed it or which one broke the other test.",
          "Reproduce the bug with a small example, make a hypothesis, fix one thing, then verify. Changing lots at once means you don't know what helped, and you might have added new bugs."]),
     1: ("Gives some sensible steps or a reason, but not both, or the reasoning is vague.",
         ["Change one line, then test it.", "You should look for the bug before changing things."]),
     0: ("Gives no useful steps, or says changing many things at once is better.",
         ["Change everything you can think of until it works.", "Just rewrite the whole program."])})
print("6.5 written")
