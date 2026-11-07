import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-2"
from build import *
import outline, re
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'
def jd(a, b):
    return int(a / b)

# ====================================================================== 2.4.1
Lesson("j2-l4.1", "Records and enums", ["J2.10"], [
    ("o1", "Declare a record, and use its accessors, equals and toString, with validation in a compact constructor"),
    ("o2", "Declare an enum with fields, a constructor and methods, and look constants up by name"),
    ("o3", "Choose between a class, a record and an enum for a given thing"),
], ["j2-l3.3"], 45, ["I25", "I37", "R8"], r'''
## Before you start

You should know how to write `equals`, `hashCode` and `toString` by hand ([static, toString and equals](j2-l1.4)) and what immutability is ([Immutability and defensive copies](j2-l2.2)).

**Quick check.** Why did `Point` need both `equals` and `hashCode`?

<details><summary>Show the answer</summary>

Equal objects must have equal hash codes, and hash-based collections rely on that.

</details>

## Explanation

Writing a small class that just carries a few values means a lot of repeated code: fields, a constructor, accessors, `equals`, `hashCode`, `toString`. Java has two shortcuts for common shapes of class.

### Records: a class for carrying values

A **record** declares all of that in one line `[I25]`:

```java
record Point(int x, int y) {}
```

From that header the compiler creates, for you:

- a private final field for each **component** (`x`, `y`);
- a constructor taking them in order;
- accessor methods named after the components: `p.x()` and `p.y()` (no `get` prefix);
- `equals` and `hashCode` that compare all the components;
- a `toString` like `Point[x=1, y=2]`.

```java runnable
record Point(int x, int y) {}

void main() {
    Point a = new Point(1, 2);
    Point b = new Point(1, 2);
    IO.println(a);
    IO.println(a.equals(b));
    IO.println(a.x());
}
```

It prints `Point[x=1, y=2]`, `true` and `1`. All records extend `java.lang.Record` `[I37]`.

A record is **shallowly immutable**: its fields can't be reassigned. But if a component is an array or a list, the contents can still change, so the defensive-copy rule still applies.

**Adding rules.** A record can have extra methods and static members. To validate its values, write a **compact constructor**, a constructor with no parameter list, which runs before the fields are assigned `[I25]`:

```java
record Rect(int w, int h) {
    Rect {
        if (w < 0 || h < 0) {
            throw new IllegalArgumentException("negative size");
        }
    }

    int area() {
        return w * h;
    }
}
```

A record can't extend another class, and can't have instance fields beyond its components, but it can implement interfaces.

### Enums: a fixed set of named values

An **enum** is a type with a small, fixed list of constants:

```java
enum Level { LOW, MEDIUM, HIGH }
```

You write `Level.HIGH`. Enums work well with `switch`, and the compiler checks you've covered every constant when you use a `switch` expression:

```java
String label(Level level) {
    return switch (level) {
        case LOW -> "low";
        case MEDIUM -> "medium";
        case HIGH -> "high";
    };
}
```

Useful methods: `Level.values()` (an array of all constants), `level.name()` (`"HIGH"`), `level.ordinal()` (its position, starting at 0), and `Level.valueOf("HIGH")`, which finds a constant by its exact name and throws `IllegalArgumentException` if there's no such constant.

Compare enum constants with `==`; there's exactly one object per constant.

**Enums with data.** An enum can have fields, a constructor and methods, like a class:

```java runnable
enum Size {
    SMALL(250), MEDIUM(330), LARGE(500);

    private final int ml;

    Size(int ml) {
        this.ml = ml;
    }

    int ml() {
        return ml;
    }
}

void main() {
    IO.println(Size.MEDIUM.ml());
    IO.println(Size.valueOf("LARGE").ml());
}
```

It prints `330` then `500`. The constants are created once, by calling the constructor with the numbers in brackets.

### Choosing: class, record or enum?

| Use a… | when the thing is… | Example |
|---|---|---|
| **record** | just its values; two with equal values are interchangeable | `Point`, `Money`, a transaction |
| **enum** | one of a small, fixed set known in advance | `Level`, `DayOfWeek`, a card suit |
| **class** | something with identity and changing state, or behaviour beyond its data | `Account`, `Player` |

## Worked examples

### Example 1: shrinking a class to a record

*Task: `Point` is 25 lines: fields, a constructor, `x()` and `y()`, `equals`, `hashCode`, `toString`. Replace it.*

**Step 1 — List the components,** in order: `x`, `y`.

**Step 2 — Check the class does nothing beyond carrying and comparing those values.** It doesn't.

**Step 3 — Replace the whole class with `record Point(int x, int y) {}`.**

**Step 4 — Check callers.** They already used `p.x()`, so nothing else changes. If they used `getX()`, they would need updating. The `toString` format is the same as the hand-written one, `Point[x=1, y=2]`.

### Example 2: when to reach for an enum

*Task: an order has a status that is exactly one of `NEW`, `PAID` or `SHIPPED`. A teammate used the strings `"new"`, `"paid"`, `"shipped"`.*

**Step 1 — What goes wrong with strings?** A typo such as `"payed"` compiles and fails at run time, or silently never matches.

**Step 2 — Use an enum:** `enum Status { NEW, PAID, SHIPPED }`.

**Step 3 — Now a typo like `Status.PAYED` is a compile error,** and a `switch` over `Status` can be checked for completeness.

## Where this is used

- **Data carriers:** results, events, messages, and values returned from methods are usually records in modern Java.
- **State and kind fields:** statuses, roles, currencies, and directions are enums.
- **Frameworks:** Spring and JSON libraries both work well with records and enums, as you'll see in Stage 7.

## Common mistakes

:::mistake{id=MC49}
**Calling `p.getX()` on a record.** Record accessors are named after the component, so use `p.x()`.
:::

:::mistake{id=MC50}
**Using strings for a fixed set of options.** A misspelt string compiles. A misspelt enum constant doesn't.
:::

:::mistake{id=MC51}
**Assuming a record's array or list component can't change.** The field can't be reassigned, but the array or list it points at can be modified, so copy it in.
:::

## Practice

::exercise{id=j2-l4.1-write-record}

::exercise{id=j2-l4.1-write-enum}

::exercise{id=j2-l4.1-modify-point}

::exercise{id=j2-l4.1-explain-choose}

## Version notes

**Records** were added in **Java 16**, and **sealed** types (next lesson) in **Java 17** `[I25]`. Enums have existed since Java 5. Code from before Java 16 writes the class out by hand, and you'll meet plenty of it.

## Further reading

- **JEP 395: Records** `[I25]` explains the design, including the compact constructor.
- **The `java.lang.Record` documentation** `[I37]`.
- **Qian & Lehman (2017)** `[R8]` for the research on novice difficulty with types.

## How you'll be assessed

- The **write** exercises check that you can write a validating record and an enum with data (*implementation*).
- The **modify** exercise checks that you can replace a hand-written value class with a record without changing behaviour (*modification*).
- The **explain** exercise checks that you can choose the right kind of type and say why (*explanation*).
''' + FOOT, features=[("records", 16), ("compact constructors", 16)])

ex = Exercises("j2-l4.1")
RECT_DRV = 'String run(int w, int h) {\n    try {\n        Rect r = new Rect(w, h);\n        return r + " area=" + r.area();\n    } catch (IllegalArgumentException e) {\n        return "rejected";\n    }\n}'
RECT_SOL = 'record Rect(int w, int h) {\n    Rect {\n        if (w < 0 || h < 0) {\n            throw new IllegalArgumentException("negative size");\n        }\n    }\n\n    int area() {\n        return w * h;\n    }\n}\n\n'
ex.method("write", "j2-l4.1-write-record", "A rectangle that can't be negative", ["o1"], ["J2.10"], ["IMPL"],
    "`Rect` is a record. Finish it: `area()` should return `w * h`, and a **compact constructor** should refuse a negative width or height with an `IllegalArgumentException`. (Zero is allowed.) The driver shows the record's own `toString`, e.g. `Rect[w=3, h=4] area=12`, or `rejected`.",
    [("run", [("w", "int"), ("h", "int")], "String")],
    {"run": lambda w, h: "rejected" if w < 0 or h < 0 else f"Rect[w={w}, h={h}] area={w*h}"},
    [("run", [3, 4]), ("run", [-1, 4]), ("run", [0, 0])],
    [("run", [5, -2]), ("run", [0, 7]), ("run", [10, 10]), ("run", [-3, -3]), ("run", [1, 1])],
    'record Rect(int w, int h) {\n    int area() {\n        return 0;\n    }\n}\n\n' + RECT_DRV,
    RECT_SOL + RECT_DRV,
    {"rejects-zero": RECT_SOL.replace("w < 0 || h < 0", "w <= 0 || h <= 0") + RECT_DRV,
     "area-adds": RECT_SOL.replace("return w * h;", "return w + h;") + RECT_DRV},
    ("Add a constructor with no parameter list inside the record, and check the components inside it.", "Rect { if (w < 0 || h < 0) throw new IllegalArgumentException(\"negative size\"); }  and  int area() { return w * h; }"),
    source_tests=[("validates in a compact constructor", ["Rect {"], None)],
    difficulty=3)
SIZE_DRV = 'int total(String[] names) {\n    int sum = 0;\n    for (String n : names) {\n        sum += Size.valueOf(n.toUpperCase()).ml();\n    }\n    return sum;\n}'
SIZE_SOL = 'enum Size {\n    SMALL(250), MEDIUM(330), LARGE(500);\n\n    private final int ml;\n\n    Size(int ml) {\n        this.ml = ml;\n    }\n\n    int ml() {\n        return ml;\n    }\n}\n\n'
ex.method("write", "j2-l4.1-write-enum", "Drink sizes", ["o2"], ["J2.10"], ["IMPL"],
    "Give each `Size` its volume: `SMALL` is 250 ml, `MEDIUM` 330 ml and `LARGE` 500 ml. Store it in a field set by a constructor, and return it from `ml()`. The driver adds up the volumes of a list of size names.",
    [("total", [("names", "String[]")], "int")],
    {"total": lambda ns: sum({"small": 250, "medium": 330, "large": 500}[n.lower()] for n in ns)},
    [("total", [["small", "large"]]), ("total", [["medium"]]), ("total", [[]])],
    [("total", [["small", "small", "small"]]), ("total", [["LARGE", "Medium"]]), ("total", [["large", "large"]]), ("total", [["medium", "small", "large"]]), ("total", [["SMALL"]])],
    'enum Size {\n    SMALL, MEDIUM, LARGE;\n\n    int ml() {\n        return 0;\n    }\n}\n\n' + SIZE_DRV,
    SIZE_SOL + SIZE_DRV,
    {"wrong-medium": SIZE_SOL.replace("MEDIUM(330)", "MEDIUM(300)") + SIZE_DRV,
     "doubles": SIZE_SOL.replace("return ml;", "return ml * 2;") + SIZE_DRV},
    ("Each constant takes a number in brackets, so the enum needs a constructor and a field to store it.", "SMALL(250), MEDIUM(330), LARGE(500); private final int ml; Size(int ml) { this.ml = ml; } int ml() { return ml; }"),
    difficulty=2)
POINT_CLASS = 'class Point {\n    private final int x;\n    private final int y;\n\n    Point(int x, int y) {\n        this.x = x;\n        this.y = y;\n    }\n\n    int x() {\n        return x;\n    }\n\n    int y() {\n        return y;\n    }\n\n    @Override\n    public boolean equals(Object o) {\n        if (this == o) return true;\n        if (!(o instanceof Point p)) return false;\n        return x == p.x && y == p.y;\n    }\n\n    @Override\n    public int hashCode() {\n        return Objects.hash(x, y);\n    }\n\n    @Override\n    public String toString() {\n        return "Point[x=" + x + ", y=" + y + "]";\n    }\n}\n\n'
PT_DRV = 'String run(int x1, int y1, int x2, int y2) {\n    Point a = new Point(x1, y1);\n    Point b = new Point(x2, y2);\n    return a.equals(b) + " " + a + " " + a.x();\n}'
ex.method("modify", "j2-l4.1-modify-point", "Shrink it to a record", ["o1"], ["J2.10"], ["MOD"],
    "`Point` is a hand-written value class, 30 lines long. Replace it with a **record** that behaves identically: same accessors `x()` and `y()`, same `equals`, and the same `toString`. The driver shouldn't need changing, and the output must stay the same.",
    [("run", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "String")],
    {"run": lambda x1, y1, x2, y2: f"{str(x1 == x2 and y1 == y2).lower()} Point[x={x1}, y={y1}] {x1}"},
    [("run", [1, 2, 1, 2]), ("run", [1, 2, 3, 4]), ("run", [0, 0, 0, 0])],
    [("run", [5, 6, 6, 5]), ("run", [-1, -2, -1, -2]), ("run", [7, 8, 7, 9]), ("run", [100, 0, 100, 0]), ("run", [3, 3, 4, 3])],
    POINT_CLASS + PT_DRV,
    'record Point(int x, int y) {}\n\n' + PT_DRV,
    {"components-swapped": 'record Point(int y, int x) {}\n\n' + PT_DRV},
    ("A record header lists the components in the order that the toString shows them.", "record Point(int x, int y) {}"),
    source_tests=[("it is a record", ["record Point"], ["class Point"])],
    difficulty=2)
ex.explain("j2-l4.1-explain-choose", "Class, record or enum?", ["o3"], ["J2.10"],
    "For each of these, say whether you'd use a **class**, a **record** or an **enum**, with a one-line reason: (a) a bank account with a balance that changes; (b) a pair of map coordinates; (c) the four seasons; (d) the result of a search: a name and a score that never change once created.",
    "A full answer says class for the account (identity and changing state), record for the coordinates (just values, equal if the components are equal), enum for the seasons (a small fixed set), and record for the search result (immutable data).",
    {2: ("Chooses class for (a), record for (b) and (d), enum for (c), each with a correct reason (identity and changing state; just values; a fixed set known in advance; immutable data).",
         ["(a) class, because an account has identity and its balance changes. (b) record, because it's just two values and equal coordinates are the same. (c) enum, because the seasons are a small fixed set. (d) record, since it only carries data that never changes.",
          "Account: class (identity, mutable state). Coordinates: record (pure values). Seasons: enum (fixed set). Search result: record (immutable data carrier)."]),
     1: ("Gets two or three of the four right, or gives choices without reasons.",
         ["(a) class (b) record (c) enum (d) class", "Record for most of them."]),
     0: ("Incorrect, for example uses an enum for the account or a class for everything with no reasoning.",
         ["They should all be enums.", "Use a class for everything."])})
reg({"j2-l4.1": ("Records and enums", ["J2.10"])},
    {"MC49": (["J2.10"], "Platform", "Record accessors are named getX()"),
     "MC50": (["J2.10"], "Platform", "Strings are as good as an enum for a fixed set of options"),
     "MC51": (["J2.10"], "R8", "An array or list inside a record cannot change because the record is immutable")})

# ====================================================================== 2.4.2
Lesson("j2-l4.2", "Sealed types and pattern-matching switch", ["J2.11"], [
    ("o1", "Declare a sealed interface with record implementations to model a closed set of possibilities"),
    ("o2", "Write a pattern-matching switch expression that the compiler checks is complete"),
    ("o3", "Find and fix a switch that doesn't cover every case, without hiding the problem with default"),
], ["j2-l4.1"], 45, ["I26", "I27", "R8"], r'''
## Before you start

You should know records and enums ([Records and enums](j2-l4.1)) and interfaces ([Interfaces and polymorphism](j2-l3.1)).

**Quick check.** How does the compiler help when you `switch` over an enum without a `default`?

<details><summary>Show the answer</summary>

In a `switch` expression it makes sure you covered every constant, and gives an error if you didn't.

</details>

## Explanation

### A closed set of kinds, each with its own data

An enum gives you a fixed set of constants, all of the same shape. Often each kind needs **different data**. A bank transaction might be a deposit (an amount), a withdrawal (an amount) or a fee (a percentage). A **sealed interface** with a record per kind models that.

```java
sealed interface Txn permits Deposit, Withdrawal, Fee {}

record Deposit(int amount) implements Txn {}
record Withdrawal(int amount) implements Txn {}
record Fee(int percent) implements Txn {}
```

`sealed` restricts which classes may implement the interface: only those named in `permits` `[I26]`. Nobody can add a fourth kind from outside. That's the point: the list is **closed**, so the compiler knows every possibility.

### Pattern matching in `switch`

A `switch` can test what **type** a value has, and give you a typed variable `[I27]`:

```java
int apply(Txn t, int balance) {
    return switch (t) {
        case Deposit d    -> balance + d.amount();
        case Withdrawal w -> balance - w.amount();
        case Fee f        -> balance - balance * f.percent() / 100;
    };
}
```

Each `case Deposit d` means *if `t` is a `Deposit`, call it `d` and run this*. Inside, `d` has type `Deposit`, so `d.amount()` works.

### Exhaustiveness: the compiler checks you covered everything

Because `Txn` is sealed, the compiler knows the only possible kinds, so it can check that the `switch` handles **all** of them `[I27]`. If you forget one, the code **doesn't compile**:

```
error: the switch expression does not cover all possible input values
```

This is a big benefit. If you later add `record Refund(...) implements Txn`, every `switch` over `Txn` that lacks a `Refund` case stops compiling, and the compiler shows you every place to update.

That's why you shouldn't add a `default ->` branch to such a switch. A `default` makes the compiler happy, and *silently sends the new kind to the default branch*, so the bug moves from compile time to run time.

### Guards: `when`

A case can have an extra condition:

```java
String size(Shape s) {
    return switch (s) {
        case Circle c when c.r() > 10 -> "big circle";
        case Circle c                 -> "circle";
        case Square q                 -> "square";
    };
}
```

Cases are tried **from top to bottom**, so put the more specific one (the one with `when`) before the general one for the same type. An unguarded `case Circle c` placed *first* would catch every circle and the guarded case below it could never run. The compiler rejects that as a *dominated* label `[I27]`.

### Sealed hierarchies versus ordinary interfaces

| | Ordinary interface | Sealed interface |
|---|---|---|
| Who can add implementations? | anyone, anywhere | only the permitted types |
| Good when | new kinds should be easy to add by others (plug-ins) | the set of kinds is part of the design (transactions, shapes, results) |
| `switch` completeness | can't be checked | checked by the compiler |

Choose by asking: *do I want the compiler to know every possible kind?*

## Worked examples

### Example 1: modelling results

*Task: a parser either succeeds with a number or fails with a message. Model that.*

**Step 1 — Two kinds, different data.** Success has a `value`; failure has a `message`.

**Step 2 — A sealed interface with a record per kind:**

```java
sealed interface Result permits Ok, Failed {}
record Ok(int value) implements Result {}
record Failed(String message) implements Result {}
```

**Step 3 — Handle both with a switch, with no `default`:**

```java
String show(Result r) {
    return switch (r) {
        case Ok o     -> "value " + o.value();
        case Failed f -> "failed: " + f.message();
    };
}
```

**Step 4 — Check.** Adding a third kind makes `show` stop compiling until you handle it.

### Example 2: fixing an incomplete switch

*Task: the compiler says the switch doesn't cover all possible input values. `Shape` has `Circle`, `Square` and `Triangle`.*

**Step 1 — Find the missing kind.** The switch has cases for `Circle` and `Square`.

**Step 2 — Add the `Triangle` case,** with the behaviour that kind needs.

**Step 3 — Don't add `default` to silence it.** That would hide the next missing kind too.

## Predict, then run

::exercise{id=j2-l4.2-predict-guards}

## Where this is used

- **Results and errors:** "succeeded or failed with a reason" is modelled with sealed types in many modern codebases.
- **Commands, events, messages:** each kind has its own data, and handling code is a `switch` that must cover them all.
- **Parsers and interpreters:** syntax trees are naturally closed hierarchies.

## Common mistakes

:::mistake{id=MC52}
**Adding `default` to make the compiler stop complaining.** It hides the missing case now and every future one.
:::

:::mistake{id=MC53}
**Putting a general case before a guarded one for the same type.** The guarded case is dominated and can't run, and the compiler reports an error.
:::

## Practice

::exercise{id=j2-l4.2-write-transactions}

::exercise{id=j2-l4.2-debug-switch}

::exercise{id=j2-l4.2-explain-sealed}

## Version notes

**Sealed classes and interfaces** were added in **Java 17** `[I26]`, and **pattern matching for `switch`** (including `when` guards) in **Java 21** `[I27]`. Code written for earlier versions uses `if (x instanceof Deposit d) ... else if ...` chains, which the compiler can't check for completeness.

## Further reading

- **JEP 409: Sealed Classes** `[I26]` and **JEP 441: Pattern Matching for switch** `[I27]` describe the design, including how exhaustiveness uses the `permits` list.
- **Qian & Lehman (2017)** `[R8]` for research on misunderstandings of types.

## How you'll be assessed

- The **write** exercise checks that you can write an exhaustive pattern-matching switch over a sealed interface (*implementation*).
- The **debug** exercise checks that you can fix an incomplete switch without using `default` (*debugging*).
- The **predict** exercise checks that you can trace cases and guards in order (*identifying mistakes*).
- The **explain** exercise checks that you can say why sealed types plus a switch without `default` is safer (*explanation*).
''' + FOOT, features=[("sealed types", 17), ("pattern matching for switch", 21)])

ex = Exercises("j2-l4.2")
def txn_run(specs):
    b = 0
    for s in specs:
        k, n = s.split(":"); n = int(n)
        if k == "d": b += n
        elif k == "w": b -= n
        else: b -= jd(b * n, 100)
    return b
TX_TYPES = 'sealed interface Txn permits Deposit, Withdrawal, Fee {}\n\nrecord Deposit(int amount) implements Txn {}\nrecord Withdrawal(int amount) implements Txn {}\nrecord Fee(int percent) implements Txn {}\n\n'
TX_DRV = '\n\nint run(String[] specs) {\n    int balance = 0;\n    for (String s : specs) {\n        String[] p = s.split(":");\n        int n = Integer.parseInt(p[1]);\n        Txn t;\n        if (p[0].equals("d")) {\n            t = new Deposit(n);\n        } else if (p[0].equals("w")) {\n            t = new Withdrawal(n);\n        } else {\n            t = new Fee(n);\n        }\n        balance = apply(t, balance);\n    }\n    return balance;\n}'
TX_APPLY = 'int apply(Txn t, int balance) {\n    return switch (t) {\n        case Deposit d -> balance + d.amount();\n        case Withdrawal w -> balance - w.amount();\n        case Fee f -> balance - balance * f.percent() / 100;\n    };\n}'
ex.method("write", "j2-l4.2-write-transactions", "Apply a transaction", ["o1", "o2"], ["J2.11"], ["IMPL"],
    "`Txn` is a sealed interface with three record kinds: `Deposit(amount)`, `Withdrawal(amount)` and `Fee(percent)`. Write `apply(Txn t, int balance)` as a **pattern-matching `switch` expression** that returns the new balance: a deposit adds, a withdrawal subtracts, and a fee takes that percentage **of the current balance** (rounded down). Don't use `default`: the compiler should check you covered every kind.",
    [("run", [("specs", "String[]")], "int")], {"run": txn_run},
    [("run", [["d:100", "w:30"]]), ("run", [["d:200", "f:10"]]), ("run", [[]])],
    [("run", [["d:1000", "f:5", "f:5"]]), ("run", [["w:50"]]), ("run", [["d:99", "f:50"]]), ("run", [["d:10", "w:3", "d:4", "f:25"]]), ("run", [["d:7", "f:100"]])],
    TX_TYPES + 'int apply(Txn t, int balance) {\n    return balance;\n}' + TX_DRV,
    TX_TYPES + TX_APPLY + TX_DRV,
    {"fee-of-the-amount": TX_TYPES + TX_APPLY.replace("balance - balance * f.percent() / 100", "balance - f.percent()") + TX_DRV,
     "withdrawal-adds": TX_TYPES + TX_APPLY.replace("balance - w.amount()", "balance + w.amount()") + TX_DRV},
    ("Use return switch (t) { case Deposit d -> ...; case Withdrawal w -> ...; case Fee f -> ...; };", "case Fee f -> balance - balance * f.percent() / 100;"),
    source_tests=[("uses a switch on the transaction", ["switch (t)"], None), ("no default branch", None, ["default"])],
    difficulty=3)
SH_TYPES = 'sealed interface Shape permits Circle, Square, Triangle {}\n\nrecord Circle(int r) implements Shape {}\nrecord Square(int side) implements Shape {}\nrecord Triangle(int base, int height) implements Shape {}\n\n'
SH_DRV = '\n\nString run(String kind, int a, int b) {\n    Shape s;\n    if (kind.equals("circle")) {\n        s = new Circle(a);\n    } else if (kind.equals("square")) {\n        s = new Square(a);\n    } else {\n        s = new Triangle(a, b);\n    }\n    return describe(s);\n}'
SH_BAD = 'String describe(Shape s) {\n    return switch (s) {\n        case Circle c -> "circle r=" + c.r();\n        case Square q -> "square side=" + q.side();\n    };\n}'
SH_GOOD = 'String describe(Shape s) {\n    return switch (s) {\n        case Circle c -> "circle r=" + c.r();\n        case Square q -> "square side=" + q.side();\n        case Triangle t -> "triangle base=" + t.base() + " height=" + t.height();\n    };\n}'
def shape_run(k, a, b):
    return {"circle": f"circle r={a}", "square": f"square side={a}"}.get(k, f"triangle base={a} height={b}")
ex.method("debug", "j2-l4.2-debug-switch", "The switch that misses a shape", ["o3"], ["J2.11"], ["DEBUG"],
    "This code doesn't compile: the compiler says the `switch` doesn't cover all possible input values. Find the missing kind and add its case, so a triangle is described as `triangle base=3 height=4`. **Don't** add a `default` branch: it would hide the same mistake in future.",
    [("run", [("kind", "String"), ("a", "int"), ("b", "int")], "String")], {"run": shape_run},
    [("run", ["circle", 3, 0]), ("run", ["square", 5, 0]), ("run", ["triangle", 3, 4])],
    [("run", ["triangle", 10, 2]), ("run", ["circle", 1, 9]), ("run", ["square", 0, 0]), ("run", ["triangle", 1, 1]), ("run", ["circle", 7, 7])],
    SH_TYPES + SH_BAD + SH_DRV,
    SH_TYPES + SH_GOOD + SH_DRV,
    {"default-hides-it": SH_TYPES + SH_BAD.replace('    };', '        default -> "unknown";\n    };') + SH_DRV},
    ("Which of the three records has no case in the switch?", "case Triangle t -> \"triangle base=\" + t.base() + \" height=\" + t.height();"),
    source_tests=[("handles Triangle explicitly", ["case Triangle"], None), ("no default branch", None, ["default"])],
    starter_compiles=False, difficulty=2)
ex.predict("j2-l4.2-predict-guards", "Which case runs?", ["o2"], ["J2.11"],
    "Work out what this program prints. Cases are tried from top to bottom.",
    '''sealed interface Shape permits Circle, Square {}

record Circle(int r) implements Shape {}
record Square(int side) implements Shape {}

String size(Shape s) {
    return switch (s) {
        case Circle c when c.r() > 10 -> "big circle";
        case Circle c -> "circle";
        case Square q when q.side() > 10 -> "big square";
        case Square q -> "square";
    };
}

void main() {
    IO.println(size(new Circle(3)));
    IO.println(size(new Circle(30)));
    IO.println(size(new Square(30)));
    IO.println(size(new Square(10)));
}''', "circle\nbig circle\nbig square\nsquare",
    ("For each value, find the first case that matches: both the type and the when condition.", "Circle(3): not over 10, so \"circle\". Square(10): 10 > 10 is false, so \"square\"."),
    difficulty=2)
ex.explain("j2-l4.2-explain-sealed", "Why no default?", ["o2", "o3"], ["J2.11"],
    "A teammate adds `default -> 0;` to a `switch` over a sealed `Txn` interface \"to be safe\". Explain what the compiler does for a sealed type when there is **no** `default`, what happens when someone later adds a fourth kind of transaction with and without the `default`, and why the teammate's change makes the code less safe.",
    "A full answer says that for a sealed type the compiler knows every permitted kind and checks the switch covers them all; without default, adding a fourth kind makes every switch over Txn fail to compile until it handles it; with default, the new kind silently falls into the default branch and gives a wrong result at run time, so the error moves from compile time to run time.",
    {2: ("Says the compiler checks completeness for a sealed type; without default adding a kind causes compile errors that show every switch to update; with default the new kind silently takes the default branch, so the bug appears at run time.",
         ["With a sealed type the compiler knows all the permitted kinds, so it checks every case is covered. If someone adds a fourth kind, every switch without a default stops compiling, which tells you exactly where to update. With default -> 0 the new kind would silently return 0, so the mistake only shows up at run time, which is worse.",
          "Without a default the compiler guarantees the switch handles every kind. A new kind then causes a compile error in each switch. A default branch makes the compiler accept it and quietly sends the new kind down the default path, hiding the bug until run time."]),
     1: ("Says default hides problems or that the compiler checks coverage, but doesn't connect it to adding a new kind.",
         ["Default hides the problem.", "The compiler checks all the cases are covered."]),
     0: ("Incorrect, for example says default is always required or makes the code safer.",
         ["A switch always needs a default.", "Default makes it safer."])})
reg({"j2-l4.2": ("Sealed types and pattern-matching switch", ["J2.11"])},
    {"MC52": (["J2.11"], "Platform", "Adding default to a switch over a sealed type is the safe thing to do"),
     "MC53": (["J2.11"], "Platform", "The order of cases in a pattern switch does not matter")})

# ====================================================================== 2.5.1
Lesson("j2-l5.1", "Catching exceptions", ["J2.12"], [
    ("o1", "Use try, catch and finally to handle a specific exception"),
    ("o2", "Predict which lines run when an exception is thrown, including finally"),
    ("o3", "Fix code that catches too much or swallows an error silently"),
], ["j2-l4.2", "j1-l6.4"], 45, ["I40", "R16", "R8"], r'''
## Before you start

You've seen exceptions as crashes with stack traces ([Exceptions and stack traces](j1-l6.4)), and you've seen `try` / `catch` in the drivers of earlier exercises.

**Quick check.** What does `Integer.parseInt("abc")` do?

<details><summary>Show the answer</summary>

It throws a `NumberFormatException`, and the program crashes with a stack trace unless that exception is caught.

</details>

## Explanation

### Handling an exception

When code throws an exception, the method stops and the exception travels up the call chain looking for a handler. If none is found, the program ends. To **catch** it:

```java
try {
    int n = Integer.parseInt(text);
    IO.println("Got " + n);
} catch (NumberFormatException e) {
    IO.println("That isn't a number");
}
```

- The `try` block runs normally. If a line in it throws a `NumberFormatException`, the **rest of the block is skipped** and Java jumps to the matching `catch`.
- If nothing is thrown, the `catch` is skipped.
- `e` is the exception object. `e.getMessage()` gives its message.

### Several catches, most specific first

```java
try {
    int x = Integer.parseInt(a);
    int y = Integer.parseInt(b);
    return String.valueOf(x / y);
} catch (NumberFormatException e) {
    return "not a number";
} catch (ArithmeticException e) {
    return "divide by zero";
}
```

Java uses the **first** `catch` that matches, so put specific types before general ones. Exception types form a hierarchy `[I40]`: `Throwable` is the superclass of all errors and exceptions. A `catch (Exception e)` catches almost everything, so if it came first the more specific ones after it would never run (and the compiler rejects that). To handle two types the same way: `catch (NumberFormatException | ArithmeticException e)`.

### `finally`: code that always runs

```java runnable
int attempt(String s) {
    try {
        IO.println("parsing");
        int n = Integer.parseInt(s);
        IO.println("parsed " + n);
        return n;
    } catch (NumberFormatException e) {
        IO.println("bad");
        return -1;
    } finally {
        IO.println("done");
    }
}

void main() {
    IO.println(attempt("12"));
    IO.println(attempt("x"));
}
```

It prints:

```
parsing
parsed 12
done
12
parsing
bad
done
-1
```

Notice that `done` is printed **before** the returned value shows up: `finally` runs as the method is leaving, whether it leaves by finishing, by `return`, or by an exception. Use it for clean-up that must happen regardless. (Lesson 2.5.3 shows a neater way for resources.)

### What to catch, and what not to

- **Catch the most specific type you can handle.** `catch (NumberFormatException e)` says exactly what you expect to go wrong.
- **Don't catch `Exception` just to make errors go away.** It also catches bugs you didn't expect, such as a `NullPointerException` from a typo, and hides them.
- **Never leave a `catch` block empty.** An empty catch (or one that just returns a default silently) is called *swallowing* the exception: the program carries on in a wrong state, and nobody ever learns why. If you really do want to ignore it, say so in a comment and be sure.
- **Keep the `try` block small.** Wrap just the lines that can throw, so a failure on one item doesn't throw away everything else.

### Catching per item

Compare two ways to sum a list of text numbers where bad entries should be skipped:

```java
// one try around the loop: the first bad entry ends the whole thing
try {
    for (String p : parts) sum += Integer.parseInt(p);
} catch (NumberFormatException e) { }

// the try inside the loop: each bad entry is skipped on its own
for (String p : parts) {
    try {
        sum += Integer.parseInt(p);
    } catch (NumberFormatException e) {
        // skip this one
    }
}
```

The second matches the requirement; the first stops at the first bad entry.

## Worked examples

### Example 1: a safe conversion

*Task: `parseOr(text, fallback)` returns the number in `text`, or `fallback` if it isn't one.*

**Step 1 — Which exception?** `NumberFormatException` from `Integer.parseInt`.

**Step 2 — Wrap just the parse in `try`, and return the fallback in the catch.**

```java
int parseOr(String text, int fallback) {
    try {
        return Integer.parseInt(text.trim());
    } catch (NumberFormatException e) {
        return fallback;
    }
}
```

**Step 3 — Check.** `parseOr(" 7 ", 0)` is 7 (trimmed), `parseOr("abc", -1)` is -1.

### Example 2: spotting a swallowed bug

*Task: why does `average` print 0 for every input?*

```java
double average(String[] parts) {
    try {
        double sum = 0;
        for (String p : parts) sum += Double.parseDouble(p);
        return sum / parts.length;
    } catch (Exception e) {
        return 0;
    }
}
```

**Step 1 — What does `catch (Exception e)` cover?** Everything: bad numbers, a null `parts`, anything.

**Step 2 — So the real problem is hidden.** One bad entry throws away the whole sum.

**Step 3 — Fix:** catch only `NumberFormatException`, inside the loop, and decide deliberately what to do with a bad entry.

## Predict, then run

::exercise{id=j2-l5.1-predict-finally}

## Where this is used

- **Anything with input:** user typing, files, network messages all produce bad data. Catching at the right place keeps one bad item from crashing everything.
- **Robust services** log an unexpected exception and continue with the next request, rather than stopping.
- **Debugging:** swallowed exceptions are among the hardest bugs to find, because the evidence has been thrown away.

## Common mistakes

:::mistake{id=MC54}
**`catch (Exception e)` around a whole method.** It hides bugs and makes one bad item discard all the good ones.
:::

:::mistake{id=MC55}
**An empty `catch` block.** The error disappears, and the program continues in an unknown state.
:::

:::mistake{id=MC56}
**Expecting the lines after the throwing statement in `try` to run.** They're skipped as soon as something throws.
:::

## Practice

::exercise{id=j2-l5.1-write-parse}

::exercise{id=j2-l5.1-write-divide}

::exercise{id=j2-l5.1-debug-sum}

::exercise{id=j2-l5.1-explain-swallow}

## Further reading

- **The `java.lang.Throwable` documentation** `[I40]` describes the class every exception extends.
- **McCauley et al. (2008)** `[R16]` on debugging: swallowed exceptions are an example of removing the evidence a debugger needs.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can catch specific exceptions and return a sensible result (*implementation*).
- The **predict** exercise checks that you can trace `try`, `catch` and `finally` (*identifying mistakes*).
- The **debug** exercise checks that you can fix an over-broad catch (*debugging*).
- The **explain** exercise checks that you can say why swallowing exceptions is dangerous (*explanation*).
''' + FOOT)

ex = Exercises("j2-l5.1")
def parse_or(t, f):
    s = t.strip()
    return int(s) if re.fullmatch(r"[+-]?[0-9]+", s) else f
ex.method("write", "j2-l5.1-write-parse", "A safe parse", ["o1"], ["J2.12"], ["IMPL"],
    "Write `parseOr(String text, int fallback)`: return the whole number in `text` (ignoring spaces at either end), or `fallback` if it isn't a valid whole number. Catch the specific exception that `Integer.parseInt` throws.",
    [("parseOr", [("text", "String"), ("fallback", "int")], "int")], {"parseOr": parse_or},
    [("parseOr", ["42", 0]), ("parseOr", ["abc", -1]), ("parseOr", [" 7 ", 0])],
    [("parseOr", ["", 5]), ("parseOr", ["-3", 0]), ("parseOr", ["3.5", 9]), ("parseOr", ["12x", 1]), ("parseOr", ["  ", 2]), ("parseOr", ["+8", 0])],
    'int parseOr(String text, int fallback) {\n    return Integer.parseInt(text.trim());\n}',
    'int parseOr(String text, int fallback) {\n    try {\n        return Integer.parseInt(text.trim());\n    } catch (NumberFormatException e) {\n        return fallback;\n    }\n}',
    {"returns-zero": 'int parseOr(String text, int fallback) {\n    try { return Integer.parseInt(text.trim()); } catch (NumberFormatException e) { return 0; }\n}',
     "no-trim": 'int parseOr(String text, int fallback) {\n    try { return Integer.parseInt(text); } catch (NumberFormatException e) { return fallback; }\n}'},
    ("Put the parse inside try, and return the fallback from the catch for NumberFormatException.", "try { return Integer.parseInt(text.trim()); } catch (NumberFormatException e) { return fallback; }"),
    source_tests=[("catches the specific exception", ["catch (NumberFormatException"], ["catch (Exception"])],
    difficulty=2)
def safe_div(a, b):
    ok = lambda s: re.fullmatch(r"[+-]?[0-9]+", s.strip())
    if not ok(a) or not ok(b): return "not a number"
    y = int(b.strip())
    if y == 0: return "divide by zero"
    return str(jd(int(a.strip()), y))
ex.method("write", "j2-l5.1-write-divide", "Two things that can go wrong", ["o1"], ["J2.12"], ["IMPL"],
    "Write `safeDivide(String a, String b)`: parse both texts as whole numbers (ignoring spaces) and return `a / b` as text (whole-number division). If either isn't a number, return `\"not a number\"`. If `b` is zero, return `\"divide by zero\"`. Use **two separate `catch` blocks**, one for each exception.",
    [("safeDivide", [("a", "String"), ("b", "String")], "String")], {"safeDivide": safe_div},
    [("safeDivide", ["10", "2"]), ("safeDivide", ["x", "2"]), ("safeDivide", ["5", "0"])],
    [("safeDivide", ["7", "2"]), ("safeDivide", ["-9", "2"]), ("safeDivide", ["4", ""]), ("safeDivide", [" 8 ", " 4 "]), ("safeDivide", ["0", "5"]), ("safeDivide", ["abc", "0"])],
    'String safeDivide(String a, String b) {\n    int x = Integer.parseInt(a.trim());\n    int y = Integer.parseInt(b.trim());\n    return String.valueOf(x / y);\n}',
    'String safeDivide(String a, String b) {\n    try {\n        int x = Integer.parseInt(a.trim());\n        int y = Integer.parseInt(b.trim());\n        return String.valueOf(x / y);\n    } catch (NumberFormatException e) {\n        return "not a number";\n    } catch (ArithmeticException e) {\n        return "divide by zero";\n    }\n}',
    {"one-broad-catch": 'String safeDivide(String a, String b) {\n    try {\n        int x = Integer.parseInt(a.trim());\n        int y = Integer.parseInt(b.trim());\n        return String.valueOf(x / y);\n    } catch (Exception e) {\n        return "not a number";\n    }\n}',
     "messages-swapped": 'String safeDivide(String a, String b) {\n    try {\n        int x = Integer.parseInt(a.trim());\n        int y = Integer.parseInt(b.trim());\n        return String.valueOf(x / y);\n    } catch (NumberFormatException e) {\n        return "divide by zero";\n    } catch (ArithmeticException e) {\n        return "not a number";\n    }\n}'},
    ("Integer.parseInt can throw NumberFormatException; x / y with y == 0 throws ArithmeticException. Catch each one separately.", "catch (NumberFormatException e) { return \"not a number\"; } catch (ArithmeticException e) { return \"divide by zero\"; }"),
    source_tests=[("catches both specific exceptions", ["catch (NumberFormatException", "catch (ArithmeticException"], None)],
    difficulty=3)
ex.predict("j2-l5.1-predict-finally", "What runs, and in what order?", ["o2"], ["J2.12"],
    "Work out exactly what this program prints. Remember that `finally` runs as the method is left.",
    '''int attempt(String s) {
    try {
        IO.println("parsing");
        int n = Integer.parseInt(s);
        IO.println("parsed " + n);
        return n;
    } catch (NumberFormatException e) {
        IO.println("bad");
        return -1;
    } finally {
        IO.println("done");
    }
}

void main() {
    IO.println(attempt("12"));
    IO.println(attempt("x"));
}''', "parsing\nparsed 12\ndone\n12\nparsing\nbad\ndone\n-1",
    ("Follow each call separately. Does finally run for both? When is the returned value printed?", "finally runs before the value is passed back, so \"done\" comes before the number is printed."),
    difficulty=3)
SUM_BAD = 'int sumValid(String[] parts) {\n    int sum = 0;\n    try {\n        for (String p : parts) {\n            sum += Integer.parseInt(p.trim());\n        }\n    } catch (Exception e) {\n        return 0;\n    }\n    return sum;\n}'
SUM_GOOD = 'int sumValid(String[] parts) {\n    int sum = 0;\n    for (String p : parts) {\n        try {\n            sum += Integer.parseInt(p.trim());\n        } catch (NumberFormatException e) {\n            // skip entries that are not numbers\n        }\n    }\n    return sum;\n}'
ex.method("debug", "j2-l5.1-debug-sum", "One bad entry ruins everything", ["o3"], ["J2.12"], ["DEBUG"],
    "`sumValid` should add up the entries that are numbers and **skip** the ones that aren't, so `{\"1\", \"x\", \"3\"}` gives `4`. It returns `0` as soon as one entry is bad. Fix it: catch only the exception you expect, and make a bad entry affect only itself.",
    [("sumValid", [("parts", "String[]")], "int")],
    {"sumValid": lambda ps: sum(int(p.strip()) for p in ps if re.fullmatch(r"[+-]?[0-9]+", p.strip()))},
    [("sumValid", [["1", "x", "3"]]), ("sumValid", [["5", "6"]]), ("sumValid", [[]])],
    [("sumValid", [["x", "y"]]), ("sumValid", [[" 4 ", "z", "-1"]]), ("sumValid", [["10", "", "20", "abc", "30"]]), ("sumValid", [["7"]]), ("sumValid", [["a", "2", "b"]])],
    SUM_BAD, SUM_GOOD,
    {"catch-outside-the-loop": 'int sumValid(String[] parts) {\n    int sum = 0;\n    try {\n        for (String p : parts) sum += Integer.parseInt(p.trim());\n    } catch (NumberFormatException e) {\n    }\n    return sum;\n}'},
    ("Where does the try block sit? Which entries does the catch affect?", "Move try/catch inside the loop, and catch NumberFormatException instead of Exception."),
    source_tests=[("catches the specific exception, not Exception", ["catch (NumberFormatException"], ["catch (Exception"])],
    difficulty=3)
ex.explain("j2-l5.1-explain-swallow", "The empty catch", ["o3"], ["J2.12"],
    "In a code review you find `try { process(order); } catch (Exception e) { }`. Explain three problems with it, and say what you'd write instead if the only expected failure is an `InvalidOrderException` that should be reported to the user.",
    "A full answer names that it catches every exception, including unexpected bugs; that the empty block swallows the error so nothing is reported or logged and the program continues in an unknown state; that it makes the failure hard to diagnose later; and suggests catching only InvalidOrderException and reporting a message to the user, letting others propagate.",
    {2: ("Gives at least three problems (catches everything including bugs, silently swallows the error, leaves the program in an unknown state or makes diagnosis hard) and proposes catching only InvalidOrderException and telling the user.",
         ["It catches every exception, including bugs like a NullPointerException I never expected. The empty block swallows the error, so nothing is logged or shown and nobody knows an order failed. And the program carries on as if it worked, in a state that may be wrong. I'd catch only InvalidOrderException and show the user a message, and let anything else propagate.",
          "Problems: too broad, silent, and it hides the evidence for debugging. Instead: catch (InvalidOrderException e) { tell the user what was wrong }, and leave other exceptions to be handled elsewhere."]),
     1: ("Gives one or two problems, or gives the fix without explaining the problems.",
         ["It hides errors.", "Catch the specific exception."]),
     0: ("Incorrect, for example says an empty catch is the safest way to keep a program running.",
         ["It keeps the program running, so it's fine.", "Exceptions should never be caught."])})
reg({"j2-l5.1": ("Catching exceptions", ["J2.12"])},
    {"MC54": (["J2.12"], "Platform", "Wrapping a whole method in catch (Exception e) is a safe way to make it robust"),
     "MC55": (["J2.12"], "Platform", "An empty catch block is harmless"),
     "MC56": (["J2.12"], "R8", "Lines after the throwing statement in a try block still run")})

# ====================================================================== 2.5.2
Lesson("j2-l5.2", "Custom and checked exceptions", ["J2.13"], [
    ("o1", "Define a custom exception class and throw it, declaring it with throws when it is checked"),
    ("o2", "Wrap a low-level exception in a higher-level one, keeping the original as the cause"),
    ("o3", "Explain the difference between checked and unchecked exceptions and when to use each"),
], ["j2-l5.1"], 45, ["I40", "R16"], r'''
## Before you start

You should be able to catch specific exceptions ([Catching exceptions](j2-l5.1)) and read a stack trace ([Exceptions and stack traces](j1-l6.4)).

**Quick check.** Why is `catch (NumberFormatException e)` better than `catch (Exception e)` for a failed parse?

<details><summary>Show the answer</summary>

It handles only the failure you expect, and doesn't hide unrelated bugs.

</details>

## Explanation

### Your own exceptions

Java's exceptions (`NumberFormatException`, `IllegalArgumentException`) describe general problems. For a bank, the problem *"you tried to spend more than you have"* deserves its own name. An exception is just a class, so you write one by extending an existing exception class:

```java
class InsufficientFundsException extends Exception {
    private final int shortBy;

    InsufficientFundsException(int shortBy) {
        super("short by " + shortBy);       // the message
        this.shortBy = shortBy;
    }

    int shortBy() {
        return shortBy;
    }
}
```

`super("...")` passes the message to the parent, so `getMessage()` works. The class can carry extra data (here, how much was missing) so the handler can use it.

You throw it like any other exception:

```java
throw new InsufficientFundsException(amount - balance);
```

### Checked and unchecked

Java divides exceptions into two groups `[I40]`:

- **Checked exceptions** are subclasses of `Exception` that are *not* `RuntimeException`. The compiler **forces** the caller to deal with them: catch them, or declare them with `throws`.
- **Unchecked exceptions** are `RuntimeException` and its subclasses (and `Error`). The compiler doesn't force anything. `NullPointerException`, `IllegalArgumentException` and `NumberFormatException` are unchecked.

```java
void spend(int amount) throws InsufficientFundsException {     // declared
    if (amount > balance) {
        throw new InsufficientFundsException(amount - balance);
    }
    balance -= amount;
}
```

A caller of `spend` must either wrap the call in `try` / `catch (InsufficientFundsException e)`, or declare `throws InsufficientFundsException` itself. Forgetting gives a compile error: `unreported exception InsufficientFundsException; must be caught or declared to be thrown`.

### Choosing which to extend

| Use… | when… | Example |
|---|---|---|
| **Checked** (`extends Exception`) | the caller can reasonably be expected to recover, and you want the compiler to remind them | a payment declined, a file that may not exist |
| **Unchecked** (`extends RuntimeException`) | it signals a programming mistake or a condition callers usually can't fix | a bad argument, a violated rule |

Many modern codebases lean towards unchecked exceptions, because checked ones spread `throws` clauses through every layer. A good rule: **checked when the caller has a real way to recover; otherwise unchecked.**

### Wrapping: keep the cause

Often a low-level problem should be reported in higher-level terms. A failed number parse while reading settings becomes "the configuration is bad". But don't throw away the original: pass it as the **cause**.

```java
class ConfigException extends RuntimeException {
    ConfigException(String message, Throwable cause) {
        super(message, cause);
    }
}

int readPort(String text) {
    try {
        return Integer.parseInt(text);
    } catch (NumberFormatException e) {
        throw new ConfigException("bad port: " + text, e);     // e is kept as the cause
    }
}
```

The original exception stays attached: `getCause()` returns it `[I40]`, and when the program crashes, the stack trace shows both, with a `Caused by:` line. That's what makes such traces useful for finding the real problem. Dropping the cause (`throw new ConfigException("bad port")` with no `e`) loses the evidence.

## Worked examples

### Example 1: a wallet that refuses

*Task: `Wallet.spend` should fail if the money isn't there, and the caller should be able to see how much was missing.*

**Step 1 — Define the exception with the useful data:** `shortBy`.

**Step 2 — Check before changing anything, and throw:**

```java
void spend(int amount) throws InsufficientFundsException {
    if (amount > balance) {
        throw new InsufficientFundsException(amount - balance);
    }
    balance -= amount;
}
```

**Step 3 — Check the order.** The check happens before `balance -= amount`, so a refused spend leaves the balance alone.

### Example 2: choosing the type

*Task: should `new Money(-5)` throw a checked or an unchecked exception?*

**Step 1 — Could the caller recover?** Passing a negative amount is a programming error.

**Step 2 — So use unchecked:** `IllegalArgumentException`. A checked exception would force `try`/`catch` on every `new Money(...)` for no benefit.

## Where this is used

- **Domain errors** such as `InsufficientFundsException`, `OrderNotFoundException`, `PaymentDeclinedException` make code read like the business.
- **Layered applications** wrap low-level errors (database, file) in higher-level ones, keeping the cause.
- **Stack traces** with `Caused by:` are how you diagnose most production failures.

## Common mistakes

:::mistake{id=MC57}
**Throwing away the cause when wrapping.** `throw new ConfigException("bad port")` loses the original exception. Pass it as the second argument.
:::

:::mistake{id=MC58}
**Making everything a checked exception.** Callers end up with `try` / `catch` and `throws` everywhere for errors they can't do anything about.
:::

## Practice

::exercise{id=j2-l5.2-write-insufficient}

::exercise{id=j2-l5.2-write-wrap}

::exercise{id=j2-l5.2-explain-checked}

## Further reading

- **The `java.lang.Throwable` documentation** `[I40]` defines checked exceptions and `getCause()`.
- **McCauley et al. (2008)** `[R16]` on debugging: the chain of causes in a stack trace is evidence you can follow.

## How you'll be assessed

- The **write** exercises check that you can define and throw a checked exception, and wrap one while keeping the cause (*implementation*).
- The **explain** exercise checks that you can say when to use checked and unchecked exceptions (*explanation*).
''' + FOOT)

ex = Exercises("j2-l5.2")
def wallet_run(start, amounts):
    bal, out = start, []
    for a in amounts:
        if a > bal: out.append(f"short by {a - bal}")
        else: bal -= a; out.append("ok")
    return " ".join(out) + (" " if out else "") + f"balance {bal}"
W_DRV = '\n\nString run(int start, int[] amounts) {\n    Wallet w = new Wallet(start);\n    StringBuilder out = new StringBuilder();\n    for (int a : amounts) {\n        try {\n            w.spend(a);\n            out.append("ok ");\n        } catch (InsufficientFundsException e) {\n            out.append(e.getMessage()).append(" ");\n        }\n    }\n    return out + "balance " + w.balance();\n}'
W_SOL = 'class InsufficientFundsException extends Exception {\n    private final int shortBy;\n\n    InsufficientFundsException(int shortBy) {\n        super("short by " + shortBy);\n        this.shortBy = shortBy;\n    }\n\n    int shortBy() {\n        return shortBy;\n    }\n}\n\nclass Wallet {\n    private int balance;\n\n    Wallet(int balance) {\n        this.balance = balance;\n    }\n\n    void spend(int amount) throws InsufficientFundsException {\n        if (amount > balance) {\n            throw new InsufficientFundsException(amount - balance);\n        }\n        balance -= amount;\n    }\n\n    int balance() {\n        return balance;\n    }\n}'
ex.method("write", "j2-l5.2-write-insufficient", "A wallet that refuses", ["o1"], ["J2.13"], ["IMPL"],
    "Write the **checked** exception `InsufficientFundsException` (extend `Exception`; its constructor takes how many pence the wallet is short by, and its message is `short by <n>`). Then make `Wallet.spend` declare it with `throws` and throw it when the amount is more than the balance, **without** changing the balance. The driver spends a list of amounts and shows each result.",
    [("run", [("start", "int"), ("amounts", "int[]")], "String")], {"run": wallet_run},
    [("run", [100, [30, 80]]), ("run", [50, [60]]), ("run", [10, []])],
    [("run", [100, [100, 1]]), ("run", [0, [5]]), ("run", [20, [5, 5, 5, 5, 5]]), ("run", [10, [11, 10]]), ("run", [1000, [400, 400, 400]])],
    'class Wallet {\n    private int balance;\n\n    Wallet(int balance) {\n        this.balance = balance;\n    }\n\n    void spend(int amount) {\n        balance -= amount;\n    }\n\n    int balance() {\n        return balance;\n    }\n}' + W_DRV,
    W_SOL + W_DRV,
    {"message-wrong": W_SOL.replace('"short by " + shortBy', '"short: " + shortBy') + W_DRV,
     "spends-then-checks": W_SOL.replace("        if (amount > balance) {\n            throw new InsufficientFundsException(amount - balance);\n        }\n        balance -= amount;", "        balance -= amount;\n        if (balance < 0) {\n            throw new InsufficientFundsException(-balance);\n        }") + W_DRV},
    ("Write the exception class first. Then in spend: check, throw, and only then change the balance.", "if (amount > balance) { throw new InsufficientFundsException(amount - balance); } balance -= amount;"),
    source_tests=[("the exception is checked", ["class InsufficientFundsException extends Exception"], None), ("spend declares it", ["throws InsufficientFundsException"], None)],
    starter_compiles=False, difficulty=3)
def port_msg(t):
    return f"port {int(t)}" if re.fullmatch(r"[0-9]+", t) else f"bad port: {t} <- NumberFormatException"
P_DRV = '\n\nString describePort(String text) {\n    try {\n        return "port " + readPort(text);\n    } catch (ConfigException e) {\n        return e.getMessage() + " <- " + e.getCause().getClass().getSimpleName();\n    }\n}'
P_SOL = 'class ConfigException extends RuntimeException {\n    ConfigException(String message, Throwable cause) {\n        super(message, cause);\n    }\n}\n\nint readPort(String text) {\n    try {\n        return Integer.parseInt(text);\n    } catch (NumberFormatException e) {\n        throw new ConfigException("bad port: " + text, e);\n    }\n}'
ex.method("write", "j2-l5.2-write-wrap", "Wrap and keep the cause", ["o2"], ["J2.13"], ["IMPL"],
    "Write `ConfigException` (unchecked: `extends RuntimeException`, with a constructor taking a message **and a cause**) and `readPort`, which parses a port number and, if the text isn't a number, throws a `ConfigException` with the message `bad port: <text>` **and the original exception as its cause**. The driver prints the message and the name of the cause's class.",
    [("describePort", [("text", "String")], "String")], {"describePort": port_msg},
    [("describePort", ["8080"]), ("describePort", ["abc"]), ("describePort", ["0"])],
    [("describePort", ["443"]), ("describePort", ["80x"]), ("describePort", [""]), ("describePort", ["12"]), ("describePort", ["port"]), ("describePort", ["65535"])],
    'int readPort(String text) {\n    return Integer.parseInt(text);\n}' + P_DRV,
    P_SOL + P_DRV,
    {"cause-dropped": P_SOL.replace('throw new ConfigException("bad port: " + text, e);', 'throw new ConfigException("bad port: " + text, null);') + P_DRV,
     "message-missing-text": P_SOL.replace('"bad port: " + text', '"bad port"') + P_DRV},
    ("The constructor should pass both arguments to super(message, cause). In readPort, catch NumberFormatException and pass it to the new exception.", "throw new ConfigException(\"bad port: \" + text, e);"),
    source_tests=[("ConfigException is unchecked", ["class ConfigException extends RuntimeException"], None)],
    starter_compiles=False, difficulty=3)
ex.explain("j2-l5.2-explain-checked", "Checked or unchecked?", ["o3"], ["J2.13"],
    "Explain the difference between a **checked** and an **unchecked** exception: what the compiler forces you to do in each case, and one example of each. Then say which you would choose for (a) a payment that was declined by the bank, and (b) a method called with a negative number where only positive numbers make sense, and why.",
    "A full answer says checked exceptions (Exception but not RuntimeException) must be caught or declared with throws, while unchecked (RuntimeException subclasses) need not; gives an example of each; chooses checked for the declined payment (the caller can recover) and unchecked for the negative argument (a programming mistake the caller cannot sensibly recover from).",
    {2: ("Says checked exceptions must be caught or declared and unchecked need not, gives an example of each, and chooses checked for the declined payment and unchecked for the bad argument, with reasons about recovery.",
         ["Checked exceptions, like IOException or my own that extend Exception, must be caught or declared with throws. Unchecked ones, like IllegalArgumentException, extend RuntimeException and the compiler doesn't force anything. A declined payment I'd make checked, because the caller can recover by trying another card. A negative argument I'd make unchecked, because it's a programming mistake the caller can't do anything about.",
          "Checked: the compiler forces you to catch or declare (e.g. a custom exception extending Exception). Unchecked: it doesn't (e.g. NullPointerException). (a) checked, since the caller can handle it. (b) unchecked, since it signals a bug."]),
     1: ("Explains the compiler difference but doesn't choose correctly or doesn't give reasons.",
         ["Checked ones must be caught and unchecked ones don't need to be.", "Both should be unchecked."]),
     0: ("Incorrect, for example reverses the two, or says unchecked exceptions can't be thrown.",
         ["Unchecked ones must be caught.", "Checked means it was checked by a person."])})
reg({"j2-l5.2": ("Custom and checked exceptions", ["J2.13"])},
    {"MC57": (["J2.13"], "Platform", "When wrapping an exception, the original can be dropped"),
     "MC58": (["J2.13"], "Platform", "Every custom exception should be a checked exception")})

# ====================================================================== 2.5.3
Lesson("j2-l5.3", "Cleanup and where to catch", ["J2.14"], [
    ("o1", "Use try-with-resources so a resource is always closed, and predict the order of opening and closing"),
    ("o2", "Decide where in a program an exception should be caught, and catch it there"),
    ("o3", "Explain why errors should not be swallowed or logged and thrown away"),
], ["j2-l5.2"], 45, ["I39", "I40", "R16"], r'''
## Before you start

You should know how to catch and throw exceptions ([Catching exceptions](j2-l5.1), [Custom and checked exceptions](j2-l5.2)).

**Quick check.** What does a `finally` block do?

<details><summary>Show the answer</summary>

It runs as the `try` is left, whether that happens normally, by `return` or because of an exception.

</details>

## Explanation

### Resources must be released

Some objects hold something that has to be given back: a file, a network connection, a database connection. If you forget, they leak, and a long-running program eventually runs out. The old way is `try` / `finally`:

```java
Connection c = open();
try {
    use(c);
} finally {
    c.close();
}
```

It works, but with two resources, and `close` itself able to throw, the code gets tangled quickly.

### try-with-resources

A class that implements the `AutoCloseable` interface has a `close()` method. Declare the resource in the **header** of the `try`, and Java calls `close()` for you when the block exits, however it exits `[I39]`:

```java
try (Gate a = new Gate(log, "A"); Gate b = new Gate(log, "B")) {
    log.add("work");
}
```

Writing your own is just implementing the interface:

```java
class Gate implements AutoCloseable {
    private final List<String> log;
    private final String name;

    Gate(List<String> log, String name) {
        this.log = log;
        this.name = name;
        log.add("open " + name);
    }

    @Override
    public void close() {
        log.add("close " + name);
    }
}
```

The log for the `try` above reads: `open A`, `open B`, `work`, `close B`, `close A`. Resources close in the **reverse** of the order they were opened, like unstacking plates, and they close **even if the block throws**.

```java runnable
class Gate implements AutoCloseable {
    private final String name;

    Gate(String name) {
        this.name = name;
        IO.println("open " + name);
    }

    @Override
    public void close() {
        IO.println("close " + name);
    }
}

void main() {
    try (Gate a = new Gate("A"); Gate b = new Gate("B")) {
        IO.println("work");
        throw new IllegalStateException("boom");
    } catch (IllegalStateException e) {
        IO.println("caught " + e.getMessage());
    }
}
```

It prints `open A`, `open B`, `work`, `close B`, `close A`, `caught boom`: the resources were closed **before** the `catch` ran. Prefer try-with-resources over `finally` whenever the thing is `AutoCloseable`. You'll use it for files in lesson 3.4.1.

### Where should an exception be caught?

The throwing code is often not the right place to handle the problem. Think of the call chain as layers: a **low-level** method parses a number, a **mid-level** method totals a list, and a **top-level** method (the one that talks to the user) prints a report. Each layer knows different things.

**Catch where you can do something meaningful about it.** Meaningful means:

- **retry** the operation;
- **report** a helpful message to the person (only the top level knows how to talk to them);
- **translate** it into a higher-level exception (and keep the cause);
- **clean up and continue** with the next item.

Guidelines:

- **Don't catch low down just to print and carry on.** A low-level method that prints an error and returns `0` hides the failure from everyone above it.
- **Don't catch so high that you can't say anything useful,** like a single `catch (Exception e)` in `main` printing "something went wrong".
- **Let exceptions propagate until someone can handle them.** Not catching is a legitimate decision, and with checked exceptions it is made visible by `throws`.

A good place for the final catch is the **boundary** with the outside world: the top of a command, a request handler, a button click. There you turn a failure into a message the person can use.

### Log-and-rethrow, and swallowing

Two habits to avoid:

- **Swallowing:** catching and doing nothing (or returning a default silently), so the error disappears.
- **Log and rethrow at every level:** each layer catches, writes a log line, and rethrows. The same failure then appears five times in the logs and obscures the real order of events. Log once, where it's handled.

## Worked examples

### Example 1: closing in the right order

*Task: predict the log from a `try` with resources `A` then `B`, when the body throws.*

**Step 1 — Opening order:** `open A`, `open B`.

**Step 2 — The body runs** until it throws.

**Step 3 — Closing is reverse:** `close B`, `close A`, **before** any `catch`.

**Step 4 — Then the catch runs.** Full log: `open A, open B, work, close B, close A, caught`.

### Example 2: choosing where to catch

*Task: `total(items)` parses text and can throw `NumberFormatException`. `report(items)` is what the user sees. Where do you catch it?*

**Step 1 — Can `total` do anything useful about a bad entry?** No: it doesn't know what the person typed or how to tell them.

**Step 2 — Can `report` (the boundary)?** Yes: it can print "could not read the numbers".

**Step 3 — Catch in `report`,** and let `total` stay simple:

```java
String report(String[] items) {
    try {
        return "total=" + total(items);
    } catch (NumberFormatException e) {
        return "error: could not read the numbers";
    }
}
```

## Where this is used

- **Files, sockets and databases:** every one of them is `AutoCloseable` and used in try-with-resources.
- **Web applications** catch exceptions at one boundary and turn them into error pages or responses.
- **Command-line tools** catch at the top of `main` and print a clean message and exit code.

## Common mistakes

:::mistake{id=MC59}
**Opening a resource without closing it** (or closing it only on the success path). If an exception occurs first, it leaks. Use try-with-resources.
:::

:::mistake{id=MC60}
**Catching low down, printing, and returning a default.** Callers can't tell something went wrong, so they carry on with bad data.
:::

:::mistake{id=MC61}
**Expecting try-with-resources to close in the order written.** It closes in reverse order.
:::

## Practice

::exercise{id=j2-l5.3-write-gate}

::exercise{id=j2-l5.3-write-report}

::exercise{id=j2-l5.3-explain-where}

## Further reading

- **The `java.lang.AutoCloseable` documentation** `[I39]` describes how `close()` is called on leaving a try-with-resources block.
- **The `java.lang.Throwable` documentation** `[I40]`.
- **McCauley et al. (2008)** `[R16]`: handling an error where it can be diagnosed is easier than diagnosing a swallowed one.

## How you'll be assessed

- The **write** exercises check that you can write an `AutoCloseable` class and use it, and that you can catch an exception at the right layer (*implementation*).
- The **explain** exercise checks that you can reason about where to catch and why not to swallow (*explanation*).
''' + FOOT)

ex = Exercises("j2-l5.3")
def gate_run(a, b, fail):
    log = [f"open {a}", f"open {b}", "work", f"close {b}", f"close {a}"]
    if fail: log.append("caught")
    return ",".join(log)
G_DRV = '\n\nString run(String first, String second, boolean fail) {\n    List<String> log = new ArrayList<>();\n    try (Gate a = new Gate(log, first); Gate b = new Gate(log, second)) {\n        log.add("work");\n        if (fail) {\n            throw new IllegalStateException("boom");\n        }\n    } catch (IllegalStateException e) {\n        log.add("caught");\n    }\n    return String.join(",", log);\n}'
G_SOL = 'class Gate implements AutoCloseable {\n    private final List<String> log;\n    private final String name;\n\n    Gate(List<String> log, String name) {\n        this.log = log;\n        this.name = name;\n        log.add("open " + name);\n    }\n\n    @Override\n    public void close() {\n        log.add("close " + name);\n    }\n}'
ex.method("write", "j2-l5.3-write-gate", "A resource that closes itself", ["o1"], ["J2.14"], ["IMPL"],
    "Write `Gate`, a class that implements `AutoCloseable`. Its constructor adds `open <name>` to the log it is given, and its `close()` adds `close <name>`. The driver opens two gates in a try-with-resources, does some work (sometimes throwing), and returns the log. You don't need to write any `close` calls yourself: the `try` does that.",
    [("run", [("first", "String"), ("second", "String"), ("fail", "boolean")], "String")], {"run": gate_run},
    [("run", ["A", "B", False]), ("run", ["A", "B", True]), ("run", ["x", "y", False])],
    [("run", ["door", "lock", True]), ("run", ["1", "2", False]), ("run", ["north", "south", True]), ("run", ["a", "a", False]), ("run", ["in", "out", True])],
    '// Write the class Gate here.\n\nclass Gate {\n    Gate(List<String> log, String name) {\n    }\n}' + G_DRV,
    G_SOL + G_DRV,
    {"close-not-logged-in-order": G_SOL.replace('log.add("close " + name);', 'log.add("closed " + name);') + G_DRV,
     "open-not-logged": G_SOL.replace('        log.add("open " + name);\n', '') + G_DRV},
    ("Implement AutoCloseable: log \"open \" + name in the constructor, and log \"close \" + name in a public void close() method.", "class Gate implements AutoCloseable { ... @Override public void close() { log.add(\"close \" + name); } }"),
    source_tests=[("Gate implements AutoCloseable", ["Gate implements AutoCloseable"], None)],
    starter_compiles=False, difficulty=3)
def report_fn(items):
    if all(re.fullmatch(r"[+-]?[0-9]+", s.strip()) for s in items):
        return f"total={sum(int(s.strip()) for s in items)}"
    return "error: could not read the numbers"
R_TOTAL = 'int total(String[] items) {\n    int sum = 0;\n    for (String item : items) {\n        sum += Integer.parseInt(item.trim());\n    }\n    return sum;\n}\n\n'
ex.method("write", "j2-l5.3-write-report", "Catch at the boundary", ["o2"], ["J2.14"], ["IMPL"],
    "`total` adds up text numbers and throws a `NumberFormatException` if one isn't a number. It shouldn't catch anything: it can't say anything useful. `report` is the **boundary** that talks to the person. Write it so that it returns `total=<n>` normally, and `error: could not read the numbers` if any entry is bad. Leave `total` alone.",
    [("report", [("items", "String[]")], "String")], {"report": report_fn},
    [("report", [["1", "2", "3"]]), ("report", [["1", "x"]]), ("report", [[]])],
    [("report", [["10"]]), ("report", [[" 5 ", "6"]]), ("report", [["a"]]), ("report", [["1", "2", "", "4"]]), ("report", [["-3", "3"]]), ("report", [["7", "7.5"]])],
    R_TOTAL + 'String report(String[] items) {\n    return "total=" + total(items);\n}',
    R_TOTAL + 'String report(String[] items) {\n    try {\n        return "total=" + total(items);\n    } catch (NumberFormatException e) {\n        return "error: could not read the numbers";\n    }\n}',
    {"returns-zero-total": R_TOTAL + 'String report(String[] items) {\n    try {\n        return "total=" + total(items);\n    } catch (NumberFormatException e) {\n        return "total=0";\n    }\n}',
     "wrong-exception": R_TOTAL + 'String report(String[] items) {\n    try {\n        return "total=" + total(items);\n    } catch (ArithmeticException e) {\n        return "error: could not read the numbers";\n    }\n}'},
    ("Put the call to total inside try in report, and catch the exception that parseInt throws.", "try { return \"total=\" + total(items); } catch (NumberFormatException e) { return \"error: could not read the numbers\"; }"),
    source_tests=[("catches the specific exception", ["catch (NumberFormatException"], ["catch (Exception"])],
    difficulty=2)
ex.explain("j2-l5.3-explain-where", "Who should catch it?", ["o2", "o3"], ["J2.14"],
    "In a banking program, `transfer(from, to, amount)` calls `withdraw`, which throws `InsufficientFundsException` when the account is short. The user pressed a **Transfer** button in the app. (a) Which layer should catch the exception, and what should it do? (b) Why shouldn't `withdraw` catch it, print a message and return? (c) Give one reason not to catch `Exception`, log it and carry on at every layer.",
    "A full answer says the layer that talks to the user (the code behind the Transfer button, the boundary) should catch it and show a clear message such as that there are insufficient funds; withdraw shouldn't because it can't talk to the user and would hide the failure so transfer would carry on as if it worked; and catching broadly and logging at every layer duplicates the log entries, hides which failure was real, or lets the program continue in a wrong state.",
    {2: ("Says the boundary layer behind the Transfer button should catch it and tell the user; withdraw shouldn't because it can't report to the user and would hide the failure from transfer; and gives a reason such as duplicate logs or carrying on in a wrong state.",
         ["The code behind the Transfer button should catch it and show the user a message like \"not enough money\". withdraw shouldn't catch it and print, because then transfer wouldn't know the withdrawal failed and might still add the money to the other account. Catching and logging at every layer fills the logs with duplicates and can let the program carry on in a wrong state.",
          "The top layer, where the user clicks Transfer, should catch it and report the shortfall. withdraw can't tell the user anything useful and swallowing it would make transfer behave as if it worked. Logging and continuing at every layer duplicates the log and hides the real failure."]),
     1: ("Gets the right layer or the problem with catching in withdraw, but not both, or gives no reason for part (c).",
         ["The button code should catch it.", "withdraw shouldn't catch it."]),
     0: ("Incorrect, for example says withdraw should catch and ignore it, or that the whole program should catch Exception once at the very start.",
         ["withdraw should catch it and carry on.", "Catch everything in main."])})
reg({"j2-l5.3": ("Cleanup and where to catch", ["J2.14"])},
    {"MC59": (["J2.14"], "Platform", "A resource only needs closing on the success path"),
     "MC60": (["J2.14"], "Platform", "Catching low down, printing and returning a default is good error handling"),
     "MC61": (["J2.14"], "Platform", "try-with-resources closes resources in the order they are written")})
print("2.4 and 2.5 written")
