import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-4"
from build import *
import outline
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'
def lv(name): return {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3}[name]

# ====================================================================== 4.3.1
Lesson("j4-l3.1", "Your first unit tests", ["J4.05"], [
    ("o1", "Write checks that pin down a rule with typical values and with both sides of every boundary"),
    ("o2", "Read a JUnit test and its failure output, and say what a passing suite does and does not prove"),
    ("o3", "Judge a set of tests by whether it catches deliberately broken versions of the code"),
], ["j4-l2.2", "j3-l5.3"], 55, ["I68", "R16"], r'''
## Before you start

You have written small `check` helpers and read tests as specifications ([Writing your own checks](j1-l7.3)), and you've seen a JUnit failure in Maven output ([Maven: lifecycle, dependencies and conflicts](j4-l2.2)).

**Quick check.** Where should the **expected** value in a check come from: running the code, or the requirement?

<details><summary>Show the answer</summary>

The requirement. An expected value copied from what the code returns can never fail.

</details>

## Explanation

### What a unit test is

A **unit test** is a small piece of code that runs a small piece of your program (a *unit*: a method or a class) with chosen inputs and checks the result. Run them all after every change, and you learn within seconds when something you didn't mean to break has broken. That safety net is what makes it possible to change code confidently, which the next lessons rely on.

### The shape of a test

A JUnit test from the Maven project in the last module:

```java
class PriceTest {

    @Test
    void addsTwentyPercent() {
        assertEquals(1200, Price.withTax(1000));
    }

    @Test
    void rejectsNegativePrices() {
        assertThrows(IllegalArgumentException.class, () -> Price.withTax(-1));
    }
}
```

- **`@Test`** marks a method that JUnit should run. Test methods can't be `private` `[I68]`.
- **`assertEquals(expected, actual)`** compares two values, with the **expected** one first and an optional failure message last `[I68]`. If they differ, it throws and the test fails.
- **`assertThrows`** passes only if the code throws the named exception.
- A test **passes** if it finishes without throwing, **fails** if an assertion throws, and has an **error** if something unexpected throws.

Each test has three parts, often called **arrange, act, assert**: set up the inputs, call the code, check the result. Keep each test about **one thing**, and give it a name that says what is being checked (`rejectsNegativePrices`, not `test3`), so a failure names its own problem.

JUnit isn't available inside this platform's runner, so in this lesson's exercises your tests are plain methods that return `true` when every check passes. The skills (choosing inputs, working out expected values, covering boundaries) are the same.

### Choosing what to test

Take this rule: *"An order of 10,000 pence or more gets 10% off. Members get a further 2% off, on any order. The total discount is the price times those percentages added up, divided by 100 and rounded down."* What do you check?

1. **A typical value from each case:** a big order, a small order, a member, a non-member.
2. **Both sides of every boundary.** The rule changes at 10,000, so test **9,999 and 10,000**. Most bugs live on a boundary, where a `>` should have been `>=`.
3. **Rounding.** A price where the discount isn't a whole number of pence (101 pence for a member is 2.02 pence off) shows whether you round down.
4. **Combinations:** a member *and* a big order, which is where interactions hide.

And work out each expected value **by hand from the rule**: 10,000 non-member: 10% of 10,000 is 1,000, so **9,000**. Never copy a number from the code's output.

### Do your tests catch bugs? The mutation idea

Passing tests prove only that the cases you chose work; they don't prove the code is right (as in lesson 1.7.3). A better question is: **if the code were wrong, would my tests notice?** You can test your tests: make a copy of the code with a small deliberate bug, a **mutant** (change `>=` to `>`, `10` to `11`, round up instead of down), and run your tests against it. A good suite **fails** on every mutant. If a mutant **survives** (the tests still pass), you've found a hole: a case you haven't checked.

The exercises in this module work that way: you write a check method, and it's run against the correct code (which must pass) and against several broken versions (each of which must fail). Tools exist that do this automatically on real projects.

## Worked examples

### Example 1: finding the case that kills a mutant

*Task: a mutant changes `pence >= 10000` to `pence > 10000`. Which check catches it?*

**Step 1 — Where do the two versions differ?** Only at exactly 10,000: the correct code gives 10% off, the mutant gives none.

**Step 2 — So check that input:** 10,000 pence, non-member. Expected from the rule: 1,000 off, so **9,000**.

**Step 3 — Result:** the correct code returns 9,000 (pass); the mutant returns 10,000 (fail). The mutant is killed. A test at 20,000 would not have noticed.

### Example 2: reading a failure

*Task: `expected: <1200> but was: <1250>` in `PriceTest.addsTwentyPercent`. What do you do first?*

**Step 1 — Which is wrong, the test or the code?** Go back to the requirement: should the tax be 20% or 25%?

**Step 2 — If the rule is 20%:** the code is wrong (it returned 1250). Fix the code.

**Step 3 — If the rule changed to 25%:** the test is out of date. Update the expected value to 1250, and note the rule change in the commit message.

## Where this is used

- **Every professional codebase** has automated tests, and a pull request without them is usually sent back.
- **Continuous integration** runs the whole suite on every push.
- **Legacy code** becomes safe to change only after tests are added around it.

## Common mistakes

:::mistake{id=MC142}
**Computing the expected value by running the code.** The test then restates what the code does, including its bugs, and can never fail.
:::

:::mistake{id=MC143}
**Testing only typical values.** Bugs cluster at boundaries and special cases. Test both sides of each boundary.
:::

:::mistake{id=MC144}
**Believing a passing suite means the code is correct.** It means the checked cases work. Ask whether the tests would catch a deliberately broken version.
:::

## Practice

::exercise{id=j4-l3.1-write-discount-tests}

::exercise{id=j4-l3.1-write-age-tests}

::exercise{id=j4-l3.1-explain-junit}

## Further reading

- **JUnit User Guide, "Writing Tests"** `[I68]` documents `@Test`, `assertEquals` and the other assertions.
- **McCauley et al. (2008)** `[R16]` on debugging: a failing test is a reproducible case, the first step of any fix.

## How you'll be assessed

- The **write** exercises check that your tests pass the correct code and catch every broken version (*implementation*).
- The **explain** exercise checks that you can read a JUnit failure and say what a passing suite does and doesn't prove (*explanation*).
''' + FOOT)

ex = Exercises("j4-l3.1")
DISC_IFACE = 'interface Discount {\n    int apply(int pence, boolean member);\n}\n\n'
DISC_CORRECT = 'class Correct implements Discount {\n    public int apply(int pence, boolean member) {\n        int percent = (pence >= 10000 ? 10 : 0) + (member ? 2 : 0);\n        return pence - pence * percent / 100;\n    }\n}\n\n'
def mutant(name, body):
    return f'class {name} implements Discount {{\n    public int apply(int pence, boolean member) {{\n{body}\n    }}\n}}\n\n'
DISC_MUTANTS = (
    mutant("Mutant1", '        int percent = (pence > 10000 ? 10 : 0) + (member ? 2 : 0);\n        return pence - pence * percent / 100;') +
    mutant("Mutant2", '        int percent = pence >= 10000 ? 10 + (member ? 2 : 0) : 0;\n        return pence - pence * percent / 100;') +
    mutant("Mutant3", '        int percent = (pence >= 10000 ? 10 : 0) + (member ? 3 : 0);\n        return pence - pence * percent / 100;') +
    mutant("Mutant4", '        int percent = (pence >= 10000 ? 11 : 0) + (member ? 2 : 0);\n        return pence - pence * percent / 100;') +
    mutant("Mutant5", '        int percent = (pence >= 10000 ? 10 : 0) + (member ? 2 : 0);\n        return pence - (pence * percent + 99) / 100;') +
    mutant("Mutant6", '        int percent = pence >= 10000 ? 10 : 0;\n        return pence - pence * percent / 100;'))
DISC_HELP = '// check(d, pence, member, expected) is true when the discount code gives the expected price.\nboolean check(Discount d, int pence, boolean member, int expected) {\n    return d.apply(pence, member) == expected;\n}\n\n'
DISC_DRV = 'String run(String which) {\n    Discount d = switch (which) {\n        case "mutant1" -> new Mutant1();\n        case "mutant2" -> new Mutant2();\n        case "mutant3" -> new Mutant3();\n        case "mutant4" -> new Mutant4();\n        case "mutant5" -> new Mutant5();\n        case "mutant6" -> new Mutant6();\n        default -> new Correct();\n    };\n    return allPass(d) ? "pass" : "fail";\n}'
DISC_RULE = "The rule: an order of **10,000 pence or more** gets 10% off; **members** get a further 2% off, on any order. The total discount is the price times those percentages **added together**, divided by 100 and **rounded down**; the result is the price minus the discount."
DISC_SOL = 'boolean allPass(Discount d) {\n    return check(d, 5000, false, 5000)\n            && check(d, 9999, false, 9999)\n            && check(d, 10000, false, 9000)\n            && check(d, 20000, false, 18000)\n            && check(d, 5000, true, 4900)\n            && check(d, 20000, true, 17600)\n            && check(d, 101, true, 99);\n}\n\n'
DISC_STARTER = 'boolean allPass(Discount d) {\n    return true;   // write your checks here\n}\n\n'
def disc_start(allpass): return DISC_IFACE + DISC_CORRECT + DISC_MUTANTS + DISC_HELP + allpass + DISC_DRV
ex.method("write", "j4-l3.1-write-discount-tests", "Kill the mutants", ["o1", "o3"], ["J4.05"], ["IMPL"],
    f"`Discount` has a correct implementation (`Correct`) and six **mutants**: copies with one small deliberate bug each. Write `allPass(Discount d)`: it should return `true` only if **every** check you make passes. Your checks must pass for `Correct` and fail for **every** mutant. Use the `check(d, pence, member, expected)` helper.\n\n{DISC_RULE}\n\nWork out each expected value **by hand from the rule**, as a real tester would. (Reading the code of `Correct` and comparing against it would be cheating: it can't find a bug in itself.) Hint: for each mutant, ask which single input makes it behave differently.",
    [("run", [("which", "String")], "String")], {"run": lambda w: "pass" if w == "correct" else "fail"},
    [("run", ["correct"]), ("run", ["mutant1"]), ("run", ["mutant6"])],
    [("run", ["mutant2"]), ("run", ["mutant3"]), ("run", ["mutant4"]), ("run", ["mutant5"]), ("run", ["correct"]), ("run", ["mutant1"])],
    disc_start(DISC_STARTER), disc_start(DISC_SOL),
    {"only-typical-values": disc_start('boolean allPass(Discount d) {\n    return check(d, 5000, false, 5000)\n            && check(d, 20000, false, 18000);\n}\n\n'),
     "expects-the-wrong-value": disc_start('boolean allPass(Discount d) {\n    return check(d, 10000, false, 9100)\n            && check(d, 5000, true, 4900)\n            && check(d, 101, true, 99);\n}\n\n'),
     "misses-rounding-and-boundary": disc_start('boolean allPass(Discount d) {\n    return check(d, 5000, false, 5000)\n            && check(d, 20000, false, 18000)\n            && check(d, 5000, true, 4900)\n            && check(d, 20000, true, 17600);\n}\n\n')},
    ("Think about what each mutant changes: the 10000 boundary, members on small orders, the member percentage, the big-order percentage, rounding, and members in general. Write one check per difference.", "check(d, 10000, false, 9000) kills the > mutant; check(d, 5000, true, 4900) kills the mutants that ignore members on small orders; check(d, 101, true, 99) kills rounding up."),
    difficulty=4)
AGE_IFACE = 'interface Pricing {\n    int price(int age);\n}\n\n'
AGE_CORRECT = 'class CorrectPricing implements Pricing {\n    public int price(int age) {\n        if (age < 5) return 0;\n        if (age < 18) return 500;\n        if (age < 65) return 1000;\n        return 700;\n    }\n}\n\n'
def amutant(name, body): return f'class {name} implements Pricing {{\n    public int price(int age) {{\n{body}\n    }}\n}}\n\n'
AGE_MUTANTS = (
    amutant("AgeMutant1", '        if (age <= 5) return 0;\n        if (age < 18) return 500;\n        if (age < 65) return 1000;\n        return 700;') +
    amutant("AgeMutant2", '        if (age < 5) return 0;\n        if (age <= 18) return 500;\n        if (age < 65) return 1000;\n        return 700;') +
    amutant("AgeMutant3", '        if (age < 5) return 0;\n        if (age < 18) return 500;\n        if (age <= 65) return 1000;\n        return 700;') +
    amutant("AgeMutant4", '        if (age < 5) return 0;\n        if (age < 18) return 500;\n        if (age < 65) return 1000;\n        return 600;') +
    amutant("AgeMutant5", '        if (age < 4) return 0;\n        if (age < 18) return 500;\n        if (age < 65) return 1000;\n        return 700;'))
AGE_HELP = '// check(p, age, expected) is true when the pricing gives the expected price for that age.\nboolean check(Pricing p, int age, int expected) {\n    return p.price(age) == expected;\n}\n\n'
AGE_DRV = 'String run(String which) {\n    Pricing p = switch (which) {\n        case "mutant1" -> new AgeMutant1();\n        case "mutant2" -> new AgeMutant2();\n        case "mutant3" -> new AgeMutant3();\n        case "mutant4" -> new AgeMutant4();\n        case "mutant5" -> new AgeMutant5();\n        default -> new CorrectPricing();\n    };\n    return allPass(p) ? "pass" : "fail";\n}'
AGE_SOL = 'boolean allPass(Pricing p) {\n    return check(p, 0, 0)\n            && check(p, 4, 0)\n            && check(p, 5, 500)\n            && check(p, 17, 500)\n            && check(p, 18, 1000)\n            && check(p, 64, 1000)\n            && check(p, 65, 700)\n            && check(p, 90, 700);\n}\n\n'
def age_start(ap): return AGE_IFACE + AGE_CORRECT + AGE_MUTANTS + AGE_HELP + ap + AGE_DRV
ex.method("write", "j4-l3.1-write-age-tests", "Both sides of every boundary", ["o1", "o3"], ["J4.05"], ["IMPL"],
    "A ticket price depends on age: **under 5** is free (0), **5 to 17** costs 500, **18 to 64** costs 1000, and **65 and over** costs 700. `CorrectPricing` follows the rule; five mutants each break it at one boundary or value. Write `allPass(Pricing p)` so that your checks pass for the correct pricing and fail for **every** mutant. Use `check(p, age, expected)`. Work out expected prices from the rule, not from the code.",
    [("run", [("which", "String")], "String")], {"run": lambda w: "pass" if w == "correct" else "fail"},
    [("run", ["correct"]), ("run", ["mutant1"]), ("run", ["mutant4"])],
    [("run", ["mutant2"]), ("run", ["mutant3"]), ("run", ["mutant5"]), ("run", ["correct"]), ("run", ["mutant1"])],
    age_start('boolean allPass(Pricing p) {\n    return true;   // write your checks here\n}\n\n'), age_start(AGE_SOL),
    {"checks-the-middle-only": age_start('boolean allPass(Pricing p) {\n    return check(p, 2, 0)\n            && check(p, 10, 500)\n            && check(p, 40, 1000)\n            && check(p, 80, 700);\n}\n\n'),
     "forgets-one-boundary": age_start('boolean allPass(Pricing p) {\n    return check(p, 4, 0)\n            && check(p, 5, 500)\n            && check(p, 17, 500)\n            && check(p, 18, 1000)\n            && check(p, 64, 1000)\n            && check(p, 90, 700);\n}\n\n')},
    ("The prices change at ages 5, 18 and 65. For each, check the age just below and the age exactly at the boundary, with the price the rule gives.", "check(p, 4, 0), check(p, 5, 500), check(p, 17, 500), check(p, 18, 1000), check(p, 64, 1000), check(p, 65, 700)"),
    difficulty=3)
ex.explain("j4-l3.1-explain-junit", "Read the test, read the failure", ["o2"], ["J4.05"],
    "A project has this JUnit test:\n\n```java\nclass PriceTest {\n    @Test\n    void addsTwentyPercent() {\n        assertEquals(1200, Price.withTax(1000));\n    }\n}\n```\n\nAfter someone edits `Price.java`, the build prints:\n\n```\nTests run: 4, Failures: 1, Errors: 0, Skipped: 0\norg.opentest4j.AssertionFailedError: expected: <1200> but was: <1250>\n\tat com.example.shop.PriceTest.addsTwentyPercent(PriceTest.java:12)\n```\n\n(a) What do `@Test` and `assertEquals(1200, ...)` do, and which argument is the expected value? (b) What does the failure message tell you, and what should you check before changing anything? (c) The other three tests pass. Does that prove `Price` is correct? How could you test whether your tests are any good?",
    "A full answer says @Test marks a method for JUnit to run and assertEquals compares the expected value (the first argument, 1200) with the actual result and fails if they differ; the message says the test wanted 1200 but the code returned 1250 so check the requirement to decide whether the code or the test is wrong; and passing tests only show the checked cases work, so you can test your tests by running them against deliberately broken versions (mutants) and seeing that they fail.",
    {2: ("Explains @Test and the expected-first assertEquals, reads the failure as expected 1200 versus actual 1250 and says to check the requirement to see whether code or test is wrong, and says passing doesn't prove correctness and mutants (deliberate bugs) show whether the tests would notice.",
         ["@Test tells JUnit to run the method, and assertEquals compares the expected value (the first argument, 1200) with what Price.withTax returns, failing if they differ. The message says the test expected 1200 but the code gave 1250. Before changing anything I'd check the requirement to see whether the tax rate really changed, because either the code or the test could be wrong. Three passing tests don't prove the code is correct, only that those cases work. To test the tests I'd make copies of the code with small deliberate bugs, mutants, and check that the tests fail on each one.",
          "(a) @Test marks a test; assertEquals(expected, actual) with 1200 as expected. (b) Expected 1200, actual 1250; check the requirement to see which is wrong. (c) No, it only shows those cases pass. Mutating the code with deliberate bugs shows whether the tests catch them."]),
     1: ("Answers some parts, for example reads the message but not the order of arguments, or says passing proves correctness.",
         ["It expected 1200 and got 1250.", "The other tests passed so it's fine."]),
     0: ("Incorrect, for example says 1250 is the expected value, or that the test framework is broken.",
         ["It expected 1250 and got 1200.", "JUnit is broken."])})
reg({"j4-l3.1": ("Your first unit tests", ["J4.05"])},
    {"MC142": (["J4.05"], "Platform", "The expected value of a test can be taken from running the code"),
     "MC143": (["J4.05"], "R16", "Testing typical values is enough to find boundary bugs"),
     "MC144": (["J4.05"], "Platform", "If all tests pass, the code is correct")})

# ====================================================================== 4.3.2
Lesson("j4-l3.2", "Good tests: edges, exceptions and test doubles", ["J4.06"], [
    ("o1", "Write checks for error cases, including that the right exception is thrown for each invalid input"),
    ("o2", "Replace something you can't control, such as the clock, with a test double"),
    ("o3", "Explain why a test is flaky or misleading and how to fix it"),
], ["j4-l3.1"], 55, ["I68", "R16"], r'''
## Before you start

You can write tests that cover boundaries and that kill mutants ([Your first unit tests](j4-l3.1)).

**Quick check.** What does a surviving mutant tell you?

<details><summary>Show the answer</summary>

That your tests have a gap: there's a bug your checks wouldn't notice.

</details>

## Explanation

### Test the error cases too

Valid input is half of a rule. The other half is **what happens when input is invalid**. If a method promises to throw `IllegalArgumentException` for a bad value, that promise needs a test, and it must be the **right** exception: callers `catch` a specific type.

In JUnit:

```java
@Test
void rejectsNegativePrices() {
    assertThrows(IllegalArgumentException.class, () -> Price.withTax(-1));
}
```

`assertThrows` passes only if the code **does** throw that type (or a subtype) `[I68]`. It fails if nothing is thrown, and it fails if a different exception is thrown. So three things can go wrong, and a good suite notices each: no exception, the wrong exception, and an exception for input that was valid.

A hand-rolled version, for the exercises here, is a helper that runs some code and reports what happened:

```java
boolean throwsIAE(Parser p, String text) {
    try {
        p.parsePercent(text);
        return false;                        // nothing was thrown
    } catch (IllegalArgumentException e) {
        return true;                         // exactly the exception we want
    } catch (RuntimeException e) {
        return false;                        // some other exception: wrong type
    }
}
```

Cover **both sides of the validity boundary** again: if `0` to `100` are valid percentages, test `-1`, `0`, `100` and `101`.

### Many cases, one test: parameterised tests

When the same check applies to many inputs, writing a method per case is noisy. A **parameterised test** runs one method with a table of values `[I68]`:

```java
class PriceParamTest {

    @ParameterizedTest
    @CsvSource({
        "0, 0",
        "1, 1",
        "5, 6",
        "1000, 1200",
        "99, 118"
    })
    void withTaxMatchesTheRule(int pence, int expected) {
        assertEquals(expected, Price.withTax(pence));
    }
}
```

Maven reports it as one class with five test runs:

```
[INFO] Running com.example.shop.PriceParamTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.041 s -- in com.example.shop.PriceParamTest
```

When it fails, each row is reported separately, with its position. After I changed the code's rate to 25%, two rows failed:

```
[ERROR] com.example.shop.PriceParamTest.withTaxMatchesTheRule(int, int)[4] -- FAILURE!
[ERROR] com.example.shop.PriceParamTest.withTaxMatchesTheRule(int, int)[5] -- FAILURE!
```

`[4]` and `[5]` are the 4th and 5th rows (`1000, 1200` and `99, 118`): 1000 gave 1250 and 99 gave 123. The first three rows still passed (0, 1 and 6 all happen to be the same at 20% and 25%, for these inputs). A table makes it easy to add a boundary case with one line.

### Things you can't control: test doubles

A test must give the **same result every time**. Code that depends on the **current time**, a **random number**, the **network** or a **database** doesn't, unless you take control of that dependency.

```java
String greet() {
    int hour = LocalTime.now().getHour();      // the answer depends on when the test runs
    return hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
}
```

A test for this passes in the morning and fails in the evening: it is **flaky**. The fix is to **inject** the dependency through an interface, so a test can substitute its own:

```java
interface Clock {
    int hour();
}

class Greeter {
    String greet(Clock clock) {
        int hour = clock.hour();
        return hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
    }
}
```

In production you pass a clock that reads the real time. In a test you pass a **test double**: a stand-in that returns whatever you choose.

```java
class FakeClock implements Clock {
    private final int hour;
    FakeClock(int hour) { this.hour = hour; }
    public int hour() { return hour; }
}
// new Greeter().greet(new FakeClock(9)) is always "Good morning"
```

A **fake** is a simple working implementation like this one. (Other kinds of double record calls, or return canned answers; the principle is the same.) This is the interface-based design from Stage 2, put to work.

### Don't overuse doubles

Replace things that are **slow, random, external or hard to set up** (time, network, database, files). Don't replace your own simple classes: a test that checks only that your mock was called says nothing about whether the real code works. The more you fake, the less the test proves.

### What makes a test bad

| Problem | Why it hurts | Fix |
|---|---|---|
| **Flaky**: depends on time, random numbers, order or external services | passes and fails with no code change, so people stop trusting failures | inject and fake the uncontrolled input |
| **Asserts nothing**: it runs the code and prints, but never checks | always passes, proves nothing | add an assertion on the result |
| **Tests the implementation**, not the behaviour | breaks whenever you refactor, even though nothing is wrong | assert what the code returns or does, not how |
| **Several unrelated checks in one test** | the first failure hides the rest, and the name says nothing | one idea per test |
| **A vague name** (`test1`) | a failure doesn't say what broke | name it for the behaviour |

## Worked examples

### Example 1: killing an exception mutant

*Task: `parsePercent("101%")` must throw `IllegalArgumentException`. A mutant accepts 101. Which check catches it?*

**Step 1 — Where do they differ?** Only for 101 (and above): the correct code throws, the mutant returns 101.

**Step 2 — Check it:** `throwsIAE(p, "101%")` must be `true`.

**Step 3 — And the other side:** `parsePercent("100%")` must **not** throw and must return 100, which catches a mutant that rejects 100.

### Example 2: making a greeting testable

*Task: how do you test that 9 o'clock gives `"Good morning"`?*

**Step 1 — What's uncontrolled?** The clock.

**Step 2 — Give `greet` a `Clock` parameter,** so the time becomes an input.

**Step 3 — Test with a fake:** `new Greeter().greet(new FakeClock(9))` is always `"Good morning"`, at any time of day.

## Where this is used

- **Any code that touches time, money rates, random numbers, the network or a database** is tested through doubles.
- **Flaky tests** are one of the most corrosive problems in real teams: a suite people don't trust is a suite they ignore.
- **Interfaces and dependency injection** (Stage 7, Spring) exist largely to make this easy.

## Common mistakes

:::mistake{id=MC145}
**Testing only that valid input works.** The error cases are part of the rule. Check that the right exception is thrown, and that valid boundary values aren't rejected.
:::

:::mistake{id=MC146}
**A test that depends on the real clock, random numbers or the network.** It passes or fails with no change to the code. Inject a fake.
:::

:::mistake{id=MC147}
**A test with no assertion.** It can't fail, so it proves nothing.
:::

## Practice

::exercise{id=j4-l3.2-write-exception-tests}

::exercise{id=j4-l3.2-write-fake}

::exercise{id=j4-l3.2-explain-quality}

## Further reading

- **JUnit User Guide, "Writing Tests"** `[I68]` covers `assertThrows` and parameterised tests (`@ParameterizedTest`, `@CsvSource`).
- **McCauley et al. (2008)** `[R16]` on debugging: a flaky test is a bug in the test, and finding why it varies is the same hypothesise-and-test cycle.

## How you'll be assessed

- The **write** exercises check that you can test error cases against broken versions, and write a fake that controls an input (*implementation*).
- The **explain** exercise checks that you can diagnose a flaky or empty test (*explanation*).
''' + FOOT)

ex = Exercises("j4-l3.2")
PARSE_IFACE = 'interface Parser {\n    int parsePercent(String text);\n}\n\n'
PARSE_CORRECT = 'class CorrectParser implements Parser {\n    public int parsePercent(String text) {\n        if (!text.matches("[0-9]+%")) {\n            throw new IllegalArgumentException("not a percentage: " + text);\n        }\n        int value = Integer.parseInt(text.substring(0, text.length() - 1));\n        if (value > 100) {\n            throw new IllegalArgumentException("over 100: " + text);\n        }\n        return value;\n    }\n}\n\n'
def pmutant(name, body): return f'class {name} implements Parser {{\n    public int parsePercent(String text) {{\n{body}\n    }}\n}}\n\n'
PARSE_MUTANTS = (
    pmutant("ParseMutant1", '        if (!text.matches("[0-9]+%")) {\n            throw new IllegalArgumentException("not a percentage");\n        }\n        return Integer.parseInt(text.substring(0, text.length() - 1));') +
    pmutant("ParseMutant2", '        if (!text.matches("[0-9]+%")) {\n            throw new IllegalArgumentException("not a percentage");\n        }\n        int value = Integer.parseInt(text.substring(0, text.length() - 1));\n        if (value >= 100) {\n            throw new IllegalArgumentException("over 100");\n        }\n        return value;') +
    pmutant("ParseMutant3", '        String digits = text.endsWith("%") ? text.substring(0, text.length() - 1) : text;\n        if (!digits.matches("[0-9]+")) {\n            throw new IllegalArgumentException("not a number");\n        }\n        int value = Integer.parseInt(digits);\n        if (value > 100) {\n            throw new IllegalArgumentException("over 100");\n        }\n        return value;') +
    pmutant("ParseMutant4", '        if (!text.matches("[0-9]+%")) {\n            throw new IllegalStateException("not a percentage");\n        }\n        int value = Integer.parseInt(text.substring(0, text.length() - 1));\n        if (value > 100) {\n            throw new IllegalArgumentException("over 100");\n        }\n        return value;') +
    pmutant("ParseMutant5", '        if (!text.matches("-?[0-9]+%")) {\n            throw new IllegalArgumentException("not a percentage");\n        }\n        int value = Integer.parseInt(text.substring(0, text.length() - 1));\n        if (value > 100) {\n            throw new IllegalArgumentException("over 100");\n        }\n        return value;'))
PARSE_HELP = '// throwsIAE(p, text) is true only if parsing the text throws an IllegalArgumentException (and nothing else).\nboolean throwsIAE(Parser p, String text) {\n    try {\n        p.parsePercent(text);\n        return false;\n    } catch (IllegalArgumentException e) {\n        return true;\n    } catch (RuntimeException e) {\n        return false;\n    }\n}\n\n// returns(p, text, expected) is true if parsing the text gives the expected value.\nboolean returns(Parser p, String text, int expected) {\n    try {\n        return p.parsePercent(text) == expected;\n    } catch (RuntimeException e) {\n        return false;\n    }\n}\n\n'
PARSE_DRV = 'String run(String which) {\n    Parser p = switch (which) {\n        case "mutant1" -> new ParseMutant1();\n        case "mutant2" -> new ParseMutant2();\n        case "mutant3" -> new ParseMutant3();\n        case "mutant4" -> new ParseMutant4();\n        case "mutant5" -> new ParseMutant5();\n        default -> new CorrectParser();\n    };\n    return allPass(p) ? "pass" : "fail";\n}'
PARSE_SOL = 'boolean allPass(Parser p) {\n    return returns(p, "0%", 0)\n            && returns(p, "42%", 42)\n            && returns(p, "100%", 100)\n            && throwsIAE(p, "101%")\n            && throwsIAE(p, "50")\n            && throwsIAE(p, "abc%")\n            && throwsIAE(p, "-5%")\n            && throwsIAE(p, "");\n}\n\n'
def parse_start(ap): return PARSE_IFACE + PARSE_CORRECT + PARSE_MUTANTS + PARSE_HELP + ap + PARSE_DRV
ex.method("write", "j4-l3.2-write-exception-tests", "Test the error cases", ["o1"], ["J4.06"], ["IMPL"],
    "`parsePercent(text)` turns text such as `\"42%\"` into the number 42. The rule: the text must be digits followed by `%`, and the value must be **0 to 100**; anything else must throw an **`IllegalArgumentException`**. `CorrectParser` follows it; five mutants don't (one accepts 101, one rejects 100, one doesn't need the `%`, one throws the **wrong exception type**, one accepts negative numbers). Write `allPass(Parser p)` using the helpers `returns` and `throwsIAE`, so that it's `true` for the correct parser and `false` for every mutant.",
    [("run", [("which", "String")], "String")], {"run": lambda w: "pass" if w == "correct" else "fail"},
    [("run", ["correct"]), ("run", ["mutant1"]), ("run", ["mutant4"])],
    [("run", ["mutant2"]), ("run", ["mutant3"]), ("run", ["mutant5"]), ("run", ["correct"]), ("run", ["mutant1"])],
    parse_start('boolean allPass(Parser p) {\n    return true;   // write your checks here\n}\n\n'), parse_start(PARSE_SOL),
    {"only-valid-input": parse_start('boolean allPass(Parser p) {\n    return returns(p, "0%", 0)\n            && returns(p, "42%", 42)\n            && returns(p, "100%", 100);\n}\n\n'),
     "forgets-the-exception-type-and-the-boundary": parse_start('boolean allPass(Parser p) {\n    return returns(p, "42%", 42)\n            && throwsIAE(p, "abc%")\n            && throwsIAE(p, "101%");\n}\n\n')},
    ("Check valid values at both ends (0 and 100), and invalid ones: just over the limit, no percent sign, letters, a negative number, empty text. Use throwsIAE for the invalid ones so the exception type is checked too.", "returns(p, \"100%\", 100) && throwsIAE(p, \"101%\") && throwsIAE(p, \"50\") && throwsIAE(p, \"-5%\")"),
    difficulty=4)
CLOCK_IFACE = 'interface Clock {\n    int hour();\n}\n\nclass Greeter {\n    String greet(Clock clock) {\n        int hour = clock.hour();\n        return hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";\n    }\n}\n\n'
CLOCK_DRV = 'String run(int hour) {\n    return new Greeter().greet(new FakeClock(hour));\n}'
def greet(h): return "Good morning" if h < 12 else "Good afternoon" if h < 18 else "Good evening"
ex.method("write", "j4-l3.2-write-fake", "A clock you control", ["o2"], ["J4.06"], ["IMPL"],
    "`Greeter.greet` takes a `Clock`, so a test can decide what time it is. Write the **test double** `FakeClock`: a class that `implements Clock`, is constructed with an hour (`new FakeClock(9)`), and whose `hour()` returns exactly that hour. The driver then checks the greeting for a chosen hour.",
    [("run", [("hour", "int")], "String")], {"run": greet},
    [("run", [9]), ("run", [14]), ("run", [20])],
    [("run", [0]), ("run", [11]), ("run", [12]), ("run", [17]), ("run", [18]), ("run", [23])],
    CLOCK_IFACE + '// Write the class FakeClock here.\n\n' + CLOCK_DRV,
    CLOCK_IFACE + 'class FakeClock implements Clock {\n    private final int hour;\n\n    FakeClock(int hour) {\n        this.hour = hour;\n    }\n\n    public int hour() {\n        return hour;\n    }\n}\n\n' + CLOCK_DRV,
    {"always-nine": CLOCK_IFACE + 'class FakeClock implements Clock {\n    FakeClock(int hour) {\n    }\n\n    public int hour() {\n        return 9;\n    }\n}\n\n' + CLOCK_DRV,
     "off-by-one": CLOCK_IFACE + 'class FakeClock implements Clock {\n    private final int hour;\n\n    FakeClock(int hour) {\n        this.hour = hour + 1;\n    }\n\n    public int hour() {\n        return hour;\n    }\n}\n\n' + CLOCK_DRV},
    ("A fake is just a small class that implements the interface. Store the hour you're given and return it.", "class FakeClock implements Clock { private final int hour; FakeClock(int hour) { this.hour = hour; } public int hour() { return hour; } }"),
    source_tests=[("FakeClock implements Clock", ["FakeClock implements Clock"], None)],
    starter_compiles=False, difficulty=2)
ex.explain("j4-l3.2-explain-quality", "What is wrong with these tests?", ["o3"], ["J4.06"],
    "Here are two tests for a method `Greeter.greet()` that uses the current time, and for `Basket.total()`:\n\n```java\n@Test\nvoid greetsInTheMorning() {\n    assertEquals(\"Good morning\", new Greeter().greet());\n}\n\n@Test\nvoid totalWorks() {\n    Basket basket = new Basket();\n    basket.add(new Random().nextInt(100));\n    basket.total();\n    System.out.println(basket.total());\n}\n```\n\n(a) Why will the first test sometimes pass and sometimes fail? How would you make it reliable? (b) List **two** problems with the second test. (c) Give a better name for each, and say what you'd assert in the second.",
    "A full answer says the first depends on the real current time so it passes in the morning and fails otherwise, fixed by injecting a Clock and using a fake with a fixed hour; the second uses a random value so it isn't repeatable and has no assertion (it only prints), so it can't fail; and better names say the behaviour (such as greetsGoodMorningBeforeNoon, totalOfOneItemIsItsPrice) with an assertion that the total equals the price of the single item added, using a fixed value.",
    {2: ("Says the first depends on the real clock so it is flaky, fixed by injecting a Clock with a fake; says the second is non-repeatable because of the random number and asserts nothing; and gives behaviour-based names and a fixed-value assertion on the total.",
         ["The first test depends on the real time, so it passes in the morning and fails in the afternoon. I'd inject a Clock and pass a FakeClock(9). The second test uses a random number, so it isn't repeatable, and it never asserts anything, it only prints, so it can't fail. Better names: greetsGoodMorningBeforeNoon and totalOfOneItemIsItsPrice. I'd add one item with a fixed price like 40 and assertEquals(40, basket.total()).",
          "(a) It uses the real clock so it's flaky; use a Clock interface and a fake. (b) Random input and no assertion. (c) greetsGoodMorningAt9 and totalOfSingleItemEqualsItsPrice, asserting the total equals the fixed price."]),
     1: ("Finds some of the problems, or fixes them without explaining them.",
         ["It uses the current time.", "It doesn't have an assertion."]),
     0: ("Incorrect, for example says the tests are fine, or that adding more printing would fix them.",
         ["They're fine as they are.", "Add more println calls."])})
reg({"j4-l3.2": ("Good tests: edges, exceptions and test doubles", ["J4.06"])},
    {"MC145": (["J4.06"], "I68", "A test suite only needs to cover valid input"),
     "MC146": (["J4.06"], "Platform", "A test that depends on the real clock or random numbers is fine if it usually passes"),
     "MC147": (["J4.06"], "Platform", "A test that runs the code and prints the result is a good test")})
print("4.3 written")
