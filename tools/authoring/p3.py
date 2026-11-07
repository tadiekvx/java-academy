from proj import *

def fmt(p):
    sign = "-" if p < 0 else ""
    a = abs(p)
    return f"{sign}£{a // 100}.{a % 100:02d}"
def bal(t): return sum(t)
def can(b, amt, od): return amt > 0 and b - amt >= -od
def with_tx(t, a): return t + [a]
def mini(t, n):
    recent = t[::-1][:n]
    lines = [("Deposit " if x >= 0 else "Withdrawal ") + fmt(abs(x)) for x in recent]
    return "\n".join(lines + [f"Balance: {fmt(sum(t))}"])
def remaining(today, limit): return max(0, limit - sum(-x for x in today if x < 0))
def can_today(b, amt, od, today, limit): return can(b, amt, od) and amt <= remaining(today, limit)

SOLUTION = '''
String formatMoney(int pence) {
    String sign = pence < 0 ? "-" : "";
    int absolute = Math.abs(pence);
    String padding = absolute % 100 < 10 ? "0" : "";
    return sign + "£" + absolute / 100 + "." + padding + absolute % 100;
}

int balance(int[] transactions) {
    int total = 0;
    for (int transaction : transactions) {
        total += transaction;
    }
    return total;
}

boolean canWithdraw(int balance, int amount, int overdraftLimit) {
    return amount > 0 && balance - amount >= -overdraftLimit;
}

int[] withTransaction(int[] transactions, int amount) {
    int[] updated = Arrays.copyOf(transactions, transactions.length + 1);
    updated[transactions.length] = amount;
    return updated;
}

String miniStatement(int[] transactions, int count) {
    String text = "";
    int shown = 0;
    for (int i = transactions.length - 1; i >= 0 && shown < count; i--) {
        int amount = transactions[i];
        text += (amount >= 0 ? "Deposit " : "Withdrawal ") + formatMoney(Math.abs(amount)) + "\\n";
        shown++;
    }
    return text + "Balance: " + formatMoney(balance(transactions));
}

int dailyWithdrawalRemaining(int[] todaysTransactions, int dailyLimit) {
    int withdrawn = 0;
    for (int transaction : todaysTransactions) {
        if (transaction < 0) {
            withdrawn += -transaction;
        }
    }
    return Math.max(0, dailyLimit - withdrawn);
}

boolean canWithdrawToday(int balance, int amount, int overdraftLimit, int[] todaysTransactions, int dailyLimit) {
    return canWithdraw(balance, amount, overdraftLimit) && amount <= dailyWithdrawalRemaining(todaysTransactions, dailyLimit);
}

void main() {
    int[] history = {10000, -2500};
    history = withTransaction(history, 4000);
    IO.println(miniStatement(history, 2));
}
'''
STARTER = '''
// Brightbank, stage 1: the account logic. Money is whole pence in an int.
// A transaction is positive for a deposit and negative for a withdrawal; an account is its int[] of transactions.
// The methods are stubs that compile but give the wrong answers. The brief and milestones say what each must do.

String formatMoney(int pence) {
    return "";
}

int balance(int[] transactions) {
    return 0;
}

boolean canWithdraw(int balance, int amount, int overdraftLimit) {
    return false;
}

int[] withTransaction(int[] transactions, int amount) {
    return transactions;
}

String miniStatement(int[] transactions, int count) {
    return "";
}

int dailyWithdrawalRemaining(int[] todaysTransactions, int dailyLimit) {
    return 0;
}

boolean canWithdrawToday(int balance, int amount, int overdraftLimit, int[] todaysTransactions, int dailyLimit) {
    return false;
}

void main() {
    // Optional: try your methods out here.
}
'''
S = SOLUTION
wrongs = {
  "m1-no-padding": S.replace('    String padding = absolute % 100 < 10 ? "0" : "";\n', '    String padding = "";\n'),
  "m2-counts-only-deposits": S.replace("total += transaction;", "if (transaction > 0) {\n            total += transaction;\n        }"),
  "m3-allows-zero-and-negative": S.replace("return amount > 0 && balance - amount >= -overdraftLimit;", "return balance - amount >= -overdraftLimit;"),
  "m3-overdraft-exclusive": S.replace("balance - amount >= -overdraftLimit", "balance - amount > -overdraftLimit"),
  "m4-changes-the-original": S.replace("int[] updated = Arrays.copyOf(transactions, transactions.length + 1);", "int[] updated = transactions;"),
  "m5-oldest-first": S.replace("for (int i = transactions.length - 1; i >= 0 && shown < count; i--) {", "for (int i = 0; i < transactions.length && shown < count; i++) {"),
  "m5-shows-all": S.replace("&& shown < count", ""),
  "m6-counts-deposits": S.replace("        if (transaction < 0) {\n            withdrawn += -transaction;\n        }", "        withdrawn += Math.abs(transaction);"),
  "m6-ignores-daily-limit": S.replace("&& amount <= dailyWithdrawalRemaining(todaysTransactions, dailyLimit)", ""),
}
T = [[], [10000], [10000, -2500], [5000, -1000, 250, -4000], [100, 100, 100, 100, 100, 100], [-300, -200, 500]]
ms = [
 dict(id="m1", title="Money as text", methods=[("formatMoney", [("pence", "int")], "String")], fns={"formatMoney": fmt},
  instructions="`formatMoney(int pence)` returns whole pence as `£12.34`, with two digits of pence and a leading `-` for negatives (`-105` → `-£1.05`, `5` → `£0.05`). You may reuse your formatter from the receipt project, but write it again here from the specification.",
  visible=[(None, [1234]), (None, [5]), (None, [-105])],
  hidden=[(None, [0], "zero"), (None, [100], "exactly a pound"), (None, [10], "ten pence"), (None, [99999], "large"), (None, [-5], "negative pence")]),
 dict(id="m2", title="The balance", methods=[("balance", [("transactions", "int[]")], "int")], fns={"balance": bal},
  instructions="`balance(transactions)` returns the account balance: the sum of every transaction (positive deposits, negative withdrawals). A new account's balance is 0.",
  visible=[(None, [[]]), (None, [[10000, -2500]]), (None, [[5000, -1000, 250, -4000]])],
  hidden=[(None, [[-300, -200, 500]], "ends at zero"), (None, [[-100]], "overdrawn"), (None, [[1, 1, 1]], "small"), (None, [[100000, -99999]], "one left"), (None, [[0]], "zero transaction")]),
 dict(id="m3", title="Can I withdraw?", methods=[("canWithdraw", [("balance", "int"), ("amount", "int"), ("overdraftLimit", "int")], "boolean")], fns={"canWithdraw": can},
  instructions="`canWithdraw(balance, amount, overdraftLimit)` says whether a withdrawal is allowed. The amount must be **positive** (you can't withdraw zero or a negative amount). After the withdrawal the balance must not fall below minus the overdraft limit: with a £100 (10000 pence) overdraft, a balance of -£100 is allowed but -£100.01 is not.",
  visible=[(None, [5000, 2000, 0]), (None, [1000, 2000, 0]), (None, [1000, 2000, 5000])],
  hidden=[(None, [1000, 1000, 0], "exactly to zero"), (None, [1000, 11000, 10000], "exactly to the limit"), (None, [1000, 11001, 10000], "one over the limit"), (None, [1000, 0, 10000], "zero amount"), (None, [1000, -50, 10000], "negative amount"), (None, [-5000, 5000, 10000], "already overdrawn")]),
 dict(id="m4", title="Record a transaction", methods=[("withTransaction", [("transactions", "int[]"), ("amount", "int")], "int[]")], fns={"withTransaction": with_tx},
  instructions="`withTransaction(transactions, amount)` returns a **new** array: the same transactions with `amount` added at the end. The original array must not be changed (other code may still be using it). Arrays can't grow, so the new one must be a copy.",
  visible=[(None, [[], 500]), (None, [[10000], -2500]), (None, [[1, 2, 3], 4])],
  hidden=[(None, [[100, 200], 0], "zero amount"), (None, [[-5], -5], "repeated value"), (None, [[7, 7, 7, 7], 7], "four sevens"), (None, [[0], 99999], "large")]),
 dict(id="m5", title="Mini statement", methods=[("miniStatement", [("transactions", "int[]"), ("count", "int")], "String")], fns={"miniStatement": mini},
  instructions="""
  `miniStatement(transactions, count)` returns a string of lines separated by `\\n` (no `\\n` after the last line):

  - the **most recent** `count` transactions, **newest first**, one per line, as `Deposit £5.00` or `Withdrawal £25.00` (the amount is always shown positive; a transaction of zero counts as a deposit);
  - then a last line `Balance: ` and the **whole** account balance (not just the shown transactions).

  If there are fewer than `count` transactions, show them all. If there are none, there is only the balance line.
  """,
  visible=[(None, [[], 5]), (None, [[10000, -2500], 5]), (None, [[5000, -1000, 250, -4000], 2])],
  hidden=[(None, [[100, 100, 100, 100, 100, 100], 3], "last three of six"), (None, [[-300, -200, 500], 0], "count zero"), (None, [[10000], 1], "exactly one"), (None, [[-300, -200, 500], 3], "exactly all"), (None, [[0, 0], 5], "zero transactions"), (None, [[100, -100], 1], "latest only")]),
 dict(id="m6", title="Change request: a daily limit", methods=[("dailyWithdrawalRemaining", [("todaysTransactions", "int[]"), ("dailyLimit", "int")], "int"), ("canWithdrawToday", [("balance", "int"), ("amount", "int"), ("overdraftLimit", "int"), ("todaysTransactions", "int[]"), ("dailyLimit", "int")], "boolean")],
  fns={"dailyWithdrawalRemaining": remaining, "canWithdrawToday": can_today},
  instructions="""
  **A change request has arrived.** The bank is adding a **daily withdrawal limit**. Without breaking milestones 1–5:

  - `dailyWithdrawalRemaining(todaysTransactions, dailyLimit)` returns how much more may be withdrawn today: the limit minus the total already withdrawn today (deposits don't count). It's never below 0.
  - `canWithdrawToday(balance, amount, overdraftLimit, todaysTransactions, dailyLimit)` allows a withdrawal only if `canWithdraw` would allow it **and** the amount doesn't exceed what remains of today's allowance.

  Reuse what you already have; don't copy its logic.
  """,
  visible=[("dailyWithdrawalRemaining", [[], 30000]), ("dailyWithdrawalRemaining", [[-10000, 5000], 30000]), ("canWithdrawToday", [100000, 5000, 0, [-10000], 30000])],
  hidden=[("dailyWithdrawalRemaining", [[-40000], 30000], "over the limit already"), ("dailyWithdrawalRemaining", [[5000], 30000], "only deposits"), ("canWithdrawToday", [100000, 20000, 0, [-10000], 30000], "exactly the allowance"), ("canWithdrawToday", [100000, 20001, 0, [-10000], 30000], "one over the allowance"), ("canWithdrawToday", [1000, 5000, 0, [], 30000], "daily fine, balance not"), ("canWithdrawToday", [100000, 0, 0, [], 30000], "zero amount")]),
]
rubric = [
 ("Correctness at the edges", "Several milestones fail on boundary values (exactly at a limit, empty, zero)", "Passes typical cases and most boundaries", "Every boundary in the brief behaves as specified, including the change request"),
 ("Reuse and decomposition", "The same logic written in several places", "Some reuse, but some repetition remains", "Each rule written once; later methods call earlier ones"),
 ("Handling the change request", "Milestones 1–5 broke when milestone 6 was added", "Milestone 6 works but required copying logic", "Milestone 6 was added by calling existing methods; milestones 1–5 still pass"),
 ("Design note", "Missing or describes the code line by line", "Explains the split but not the money or array decisions", "Explains why money is pence, why withTransaction copies, and what the change request taught you"),
]
project("j1-p3-brightbank", "Brightbank account logic", "B",
    "Build the rules of a bank account from requirements, then absorb a change request without breaking what you wrote.",
    """
    **Brightbank** is the application you'll grow throughout this course. This is its first stage: the *rules* of a bank account, with no screens yet.

    An account is represented by an `int[]` of **transactions** in whole pence: positive for a deposit, negative for a withdrawal. You'll write methods that compute the balance, decide whether a withdrawal is allowed, record a transaction, and produce a mini statement.

    This is an **independent build**, with a twist: partway through, a **change request** arrives (milestone 6). The way you structured milestones 1–5 decides how painful it is, which is the lesson. Later in the course you'll come back and restructure this program with classes (Stage 2, object-oriented programming), and you'll see why parallel arrays and loose methods get awkward.
    """, 5, ["j1-l5.4", "j1-l6.2"], ["J1.02", "J1.06", "J1.08", "J1.09", "J1.10"],
    ["Money is whole pence in an int. Deposits are positive transactions; withdrawals are negative.",
     "An overdraft limit is the most the balance may fall below zero.",
     "Methods must not modify arrays passed in unless the milestone says so."],
    ["Write each rule once and reuse it.", "No method longer than 25 lines."],
    ["Given a balance of £10.00, an overdraft of £100, and a £110.00 withdrawal, then it is allowed; a £110.01 withdrawal is not.",
     "Given 6 transactions and count 3, then the statement shows the 3 newest, newest first, and the balance of all 6.",
     "Given the daily limit change request, then milestones 1 to 5 still pass unchanged.",
     "Given a withdrawal of zero or a negative amount, then it is never allowed."],
    ms, rubric,
    "In 150 words or fewer: Why did withTransaction have to copy the array? Which of your methods was easiest to change when the daily limit arrived, and which was hardest?",
    STARTER, SOLUTION, wrongs)
print("P3 written")
