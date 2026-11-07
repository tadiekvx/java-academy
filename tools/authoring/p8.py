import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-4"
from proj import *

def domestic(g): return 300 if g <= 500 else 450 if g <= 2000 else 450 + ((g - 2000 + 999) // 1000) * 100
def intl(g): return 800 if g <= 500 else 1200 if g <= 2000 else 1200 + ((g - 2000 + 999) // 1000) * 250
def quote(g, express, country):
    if g <= 0 or country == "": return "rejected"
    c = domestic(g) if country == "UK" else intl(g)
    return f"cost={c * 2 if express else c}"
def quote_valid(g, express, country):
    c = domestic(g) if country == "UK" else intl(g)
    return f"cost={c * 2 if express else c}"

DRV = '''
// ---------------------------------------------------------------------------------------------
// The callers of the calculator. Don't change them.
// ---------------------------------------------------------------------------------------------

String quote(int grams, boolean express, String country) {
    try {
        return "cost=" + shippingCost(grams, express, country);
    } catch (IllegalArgumentException e) {
        return "rejected";
    }
}

void main() {
    // Optional: try the calculator out here.
}
'''
INHERITED = '''
// INHERITED CODE: the shipping calculator for the shop. Costs are in pence.
// Ticket 482: "Customers in the US are being charged the UK (domestic) price."

int shippingCost(int grams, boolean express, String country) {
    int cost;
    if (country.startsWith("U")) {
        if (grams <= 500) {
            cost = 300;
        } else if (grams <= 2000) {
            cost = 450;
        } else {
            cost = 450 + ((grams - 2000 + 999) / 1000) * 100;
        }
    } else {
        if (grams <= 500) {
            cost = 800;
        } else if (grams <= 2000) {
            cost = 1200;
        } else {
            cost = 1200 + ((grams - 2000 + 999) / 1000) * 250;
        }
    }
    if (express) {
        cost = cost * 2;
    }
    return cost;
}
'''
FINAL = '''
// The shipping calculator for the shop. Costs are in pence.

int shippingCost(int grams, boolean express, String country) {
    if (grams <= 0) {
        throw new IllegalArgumentException("weight must be positive: " + grams);
    }
    if (country.isEmpty()) {
        throw new IllegalArgumentException("a country is required");
    }
    int cost = country.equals("UK") ? domesticCost(grams) : internationalCost(grams);
    return express ? cost * 2 : cost;
}

int domesticCost(int grams) {
    if (grams <= 500) {
        return 300;
    }
    if (grams <= 2000) {
        return 450;
    }
    return 450 + extraKilos(grams) * 100;
}

int internationalCost(int grams) {
    if (grams <= 500) {
        return 800;
    }
    if (grams <= 2000) {
        return 1200;
    }
    return 1200 + extraKilos(grams) * 250;
}

// Whole kilograms (rounded up) beyond the first 2 kg.
int extraKilos(int grams) {
    return (grams - 2000 + 999) / 1000;
}
'''
SOLUTION = FINAL + DRV
STARTER = INHERITED + DRV
S = SOLUTION
wrongs = {
  "m1-treats-ireland-as-domestic": S.replace('country.equals("UK") ?', '(country.equals("UK") || country.equals("IE")) ?'),
  "m2-changes-a-boundary": S.replace("if (grams <= 500) {\n        return 300;", "if (grams < 500) {\n        return 300;"),
  "m2-not-extracted": INHERITED.replace('country.startsWith("U")', 'country.equals("UK")') + DRV,
  "m3-rejects-only-negative": S.replace("if (grams <= 0) {", "if (grams < 0) {"),
  "m3-accepts-an-empty-country": S.replace('    if (country.isEmpty()) {\n        throw new IllegalArgumentException("a country is required");\n    }\n', ""),
}
M1_V = [(None, [250, False, "UK"]), (None, [1500, True, "US"]), (None, [3500, False, "UK"])]
M1_H = [(None, [250, False, "US"], "the ticket: US is international"), (None, [250, False, "UA"], "another country starting with U"), (None, [2500, True, "UK"], "UK express over 2kg"), (None, [500, False, "IE"], "Ireland"), (None, [2001, False, "UK"], "just over 2kg"), (None, [100, True, "DE"], "express abroad"), (None, [500, False, "UK"], "exactly 500 grams"), (None, [500, False, "FR"], "exactly 500 grams abroad"), (None, [2000, False, "UK"], "exactly 2 kg")]
ms = [
 dict(id="m1", title="Fix ticket 482", methods=[("quote", [("grams", "int"), ("express", "boolean"), ("country", "String")], "String")], fns={"quote": quote_valid},
  instructions="""
  **Ticket 482:** *"Customers in the US are being charged the UK (domestic) price."*

  Start by **reproducing** it: call `quote(250, false, "US")` and compare with `quote(250, false, "UK")`. Then find the cause in `shippingCost`. Only customers in the **UK** pay domestic prices; every other country pays international prices. Make the smallest change that fixes it, and run all the checks.
  """,
  visible=M1_V, hidden=M1_H),
 dict(id="m2", title="Refactor under the tests", methods=[("quote", [("grams", "int"), ("express", "boolean"), ("country", "String")], "String")], fns={"quote": quote_valid},
  instructions="""
  The calculator works, but it's one long method with the same "round up to whole kilos" calculation written twice. Your teammates will have to change it soon, so **refactor it first**, now that the checks pin its behaviour down.

  Extract `int domesticCost(int grams)` and `int internationalCost(int grams)` (the price **before** any express charge), and put the repeated kilos calculation in one place. Don't change any answer: the same checks must still pass. The check also looks for the two new methods.
  """,
  visible=M1_V, hidden=M1_H,
  source_tests=[("domesticCost is extracted", ["int domesticCost("], None), ("internationalCost is extracted", ["int internationalCost("], None)]),
 dict(id="m3", title="Respond to the review", methods=[("quote", [("grams", "int"), ("express", "boolean"), ("country", "String")], "String")], fns={"quote": quote},
  instructions="""
  You open a pull request with your changes. The reviewer replies:

  > *"Thanks, much clearer. Two requests before we merge: a weight of zero or less makes no sense, and an empty country would silently be charged the international price. Both should be rejected, not priced."*

  Make `shippingCost` throw an `IllegalArgumentException` for a weight of **zero or less**, and for an **empty country**. (The caller `quote` turns the exception into `rejected`.) Valid orders must price exactly as before.
  """,
  visible=[(None, [250, False, "UK"]), (None, [0, False, "UK"]), (None, [250, False, ""])],
  hidden=[(None, [-5, False, "UK"], "negative weight"), (None, [1, False, "UK"], "one gram is valid"), (None, [500, True, "FR"], "valid order unchanged"), (None, [100, False, ""], "empty country"), (None, [0, True, ""], "both invalid"), (None, [2000, False, "US"], "valid, international")]),
]
rubric = [
 ("Reproduce, then fix", "Changed code without reproducing the ticket, or the fix is broader than the bug", "Fixed the bug but didn't confirm it with a failing case first", "Reproduced the ticket with a specific call, found the cause, and made the smallest fix"),
 ("Safe refactoring", "The refactor changed an answer, or was done without running the checks", "Behaviour unchanged but steps were large", "Small steps with the checks run after each; the structure is clearer and no answer changed"),
 ("Handling review", "The review comments were ignored, or fixed with a new bug", "Both requests done, but valid orders changed behaviour", "Both rejections added, valid orders unchanged, and the change kept separate from the refactor"),
 ("Design note", "Missing, or only says what the code does", "Describes the changes but not the reasoning", "Explains the cause of the bug, why the refactor was safe, and what you would test next"),
]
project("j4-a1-first-ticket", "First week on the job", "C",
    "Take over an inherited calculator: reproduce a bug ticket, refactor safely under the checks, and respond to a code review.",
    """
    It's your first week. You've been handed the shop's **shipping calculator**, written by someone who has left. There's a ticket, there's messy code, and a reviewer is waiting.

    This is what the stage prepared you for, in one task:

    1. **Fix a ticket** by reproducing the bug first, finding the cause, and making the smallest fix.
    2. **Refactor safely**: the code is hard to read and will have to change again. With the checks as a safety net, extract methods without changing a single answer.
    3. **Respond to review**: the reviewer asks for two more rejections. Add them without disturbing what already works.

    A real task like this would use a repository, a branch, commits and a pull request. This platform can't run Git, so work in one file here and think about what each milestone would be as a **commit with a clear message**, and which would be separate PRs. Your design note should say so.
    """, 3, ["j4-l3.2", "j4-l4.2", "j4-l4.3"], ["J4.05", "J4.06", "J4.08", "J4.09"],
    ["Only the UK pays domestic prices; every other country pays international prices.",
     "Refactoring must not change any answer.",
     "A weight of zero or less, and an empty country, must be rejected with an `IllegalArgumentException`.",
     "Valid orders price exactly as before."],
    ["Fix the bug and refactor in separate steps.", "Run all the checks after every change."],
    ["Given a US customer, then the international price applies.",
     "Given the refactor, then every earlier check still passes and `domesticCost` and `internationalCost` exist.",
     "Given a zero weight or an empty country, then the order is rejected.",
     "Given a valid order, then the price is unchanged by the review changes."],
    ms, rubric,
    "In 150 words or fewer: What caused the bug, and how did you reproduce it? How did you know the refactor changed no behaviour? If this were a real repository, what would your commits and pull requests have been, and what would their messages say?",
    STARTER, SOLUTION, wrongs)
print("P8 written")
