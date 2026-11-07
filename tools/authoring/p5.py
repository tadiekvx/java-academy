import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-2"
from proj import *

def fmt(p):
    sign = "-" if p < 0 else ""
    a = abs(p)
    return f"{sign}£{a // 100}.{a % 100:02d}"

def sim(overdraft, fee, ops, savings=False):
    """Independent model of the account rules. Returns (output tokens, balance, history list)."""
    bal, hist, out = 0, [], []
    for op in ops:
        k, n = op.split(":"); n = int(n)
        if k == "i":
            interest = bal * n // 100
            if interest > 0:
                bal += interest; hist.append(("D", interest))
            continue
        if n <= 0:
            out.append("invalid"); continue
        if k == "d":
            bal += n; hist.append(("D", n)); out.append("ok")
        else:
            total = n + fee
            if bal - total < -overdraft:
                out.append(f"short by {total - bal - overdraft}")
            else:
                bal -= n; hist.append(("W", n))
                if fee: bal -= fee; hist.append(("W", fee))
                out.append("ok")
    return out, bal, hist

def m1(overdraft, ops):
    out, bal, _ = sim(overdraft, 0, ops)
    return "".join(t + " " for t in out) + f"balance {bal}"
def m2(ops):
    _, bal, hist = sim(0, 0, ops)
    return f"{len(hist)} {bal}"
def m3(overdraft, ops, count):
    _, bal, hist = sim(overdraft, 0, ops)
    lines = [("Deposit " if k == "D" else "Withdrawal ") + fmt(n) for k, n in hist[::-1][:count]]
    return "\n".join(lines + [f"Balance: {fmt(bal)}"])
def m4(kind, ops):
    savings = kind == "savings"
    out, bal, _ = sim(0 if savings else 10000, 0 if savings else 50, ops)
    return "".join(t + " " for t in out) + f"balance {bal}"

PRELUDE = '''
class Money {
    static String format(int pence) {
        String sign = pence < 0 ? "-" : "";
        int absolute = Math.abs(pence);
        String padding = absolute % 100 < 10 ? "0" : "";
        return sign + "£" + absolute / 100 + "." + padding + absolute % 100;
    }
}

sealed interface Transaction permits Deposit, Withdrawal {}

record Deposit(int amount) implements Transaction {}

record Withdrawal(int amount) implements Transaction {}

class InsufficientFundsException extends Exception {
    final int shortBy;

    InsufficientFundsException(int shortBy) {
        super("short by " + Money.format(shortBy));
        this.shortBy = shortBy;
    }
}
'''
DRIVERS = '''
// ---------------------------------------------------------------------------------------------
// The checks call these methods. They show how your classes will be used. Don't change them.
// ---------------------------------------------------------------------------------------------

String m1(int overdraft, String[] ops) {
    Account a = new Account(overdraft);
    StringBuilder out = new StringBuilder();
    for (String op : ops) {
        String[] p = op.split(":");
        int n = Integer.parseInt(p[1]);
        try {
            if (p[0].equals("d")) {
                a.deposit(n);
            } else {
                a.withdraw(n);
            }
            out.append("ok ");
        } catch (InsufficientFundsException e) {
            out.append("short by ").append(e.shortBy).append(" ");
        } catch (IllegalArgumentException e) {
            out.append("invalid ");
        }
    }
    return out + "balance " + a.balance();
}

String m2(String[] ops) {
    Account a = new Account(0);
    for (String op : ops) {
        String[] p = op.split(":");
        int n = Integer.parseInt(p[1]);
        try {
            if (p[0].equals("d")) {
                a.deposit(n);
            } else {
                a.withdraw(n);
            }
        } catch (InsufficientFundsException | IllegalArgumentException e) {
            // refused: not recorded
        }
    }
    List<Transaction> h = a.history();
    try {
        h.clear();
        h.add(new Deposit(999));
    } catch (UnsupportedOperationException e) {
        // an unmodifiable list refused: fine
    }
    return a.history().size() + " " + a.balance();
}

String m3(int overdraft, String[] ops, int count) {
    Account a = new Account(overdraft);
    for (String op : ops) {
        String[] p = op.split(":");
        int n = Integer.parseInt(p[1]);
        try {
            if (p[0].equals("d")) {
                a.deposit(n);
            } else {
                a.withdraw(n);
            }
        } catch (InsufficientFundsException | IllegalArgumentException e) {
            // refused
        }
    }
    return a.miniStatement(count);
}

String m4(String type, String[] ops) {
    Account a = type.equals("savings") ? new SavingsAccount() : new CurrentAccount();
    StringBuilder out = new StringBuilder();
    for (String op : ops) {
        String[] p = op.split(":");
        int n = Integer.parseInt(p[1]);
        try {
            if (p[0].equals("i")) {
                ((SavingsAccount) a).addInterest(n);
                continue;
            }
            if (p[0].equals("d")) {
                a.deposit(n);
            } else {
                a.withdraw(n);
            }
            out.append("ok ");
        } catch (InsufficientFundsException e) {
            out.append("short by ").append(e.shortBy).append(" ");
        } catch (IllegalArgumentException e) {
            out.append("invalid ");
        }
    }
    return out + "balance " + a.balance();
}

void main() {
    // Optional: try your classes out here.
}
'''
SOLUTION_CLASSES = '''
class Account {
    private final int overdraftLimit;
    private int balance;
    private final List<Transaction> history = new ArrayList<>();

    Account(int overdraftLimit) {
        this.overdraftLimit = overdraftLimit;
    }

    // The fee charged on each successful withdrawal. A hook for subclasses.
    int fee() {
        return 0;
    }

    void deposit(int amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("a deposit must be positive");
        }
        balance += amount;
        history.add(new Deposit(amount));
    }

    void withdraw(int amount) throws InsufficientFundsException {
        if (amount <= 0) {
            throw new IllegalArgumentException("a withdrawal must be positive");
        }
        int total = amount + fee();
        if (balance - total < -overdraftLimit) {
            throw new InsufficientFundsException(total - balance - overdraftLimit);
        }
        balance -= amount;
        history.add(new Withdrawal(amount));
        if (fee() > 0) {
            balance -= fee();
            history.add(new Withdrawal(fee()));
        }
    }

    int balance() {
        return balance;
    }

    List<Transaction> history() {
        return new ArrayList<>(history);
    }

    String miniStatement(int count) {
        StringBuilder text = new StringBuilder();
        int shown = 0;
        for (int i = history.size() - 1; i >= 0 && shown < count; i--) {
            String line = switch (history.get(i)) {
                case Deposit d -> "Deposit " + Money.format(d.amount());
                case Withdrawal w -> "Withdrawal " + Money.format(w.amount());
            };
            text.append(line).append("\\n");
            shown++;
        }
        return text + "Balance: " + Money.format(balance);
    }
}

class CurrentAccount extends Account {
    CurrentAccount() {
        super(10000);
    }

    @Override
    int fee() {
        return 50;
    }
}

class SavingsAccount extends Account {
    SavingsAccount() {
        super(0);
    }

    void addInterest(int percent) {
        int interest = balance() * percent / 100;
        if (interest > 0) {
            deposit(interest);
        }
    }
}
'''
SOLUTION = PRELUDE + SOLUTION_CLASSES + DRIVERS
STARTER = '''// Brightbank v2: the same rules as stage 1, now as classes.
// Money is whole pence. A transaction is a Deposit or a Withdrawal record (given below).
// The classes at the bottom compile but are stubs that give wrong answers. The brief says what they must do.
''' + PRELUDE + '''
class Account {
    // TODO: fields, rules, history

    Account(int overdraftLimit) {
    }

    void deposit(int amount) {
    }

    void withdraw(int amount) throws InsufficientFundsException {
    }

    int balance() {
        return 0;
    }

    List<Transaction> history() {
        return List.of();
    }

    String miniStatement(int count) {
        return "";
    }
}

// Milestone 4 (the change request) needs these two. They already compile.
class CurrentAccount extends Account {
    CurrentAccount() {
        super(0);
    }
}

class SavingsAccount extends Account {
    SavingsAccount() {
        super(0);
    }

    void addInterest(int percent) {
    }
}
''' + DRIVERS
S = SOLUTION
wrongs = {
  "m1-accepts-zero-deposit": S.replace("if (amount <= 0) {\n            throw new IllegalArgumentException(\"a deposit must be positive\");", "if (amount < 0) {\n            throw new IllegalArgumentException(\"a deposit must be positive\");"),
  "m1-overdraft-exclusive": S.replace("if (balance - total < -overdraftLimit) {", "if (balance - total <= -overdraftLimit) {"),
  "m1-shortby-ignores-balance": S.replace("total - balance - overdraftLimit", "total"),
  "m2-leaks-the-history": S.replace("return new ArrayList<>(history);", "return history;"),
  "m2-records-refused": S.replace("        int total = amount + fee();\n        if (balance - total < -overdraftLimit) {\n            throw", "        int total = amount + fee();\n        history.add(new Withdrawal(0));\n        if (balance - total < -overdraftLimit) {\n            throw"),
  "m3-oldest-first": S.replace("for (int i = history.size() - 1; i >= 0 && shown < count; i--) {", "for (int i = 0; i < history.size() && shown < count; i++) {"),
  "m3-no-count-limit": S.replace(" && shown < count", ""),
  "m4-no-fee": S.replace("        return 50;", "        return 0;"),
  "m4-savings-can-overdraw": S.replace("super(0);\n    }\n\n    void addInterest", "super(10000);\n    }\n\n    void addInterest"),
  "m4-interest-rounds-up": S.replace("int interest = balance() * percent / 100;", "int interest = (balance() * percent + 99) / 100;"),
}
ms = [
 dict(id="m1", title="The account and its rules", methods=[("m1", [("overdraft", "int"), ("ops", "String[]")], "String")], fns={"m1": m1},
  instructions="""
  Write `Account(int overdraftLimit)` with `deposit`, `withdraw` and `balance`. The rules:

  - A deposit or withdrawal amount must be **positive**. Otherwise throw an `IllegalArgumentException` and change nothing.
  - A withdrawal may take the balance down to **minus the overdraft limit**, and no further. If it would go past that, throw the (already written) `InsufficientFundsException`, with `shortBy` set to **how many pence too many** it asked for, and leave the balance alone.
  - Make the account's data `private`.

  The check calls `m1`, which applies a list of operations such as `"d:500"` and `"w:200"` and prints `ok`, `invalid` or `short by <n>` for each, then the final balance.
  """,
  visible=[(None, [0, ["d:500", "w:200"]]), (None, [0, ["w:100"]]), (None, [0, ["d:0", "w:-5"]])],
  hidden=[(None, [10000, ["w:10000"]], "exactly to the limit"), (None, [10000, ["w:10001"]], "one past the limit"), (None, [0, ["d:100", "w:100"]], "exactly to zero"), (None, [500, ["d:100", "w:700", "w:100"]], "short by with some money"), (None, [0, []], "no operations"), (None, [0, ["d:1", "d:1", "w:1", "w:5"]], "mixed")]),
 dict(id="m2", title="A history that can't be tampered with", methods=[("m2", [("ops", "String[]")], "String")], fns={"m2": m2},
  instructions="""
  Record each **successful** deposit and withdrawal in the account's history, as a `Deposit` or `Withdrawal` record. `history()` returns the list of transactions, oldest first.

  Refused operations aren't recorded. And code outside the account must not be able to change the account by changing the list it gets: the check tries to clear the list it receives, and add to it, then looks at the account again.

  `m2` returns the number of transactions in the history, then the balance, e.g. `2 300`.
  """,
  visible=[(None, [["d:500", "w:200"]]), (None, [[]]), (None, [["w:100", "d:50"]])],
  hidden=[(None, [["d:100", "d:100", "d:100"]], "three deposits"), (None, [["d:0", "w:0"]], "invalid only"), (None, [["d:100", "w:101"]], "refused withdrawal"), (None, [["d:5", "w:5", "d:5", "w:5"]], "back to zero"), (None, [["w:1", "w:2", "w:3"]], "all refused")]),
 dict(id="m3", title="The mini statement", methods=[("m3", [("overdraft", "int"), ("ops", "String[]"), ("count", "int")], "String")], fns={"m3": m3},
  instructions="""
  `miniStatement(count)` returns text lines separated by `\\n` (none after the last line): the **most recent** `count` transactions, **newest first**, as `Deposit £5.00` or `Withdrawal £25.00` (use the supplied `Money.format`), then a final line `Balance: ` with the **whole** balance. If there are fewer than `count`, show them all. If there are none, only the balance line.

  Write the lines with a pattern-matching `switch` over the sealed `Transaction` type, without a `default`, so a future transaction type can't be forgotten.
  """,
  visible=[(None, [0, ["d:10000", "w:2500"], 5]), (None, [0, [], 3]), (None, [0, ["d:5000", "w:1000", "d:250", "w:4000"], 2])],
  hidden=[(None, [0, ["d:100", "d:100", "d:100", "d:100", "d:100", "d:100"], 3], "last three of six"), (None, [0, ["d:500", "w:200"], 0], "count zero"), (None, [10000, ["w:300", "d:500"], 5], "overdrawn then paid in"), (None, [0, ["d:5"], 1], "exactly one"), (None, [0, ["d:100", "w:1", "d:100"], 3], "exactly all"), (None, [0, ["d:500", "w:900", "d:5"], 2], "refused ones are not shown")]),
 dict(id="m4", title="Change request: account types", methods=[("m4", [("type", "String"), ("ops", "String[]")], "String")], fns={"m4": m4},
  instructions="""
  **A change request has arrived.** The bank now has two kinds of account. Add them **without breaking milestones 1 to 3** (a plain `Account` must keep working exactly as before):

  - **`CurrentAccount`**: an overdraft limit of 10000 pence (£100), and a **fee of 50 pence on every successful withdrawal**. The fee is part of what a withdrawal costs: the withdrawal is refused if the amount **plus the fee** would pass the overdraft limit, and `shortBy` counts the fee. A successful withdrawal records the withdrawal and the fee as two transactions.
  - **`SavingsAccount`**: **never** overdrawn (limit 0), no fee, and `addInterest(percent)` which deposits `balance * percent / 100` pence (**rounded down**) if that comes to more than 0.

  Don't copy the withdrawal rules into the new classes: decide what is the same and what differs, and put each rule in one place.

  `m4` uses `"current"` or `"savings"`, applies the operations (including `"i:5"` for 5 per cent interest on savings), and prints the results and the final balance.
  """,
  visible=[(None, ["current", ["d:1000", "w:500"]]), (None, ["savings", ["d:1000", "w:2000"]]), (None, ["savings", ["d:1000", "i:5"]])],
  hidden=[(None, ["current", ["w:9950"]], "exactly to the limit with the fee"), (None, ["current", ["w:9951"]], "one past the limit"), (None, ["savings", ["d:99", "i:5"]], "interest rounds down to 4"), (None, ["savings", ["d:10", "i:5"]], "interest rounds down to 0"), (None, ["current", ["d:100", "w:100", "w:100"]], "fee on each withdrawal"), (None, ["savings", ["d:100", "w:100", "w:1"]], "no overdraft")]),
]
rubric = [
 ("Correctness at the edges", "Several milestones fail at the limits (exactly at the overdraft, zero, no transactions)", "Typical cases pass and most limits", "Every limit in the brief behaves as specified, including the fee"),
 ("Encapsulation", "Account data is public, or the history can be changed from outside", "Fields are private but a copy or a check is missing in one route", "Fields private, input checked, and the history can't be used to change the account"),
 ("Handling the change request", "Milestones 1 to 3 broke, or the withdrawal rules were copied into each subclass", "It works, but some rule is written twice", "The shared rules live once in Account; subclasses only supply what differs"),
 ("Design note", "Missing, or describes the code line by line", "Explains the classes but not the choices", "Explains each design choice (checked exception, copies, the fee hook) and what you would do if a third account type arrived"),
]
project("j2-p1-brightbank", "Brightbank as classes", "B",
    "Rebuild the Brightbank account as classes, then absorb a change request with two new account types.",
    """
    In Stage 1 you wrote Brightbank as loose methods working on an `int[]` of transactions. Now it becomes a set of **classes**, which is what the object-oriented stage is for.

    The pieces you are given: `Money.format`, a sealed `Transaction` type with `Deposit` and `Withdrawal` records, and the checked `InsufficientFundsException`. You write `Account`, and later `CurrentAccount` and `SavingsAccount`.

    This is an **independent build**: the brief tells you the rules and the checks, and you decide how to structure the code. Halfway through, a **change request** arrives (milestone 4). How you built milestones 1 to 3 decides how easy it is to absorb.

    There is one source file, so the compiler won't stop other code from touching your private fields (all the classes are in one file). The checks look at behaviour, so treat `private` as part of the job and respect it anyway.
    """, 6, ["j2-l2.1", "j2-l2.2", "j2-l3.2", "j2-l4.2", "j2-l5.2"], ["J2.05", "J2.06", "J2.08", "J2.11", "J2.13"],
    ["Money is whole pence in an int.",
     "A deposit or withdrawal must be positive, otherwise an IllegalArgumentException is thrown.",
     "A refused withdrawal throws InsufficientFundsException and changes nothing.",
     "The history lists successful transactions only, oldest first."],
    ["Account data is private.", "Each rule is written once.", "No `default` branch in the switch over `Transaction`."],
    ["Given an overdraft of 10000, when 10000 is withdrawn from an empty account, then it's allowed; 10001 is refused with `short by 1`.",
     "Given a history returned by `history()`, when the caller clears it, then the account's history is unchanged.",
     "Given a current account with a balance of 1000, when 500 is withdrawn, then the balance is 450.",
     "Given the change request, then milestones 1 to 3 still pass unchanged."],
    ms, rubric,
    "In 150 words or fewer: Which of your design choices made milestone 4 easier or harder? Why is `InsufficientFundsException` checked, while a negative amount throws an unchecked exception? What would you change if a third account type arrived?",
    STARTER, SOLUTION, wrongs)
print("P5 written")
