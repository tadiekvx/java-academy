import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-2"
from build import *
import outline
reg = outline.register

FOOT = '''
An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
'''

# ====================================================================== 2.2.1
Lesson("j2-l2.1", "Private fields and invariants", ["J2.05"], [
    ("o1", "Make fields private and give other code a small set of methods to use them"),
    ("o2", "Enforce an invariant in a constructor and in the methods that change state"),
    ("o3", "Find the ways a class can be put into an invalid state, and close them"),
], ["j2-l1.4"], 45, ["R8", "R16"], r'''
## Before you start

You should be able to write a class with fields, a constructor and methods ([Methods and this](j2-l1.2)).

**Quick check.** What does a constructor do when you write `new Account(500)`?

<details><summary>Show the answer</summary>

It runs once, as the object is created, and sets up its fields from the arguments.

</details>

## Explanation

### The problem with open fields

In the classes so far, every field could be read and changed from anywhere:

```java
class Account {
    int balance;
}
// somewhere else:
account.balance = -5000;     // nothing stops this
```

If an account should never have a negative balance, that rule is only as strong as the *weakest* piece of code that touches `balance`. With a hundred places able to change it, one careless line breaks the rule for the whole program.

### Invariants: facts that must always be true

An **invariant** is a statement about an object that must be true whenever other code can see it: *a balance is never negative*, *a temperature setting is between 10 and 30*, *a `Money` amount is a whole number of pence that isn't below zero*. Encapsulation is how you make an invariant something the **class** guarantees, instead of something every caller has to remember.

### `private`: only the class itself can touch this

```java
class Account {
    private int balance;     // only code inside Account can use this name

    int balance() {          // a read-only "getter"
        return balance;
    }
}
```

Other code can no longer write `account.balance = ...`. It has to go through the methods you provide, and those methods can check the rules.

There are three levels you'll use now:

| Modifier | Who can use it |
|---|---|
| `private` | only the class itself |
| *(none)*, "package-private" | any class in the same package |
| `public` | everyone |

A good default: **fields `private`, and only the methods that other code genuinely needs not private**.

One thing to know about this course's exercises: in a single compact file, the classes sit next to `main`, and Java lets code in the same file see each other's private members. So the compiler won't stop `main` from touching a private field here, although it would in a real project where each class has its own file. The exercises therefore check that you wrote `private`, and they check behaviour too.

### Enforcing the rule: refuse bad input at the door

The place to enforce an invariant is every spot where state can enter or change: the **constructor** and any method that changes a field. If the input would break the rule, **refuse it** by throwing an exception:

```java
class Money {
    private final int pence;

    Money(int pence) {
        if (pence < 0) {
            throw new IllegalArgumentException("pence can't be negative: " + pence);
        }
        this.pence = pence;
    }
}
```

`throw new IllegalArgumentException(...)` stops the method right there, and the object is never created in a bad state. The caller can handle that with `try` / `catch`, which you'll learn properly in lesson 2.5.1; in this lesson's exercises the driver code already does it for you.

Because a `Money` can only be built through that constructor, **every `Money` that exists is valid**. That's the payoff: you check once, and everyone downstream can trust it.

### A method that changes state must protect the rule too

```java
void setTarget(int t) {
    if (t < 10 || t > 30) {
        return;                // ignore a request outside the range
    }
    target = t;
}
```

Whether to refuse by throwing, by ignoring, or by returning `false` is a design choice. What matters is that there's **no path** around it.

### Why this lets code change safely

Once the fields are private, you can change *how* a class stores things without breaking anyone. If `balance` is later stored as a different type, only the class changes, because outside code only ever used `balance()`.

## Worked examples

### Example 1: protecting a thermostat

*Task: a `Thermostat` target must stay between 10 and 30. Right now, anyone can write `th.target = 99`.*

**Step 1 — Name the invariant:** `10 <= target <= 30`.

**Step 2 — Make the field `private`** so it can't be set directly.

**Step 3 — Give a method that checks:** `setTarget` ignores values outside the range.

**Step 4 — Change the callers** to use `setTarget` instead of assigning the field.

```java runnable
class Thermostat {
    private int target = 20;

    void setTarget(int t) {
        if (t < 10 || t > 30) {
            return;
        }
        target = t;
    }

    int target() {
        return target;
    }
}

void main() {
    Thermostat th = new Thermostat();
    th.setTarget(25);
    th.setTarget(99);
    IO.println(th.target());
}
```

**Step 5 — Check.** It prints `25`: the request for 99 was refused.

### Example 2: how many ways can this break?

*Task: how can `Account` below end up with a negative balance?*

```java
class Account {
    public int balance;
    public Account(int balance) { this.balance = balance; }
    public void setBalance(int balance) { this.balance = balance; }
}
```

**Step 1 — Look at every way state gets in.** The constructor, `setBalance`, and the public field itself.

**Step 2 — Find a bad input for each.** `new Account(-1)`, `setBalance(-1)`, and `acct.balance = -1`.

**Step 3 — Close all three:** validate in the constructor, validate in the setter, and make the field `private`. Closing two of three still leaves a hole.

## Where this is used

- **Money, identifiers, counts, ranges:** anything with a rule is a candidate for an invariant.
- **Libraries** you'll use later (collections, dates) hide their fields completely, so their authors can improve them without breaking your code.
- **Security:** a lot of vulnerabilities come from a state that was supposed to be impossible.

## Common mistakes

:::mistake{id=MC38}
**Making the field `private` but putting no check in the constructor.** `new Account(-1)` still builds a bad object.
:::

:::mistake{id=MC39}
**Validating in the setter but leaving the field `public`.** Callers go around the check by assigning the field directly.
:::

:::mistake{id=MC40}
**Treating a getter and setter for every field as encapsulation.** If a setter lets anyone assign anything, nothing is protected. Offer the operations the class means (`deposit`, `setTarget`), with rules.
:::

## Practice

::exercise{id=j2-l2.1-write-money}

::exercise{id=j2-l2.1-debug-bypass}

::exercise{id=j2-l2.1-explain-encapsulation}

## Further reading

- **McCauley et al. (2008)** `[R16]` review how debugging is taught; tracking down *which* of several routes into a class broke an invariant is a good example of the hypothesis-and-test cycle.
- **Qian & Lehman (2017)** `[R8]` cover novice misconceptions about how classes and objects protect state.

## How you'll be assessed

- The **write** exercise checks that you can make a class whose constructor refuses invalid values and whose field is private (*implementation*).
- The **debug** exercise checks that you can find code that goes around a rule and close the route (*debugging*).
- The **explain** exercise checks that you can find all the ways a class can be broken and say why encapsulation helps (*explanation*).
''' + FOOT)

ex = Exercises("j2-l2.1")
ex.method("write", "j2-l2.1-write-money", "Money that can't be negative", ["o1", "o2"], ["J2.05"], ["IMPL"],
    "Make `Money` protect its invariant: an amount of pence is **never negative**. The constructor must refuse a negative amount by throwing an `IllegalArgumentException`, and the `pence` field must be `private`. The driver `run` adds two amounts and returns `\"<total> pence\"`, or `\"rejected\"` if either amount is refused.",
    [("run", [("a", "int"), ("b", "int")], "String")],
    {"run": lambda a, b: "rejected" if a < 0 or b < 0 else f"{a + b} pence"},
    [("run", [100, 250]), ("run", [-1, 5]), ("run", [0, 0])],
    [("run", [5, -1]), ("run", [0, 5]), ("run", [-100, -100]), ("run", [1, 1]), ("run", [999, 1])],
    'class Money {\n    int pence;\n\n    Money(int pence) {\n        this.pence = pence;\n    }\n\n    int pence() {\n        return pence;\n    }\n\n    Money plus(Money other) {\n        return new Money(pence + other.pence);\n    }\n}\n\nString run(int a, int b) {\n    try {\n        Money total = new Money(a).plus(new Money(b));\n        return total.pence() + " pence";\n    } catch (IllegalArgumentException e) {\n        return "rejected";\n    }\n}',
    'class Money {\n    private final int pence;\n\n    Money(int pence) {\n        if (pence < 0) {\n            throw new IllegalArgumentException("negative money: " + pence);\n        }\n        this.pence = pence;\n    }\n\n    int pence() {\n        return pence;\n    }\n\n    Money plus(Money other) {\n        return new Money(pence + other.pence);\n    }\n}\n\nString run(int a, int b) {\n    try {\n        Money total = new Money(a).plus(new Money(b));\n        return total.pence() + " pence";\n    } catch (IllegalArgumentException e) {\n        return "rejected";\n    }\n}',
    {"field-left-public": 'class Money {\n    int pence;\n    Money(int pence) {\n        if (pence < 0) throw new IllegalArgumentException("negative");\n        this.pence = pence;\n    }\n    int pence() { return pence; }\n    Money plus(Money other) { return new Money(pence + other.pence); }\n}\n\nString run(int a, int b) {\n    try {\n        Money total = new Money(a).plus(new Money(b));\n        return total.pence() + " pence";\n    } catch (IllegalArgumentException e) {\n        return "rejected";\n    }\n}',
     "rejects-zero": 'class Money {\n    private final int pence;\n    Money(int pence) {\n        if (pence <= 0) throw new IllegalArgumentException("not positive");\n        this.pence = pence;\n    }\n    int pence() { return pence; }\n    Money plus(Money other) { return new Money(pence + other.pence); }\n}\n\nString run(int a, int b) {\n    try {\n        Money total = new Money(a).plus(new Money(b));\n        return total.pence() + " pence";\n    } catch (IllegalArgumentException e) {\n        return "rejected";\n    }\n}'},
    ("The check belongs in the constructor, before the field is set. Zero is allowed.", "if (pence < 0) throw new IllegalArgumentException(...); and private final int pence;"),
    source_tests=[("the field is private", ["private"], None), ("the constructor refuses with an exception", ["throw new IllegalArgumentException"], None)],
    difficulty=3)

def thermo(values):
    t = 20
    for v in values:
        if 10 <= v <= 30: t = v
    return t
ex.method("debug", "j2-l2.1-debug-bypass", "Going round the rule", ["o3"], ["J2.05"], ["DEBUG"],
    "`Thermostat` has a rule in `setTarget`: only values from 10 to 30 are accepted, and anything else is ignored. But `run` still ends up with out-of-range values. Find the route around the rule and close it: make the field `private`, and make `run` use `setTarget`.",
    [("run", [("values", "int[]")], "int")], {"run": thermo},
    [("run", [[5, 25]]), ("run", [[35]]), ("run", [[12, 8, 29]])],
    [("run", [[]]), ("run", [[10]]), ("run", [[30, 31]]), ("run", [[9, 9, 9]]), ("run", [[15, 40, 22, -3]])],
    'class Thermostat {\n    int target = 20;\n\n    void setTarget(int t) {\n        if (t < 10 || t > 30) {\n            return;\n        }\n        target = t;\n    }\n\n    int target() {\n        return target;\n    }\n}\n\nint run(int[] values) {\n    Thermostat th = new Thermostat();\n    for (int v : values) {\n        th.target = v;\n    }\n    return th.target();\n}',
    'class Thermostat {\n    private int target = 20;\n\n    void setTarget(int t) {\n        if (t < 10 || t > 30) {\n            return;\n        }\n        target = t;\n    }\n\n    int target() {\n        return target;\n    }\n}\n\nint run(int[] values) {\n    Thermostat th = new Thermostat();\n    for (int v : values) {\n        th.setTarget(v);\n    }\n    return th.target();\n}',
    {"private-but-still-direct": 'class Thermostat {\n    private int target = 20;\n    void setTarget(int t) {\n        if (t < 10 || t > 30) return;\n        target = t;\n    }\n    int target() { return target; }\n}\n\nint run(int[] values) {\n    Thermostat th = new Thermostat();\n    for (int v : values) {\n        th.target = v;\n    }\n    return th.target();\n}',
     "setter-range-off-by-one": 'class Thermostat {\n    private int target = 20;\n    void setTarget(int t) {\n        if (t <= 10 || t > 30) return;\n        target = t;\n    }\n    int target() { return target; }\n}\n\nint run(int[] values) {\n    Thermostat th = new Thermostat();\n    for (int v : values) {\n        th.setTarget(v);\n    }\n    return th.target();\n}'},
    ("The rule is in setTarget. Does run ever call it?", "Make target private and call th.setTarget(v) instead of assigning th.target = v."),
    source_tests=[("the field is private", ["private int target"], None), ("run goes through the setter", ["th.setTarget("], None)],
    difficulty=3)
ex.explain("j2-l2.1-explain-encapsulation", "Break the class", ["o3", "o1"], ["J2.05"],
    "This class is meant to guarantee that a balance is **never negative**:\n\n```java\nclass Account {\n    public int balance;\n    public Account(int balance) { this.balance = balance; }\n    public void setBalance(int balance) { this.balance = balance; }\n}\n```\n\n(a) Find **three different ways** to put an `Account` into a state with a negative balance. (b) Say how you would redesign the class so that none of them works. (c) Give one reason why keeping the field private makes the class easier to change later.",
    "A full answer lists the three routes (the constructor with a negative value, setBalance with a negative value, and direct assignment to the public field), redesigns with a private field, a constructor check and checked operations such as deposit/withdraw, and gives a reason such as callers only depend on the methods so the internal representation can change.",
    {2: ("Finds all three routes (constructor, setBalance, the public field), redesigns with a private field, validation in the constructor and in the methods that change it, and gives a valid reason such as other code only depends on the methods so the inside can change.",
         ["Three ways: new Account(-5); acct.setBalance(-5); and acct.balance = -5 directly, since the field is public. I'd make balance private, check in the constructor and refuse a negative amount, and replace setBalance with deposit and withdraw that check the rule. Because outside code only uses those methods, I could change how the balance is stored later without breaking anything.",
          "The constructor accepts any number, setBalance accepts any number, and the public field can be assigned directly. Fix: private field, throw in the constructor for negative values, and only offer operations that keep it valid. A private field also means I can change its type later without touching callers."]),
     1: ("Finds one or two of the routes, or redesigns without closing all of them, or gives no reason about future change.",
         ["You can call setBalance with a negative number.", "Make the field private."]),
     0: ("Incorrect, for example says the class is already safe, or that making the setter private is enough.",
         ["It's already safe.", "Just make the constructor private."])})
reg({"j2-l2.1": ("Private fields and invariants", ["J2.05"])},
    {"MC38": (["J2.05"], "Platform", "A private field is enough to protect an invariant, with no check in the constructor"),
     "MC39": (["J2.05"], "Platform", "Validating in the setter protects the class even while the field is public"),
     "MC40": (["J2.05"], "Platform", "A getter and setter for every field is the same as encapsulation")})

# ====================================================================== 2.2.2
Lesson("j2-l2.2", "Immutability and defensive copies", ["J2.06"], [
    ("o1", "Make a class immutable with final fields, and write methods that return new objects instead of changing this"),
    ("o2", "Prevent a class's array or list from being changed from outside, using copies"),
    ("o3", "Explain the difference between value and identity, and why value types are best immutable"),
], ["j2-l2.1", "j1-l6.3"], 45, ["R8", "I29"], r'''
## Before you start

You should know how to protect an invariant with `private` and checks ([Private fields and invariants](j2-l2.1)), and that two variables can refer to one object ([Objects and references](j2-l1.3)).

**Quick check.** If `a` and `b` refer to the same list, and you add an item through `b`, what does `a` see?

<details><summary>Show the answer</summary>

The new item. There's only one list.

</details>

## Explanation

Making fields `private` isn't the whole story. If a class holds an **array or a list**, and hands out the same one it was given (or returns its own), the outside world still has a way in.

### The leak: sharing the inside

```java
class Scores {
    private final int[] values;
    Scores(int[] values) { this.values = values; }    // keeps the caller's array
    int[] all() { return values; }                    // hands out the inside
}
```

The field is `private`, but:

- the caller still holds the same array as `values`, and can change it after the constructor finishes;
- `all()` returns the actual array, and the caller can overwrite its elements.

Either way, a "protected" object changes behind its own back.

### Defensive copies

The fix is a **defensive copy**: copy on the way in, and copy on the way out.

```java
Scores(int[] values) { this.values = values.clone(); }   // own copy
int[] all()          { return values.clone(); }          // hand out a copy
```

For lists the same idea reads `new ArrayList<>(songs)`. Now nothing outside shares the object's internals.

Alternatively, you can hand out a list that **can't be changed**. `List.copyOf(songs)` and `List.of(...)` create unmodifiable lists: elements can't be added, removed or replaced, and trying throws an exception `[I29]`.

### Immutable classes: objects that never change

The strongest protection is to make the object itself **immutable**: once built, it can't change. Recipe:

1. All fields `private` and `final` (a `final` field can be assigned only once, in the constructor).
2. No methods that change fields.
3. Methods that would "change" it return a **new** object instead.
4. If a field holds an array or list, copy it on the way in and don't expose it.

```java runnable
class Version {
    private final int major;
    private final int minor;

    Version(int major, int minor) {
        this.major = major;
        this.minor = minor;
    }

    Version bumpMinor() {
        return new Version(major, minor + 1);
    }

    @Override
    public String toString() {
        return major + "." + minor;
    }
}

void main() {
    Version v1 = new Version(1, 4);
    Version v2 = v1.bumpMinor();
    IO.println(v1 + " " + v2);
}
```

It prints `1.4 1.5`: `v1` is untouched. `String` works the same way: `"abc".toUpperCase()` gives a new string and leaves the original alone.

Immutable objects can be **shared freely**, because nobody can change them: no aliasing surprises, and no defensive copies of them needed.

### Value versus identity

Some things are defined by **what they hold**: a date, an amount of money, a version number, a point. Two `Money` objects with the same pence are, for all purposes, the same value. Others are defined by **who they are**: a bank account is still *that* account after its balance changes, and two accounts with the same balance are still different accounts.

- **Value types** should usually be **immutable** (and have `equals` and `hashCode` based on their contents, as in [static, toString and equals](j2-l1.4)).
- **Identity types** (accounts, players, connections) are usually mutable, and compared by identity.

Choosing which one a class is helps you decide whether it needs `final` fields or not. Records (lesson 2.4.1) are a shorthand for value types.

## Worked examples

### Example 1: an immutable version number

*Task: `bumpMajor` should give a new version with the major number up by one and the minor reset to 0, leaving the original alone.*

**Step 1 — Make the fields `private final`.**

**Step 2 — `bumpMajor` builds and returns a new `Version`:** `return new Version(major + 1, 0);`

**Step 3 — Check the original is untouched.** `new Version(2, 7).bumpMajor()` gives `3.0`, and the version you started with is still `2.7`.

### Example 2: closing a leak in a playlist

*Task: after `Playlist p = new Playlist(mine);` and then `mine.add("x")`, `p.size()` should not change.*

**Step 1 — Find the route in.** The constructor keeps the caller's list, so the caller's later changes show up.

**Step 2 — Copy on the way in:** `this.songs = new ArrayList<>(songs);`

**Step 3 — Check the route out.** If a getter returns `songs` itself, callers can still change it. Return `new ArrayList<>(songs)` (or `List.copyOf(songs)`) instead.

## Where this is used

- **Dates, money and identifiers** in every business system are immutable value objects.
- **Thread-safe code** is much easier when shared objects can't change.
- **Bugs** where a collection "changed itself" are nearly always a missing defensive copy.

## Common mistakes

:::mistake{id=MC41}
**Thinking `final` makes an object immutable.** `final` stops a **variable** being reassigned. A `final` array's elements can still be changed, and a `final` list can still have items added.
:::

:::mistake{id=MC42}
**Copying in the constructor but returning the internal list from a getter** (or the reverse). A leak in either direction is enough.
:::

## Practice

::exercise{id=j2-l2.2-write-version}

::exercise{id=j2-l2.2-write-scores}

::exercise{id=j2-l2.2-debug-playlist}

::exercise{id=j2-l2.2-explain-value-identity}

## Further reading

- **The `java.util.List` documentation** `[I29]` describes the unmodifiable lists returned by `List.of` and `List.copyOf`.
- **Qian & Lehman (2017)** `[R8]` discuss how novices think of references and copies.

## How you'll be assessed

- The **write** exercises check that you can write an immutable class and protect an array with copies (*implementation*).
- The **debug** exercise checks that you can find and close a leak in both directions (*debugging*).
- The **explain** exercise checks that you can distinguish value from identity and say what that means for immutability (*explanation*).
''' + FOOT)

ex = Exercises("j2-l2.2")
def vrun(major, minor, ops):
    o = (major, minor); c = o
    for op in ops:
        c = (c[0] + 1, 0) if op == "major" else (c[0], c[1] + 1)
    return f"{c[0]}.{c[1]} (was {o[0]}.{o[1]})"
VSTART = 'class Version {\n    private final int major;\n    private final int minor;\n\n    Version(int major, int minor) {\n        this.major = major;\n        this.minor = minor;\n    }\n\n    Version bumpMinor() {\n        return new Version(major, minor + 1);\n    }\n\n    Version bumpMajor() {\n        return new Version(major + 1, 0);\n    }\n\n    @Override\n    public String toString() {\n        return major + "." + minor;\n    }\n}\n\nString run(int major, int minor, String[] ops) {\n    Version original = new Version(major, minor);\n    Version current = original;\n    for (String op : ops) {\n        current = op.equals("major") ? current.bumpMajor() : current.bumpMinor();\n    }\n    return current + " (was " + original + ")";\n}'
ex.method("write", "j2-l2.2-write-version", "Version numbers that never change", ["o1"], ["J2.06"], ["IMPL"],
    "`Version` is meant to be immutable, but `bumpMinor` and `bumpMajor` change `this`. Make the fields `private final`, and make both methods return a **new** `Version` and leave the original alone. `run` applies a list of `\"minor\"` and `\"major\"` bumps and shows the result next to the original, e.g. `1.6 (was 1.4)`. A major bump sets the minor part back to 0.",
    [("run", [("major", "int"), ("minor", "int"), ("ops", "String[]")], "String")], {"run": vrun},
    [("run", [1, 4, ["minor", "minor"]]), ("run", [2, 7, ["major"]]), ("run", [0, 0, []])],
    [("run", [1, 0, ["major", "minor"]]), ("run", [5, 9, ["minor", "major", "minor"]]), ("run", [3, 3, ["major", "major"]]), ("run", [0, 1, ["minor"]]), ("run", [9, 9, ["minor", "minor", "minor"]])],
    'class Version {\n    private int major;\n    private int minor;\n\n    Version(int major, int minor) {\n        this.major = major;\n        this.minor = minor;\n    }\n\n    Version bumpMinor() {\n        minor++;\n        return this;\n    }\n\n    Version bumpMajor() {\n        major++;\n        minor = 0;\n        return this;\n    }\n\n    @Override\n    public String toString() {\n        return major + "." + minor;\n    }\n}\n\nString run(int major, int minor, String[] ops) {\n    Version original = new Version(major, minor);\n    Version current = original;\n    for (String op : ops) {\n        current = op.equals("major") ? current.bumpMajor() : current.bumpMinor();\n    }\n    return current + " (was " + original + ")";\n}',
    VSTART,
    {"bump-major-keeps-minor": VSTART.replace("new Version(major + 1, 0)", "new Version(major + 1, minor)"),
     "minor-bump-adds-two": VSTART.replace("new Version(major, minor + 1)", "new Version(major, minor + 2)")},
    ("Don't write to the fields in the bump methods. Build and return a new Version instead.", "return new Version(major, minor + 1); and return new Version(major + 1, 0);"),
    source_tests=[("fields are final", ["private final int major", "private final int minor"], None)],
    difficulty=3)

def scores_run(a): return max(a)
ex.method("write", "j2-l2.2-write-scores", "A class that guards its array", ["o2"], ["J2.06"], ["IMPL"],
    "`Scores` keeps the array it is given, and hands out its own array. The driver `run` then tries to damage the object twice: by changing the original array after building `Scores`, and by writing into the array that `all()` returns. Make `Scores` take **defensive copies**, so that `max()` still returns the largest of the values it was *originally* given.",
    [("run", [("input", "int[]")], "int")], {"run": scores_run},
    [("run", [[3, 9, 4]]), ("run", [[5]]), ("run", [[-4, -1, -8]])],
    [("run", [[1, 2]]), ("run", [[7, 7, 7]]), ("run", [[10, 0, 20, 5]]), ("run", [[100]]), ("run", [[-5, 50, -5]])],
    'class Scores {\n    private final int[] values;\n\n    Scores(int[] values) {\n        this.values = values;\n    }\n\n    int[] all() {\n        return values;\n    }\n\n    int max() {\n        int best = values[0];\n        for (int v : values) {\n            if (v > best) {\n                best = v;\n            }\n        }\n        return best;\n    }\n}\n\nint run(int[] input) {\n    Scores s = new Scores(input);\n    input[0] = -999;\n    s.all()[0] = 2000;\n    return s.max();\n}',
    'class Scores {\n    private final int[] values;\n\n    Scores(int[] values) {\n        this.values = values.clone();\n    }\n\n    int[] all() {\n        return values.clone();\n    }\n\n    int max() {\n        int best = values[0];\n        for (int v : values) {\n            if (v > best) {\n                best = v;\n            }\n        }\n        return best;\n    }\n}\n\nint run(int[] input) {\n    Scores s = new Scores(input);\n    input[0] = -999;\n    s.all()[0] = 2000;\n    return s.max();\n}',
    {"copy-in-only": 'class Scores {\n    private final int[] values;\n    Scores(int[] values) { this.values = values.clone(); }\n    int[] all() { return values; }\n    int max() { int best = values[0]; for (int v : values) if (v > best) best = v; return best; }\n}\n\nint run(int[] input) {\n    Scores s = new Scores(input);\n    input[0] = -999;\n    s.all()[0] = 2000;\n    return s.max();\n}',
     "copy-out-only": 'class Scores {\n    private final int[] values;\n    Scores(int[] values) { this.values = values; }\n    int[] all() { return values.clone(); }\n    int max() { int best = values[0]; for (int v : values) if (v > best) best = v; return best; }\n}\n\nint run(int[] input) {\n    Scores s = new Scores(input);\n    input[0] = -999;\n    s.all()[0] = 2000;\n    return s.max();\n}'},
    ("There are two routes: the array going in, and the array coming out. Which of them does the starter copy?", "this.values = values.clone(); and return values.clone();"),
    difficulty=3)

PLAYLIST = 'class Playlist {\n    private final List<String> songs;\n\n    Playlist(List<String> songs) {\n        this.songs = songs;\n    }\n\n    List<String> songs() {\n        return songs;\n    }\n\n    int size() {\n        return songs.size();\n    }\n}\n\nint run(String[] names) {\n    List<String> mine = new ArrayList<>(List.of(names));\n    Playlist p = new Playlist(mine);\n    mine.add("sneaky");\n    try {\n        p.songs().add("also sneaky");\n    } catch (UnsupportedOperationException e) {\n        // an unmodifiable list refused: that is fine\n    }\n    return p.size();\n}'
ex.method("debug", "j2-l2.2-debug-playlist", "The playlist that changes by itself", ["o2", "o3"], ["J2.06"], ["DEBUG"],
    "`run` builds a `Playlist` from the names, then tries to sneak extra songs in: once through the caller's own list, and once through the list that `songs()` returns. `size()` should stay equal to the number of names given. It doesn't. Find both leaks in `Playlist` and fix them (don't change `run`).",
    [("run", [("names", "String[]")], "int")], {"run": lambda n: len(n)},
    [("run", [["a", "b"]]), ("run", [[]]), ("run", [["x", "y", "z"]])],
    [("run", [["solo"]]), ("run", [["a", "a", "a", "a"]]), ("run", [["1", "2", "3", "4", "5"]]), ("run", [["p", "q"]]), ("run", [["m", "n", "o"]])],
    PLAYLIST,
    PLAYLIST.replace("this.songs = songs;", "this.songs = new ArrayList<>(songs);").replace("return songs;\n", "return new ArrayList<>(songs);\n"),
    {"copy-in-only": PLAYLIST.replace("this.songs = songs;", "this.songs = new ArrayList<>(songs);"),
     "copy-out-only": PLAYLIST.replace("return songs;\n", "return new ArrayList<>(songs);\n")},
    ("A leak can go in through the constructor, or out through songs(). Check both.", "Copy in the constructor: new ArrayList<>(songs), and return a copy (or List.copyOf) from songs()."),
    difficulty=3)
ex.explain("j2-l2.2-explain-value-identity", "Value or identity?", ["o3"], ["J2.06"],
    "A teammate asks: \"Why do we make `Money` immutable, but `BankAccount` isn't?\" Explain the difference between a **value** and an **identity**, using those two examples, and say what goes wrong if a value class like `Money` is mutable and two accounts share one `Money` object.",
    "A full answer says a value is defined by its contents (two Money objects with the same pence are interchangeable) while an account has identity (it stays that account as its balance changes); values are made immutable so they can be shared safely; if Money were mutable and shared, changing one account's balance in place would change the other's.",
    {2: ("Distinguishes value (defined by contents, interchangeable) from identity (the same account over time), says values should be immutable so sharing is safe, and gives the shared mutable Money example where one account's change alters the other.",
         ["Money is a value: two Money objects with the same pence are interchangeable, so it's safe to make it immutable and share it. A BankAccount has identity: it's still the same account when its balance changes. If Money were mutable and two accounts shared one object, adding to one account's money would change the other account's balance too.",
          "A value is defined by what it holds; an account is defined by being that particular account. Immutable values can be shared freely. If two accounts pointed at the same mutable Money, a deposit into one would silently change the other."]),
     1: ("Gets the value/identity distinction or the sharing problem, but not both.",
         ["Money is a value and an account has identity.", "Sharing a mutable object is dangerous."]),
     0: ("Incorrect, for example says immutable means it can't be used, or that accounts are immutable too.",
         ["Immutable means you can never use it.", "Both are immutable."])})
reg({"j2-l2.2": ("Immutability and defensive copies", ["J2.06"])},
    {"MC41": (["J2.06"], "R8", "A final field or variable makes the whole object it refers to unchangeable"),
     "MC42": (["J2.06"], "Platform", "Copying a list in the constructor is enough, even if a getter returns the internal list")})

# ====================================================================== 2.3.1
Lesson("j2-l3.1", "Interfaces and polymorphism", ["J2.07"], [
    ("o1", "Declare an interface and write classes that implement it"),
    ("o2", "Use an interface-typed variable and predict which implementation runs"),
    ("o3", "Explain why code written against an interface keeps working when a new implementation is added"),
], ["j2-l2.2"], 45, ["R8", "R5"], r'''
## Before you start

You should be able to write classes with methods and constructors ([Methods and this](j2-l1.2)).

**Quick check.** Which methods can you call on a variable of type `Student`: only those in the `Student` class, or any method at all?

<details><summary>Show the answer</summary>

Only those that `Student` has. The type of the variable decides what you may call.

</details>

## Explanation

### A contract without an implementation

Suppose a program must add up areas of different shapes. A rectangle's area is `width * height`; a square's is `side * side`; a circle's, something else. You'd like the adding-up code to say simply "ask each shape for its area", without caring which kind it is.

An **interface** is a **contract**: a list of methods that any class claiming to follow it must provide.

```java
interface Shape {
    int area();
}
```

An interface says *what* can be done, not *how*. It has no fields and no method bodies (for now).

### Implementing an interface

A class that agrees to the contract says so with `implements`, and provides every method:

```java
class Rect implements Shape {
    private final int width;
    private final int height;

    Rect(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public int area() {
        return width * height;
    }
}

class Square implements Shape {
    private final int side;

    Square(int side) {
        this.side = side;
    }

    public int area() {
        return side * side;
    }
}
```

Notice `public` on `area()`. Methods in an interface are automatically `public`, so the implementation must be `public` too. Leaving it off is a compile error.

### An interface is a type

You can declare a variable whose type is the interface, and put **any implementing object** in it:

```java runnable
interface Shape {
    int area();
}

class Rect implements Shape {
    private final int w, h;
    Rect(int w, int h) { this.w = w; this.h = h; }
    public int area() { return w * h; }
}

class Square implements Shape {
    private final int side;
    Square(int side) { this.side = side; }
    public int area() { return side * side; }
}

void main() {
    Shape[] shapes = { new Rect(3, 4), new Square(5) };
    int total = 0;
    for (Shape s : shapes) {
        total += s.area();
    }
    IO.println(total);
}
```

This prints `37` (12 + 25). The loop is written purely against `Shape`.

### Polymorphism: the right method runs

When the loop calls `s.area()`, Java looks at the **actual object** `s` refers to and runs *its* version of the method. This is called **polymorphism** ("many forms") or **dynamic dispatch**. The variable's type (`Shape`) decides which methods you may call; the object's real class decides which code runs.

Two consequences:

- **You can only call what the interface declares.** If `Rect` also had a `width()` method, a `Shape` variable couldn't call it.
- **New implementations just work.** Add `class Circle implements Shape` and the loop above, unchanged, handles circles too. That's the point: *code written against the contract doesn't need to change when a new case appears.*

### Interfaces are everywhere

`List` is an interface: `ArrayList` and `LinkedList` are two implementations. Code written to accept a `List` works with both. You'll see this constantly in Stage 3 and in every framework.

### One class, several interfaces

A class can `implements` several interfaces, separated by commas. (A class can extend only **one** other class, as you'll see next lesson.)

## Worked examples

### Example 1: choosing a notifier at run time

*Task: send a message by email or SMS, chosen by a string. SMS messages are cut to 10 characters.*

**Step 1 — Define the contract:** `interface Notifier { String send(String message); }`

**Step 2 — Write each implementation** with `public String send(...)`.

**Step 3 — The caller picks one, and then only talks to `Notifier`.**

```java runnable
interface Notifier {
    String send(String message);
}

class Email implements Notifier {
    public String send(String message) {
        return "email: " + message;
    }
}

class Sms implements Notifier {
    public String send(String message) {
        String shortened = message.length() > 10 ? message.substring(0, 10) : message;
        return "sms: " + shortened;
    }
}

void main() {
    Notifier n = new Sms();
    IO.println(n.send("Your parcel has arrived"));
}
```

**Step 4 — Check.** It prints `sms: Your parce`.

### Example 2: predicting which version runs

*Task: what does `a.sound()` print for each element?*

```java
Animal[] zoo = { new Dog(), new Cat() };
for (Animal a : zoo) {
    IO.println(a.sound());
}
```

**Step 1 — Look at the objects, not the variable type.** The first element is a `Dog`, the second a `Cat`.

**Step 2 — Each call runs the object's own `sound()`.** It prints `Dog`'s sound, then `Cat`'s.

## Predict, then run

::exercise{id=j2-l3.1-predict-dispatch}

## Where this is used

- **Collections and frameworks** are designed around interfaces: you write `List`, `Map` and let the implementation vary.
- **Testing:** a test can supply a fake implementation of an interface in place of a real database.
- **Plug-in designs:** payment methods, notifiers, file formats: add one by writing a new class.

## Common mistakes

:::mistake{id=MC43}
**Forgetting `public` on the implementing method.** The interface's method is public, so the implementation must be too (`area() in Rect cannot implement area() in Shape: attempting to assign weaker access privileges; was public`).
:::

:::mistake{id=MC44}
**Expecting the variable's type to decide which code runs.** For `Shape s = new Square(5);`, `s.area()` runs `Square`'s code, because the object is a `Square`.
:::

## Practice

::exercise{id=j2-l3.1-write-shapes}

::exercise{id=j2-l3.1-write-notifier}

::exercise{id=j2-l3.1-explain-polymorphism}

## Further reading

- **Lister et al. (2004)** `[R5]` studied how novices read and trace code; predicting which method runs is a tracing skill.
- **Qian & Lehman (2017)** `[R8]` review misconceptions about types and objects.

## How you'll be assessed

- The **write** exercises check that you can implement an interface and use it (*implementation*).
- The **predict** exercise checks that you know which implementation runs (*identifying mistakes*).
- The **explain** exercise checks that you can say why interface-based code survives new cases (*explanation*).
''' + FOOT)

ex = Exercises("j2-l3.1")
def total_area(specs):
    t = 0
    for s in specs:
        k, v = s.split(":")
        if k == "rect":
            w, h = v.split("x"); t += int(w) * int(h)
        else:
            t += int(v) ** 2
    return t
SHAPE_DRIVER = 'int totalArea(String[] specs) {\n    int total = 0;\n    for (String spec : specs) {\n        String[] parts = spec.split(":");\n        Shape s;\n        if (parts[0].equals("rect")) {\n            String[] d = parts[1].split("x");\n            s = new Rect(Integer.parseInt(d[0]), Integer.parseInt(d[1]));\n        } else {\n            s = new Square(Integer.parseInt(parts[1]));\n        }\n        total += s.area();\n    }\n    return total;\n}'
SHAPE_SOL = 'interface Shape {\n    int area();\n}\n\nclass Rect implements Shape {\n    private final int width;\n    private final int height;\n\n    Rect(int width, int height) {\n        this.width = width;\n        this.height = height;\n    }\n\n    public int area() {\n        return width * height;\n    }\n}\n\nclass Square implements Shape {\n    private final int side;\n\n    Square(int side) {\n        this.side = side;\n    }\n\n    public int area() {\n        return side * side;\n    }\n}\n\n'
ex.method("write", "j2-l3.1-write-shapes", "Two shapes, one interface", ["o1"], ["J2.07"], ["IMPL"],
    "`Shape` and the driver `totalArea` are written. Write the two classes the driver uses: `Rect` (constructed with width and height) and `Square` (constructed with a side). Both must **implement `Shape`**. The driver reads specs like `\"rect:3x4\"` and `\"square:5\"`, and adds up the areas.",
    [("totalArea", [("specs", "String[]")], "int")], {"totalArea": total_area},
    [("totalArea", [["rect:3x4", "square:5"]]), ("totalArea", [["square:2"]]), ("totalArea", [[]])],
    [("totalArea", [["rect:1x1"]]), ("totalArea", [["rect:10x10", "rect:2x3"]]), ("totalArea", [["square:1", "square:2", "square:3"]]), ("totalArea", [["rect:0x5", "square:4"]]), ("totalArea", [["square:9", "rect:5x5", "square:1"]])],
    'interface Shape {\n    int area();\n}\n\n// Write the classes Rect and Square here.\n\n' + SHAPE_DRIVER,
    SHAPE_SOL + SHAPE_DRIVER,
    {"square-doubles": SHAPE_SOL.replace("return side * side;", "return side * 2;") + SHAPE_DRIVER,
     "rect-adds": SHAPE_SOL.replace("return width * height;", "return width + height;") + SHAPE_DRIVER},
    ("Each class says implements Shape and provides public int area(). Square only needs one number.", "class Rect implements Shape { ... public int area() { return width * height; } }"),
    source_tests=[("Rect implements Shape", ["class Rect implements Shape"], None), ("Square implements Shape", ["class Square implements Shape"], None)],
    starter_compiles=False, difficulty=2)

def notify(channel, message):
    if channel == "email": return "email: " + message
    return "sms: " + (message[:10] if len(message) > 10 else message)
NOT_DRIVER = 'String notifyBy(String channel, String message) {\n    Notifier n = channel.equals("email") ? new Email() : new Sms();\n    return n.send(message);\n}'
NOT_BASE = 'interface Notifier {\n    String send(String message);\n}\n\nclass Email implements Notifier {\n    public String send(String message) {\n        return "email: " + message;\n    }\n}\n\n'
NOT_SMS = 'class Sms implements Notifier {\n    public String send(String message) {\n        String shortened = message.length() > 10 ? message.substring(0, 10) : message;\n        return "sms: " + shortened;\n    }\n}\n\n'
ex.method("write", "j2-l3.1-write-notifier", "A second notifier", ["o1"], ["J2.07"], ["IMPL"],
    "`Email` is written. Write `Sms`, which implements `Notifier`: its `send` returns `\"sms: \"` followed by the message **cut to its first 10 characters** (shorter messages are left whole). `notifyBy` chooses between them by name.",
    [("notifyBy", [("channel", "String"), ("message", "String")], "String")], {"notifyBy": notify},
    [("notifyBy", ["email", "Hello"]), ("notifyBy", ["sms", "Your parcel has arrived"]), ("notifyBy", ["sms", "Short"])],
    [("notifyBy", ["sms", "Exactly 10"]), ("notifyBy", ["sms", "Exactly 11!"]), ("notifyBy", ["sms", ""]), ("notifyBy", ["email", "A very long email message indeed"]), ("notifyBy", ["sms", "0123456789ABC"])],
    NOT_BASE + '// Write the class Sms here.\n\n' + NOT_DRIVER,
    NOT_BASE + NOT_SMS + NOT_DRIVER,
    {"no-cut": NOT_BASE + NOT_SMS.replace("message.length() > 10 ? message.substring(0, 10) : message", "message") + NOT_DRIVER,
     "cuts-at-eleven": NOT_BASE + NOT_SMS.replace("> 10 ? message.substring(0, 10)", "> 11 ? message.substring(0, 11)") + NOT_DRIVER},
    ("Implement send with public. Cut the message only when it's longer than 10 characters, using substring(0, 10).", "String shortened = message.length() > 10 ? message.substring(0, 10) : message; return \"sms: \" + shortened;"),
    source_tests=[("Sms implements Notifier", ["class Sms implements Notifier"], None)],
    starter_compiles=False, difficulty=2)
ex.predict("j2-l3.1-predict-dispatch", "Which sound?", ["o2"], ["J2.07"],
    "Work out what this program prints. Remember the **object** decides which code runs.",
    '''interface Animal {
    String sound();
}

class Dog implements Animal {
    public String sound() { return "Woof"; }
}

class Cat implements Animal {
    public String sound() { return "Meow"; }
}

class Robot implements Animal {
    public String sound() { return "Beep"; }
}

void main() {
    Animal[] zoo = { new Dog(), new Robot(), new Cat(), new Dog() };
    for (Animal a : zoo) {
        IO.println(a.sound());
    }
    Animal second = zoo[1];
    IO.println(second.sound());
}''', "Woof\nBeep\nMeow\nWoof\nBeep",
    ("Go through the array one object at a time. What class is each object?", "Dog, Robot, Cat, Dog, then zoo[1] again, which is the Robot."),
    difficulty=2)
ex.explain("j2-l3.1-explain-polymorphism", "A new shape arrives", ["o3"], ["J2.07"],
    "A program has `Rect` and `Square` implementing `Shape`, and a method that loops over a `Shape[]` adding up `area()`. A new requirement adds a `Circle`. (a) What changes in the adding-up method? (b) Why? (c) Say one thing you *can't* do with a `Shape` variable even if every shape class has more methods.",
    "A full answer says nothing changes in the loop; Circle just implements Shape with its own area; because the loop is written against the Shape contract and the object's own area() runs (polymorphism); and a Shape variable can only call methods declared in Shape, not methods that exist only in a class like Rect.",
    {2: ("Says the adding-up method doesn't change, because it only uses the Shape contract and each object's own area() runs; and that a Shape variable can only use methods declared in Shape.",
         ["Nothing changes in the loop. I just write Circle implements Shape with its own area(). The loop only calls area() on a Shape, and Java runs the version belonging to the actual object, so circles work automatically. A Shape variable can only call the methods Shape declares, so I couldn't call something that exists only in Rect, like a width() method.",
          "The loop stays exactly the same: it's written against the interface and polymorphism runs Circle's area(). What you can't do is call methods that aren't in Shape, even if the object has them."]),
     1: ("Says nothing changes but doesn't explain why, or explains polymorphism without the restriction on what a Shape variable can call.",
         ["Nothing changes in the loop.", "Each object runs its own area()."]),
     0: ("Incorrect, for example says every existing class must be edited, or that the loop needs a new if for circles.",
         ["You have to add an if for circles in the loop.", "All the classes need to be changed."])})
reg({"j2-l3.1": ("Interfaces and polymorphism", ["J2.07"])},
    {"MC43": (["J2.07"], "Platform", "An implementing method can be package-private (no public)"),
     "MC44": (["J2.07"], "R8", "The declared type of a variable decides which version of a method runs")})

# ====================================================================== 2.3.2
Lesson("j2-l3.2", "Inheritance, super and abstract classes", ["J2.08"], [
    ("o1", "Write a subclass with extends, call a parent constructor with super, and override a method"),
    ("o2", "Predict constructor order and which overridden method runs"),
    ("o3", "Use an abstract class that fixes the steps and leaves one step to subclasses"),
], ["j2-l3.1"], 45, ["R8", "R5"], r'''
## Before you start

You should know how interfaces and polymorphism work ([Interfaces and polymorphism](j2-l3.1)).

**Quick check.** If `Animal a = new Dog();` and both classes have `describe()`, whose version runs on `a.describe()`?

<details><summary>Show the answer</summary>

`Dog`'s. The object decides.

</details>

## Explanation

### Inheritance: a class built on another

An interface gives a contract. **Inheritance** goes further: a **subclass** takes over the fields and methods of a **superclass**, and can add to them or replace some.

```java
class Vehicle {
    String describe() {
        return "a vehicle";
    }
}

class Car extends Vehicle {
    @Override
    String describe() {
        return "a car";
    }
}
```

`Car extends Vehicle` means a `Car` **is a** `Vehicle`: you can put one wherever a `Vehicle` is expected, and everything `Vehicle` can do, a `Car` can do too. `@Override` marks a method that replaces the parent's, and lets the compiler catch mistakes in the name or parameters.

A class can extend **only one** class, but can implement many interfaces.

### `super`: using the parent's version

Inside a subclass, `super` refers to the parent's part of the object. Use it to **add to** the parent's behaviour instead of replacing it:

```java
@Override
String describe() {
    return super.describe() + " with 4 wheels";     // "a vehicle with 4 wheels"
}
```

### Constructors run parent first

Building a `Car` builds the `Vehicle` part first. If the parent has a constructor with parameters, the child must call it as its **first line** with `super(...)`:

```java
class Employee {
    String name;
    int base;
    Employee(String name, int base) {
        this.name = name;
        this.base = base;
    }
}

class Manager extends Employee {
    Manager(String name, int base) {
        super(name, base);          // must come first
    }
}
```

If you don't write a `super(...)` call, Java inserts `super()` for you, and that fails to compile if the parent has no parameterless constructor. And the order of output when constructors print is **parent first, then child**:

```java runnable
class Vehicle {
    Vehicle() { IO.println("Vehicle built"); }
}

class Car extends Vehicle {
    Car() { IO.println("Car built"); }
}

void main() {
    new Car();
}
```

It prints `Vehicle built`, then `Car built`.

### Abstract classes: a partly finished class

An **abstract class** can't be instantiated with `new`. It can hold fields, constructors and ordinary methods, **and** declare `abstract` methods that have no body and *must* be written by subclasses:

```java
abstract class Employee {
    String name;
    int base;

    Employee(String name, int base) {
        this.name = name;
        this.base = base;
    }

    abstract int bonus();               // each kind decides

    int pay() {                         // the shared recipe
        return base + bonus();
    }
}

class Engineer extends Employee {
    Engineer(String name, int base) { super(name, base); }
    int bonus() { return 500; }
}
```

`pay()` is written once, in the abstract class, and calls `bonus()`; each subclass supplies its own `bonus()`. This pattern, fixed steps with one customisable step, is called a **template method**.

### Which to choose: interface or abstract class?

- Use an **interface** for a pure contract, especially when unrelated classes might follow it.
- Use an **abstract class** when subclasses share **fields and real code**, and differ in just a few steps.

Inheritance is easy to overuse. The next lesson explains when composition is the better answer.

## Worked examples

### Example 1: extending a parent's description

*Task: `ElectricCar` should describe itself as a car, plus `(electric)`.*

**Step 1 — Which class is closest?** `Car`, whose `describe()` already says `a vehicle with 4 wheels`.

**Step 2 — Override and build on it with `super`:**

```java
class ElectricCar extends Car {
    @Override
    String describe() {
        return super.describe() + " (electric)";
    }
}
```

**Step 3 — Check.** `new ElectricCar().describe()` gives `a vehicle with 4 wheels (electric)`.

### Example 2: tracing construction

*Task: what does `new Car()` print if `Vehicle()` prints `V` and `Car()` prints `C`?*

**Step 1 — Which constructor starts?** `Car()`.

**Step 2 — Its first action is the implicit `super()`,** so `Vehicle()` runs first.

**Step 3 — Then the rest of `Car()`.** Output: `V`, then `C`.

## Predict, then run

::exercise{id=j2-l3.2-predict-constructors}

## Where this is used

- **Framework base classes:** you'll extend classes supplied by libraries and override a few methods.
- **Template methods** are common in test frameworks, servlets and anywhere the library "calls you back".
- **Reading old code:** a lot of existing Java uses deep inheritance. You'll need to follow `super` calls and overrides.

## Common mistakes

:::mistake{id=MC45}
**Expecting the child's constructor to run first.** The parent part is always built first, either by your `super(...)` or an implicit `super()`.
:::

:::mistake{id=MC46}
**Writing a method with the same name but different parameters and calling it an override.** It's a different method. `@Override` makes the compiler tell you.
:::

## Practice

::exercise{id=j2-l3.2-write-employee}

::exercise{id=j2-l3.2-modify-describe}

## Further reading

- **Lister et al. (2004)** `[R5]` link tracing skill with the ability to write code; constructor-order questions are classic tracing practice.
- **Qian & Lehman (2017)** `[R8]` review misconceptions about inheritance and constructors.

## How you'll be assessed

- The **write** exercise checks that you can extend an abstract class with `super` and write the missing step (*implementation*).
- The **predict** exercise checks that you can trace constructor order and overrides (*identifying mistakes*).
- The **modify** exercise checks that you can change an override to build on `super`, and add a subclass (*modification*).
''' + FOOT)

ex = Exercises("j2-l3.2")
EMP_BASE = 'abstract class Employee {\n    String name;\n    int base;\n\n    Employee(String name, int base) {\n        this.name = name;\n        this.base = base;\n    }\n\n    abstract int bonus();\n\n    int pay() {\n        return base + bonus();\n    }\n}\n\n'
EMP_SOL = 'class Manager extends Employee {\n    Manager(String name, int base) {\n        super(name, base);\n    }\n\n    int bonus() {\n        return base / 10;\n    }\n}\n\nclass Engineer extends Employee {\n    Engineer(String name, int base) {\n        super(name, base);\n    }\n\n    int bonus() {\n        return 500;\n    }\n}\n\n'
EMP_DRIVER = 'int payFor(String role, int base) {\n    Employee e = role.equals("manager") ? new Manager("M", base) : new Engineer("E", base);\n    return e.pay();\n}'
ex.method("write", "j2-l3.2-write-employee", "Fill in the missing step", ["o1", "o3"], ["J2.08"], ["IMPL"],
    "`Employee` is abstract: `pay()` is `base + bonus()`, and each kind of employee supplies its own `bonus()`. Write `Manager` (bonus is a tenth of the base pay, in whole pounds) and `Engineer` (a fixed bonus of 500). Each must `extend Employee` and call `super(name, base)`.",
    [("payFor", [("role", "String"), ("base", "int")], "int")],
    {"payFor": lambda r, b: b + (b // 10 if r == "manager" else 500)},
    [("payFor", ["manager", 3000]), ("payFor", ["engineer", 3000]), ("payFor", ["manager", 0])],
    [("payFor", ["manager", 5]), ("payFor", ["manager", 9999]), ("payFor", ["engineer", 0]), ("payFor", ["engineer", 12345]), ("payFor", ["manager", 100])],
    EMP_BASE + '// Write the classes Manager and Engineer here.\n\n' + EMP_DRIVER,
    EMP_BASE + EMP_SOL + EMP_DRIVER,
    {"manager-bonus-too-small": EMP_BASE + EMP_SOL.replace("base / 10", "base / 100") + EMP_DRIVER,
     "engineer-bonus-50": EMP_BASE + EMP_SOL.replace("return 500;", "return 50;") + EMP_DRIVER},
    ("Each subclass: extends Employee, a constructor that calls super(name, base), and an int bonus() method.", "class Manager extends Employee { Manager(String name, int base) { super(name, base); } int bonus() { return base / 10; } }"),
    source_tests=[("Manager extends Employee", ["class Manager extends Employee"], None), ("Engineer extends Employee", ["class Engineer extends Employee"], None), ("calls super", ["super(name, base)"], None)],
    starter_compiles=False, difficulty=3)
ex.predict("j2-l3.2-predict-constructors", "Who is built first?", ["o2"], ["J2.08"],
    "Work out what this program prints, line by line.",
    '''class Vehicle {
    Vehicle() {
        IO.println("Vehicle built");
    }

    String describe() {
        return "a vehicle";
    }
}

class Car extends Vehicle {
    Car() {
        IO.println("Car built");
    }

    @Override
    String describe() {
        return super.describe() + " with 4 wheels";
    }
}

void main() {
    Vehicle v = new Car();
    IO.println(v.describe());
}''', "Vehicle built\nCar built\na vehicle with 4 wheels",
    ("Which constructor runs first when you build a Car? Then which describe() runs, and what does super.describe() give?", "The parent is built first. v is really a Car, so Car's describe runs, adding to Vehicle's."),
    difficulty=2)
VEH = 'class Vehicle {\n    String describe() {\n        return "a vehicle";\n    }\n}\n\n'
VEH_SOL = 'class Car extends Vehicle {\n    @Override\n    String describe() {\n        return super.describe() + " with 4 wheels";\n    }\n}\n\nclass ElectricCar extends Car {\n    @Override\n    String describe() {\n        return super.describe() + " (electric)";\n    }\n}\n\n'
VEH_DRIVER = 'String describe(String kind) {\n    Vehicle v;\n    if (kind.equals("car")) {\n        v = new Car();\n    } else if (kind.equals("electric")) {\n        v = new ElectricCar();\n    } else {\n        v = new Vehicle();\n    }\n    return v.describe();\n}'
ex.method("modify", "j2-l3.2-modify-describe", "Build on the parent", ["o1"], ["J2.08"], ["MOD"],
    "`Car.describe()` replaces the parent's text. Change it to **build on** it with `super`, so a car is described as `a vehicle with 4 wheels`. Then add the class `ElectricCar` that extends `Car` and adds ` (electric)` to the end of the car's description. The driver already builds one of each.",
    [("describe", [("kind", "String")], "String")],
    {"describe": lambda k: {"car": "a vehicle with 4 wheels", "electric": "a vehicle with 4 wheels (electric)"}.get(k, "a vehicle")},
    [("describe", ["vehicle"]), ("describe", ["car"]), ("describe", ["electric"])],
    [("describe", ["other"]), ("describe", ["car"]), ("describe", ["electric"]), ("describe", [""]), ("describe", ["vehicle"])],
    VEH + 'class Car extends Vehicle {\n    @Override\n    String describe() {\n        return "a car";\n    }\n}\n\n' + VEH_DRIVER,
    VEH + VEH_SOL + VEH_DRIVER,
    {"electric-forgets-brackets": VEH + VEH_SOL.replace('" (electric)"', '" electric"') + VEH_DRIVER,
     "car-without-super": VEH + VEH_SOL.replace('super.describe() + " with 4 wheels"', '"a car with 4 wheels"') + VEH_DRIVER},
    ("Use super.describe() in Car, and in ElectricCar too. The new class needs extends Car.", "class ElectricCar extends Car { @Override String describe() { return super.describe() + \" (electric)\"; } }"),
    source_tests=[("Car builds on the parent", ["super.describe()"], None), ("ElectricCar extends Car", ["class ElectricCar extends Car"], None)],
    starter_compiles=False, difficulty=3)
reg({"j2-l3.2": ("Inheritance, super and abstract classes", ["J2.08"])},
    {"MC45": (["J2.08"], "R8", "A child constructor runs before its parent's"),
     "MC46": (["J2.08"], "Platform", "A method with the same name but different parameters overrides the parent's")})

# ====================================================================== 2.3.3
Lesson("j2-l3.3", "Composition over inheritance", ["J2.09"], [
    ("o1", "Build a class that holds another object and delegates to it"),
    ("o2", "Explain, with a reason, when to prefer composition to inheritance, using the substitution test"),
], ["j2-l3.2"], 40, ["R8", "R17"], r'''
## Before you start

You should be able to write an interface and a subclass ([Interfaces and polymorphism](j2-l3.1), [Inheritance, super and abstract classes](j2-l3.2)).

**Quick check.** In `class Car extends Vehicle`, what does "a `Car` **is a** `Vehicle`" let you do?

<details><summary>Show the answer</summary>

Use a `Car` anywhere a `Vehicle` is expected.

</details>

## Explanation

Inheritance feels powerful, and beginners often reach for it first. Experienced developers usually reach for something else first: **composition**.

### Inheritance is "is-a", composition is "has-a"

- **Inheritance:** a `Car` *is a* `Vehicle`.
- **Composition:** an `Order` *has a* `Discount`; a `Stack` *has a* list inside it.

With composition, a class keeps another object in a **field** and uses it, often by **delegating**: its own methods just call the other object's methods.

```java
class Stack {
    private final ArrayList<Integer> items = new ArrayList<>();

    void push(int value) {
        items.add(value);
    }

    int pop() {
        return items.remove(items.size() - 1);
    }
}
```

`Stack` *has* a list, and offers only the operations a stack should. The alternative, `class Stack extends ArrayList<Integer>`, would make a `Stack` **be** a list, with every list method available too: `stack.add(0, 99)` would insert at the bottom, breaking the idea of a stack.

### Why inheritance causes trouble

- **It exposes too much.** A subclass inherits *everything*, including methods that don't make sense for it.
- **It ties you to the parent's details.** A change in the parent can break every subclass.
- **It's rigid.** A class has only one parent, and the relationship is fixed when you write the code.
- **It can break substitution** (see below).

### The substitution test

Inheritance is only correct if a subclass can stand in **anywhere** its parent is used without surprises. This is sometimes called the Liskov substitution principle. Ask: *"Would any code written for the parent still work, unchanged, with this child?"*

```java
class Bird { void fly() { /* ... */ } }
class Penguin extends Bird { /* penguins can't fly */ }
```

A penguin *is a* bird in biology, but code that says `for (Bird b : birds) b.fly();` will fail or lie for a penguin. The relationship doesn't hold *in the program's terms*, so the inheritance is wrong. A better design might separate `FlyingBird` as an interface that only some birds implement.

### Delegating to a replaceable part

Composition shines when behaviour should be **swappable**. Give the class an interface-typed field and let the caller choose:

```java runnable
interface Discount {
    int apply(int pence);
}

class NoDiscount implements Discount {
    public int apply(int pence) { return pence; }
}

class PercentOff implements Discount {
    private final int percent;
    PercentOff(int percent) { this.percent = percent; }
    public int apply(int pence) { return pence - pence * percent / 100; }
}

class Order {
    private final int pence;
    private final Discount discount;

    Order(int pence, Discount discount) {
        this.pence = pence;
        this.discount = discount;
    }

    int total() {
        return discount.apply(pence);
    }
}

void main() {
    IO.println(new Order(2000, new PercentOff(10)).total());
    IO.println(new Order(2000, new NoDiscount()).total());
}
```

It prints `1800` then `2000`. `Order` never changes when a new kind of discount is added, and you can swap the discount without touching `Order`. Doing this with inheritance would mean a subclass of `Order` for every discount.

### A rule of thumb

**Prefer composition by default.** Use inheritance when there's a genuine *is-a* that survives the substitution test, when the parent was designed to be extended, and when you want the subclass to reuse most of the parent.

## Worked examples

### Example 1: replacing inheritance with delegation

*Task: `class Stack extends ArrayList<Integer>` lets callers call `add(0, 99)`. Redesign it.*

**Step 1 — Say what a stack should offer:** `push`, `pop`, `peek`, `size`. Nothing else.

**Step 2 — Hold a list privately:** `private final ArrayList<Integer> items`.

**Step 3 — Write each operation by delegating:** `push` adds at the end; `pop` removes the last; `peek` reads it.

**Step 4 — Check.** `add(0, 99)` no longer exists on a `Stack`, because it was never offered.

### Example 2: does the substitution test pass?

*Task: should `Square extends Rectangle` if `Rectangle` has `setWidth` and `setHeight` separately?*

**Step 1 — What does code written for `Rectangle` expect?** That after `setWidth(5)` and `setHeight(2)`, the area is 10.

**Step 2 — What does a `Square` have to do?** Keep width and height equal, so setting one changes the other.

**Step 3 — Does the old code still work?** No: area would be 4 and not 10. The substitution test fails, so don't inherit.

## Where this is used

- **Almost every well-designed Java library** composes behaviour from smaller parts, and gives you interfaces to plug into.
- **Strategies and policies** (discounts, fee rules, retry rules) are classic composition.
- **Code reviews** often include "can we use composition here?"

## Common mistakes

:::mistake{id=MC47}
**Using inheritance just to reuse code.** If the only reason is "I want its methods", hold an object of that type and delegate.
:::

:::mistake{id=MC48}
**Assuming real-world "is-a" means program "is-a".** A penguin is a bird, but a `Penguin` that can't `fly()` can't stand in for a `Bird` in code that calls it.
:::

## Practice

::exercise{id=j2-l3.3-write-order}

::exercise{id=j2-l3.3-write-stack}

::exercise{id=j2-l3.3-explain-inherit-compose}

## Further reading

- **Kirschner, Sweller & Clark (2006)** `[R17]` argue that minimal guidance during instruction is less effective for novices than guided instruction, which is why this course shows a worked design before asking you to critique one.
- **Qian & Lehman (2017)** `[R8]` for misconceptions about object relationships.

## How you'll be assessed

- The **write** exercises check that you can build classes by composition: one that delegates to a replaceable part, and one that hides a list (*implementation*).
- The **explain** exercise checks that you can argue for inheritance or composition using the substitution test (*explanation*).
''' + FOOT)

ex = Exercises("j2-l3.3")
def order_total(p, kind):
    pct = {"ten": 10, "half": 50}.get(kind, 0)
    return p - p * pct // 100
ORD_BASE = 'interface Discount {\n    int apply(int pence);\n}\n\nclass NoDiscount implements Discount {\n    public int apply(int pence) {\n        return pence;\n    }\n}\n\nclass PercentOff implements Discount {\n    private final int percent;\n\n    PercentOff(int percent) {\n        this.percent = percent;\n    }\n\n    public int apply(int pence) {\n        return pence - pence * percent / 100;\n    }\n}\n\n'
ORD_DRIVER = 'int total(int pence, String kind) {\n    Discount d;\n    if (kind.equals("ten")) {\n        d = new PercentOff(10);\n    } else if (kind.equals("half")) {\n        d = new PercentOff(50);\n    } else {\n        d = new NoDiscount();\n    }\n    Order order = new Order(pence, d);\n    return order.total();\n}'
ORD_SOL = 'class Order {\n    private final int pence;\n    private final Discount discount;\n\n    Order(int pence, Discount discount) {\n        this.pence = pence;\n        this.discount = discount;\n    }\n\n    int total() {\n        return discount.apply(pence);\n    }\n}\n\n'
ex.method("write", "j2-l3.3-write-order", "An order with a swappable discount", ["o1"], ["J2.09"], ["IMPL"],
    "`Discount`, `NoDiscount` and `PercentOff` are written. Write `Order` so that it **has a** `Discount` (passed to its constructor) and its `total()` returns the order's price after that discount. Don't use inheritance.",
    [("total", [("pence", "int"), ("kind", "String")], "int")], {"total": order_total},
    [("total", [2000, "ten"]), ("total", [2000, "none"]), ("total", [999, "half"])],
    [("total", [0, "ten"]), ("total", [1, "half"]), ("total", [12345, "ten"]), ("total", [100, "none"]), ("total", [5, "half"])],
    ORD_BASE + 'class Order {\n    private final int pence;\n\n    Order(int pence, Discount discount) {\n        this.pence = pence;\n    }\n\n    int total() {\n        return pence;\n    }\n}\n\n' + ORD_DRIVER,
    ORD_BASE + ORD_SOL + ORD_DRIVER,
    {"ignores-discount": ORD_BASE + ORD_SOL.replace("return discount.apply(pence);", "return pence;") + ORD_DRIVER,
     "discount-applied-twice": ORD_BASE + ORD_SOL.replace("return discount.apply(pence);", "return discount.apply(discount.apply(pence));") + ORD_DRIVER},
    ("Keep the Discount in a field. total() should delegate: ask the discount to apply itself to the price.", "private final Discount discount; ... return discount.apply(pence);"),
    source_tests=[("Order does not extend anything", None, ["extends"]), ("Order keeps a Discount", ["Discount discount"], None)],
    difficulty=2)
def stack_run(ops):
    st, out = [], []
    for op in ops:
        if op.startswith("push:"): st.append(int(op[5:]))
        elif op == "pop": out.append(str(st.pop()))
        elif op == "peek": out.append(str(st[-1]))
    return ",".join(out) + f"|{len(st)}"
STK_DRIVER = 'String run(String[] ops) {\n    Stack s = new Stack();\n    StringBuilder out = new StringBuilder();\n    for (String op : ops) {\n        if (op.startsWith("push:")) {\n            s.push(Integer.parseInt(op.substring(5)));\n        } else if (op.equals("pop")) {\n            out.append(out.isEmpty() ? "" : ",").append(s.pop());\n        } else if (op.equals("peek")) {\n            out.append(out.isEmpty() ? "" : ",").append(s.peek());\n        }\n    }\n    return out + "|" + s.size();\n}'
STK_SOL = 'class Stack {\n    private final ArrayList<Integer> items = new ArrayList<>();\n\n    void push(int value) {\n        items.add(value);\n    }\n\n    int pop() {\n        return items.remove(items.size() - 1);\n    }\n\n    int peek() {\n        return items.get(items.size() - 1);\n    }\n\n    int size() {\n        return items.size();\n    }\n}\n\n'
ex.method("write", "j2-l3.3-write-stack", "A stack that has a list", ["o1"], ["J2.09"], ["IMPL"],
    "This `Stack` **is a** list (it `extends ArrayList<Integer>`), so callers can do things a stack shouldn't allow. Redesign it by composition: remove the `extends`, keep a private list inside, and offer only `push`, `pop` (removes and returns the last pushed value), `peek` (returns it without removing) and `size`. The driver runs a list of operations and shows the values it popped or peeked, then `|` and the final size.",
    [("run", [("ops", "String[]")], "String")], {"run": stack_run},
    [("run", [["push:1", "push:2", "pop", "peek"]]), ("run", [["push:5"]]), ("run", [["push:1", "push:2", "push:3", "pop", "pop"]])],
    [("run", [["push:7", "peek", "peek"]]), ("run", [["push:1", "pop", "push:2", "pop"]]), ("run", [[]]), ("run", [["push:-4", "push:0", "pop", "peek", "size"]]), ("run", [["push:9", "push:8", "push:7", "peek", "pop", "peek"]])],
    'class Stack extends ArrayList<Integer> {\n}\n\n' + STK_DRIVER,
    STK_SOL + STK_DRIVER,
    {"pop-takes-the-first": STK_SOL.replace("items.remove(items.size() - 1)", "items.remove(0)") + STK_DRIVER,
     "peek-removes": STK_SOL.replace("return items.get(items.size() - 1);", "return items.remove(items.size() - 1);") + STK_DRIVER},
    ("Remove extends ArrayList<Integer>. Add a private field holding the list, and write the four methods using it.", "private final ArrayList<Integer> items = new ArrayList<>(); ... items.add(value); items.remove(items.size() - 1);"),
    source_tests=[("the stack no longer extends ArrayList", None, ["extends ArrayList"])],
    starter_compiles=False, difficulty=3)
ex.explain("j2-l3.3-explain-inherit-compose", "Should it inherit?", ["o2"], ["J2.09"],
    "A team proposes `class Penguin extends Bird`, where `Bird` has `void fly()`, and a loop `for (Bird b : birds) b.fly();`. Another team proposes `class Stack extends ArrayList<Integer>`. For **one** of these two (your choice), say whether you would use inheritance, using the **substitution test**, and describe what you would do instead.",
    "A full answer picks one case, applies the substitution test (code written for the parent would not still work: a penguin cannot fly, or a stack would expose list methods such as add(0, x) that break stack behaviour), and proposes an alternative (an interface such as FlyingBird that only some birds implement, or a Stack that holds a list and delegates).",
    {2: ("Chooses one case, applies the substitution test with a concrete failure of code written for the parent, and gives a workable alternative (a FlyingBird interface, or composition with delegation).",
         ["I'd not use inheritance for Penguin. Code written for Bird calls fly() on every bird, and a penguin can't fly, so it would fail or lie, which breaks the substitution test. Instead I'd make fly() part of a FlyingBird interface that only the birds that fly implement.",
          "For Stack I wouldn't inherit from ArrayList. Code written for a list expects things like add(0, x), and a stack that allowed that would stop behaving like a stack, so a Stack can't safely stand in for a list. I'd hold a private list inside Stack and delegate push, pop and peek to it."]),
     1: ("Gives a sensible conclusion without applying the substitution test, or applies it but offers no alternative.",
         ["Penguins can't fly so it's wrong.", "Don't extend ArrayList."]),
     0: ("Incorrect, for example says inheritance is always correct because a penguin is a bird in real life.",
         ["Penguin is a bird so inherit.", "Inheritance is always best."])})
reg({"j2-l3.3": ("Composition over inheritance", ["J2.09"])},
    {"MC47": (["J2.09"], "Platform", "Inheritance is the right way to reuse another class's code"),
     "MC48": (["J2.09"], "Platform", "If something is-a thing in the real world, the classes should inherit")})
print("2.2 and 2.3 written")
