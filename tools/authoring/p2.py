from proj import *

def fmt(p):
    sign = "-" if p < 0 else ""
    a = abs(p)
    return f"{sign}£{a // 100}.{a % 100:02d}"
def line_total(u, q):
    t = u * q
    return t - t * 10 // 100 if q >= 10 else t
def subtotal(us, qs): return sum(line_total(u, q) for u, q in zip(us, qs))
def receipt(ns, us, qs):
    lines = [f"{n} x{q} {fmt(line_total(u, q))}" for n, u, q in zip(ns, us, qs)]
    sub = subtotal(us, qs)
    vat = sub * 20 // 100
    return "\n".join(lines + [f"Subtotal: {fmt(sub)}", f"VAT (20%): {fmt(vat)}", f"Total: {fmt(sub + vat)}"])

SOLUTION = '''
String formatMoney(int pence) {
    String sign = pence < 0 ? "-" : "";
    int absolute = Math.abs(pence);
    String padding = absolute % 100 < 10 ? "0" : "";
    return sign + "£" + absolute / 100 + "." + padding + absolute % 100;
}

int lineTotal(int unitPrice, int quantity) {
    int total = unitPrice * quantity;
    if (quantity >= 10) {
        total -= total * 10 / 100;
    }
    return total;
}

int subtotal(int[] unitPrices, int[] quantities) {
    int sum = 0;
    for (int i = 0; i < unitPrices.length; i++) {
        sum += lineTotal(unitPrices[i], quantities[i]);
    }
    return sum;
}

String receipt(String[] names, int[] unitPrices, int[] quantities) {
    String text = "";
    for (int i = 0; i < names.length; i++) {
        text += names[i] + " x" + quantities[i] + " " + formatMoney(lineTotal(unitPrices[i], quantities[i])) + "\\n";
    }
    int sub = subtotal(unitPrices, quantities);
    int vat = sub * 20 / 100;
    return text + "Subtotal: " + formatMoney(sub) + "\\n"
            + "VAT (20%): " + formatMoney(vat) + "\\n"
            + "Total: " + formatMoney(sub + vat);
}

void main() {
    String[] names = {"Tea", "Biscuits"};
    int[] prices = {250, 199};
    int[] quantities = {2, 12};
    IO.println(receipt(names, prices, quantities));
}
'''
STARTER = '''
// Shopping basket and receipt. All money is whole pence, as an int.
// The methods are stubs that compile but give the wrong answers. The brief and milestones
// describe what each one must do; the design is yours.

String formatMoney(int pence) {
    return "";
}

int lineTotal(int unitPrice, int quantity) {
    return 0;
}

int subtotal(int[] unitPrices, int[] quantities) {
    return 0;
}

String receipt(String[] names, int[] unitPrices, int[] quantities) {
    return "";
}

void main() {
    // Optional: print a receipt for a basket of your own to try it out.
}
'''
S = SOLUTION
wrongs = {
  "m1-no-padding": S.replace('    String padding = absolute % 100 < 10 ? "0" : "";\n', '    String padding = "";\n'),
  "m1-loses-sign": S.replace('String sign = pence < 0 ? "-" : "";', 'String sign = "";'),
  "m2-no-discount": S.replace("    if (quantity >= 10) {\n        total -= total * 10 / 100;\n    }\n", ""),
  "m2-discount-above-ten": S.replace("if (quantity >= 10)", "if (quantity > 10)"),
  "m3-ignores-discount": S.replace("sum += lineTotal(unitPrices[i], quantities[i]);", "sum += unitPrices[i] * quantities[i];"),
  "m4-vat-on-nothing": S.replace("int vat = sub * 20 / 100;", "int vat = 0;"),
  "m4-lines-reversed": S.replace('names[i] + " x" + quantities[i]', 'quantities[i] + "x " + names[i]'),
}

NAMES = [[], ["Tea"], ["Tea", "Biscuits"], ["Milk", "Eggs", "Bread"], ["Pens"], ["A", "B"]]
PRICES = [[], [250], [250, 199], [115, 299, 140], [49], [1, 3333]]
QTYS = [[], [1], [2, 12], [1, 6, 2], [10], [10, 1]]

ms = [
 dict(id="m1", title="Money as text", methods=[("formatMoney", [("pence", "int")], "String")], fns={"formatMoney": fmt},
  instructions="""
  `formatMoney(int pence)` returns whole pence as pounds and pence: `1234` → `£12.34`, `5` → `£0.05`, `0` → `£0.00`, `-105` → `-£1.05`. Always exactly two digits of pence. The pound sign is `£`.
  """,
  visible=[(None, [1234]), (None, [5]), (None, [-105])],
  hidden=[(None, [0], "zero"), (None, [100], "exactly a pound"), (None, [10], "ten pence"), (None, [99999], "large"), (None, [-5], "negative pence"), (None, [101], "one pound one")]),
 dict(id="m2", title="One line of the basket", methods=[("lineTotal", [("unitPrice", "int"), ("quantity", "int")], "int")], fns={"lineTotal": line_total},
  instructions="""
  `lineTotal(unitPrice, quantity)` returns the cost of one line, in pence. Buying **10 or more** of an item takes **10% off that line**, with the discount worked out in whole pence and rounded **down**. Under 10, there is no discount.
  """,
  visible=[(None, [250, 2]), (None, [250, 10]), (None, [199, 12])],
  hidden=[(None, [250, 9], "just under the discount"), (None, [199, 10], "awkward discount"), (None, [1, 10], "rounds the discount down to zero"), (None, [100, 0], "none bought"), (None, [333, 11], "eleven"), (None, [5, 100], "a hundred")]),
 dict(id="m3", title="The basket subtotal", methods=[("subtotal", [("unitPrices", "int[]"), ("quantities", "int[]")], "int")], fns={"subtotal": subtotal},
  instructions="""
  `subtotal(unitPrices, quantities)` returns the sum of every line's `lineTotal`. The two arrays always have the same length; item *i* has price `unitPrices[i]` and quantity `quantities[i]`. An empty basket costs 0.
  """,
  visible=[(None, [[], []]), (None, [[250], [1]]), (None, [[250, 199], [2, 12]])],
  hidden=[(None, [[115, 299, 140], [1, 6, 2]], "three items"), (None, [[49], [10]], "one discounted"), (None, [[1, 3333], [10, 1]], "mixed"), (None, [[100, 100], [0, 0]], "none bought"), (None, [[500, 20], [9, 10]], "boundary of the discount")]),
 dict(id="m4", title="The receipt", methods=[("receipt", [("names", "String[]"), ("unitPrices", "int[]"), ("quantities", "int[]")], "String")], fns={"receipt": receipt},
  instructions="""
  `receipt(names, unitPrices, quantities)` returns the receipt as one string, lines separated by `\\n`, with **no** `\\n` after the last line.

  - One line per item, in basket order: `NAME xQUANTITY AMOUNT`, where AMOUNT is that line's total (after any discount) as money. Example: `Tea x2 £5.00`.
  - Then `Subtotal: ` and the subtotal as money.
  - Then `VAT (20%): ` and 20% of the subtotal, in whole pence rounded **down**, as money.
  - Then `Total: ` and the subtotal plus VAT, as money.

  An empty basket has just the three totals lines.
  """,
  visible=[(None, [[], [], []]), (None, [["Tea"], [250], [1]]), (None, [["Tea", "Biscuits"], [250, 199], [2, 12]])],
  hidden=[(None, [["Milk", "Eggs", "Bread"], [115, 299, 140], [1, 6, 2]], "three items"), (None, [["Pens"], [49], [10]], "discounted item"), (None, [["A", "B"], [1, 3333], [10, 1]], "mixed"), (None, [["Cake"], [1999], [1]], "vat rounds down")]),
]
rubric = [
 ("Decomposition", "Everything in one long method, or the same calculation written twice", "Some helper methods, but with repetition or an unclear split", "Small methods with clear names; receipt and subtotal reuse lineTotal and formatMoney"),
 ("Naming and readability", "Single-letter names and no structure a reader can follow", "Mostly clear, with some confusing names or layout", "Names say what things mean; consistent layout; no unnecessary comments or tricks"),
 ("Edge cases", "Fails for empty baskets or boundary quantities", "Handles most edges but misses one (for example exactly 10, or the sign of money)", "Empty basket, exactly 10, 9, zero quantity, rounding, all behave as specified"),
 ("Design note", "Missing or only describes what the code does", "Explains the split but not the trade-offs or the hardest case", "Explains the decomposition, names the hardest edge case, and says how it is handled"),
]
project("j1-p2-receipt", "Shopping basket and receipt", "B",
    "Price a basket with bulk discounts and print an exact receipt, designing the program yourself.",
    """
    A small shop needs a receipt generator. You're given **requirements and tests, but no instructions**: decide how to split the problem into methods, write them, and check them.

    This is an **independent build**: nobody writes your design for you. (The AI mentor isn't available inside projects yet.) If you want a refresher on any idea, the lessons are linked from [Decomposing problems](/lessons/j1-l5.4).

    Money is **whole pence in an `int`**. A basket is three parallel arrays: item names, unit prices and quantities, where item *i* uses index *i* of each.
    """, 4, ["j1-l5.4", "j1-l6.2"], ["J1.02", "J1.04", "J1.07", "J1.08", "J1.09", "J1.10"],
    ["Prices, quantities and totals are whole pence in an int, never a double.",
     "A line with 10 or more of an item gets 10% off that line, in whole pence rounded down.",
     "VAT is 20% of the subtotal, in whole pence rounded down.",
     "The receipt layout in milestone 4 is exact: spaces, capitals and line order all count."],
    ["Use at least four methods, and keep each one to 25 lines or fewer.", "Never repeat a calculation: reuse a method instead."],
    ["Given an empty basket, then the receipt has only the Subtotal, VAT and Total lines, all £0.00.",
     "Given 10 of an item at 49p, then its line shows £4.41 (10% off £4.90) and VAT is calculated from the discounted subtotal.",
     "Given 9 of an item, then no discount is applied.",
     "Given a negative or zero-pence amount, then formatMoney shows two digits of pence, with a leading minus sign for negatives."],
    ms, rubric,
    "In 150 words or fewer: How did you split the program into methods, and why there? Which case was hardest to get right, and how did you handle it?",
    STARTER, SOLUTION, wrongs)
print("P2 written")
