from build import *

Lesson("j1-l5.2", "Parameters and return values", ["J1.08"], [
    ("o1", "Pass arguments to parameters and say what each parameter holds inside the method"),
    ("o2", "Explain that changing a parameter inside a method doesn't change the caller's variable"),
    ("o3", "Tell printing a value apart from returning it, and use returned values in expressions"),
    ("o4", "Call one method from another to build up a result"),
], ["j1-l5.1"], 35, ["R8", "R5"], r'''
## Before you start

You should be able to define and call a method with parameters ([Defining and calling methods](j1-l5.1)).

**Quick check.** What does `area(4, 6)` give, if `area` returns `width * height`?

<details><summary>Show the answer</summary>

`24`. The first argument goes to the first parameter (`width` = 4), the second to the second (`height` = 6).

</details>

## Explanation

### Parameters are fresh variables

When you call a method, each **parameter** becomes a new variable, set to a **copy** of the matching argument's value:

```java runnable
int addTax(int price) {
    price = price + price / 5;   // changes the parameter
    return price;
}

void main() {
    int cost = 100;
    int withTax = addTax(cost);
    IO.println(cost);
    IO.println(withTax);
}
```

This prints `100` then `120`. The method changed its own `price`, but `cost` in `main` stayed 100, because `price` was only a **copy** of `cost`'s value. This is the same as `int b = a;` ([Variables and state](j1-l2.2)): the copy happens once, and the two variables aren't linked.

The only way a method gives something back to its caller is by `return`.

### Return versus print

| | `return value;` | `IO.println(value);` |
|---|---|---|
| What it does | Hands the value back to the caller | Shows text on screen |
| Can the caller use it? | Yes: store it, add it, pass it on | No |
| Ends the method? | Yes | No |

A method that calculates should **return** its answer; whoever called it decides what to do next (print it, add to it, compare it). A method whose job is output prints, and is `void`.

`return` ends the method **immediately**, so anything after it never runs:

```java
int pick(boolean first, int a, int b) {
    if (first) {
        return a;     // method ends here if first is true
    }
    return b;         // only reached when first is false
}
```

### Calling one method from another

Methods can call each other, which lets you build big answers from small steps:

```java runnable
int square(int n) {
    return n * n;
}

int sumOfSquares(int a, int b) {
    return square(a) + square(b);
}

void main() {
    IO.println(sumOfSquares(3, 4));
}
```

This prints `25`. To read code like this, work inside-out: `sumOfSquares(3, 4)` calls `square(3)` (9) and `square(4)` (16), then adds them.

### Scope: variables belong to their method

A variable declared inside a method exists **only inside that method**. Two methods can each have their own variable called `total` without any clash, and one method can't see another's variables. If a method needs a value from outside, it has to be passed in as an argument.

## Worked examples

### Example 1: percentage off

*Task: a method `discounted(price, percentOff)` returns the price after the discount, in pence. `discounted(2000, 25)` is 1500.*

**Step 1 — Inputs and output.** Two whole numbers in; a whole number out.

**Step 2 — Work an example by hand.** 25% of 2000 is 500; 2000 − 500 = 1500.

**Step 3 — Write the steps as code,** keeping to integer arithmetic. (`price * percentOff / 100` multiplies first, so it doesn't lose pence to rounding.)

```java runnable
int discounted(int price, int percentOff) {
    int saving = price * percentOff / 100;
    return price - saving;
}

void main() {
    IO.println(discounted(2000, 25));
}
```

### Example 2: building a bigger method from small ones

*Task: the cost of a taxi is a fixed fee plus a per-mile price. Write `fare(miles)`, using two small helper methods.*

**Step 1 — Name the pieces.** The distance part and the fixed part.

**Step 2 — One method per piece,** then combine.

```java runnable
int distanceCost(int miles) {
    return miles * 150;
}

int bookingFee() {
    return 300;
}

int fare(int miles) {
    return bookingFee() + distanceCost(miles);
}

void main() {
    IO.println(fare(4));
}
```

This prints `900`. Splitting it up means each method is easy to check on its own.

## Predict, then run

::exercise{id=j1-l5.2-predict-copies}

## Where this is used

- **Libraries**: the methods you call every day (`Math.max`, `parseInt`) take arguments and return results, and never touch your variables.
- **Testing**: because a method's result depends only on its arguments, it can be tested with fixed inputs, as in this course.
- **Reading code**: knowing that arguments are copies lets you read a call without worrying about your own variables changing.

## Common mistakes

:::mistake{id=MC13}
**Expecting a method to change the caller's variable.** `addTax(cost)` can't change `cost`. If you want the new value, return it and store it: `cost = addTax(cost);`.
:::

:::mistake{id=MC07}
**Printing when you should return.** `IO.println(a + b)` inside an `int` method doesn't give the caller a value. Use `return a + b;`.
:::

### Code after `return`

Statements after a `return` that always runs can never execute; Java reports them as an error.

### Using another method's variables

`total` declared in `main` isn't visible in `sumOfSquares`. Pass it in as a parameter.

## Practice

::exercise{id=j1-l5.2-write-discount}

::exercise{id=j1-l5.2-debug-copy}

::exercise{id=j1-l5.2-modify-fare}

::exercise{id=j1-l5.2-explain-copy}

## Further reading

- **"Notional machines and introductory programming education"** (Sorva, 2013) `[R8]`: why learners need a mental model of how code runs, including how arguments are passed. The copy rule above is part of that model.

## How you'll be assessed

- The **predict** exercise checks that you understand copies and returns.
- The **write** and **modify** exercises check that you can write methods and build on small ones (*implementation, modification*).
- The **debug** exercise checks that you can fix a method that doesn't return its result (*debugging*).
- The **explain** exercise checks that you can say why the caller's variable doesn't change.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j1-l5.2")
ex.predict("j1-l5.2-predict-copies", "Copies and results", ["o1", "o2", "o3"], ["J1.08"],
    "Predict exactly what this program prints. Remember that a parameter is a copy.",
    '''
    int bump(int n) {
        n = n + 10;
        return n;
    }

    void main() {
        int score = 5;
        int other = bump(score);
        IO.println(score);
        IO.println(other);
        score = bump(score);
        IO.println(score);
        IO.println(bump(bump(0)));
    }
    ''', '''
    5
    15
    15
    20
    ''', ("The call bump(score) doesn't change score by itself. Only an assignment does.",
          "bump(5) returns 15 but score stays 5. Then score = bump(score) stores 15. bump(bump(0)) is bump(10), which is 20."),
    misconceptions=["MC13"], difficulty=2)

def disc(price, pct): return price - price * pct // 100
ex.method("write", "j1-l5.2-write-discount", "Sale price", ["o1", "o3"], ["J1.08"], ["IMPL"],
    "Write a method called `discounted` that is given a `price` in pence and a `percentOff` (both `int`s, in that order). It returns the price after the discount, in pence. Work out the saving as `price * percentOff / 100` (whole pence, with integer division). For example, `discounted(2000, 25)` is 1500.",
    [("discounted", [("price", "int"), ("percentOff", "int")], "int")], {"discounted": disc},
    [(None, [2000, 25]), (None, [999, 10]), (None, [500, 0])],
    [(None, [100, 100], "everything off"), (None, [1, 50], "tiny price"), (None, [12345, 33], "awkward numbers"), (None, [0, 20], "free"), (None, [800, 75], "three quarters")],
    '// Write the discounted method here.\n\nvoid main() {\n    IO.println(discounted(2000, 25)); // should print 1500\n}\n',
    'int discounted(int price, int percentOff) {\n    int saving = price * percentOff / 100;\n    return price - saving;\n}\n\nvoid main() {\n    IO.println(discounted(2000, 25)); // should print 1500\n}\n',
    {"returns-saving": 'int discounted(int price, int percentOff) {\n    return price * percentOff / 100;\n}\n\nvoid main() {\n}\n',
     "divides-first": 'int discounted(int price, int percentOff) {\n    return price - price / 100 * percentOff;\n}\n\nvoid main() {\n}\n'},
    ("First work out the saving, then take it away from the price.", "int saving = price * percentOff / 100; return price - saving;"),
    starter_compiles=False, group="build-method")

def tip(bill, pct): return bill + bill * pct // 100
ex.method("write", "j1-l5.2-retrieve-tip", "Bill with tip", ["o1", "o3"], ["J1.08"], ["IMPL"],
    "Write a method called `totalWithTip` that is given a `bill` in pence and a `tipPercent` (both `int`s, in that order). It returns the bill plus the tip, in pence, working out the tip as `bill * tipPercent / 100`. For example, `totalWithTip(2000, 10)` is 2200.",
    [("totalWithTip", [("bill", "int"), ("tipPercent", "int")], "int")], {"totalWithTip": tip},
    [(None, [2000, 10]), (None, [999, 15]), (None, [500, 0])],
    [(None, [100, 100], "tip equals bill"), (None, [1, 50], "tiny bill"), (None, [12345, 12], "awkward numbers"), (None, [0, 20], "no bill"), (None, [800, 25], "quarter")],
    '// Write the totalWithTip method here.\n\nvoid main() {\n    IO.println(totalWithTip(2000, 10)); // should print 2200\n}\n',
    'int totalWithTip(int bill, int tipPercent) {\n    int tip = bill * tipPercent / 100;\n    return bill + tip;\n}\n\nvoid main() {\n    IO.println(totalWithTip(2000, 10)); // should print 2200\n}\n',
    {"returns-tip": 'int totalWithTip(int bill, int tipPercent) {\n    return bill * tipPercent / 100;\n}\n\nvoid main() {\n}\n'},
    ("The same shape as a discount, but adding instead of taking away.", "int tip = bill * tipPercent / 100; return bill + tip;"),
    starter_compiles=False, role="retrieval", group="build-method")

def vat(net, rate): return net + net * rate // 100
ex.method("write", "j1-l5.2-retrieve-vat", "Price with tax", ["o1", "o3"], ["J1.08"], ["IMPL"],
    "Write a method called `withTax` that is given a `net` price in pence and a tax `rate` as a percentage (both `int`s, in that order). It returns the net price plus the tax, in pence, working out the tax as `net * rate / 100`. For example, `withTax(1000, 20)` is 1200.",
    [("withTax", [("net", "int"), ("rate", "int")], "int")], {"withTax": vat},
    [(None, [1000, 20]), (None, [999, 5]), (None, [500, 0])],
    [(None, [100, 100], "doubles"), (None, [1, 20], "tiny"), (None, [12345, 17], "awkward numbers"), (None, [0, 20], "free"), (None, [800, 10], "ten percent")],
    '// Write the withTax method here.\n\nvoid main() {\n    IO.println(withTax(1000, 20)); // should print 1200\n}\n',
    'int withTax(int net, int rate) {\n    int tax = net * rate / 100;\n    return net + tax;\n}\n\nvoid main() {\n    IO.println(withTax(1000, 20)); // should print 1200\n}\n',
    {"returns-tax": 'int withTax(int net, int rate) {\n    return net * rate / 100;\n}\n\nvoid main() {\n}\n'},
    ("Work out the tax, then add it to the net price.", "int tax = net * rate / 100; return net + tax;"),
    starter_compiles=False, role="retrieval", group="build-method")

ex.method("debug", "j1-l5.2-debug-copy", "The price that never changes", ["o2"], ["J1.08"], ["DEBUG"],
    "`applyDiscount` is supposed to take 10% off a price, so `applyDiscount(2000)` is 1800. It returns 2000 every time. Find and fix the bug (the parameter is a copy, so look at what the method hands back).",
    [("applyDiscount", [("price", "int")], "int")], {"applyDiscount": lambda p: p - p // 10},
    [(None, [2000]), (None, [500]), (None, [0])],
    [(None, [100], "hundred"), (None, [99], "odd"), (None, [12345], "awkward"), (None, [10], "ten"), (None, [1], "one")],
    'int applyDiscount(int price) {\n    int reduced = price - price / 10;\n    price = reduced;\n    return price;\n}\n\nvoid main() {\n    IO.println(applyDiscount(2000)); // should print 1800\n}\n'.replace("    price = reduced;\n    return price;", "    return price;"),
    'int applyDiscount(int price) {\n    int reduced = price - price / 10;\n    return reduced;\n}\n\nvoid main() {\n    IO.println(applyDiscount(2000)); // should print 1800\n}\n',
    {"always-1800": 'int applyDiscount(int price) {\n    return 1800;\n}\n\nvoid main() {\n}\n'},
    ("Which value does the method return: the new price, or the old one?", "Return the reduced price: return reduced;"),
    misconceptions=["MC13"])

def fare2(m): return 300 + m * 150 + (200 if m > 10 else 0)
ex.method("modify", "j1-l5.2-modify-fare", "Long-distance surcharge", ["o4"], ["J1.08"], ["MOD"],
    "Taxis now add a 200 pence surcharge for journeys over 10 miles. Change the program so `fare` includes it, **without** changing `distanceCost` or `bookingFee`. A 10-mile journey has no surcharge.",
    [("fare", [("miles", "int")], "int")], {"fare": fare2},
    [(None, [4]), (None, [10]), (None, [12])],
    [(None, [0], "zero miles"), (None, [11], "just over"), (None, [1], "one mile"), (None, [50], "far"), (None, [9], "just under")],
    'int distanceCost(int miles) {\n    return miles * 150;\n}\n\nint bookingFee() {\n    return 300;\n}\n\nint fare(int miles) {\n    return bookingFee() + distanceCost(miles);\n}\n\nvoid main() {\n    IO.println(fare(4));\n}\n',
    'int distanceCost(int miles) {\n    return miles * 150;\n}\n\nint bookingFee() {\n    return 300;\n}\n\nint fare(int miles) {\n    int total = bookingFee() + distanceCost(miles);\n    if (miles > 10) {\n        total += 200;\n    }\n    return total;\n}\n\nvoid main() {\n    IO.println(fare(4));\n}\n',
    {"at-ten": 'int distanceCost(int miles) {\n    return miles * 150;\n}\n\nint bookingFee() {\n    return 300;\n}\n\nint fare(int miles) {\n    int total = bookingFee() + distanceCost(miles);\n    if (miles >= 10) {\n        total += 200;\n    }\n    return total;\n}\n\nvoid main() {\n}\n'},
    ("Only fare needs to change. Add the surcharge when miles is more than 10.", "Store the total in a variable, add 200 if miles > 10, then return it."))

ex.explain("j1-l5.2-explain-copy", "Why didn't cost change?", ["o2"], ["J1.08"],
    "In the code below, `cost` is still 100 after the call, even though `addTax` changes `price`. Explain why, and how you'd get the new value into `cost`.\n\n```java\nint cost = 100;\naddTax(cost);\n```",
    "A full answer says the parameter price is a copy of cost's value, so changing price doesn't affect cost; the method has to return the new value and the caller stores it, as in cost = addTax(cost).",
    {2: ("Says the parameter is a separate copy of the value so changes to it don't affect cost, and that the new value must be returned and stored (cost = addTax(cost)).",
         ["price is a copy of cost's value, not the variable itself, so changing price only changes the copy. To update cost, addTax has to return the new value and you write cost = addTax(cost);.",
          "Arguments are passed by copying the value. cost and price are separate variables. You need to return the result and assign it back."]),
     1: ("Says the method has a copy, or says to return the value, but not both.",
         ["Because price is a copy.", "You should return the value from the method."]),
     0: ("Incorrect, for example says Java forgot to update it, or that cost and price are the same variable.",
         ["cost should have changed, it's a bug in Java.", "price and cost are the same thing so it should change."])},
    misconceptions=["MC13"])
print("5.2 written")
