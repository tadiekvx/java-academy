from proj import *

def fmt(p):
    sign = "-" if p < 0 else ""
    a = abs(p)
    return f"{sign}£{a // 100}.{a % 100:02d}"
def total(e): return sum(e)
def sav(i, e): return i - sum(e)
def rate(i, e): return 0 if i == 0 else jdiv((i - sum(e)) * 100, i)
def verdict(r): return "Great" if r >= 20 else "Good" if r >= 10 else "Tight" if r >= 0 else "Overspending"
def summary(i, e):
    r = rate(i, e)
    return f"Income: {fmt(i)}\nExpenses: {fmt(sum(e))}\nSavings: {fmt(i - sum(e))} ({r}%) - {verdict(r)}"

EXP = [[], [5000], [120000, 30000], [1999, 1], [100, 200, 300, 400]]
def io_case(name, income, exps):
    stdin = f"{income}\n" + "".join(f"{e}\n" for e in exps) + "done\n"
    return (name, stdin, [summary(income, exps)])

SOLUTION = '''
int totalExpenses(int[] expenses) {
    int total = 0;
    for (int expense : expenses) {
        total += expense;
    }
    return total;
}

int savings(int income, int[] expenses) {
    return income - totalExpenses(expenses);
}

int savingsRatePercent(int income, int[] expenses) {
    if (income == 0) {
        return 0;
    }
    return savings(income, expenses) * 100 / income;
}

String verdict(int ratePercent) {
    if (ratePercent >= 20) {
        return "Great";
    } else if (ratePercent >= 10) {
        return "Good";
    } else if (ratePercent >= 0) {
        return "Tight";
    } else {
        return "Overspending";
    }
}

String formatMoney(int pence) {
    String sign = pence < 0 ? "-" : "";
    int absolute = Math.abs(pence);
    int pounds = absolute / 100;
    int remainder = absolute % 100;
    String padding = remainder < 10 ? "0" : "";
    return sign + "£" + pounds + "." + padding + remainder;
}

String summary(int income, int[] expenses) {
    int rate = savingsRatePercent(income, expenses);
    return "Income: " + formatMoney(income) + "\\n"
            + "Expenses: " + formatMoney(totalExpenses(expenses)) + "\\n"
            + "Savings: " + formatMoney(savings(income, expenses)) + " (" + rate + "%) - " + verdict(rate);
}

void main() {
    int income = Integer.parseInt(IO.readln("Monthly income in pence: ").strip());
    ArrayList<Integer> typed = new ArrayList<>();
    String line = IO.readln("Expense in pence (or done): ").strip();
    while (!line.equals("done")) {
        typed.add(Integer.parseInt(line));
        line = IO.readln("Expense in pence (or done): ").strip();
    }
    int[] expenses = new int[typed.size()];
    for (int i = 0; i < expenses.length; i++) {
        expenses[i] = typed.get(i);
    }
    IO.println(summary(income, expenses));
}
'''
STARTER = '''
// Personal finance calculator. All money is whole pence, as an int.
// Each method below is a stub that compiles but gives the wrong answer. Replace the bodies one
// milestone at a time, and use "Check milestone" after each one.

int totalExpenses(int[] expenses) {
    return 0;
}

int savings(int income, int[] expenses) {
    return 0;
}

int savingsRatePercent(int income, int[] expenses) {
    return 0;
}

String verdict(int ratePercent) {
    return "";
}

String formatMoney(int pence) {
    return "";
}

String summary(int income, int[] expenses) {
    return "";
}

void main() {
    // Milestone 7: read the income and the expenses, then print the summary.
}
'''
def wrong_main(body):  # replace the solution's method by a wrong one
    return body
S = SOLUTION
wrongs = {
  "m1-skips-last": S.replace("for (int expense : expenses) {\n        total += expense;\n    }", "for (int i = 0; i < expenses.length - 1; i++) {\n        total += expenses[i];\n    }"),
  "m2-adds": S.replace("return income - totalExpenses(expenses);", "return income + totalExpenses(expenses);"),
  "m3-divides-first": S.replace("return savings(income, expenses) * 100 / income;", "return savings(income, expenses) / income * 100;"),
  "m3-no-zero-guard": S.replace("    if (income == 0) {\n        return 0;\n    }\n", ""),
  "m4-strict": S.replace('ratePercent >= 20', 'ratePercent > 20').replace('ratePercent >= 10', 'ratePercent > 10'),
  "m5-no-padding": S.replace('    String padding = remainder < 10 ? "0" : "";\n', '    String padding = "";\n'),
  "m5-negative-sign": S.replace('String sign = pence < 0 ? "-" : "";', 'String sign = "";').replace("int absolute = Math.abs(pence);", "int absolute = Math.abs(pence);"),
  "m6-wrong-order": S.replace('"Income: " + formatMoney(income) + "\\n"\n            + "Expenses: " + formatMoney(totalExpenses(expenses)) + "\\n"', '"Expenses: " + formatMoney(totalExpenses(expenses)) + "\\n"\n            + "Income: " + formatMoney(income) + "\\n"'),
  "m7-ignores-expenses": S.replace("typed.add(Integer.parseInt(line));", "typed.add(0);"),
}

ms = []
ms.append(dict(id="m1", title="Add up the expenses", methods=[("totalExpenses", [("expenses", "int[]")], "int")], fns={"totalExpenses": total},
  instructions="""
  **Goal:** `totalExpenses` returns the sum of every amount in the array (whole pence).

  **How:** this is the *sum* pattern from [Loop patterns](/lessons/j1-l4.4), applied to an array ([Arrays](/lessons/j1-l6.1)). Start a total at 0 and add each element with an enhanced `for` loop. The sum of an empty array is 0.

  **Check:** edge cases are an empty array and a single expense.
  """,
  visible=[(None, [[]]), (None, [[5000]]), (None, [[120000, 30000]])],
  hidden=[(None, [[1, 1, 1]], "small ones"), (None, [[100, 200, 300, 400]], "four expenses"), (None, [[999999]], "one big expense"), (None, [[0, 0]], "zeros"), (None, [[1999, 1]], "rounds to a pound"), (None, [[7, 13, 21, 34, 55]], "five")]))
ms.append(dict(id="m2", title="Work out the savings", methods=[("savings", [("income", "int"), ("expenses", "int[]")], "int")], fns={"savings": sav},
  instructions="""
  **Goal:** `savings` returns income minus total expenses. It can be negative if the person overspent.

  **How:** don't re-write the loop: **call** `totalExpenses` ([Parameters and return values](/lessons/j1-l5.2)). Small methods built from smaller ones are easier to check.
  """,
  visible=[(None, [200000, [120000, 30000]]), (None, [1000, []]), (None, [1000, [1500]])],
  hidden=[(None, [0, []], "nothing at all"), (None, [500, [500]], "exactly spent"), (None, [100, [30, 30, 30]], "three small"), (None, [0, [100]], "no income"), (None, [250000, [99999, 1]], "big"), (None, [1, [2]], "overspent by one")]))
ms.append(dict(id="m3", title="Savings rate", methods=[("savingsRatePercent", [("income", "int"), ("expenses", "int[]")], "int")], fns={"savingsRatePercent": rate},
  instructions="""
  **Goal:** the savings as a whole-number percentage of income (rounded **down**, toward zero). If income is 0, the rate is 0.

  **How:** `savings(...) * 100 / income`. Multiply **before** you divide, or integer division throws the fraction away ([Arithmetic](/lessons/j1-l2.3)). Guard the zero case first ([Exceptions and stack traces](/lessons/j1-l6.4)).

  **Check:** negative savings give a negative rate. A rate of 66.67% is 66.
  """,
  visible=[(None, [200000, [120000, 30000]]), (None, [0, [100]]), (None, [1000, [1500]])],
  hidden=[(None, [300, [100]], "two thirds rounds down"), (None, [300, [400]], "negative with a remainder"), (None, [1000, [1000]], "spent everything"), (None, [1000, []], "spent nothing"), (None, [7, [3]], "tiny numbers"), (None, [100000, [99999]], "saved one pence")]))
ms.append(dict(id="m4", title="A verdict", methods=[("verdict", [("ratePercent", "int")], "String")], fns={"verdict": verdict},
  instructions="""
  **Goal:** 20% or more is `"Great"`, 10% or more is `"Good"`, 0% or more is `"Tight"`, and anything below 0 is `"Overspending"`.

  **How:** an else-if chain ([Making decisions](/lessons/j1-l3.3)). Check the most demanding condition first, and test the boundaries 20, 19, 10, 9, 0 and -1.
  """,
  visible=[(None, [25]), (None, [12]), (None, [-5])],
  hidden=[(None, [20], "exactly 20"), (None, [19], "just under 20"), (None, [10], "exactly 10"), (None, [9], "just under 10"), (None, [0], "exactly 0"), (None, [-1], "just below zero"), (None, [100], "everything saved")]))
ms.append(dict(id="m5", title="Format money", methods=[("formatMoney", [("pence", "int")], "String")], fns={"formatMoney": fmt},
  instructions="""
  **Goal:** show whole pence as pounds, like `£12.34`. Negative amounts show the sign first: `-£1.05`. Always two digits of pence.

  **How:** use `/ 100` for pounds and `% 100` for pence ([Arithmetic](/lessons/j1-l2.3)). Work with the **absolute value** (`Math.abs`) so negative numbers don't give negative pence. Add a leading `0` when the pence are below 10 ([Working with strings](/lessons/j1-l2.4)).

  **Check:** 5 pence is `£0.05`, not `£0.5`.
  """,
  visible=[(None, [1234]), (None, [5]), (None, [-105])],
  hidden=[(None, [0], "zero"), (None, [100], "exactly a pound"), (None, [99999], "large"), (None, [-5], "negative pence"), (None, [10], "ten pence"), (None, [101], "one pound one"), (None, [-100000], "minus a thousand pounds")]))
ms.append(dict(id="m6", title="The summary", methods=[("summary", [("income", "int"), ("expenses", "int[]")], "String")], fns={"summary": summary},
  instructions="""
  **Goal:** return three lines, joined with `\\n` (no `\\n` after the last line):

  ```
  Income: £2000.00
  Expenses: £1500.00
  Savings: £500.00 (25%) - Great
  ```

  **How:** build each line from the methods you've already written. Don't repeat any calculation.
  """,
  visible=[(None, [200000, [120000, 30000]]), (None, [1000, [1500]]), (None, [0, []])],
  hidden=[(None, [300, [400]], "overspending with remainder"), (None, [100000, [1999, 1]], "tiny expenses"), (None, [5000, [5000]], "break even"), (None, [123456, [100, 200, 300, 400]], "awkward numbers"), (None, [1, []], "one pence")]))
io_hidden = [io_case("one expense", 100000, [20000]), io_case("overspent", 5000, [4000, 3000]), io_case("no expenses", 7500, []), io_case("many expenses", 250000, [100, 200, 300, 400, 500])]
ms.append(dict(id="m7", title="Put it together: the whole program",
  instructions="""
  **Goal:** make `main` a complete program. It asks `Monthly income in pence: `, then keeps asking `Expense in pence (or done): ` until the person types `done`, then prints `summary(income, expenses)`.

  **How:** you don't know how many expenses there will be, so collect them in an `ArrayList<Integer>` ([ArrayList](/lessons/j1-l6.3)), then copy them into an `int[]` for your methods. The loop is the one from [Input validation loops](/lessons/j1-l4.5): read, check for `done`, and repeat. Use the **Input for Run** box to try it out before you check it.

  Input is always valid here; validating it is a stretch goal for later.
  """,
  io=dict(visible=[io_case("typical month", 200000, [120000, 30000]), io_case("one tiny expense", 1000, [1])], hidden=io_hidden)))

project("j1-p1-finance", "Personal finance calculator", "A",
    "Turn a month's income and expenses into a clear summary with a savings rate and a verdict.",
    """
    You'll build a small program that helps someone understand their month: how much they earned, how much they spent, how much is left, what percentage of their income they saved, and a one-word verdict.

    It's a **guided build**: each milestone has an explanation and its own tests, and uses an idea from an earlier lesson. Work in order: later milestones call the methods you write in earlier ones.

    All money is stored as **whole pence in an `int`** (so £12.34 is `1234`). That avoids the rounding surprises of `double`; you'll learn the details in [Arithmetic](/lessons/j1-l2.3).
    """, 3, ["j1-l4.5", "j1-l5.4", "j1-l6.3"], ["J1.05", "J1.07", "J1.08", "J1.09", "J1.10", "J1.11"],
    [], ["Money is whole pence in an int, never a double.", "Build the answer from small methods; don't repeat a calculation."], [],
    ms, [], "", STARTER, SOLUTION, wrongs)
print("P1 written")
