"""Stage 6 authoring: module 6.2 (Transactions and integrity)."""
import l6common
from l6common import Lesson, Exercises, q, register, sql_file, DB_HELPERS, CUSTOMERS, ACCOUNTS, TRANSACTIONS, accounts_of, money, accounts_of, customers_in
import build  # noqa: E402

build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-6"
ex21 = Exercises("j6-l2.1")
ex22 = Exercises("j6-l2.2")
ex23 = Exercises("j6-l2.3")


def full(method_source, main_call):
    return sql_file(method_source, main_call)


BAL = {1: 1200.00, 2: 300.50, 3: 0.00, 4: 780.25, 5: 50.00}


def f_transfer(*args):
    source, target, amount = args
    from_cents = round(float(BAL[source]) * 100) if source in BAL else None
    to_cents = round(float(BAL[target]) * 100) if target in BAL else None
    if from_cents is None or to_cents is None or from_cents - round(float(amount) * 100) < 0:
        return "23513"
    new_from = from_cents - round(float(amount) * 100)
    new_to = to_cents + round(float(amount) * 100)
    return l6common.money(new_from) + "|" + l6common.money(new_to)


def f_open(*args):
    customer_id, balance = args
    if customer_id in (1, 2, 3, 4, 5) and float(balance) > 0:
        return "accounts=1 transactions=1"
    return "accounts=0 transactions=0"


def f_withdraw(*args):
    aid, amount, expected = args
    expected_cents = round(float(expected) * 100)
    known = aid in BAL
    balance_cents = round(float(BAL[aid]) * 100) if known else None
    if known and balance_cents == expected_cents and balance_cents - round(float(amount) * 100) >= 0:
        new_cents = balance_cents - round(float(amount) * 100)
        return "ok|" + l6common.money(new_cents)
    return "conflict|" + l6common.money(expected_cents)


REGISTER = {
    "j6-l2.1": ("Constraints that keep data honest", ["J6.05"]),
    "j6-l2.2": ("Transactions: all or nothing", ["J6.06"]),
    "j6-l2.3": ("Isolation, lost updates and migrations", ["J6.07"]),
}
MISCS = {
    "MC159": (["J6.06"], "I70", "A transaction commits after every statement, so a multi-step change can be saved partially"),
    "MC160": (["J6.05"], "I69", "A foreign key is placed on the parent table of a one-to-many relationship"),
}
register(REGISTER, MISCS)


# ====================================================================== j6-l2.1
ex21.predict(
    "j6-l2.1-predict-actions",
    "Reading what a constraint blocks",
    ["o2"],
    ["J6.05"],
    "The program below deletes the transactions of one account and then deletes two accounts, one of which still has transactions. Predict the exact output, including the SQLState that a rejected statement reports.",
    """
import java.sql.*;
import java.util.*;

void main() {
    try (Connection db = Db.open()) {
        Db.reset(db);
        System.out.println("delete transactions=" + DbState(db, "DELETE FROM transactions WHERE account_id = 2"));
        System.out.println("delete unreferenced=" + DbState(db, "DELETE FROM accounts WHERE id = 2"));
        System.out.println("delete referenced=" + DbState(db, "DELETE FROM accounts WHERE id = 1"));
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
""",
    "delete transactions=ok\ndelete unreferenced=ok\ndelete referenced=23503\n",
    ["What does SQLState 23506 mean?", "Why is the second delete rejected?"],
    misconceptions=(),
    difficulty=1,
)

VIOLATION_GOOD = """
String violation(String operation) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        if (operation.equals("orphan-account")) {
            try {
                Db.update(db, "INSERT INTO accounts VALUES (9, 99, 0, 'open', '2025-01-01')");
            } catch (SQLException e) {
                return e.getSQLState();
            }
        }
        if (operation.equals("negative-balance")) {
            try {
                Db.update(db, "UPDATE accounts SET balance = -1 WHERE id = 1");
            } catch (SQLException e) {
                return e.getSQLState();
            }
        }
        if (operation.equals("duplicate-account")) {
            try {
                Db.update(db, "INSERT INTO accounts VALUES (1, 1, 5.00, 'open', '2025-01-01')");
            } catch (SQLException e) {
                return e.getSQLState();
            }
        }
        if (operation.equals("valid")) {
            Db.update(db, "INSERT INTO accounts VALUES (9, 2, 5.00, 'open', '2025-01-01')");
            return "ok";
        }
        return "unknown operation";
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

VIOLATION_BAD = """
String violation(String operation) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        Db.update(db, "INSERT INTO accounts VALUES (9, 99, 0, 'open', '2025-01-01')");
        return "ok";
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

VIOLATION_EXPECTED = {
    "orphan-account": "23506",
    "negative-balance": "23513",
    "duplicate-account": "23505",
    "valid": "ok",
    "unknown": "unknown operation",
}


def f_violation(*args):
    return VIOLATION_EXPECTED.get(args[0] if args else "unknown", "unknown operation")


ex21.method(
    "write",
    "j6-l2.1-write-violation",
    "Diagnosing a rejected write",
    ["o1", "o3"],
    ["J6.05"],
    ["IMPL"],
    "Write the statement for the operation, and read the SQLState of a statement the database rejects. Know what each class of violation means.",
    [("violation", [("operation", "String")], "String")],
    {"violation": f_violation},
    [("violation", ("orphan-account",), "a foreign key that points nowhere"),
     ("violation", ("negative-balance",), "a balance below zero"),
     ("violation", ("valid",), "a valid write")],
    [("violation", ("duplicate-account",), "a primary key that repeats"),
     ("violation", ("unknown",), "an operation that does not exist"),
     ("violation", ("orphan-account",), "a foreign key that points nowhere"),
     ("violation", ("negative-balance",), "a balance below zero"),
     ("violation", ("valid",), "a valid write")],
    starter=VIOLATION_BAD,
    solution=VIOLATION_GOOD,
    wrongs={"no-checks": VIOLATION_BAD},
    hints=["What SQLState does a foreign key violation return?", "What SQLState does a check constraint return?"],
    misconceptions=(),
    difficulty=2,
)


l6_l2_1 = Lesson("j6-l2.1", "Constraints that keep data honest", ["J6.05"], [
    ("o1", "Choose the constraint that fits each rule, and know what a foreign key, primary key and check constraint enforce"),
    ("o2", "Read the SQLState that a rejected write reports"),
    ("o3", "Explain why the database, not only the application, should enforce integrity"),
], ["j6-l1.4"], 40, ["I69", "I75", "I76"], """## Before you start

You should have written writes in the previous lesson, and you should know that a failed statement reports a SQLState.

## Explanation

A **constraint** is a rule the database holds. `NOT NULL` refuses a missing value, `UNIQUE` refuses a repeat, `CHECK` refuses a value that breaks a rule, and a **foreign key** refuses a value that points nowhere.

## Worked examples

### Example 1: a foreign key that points nowhere.

```java
INSERT INTO accounts VALUES (9, 99, 0, 'open', '2025-01-01');
```

### Example 2: a balance that breaks a rule.

```java
UPDATE accounts SET balance = -1 WHERE id = 1;
```

## Predict, then run

::exercise{id=j6-l2.1-predict-actions}

## Where this is used

- A bank that refuses an overdraft, or a schema that refuses a second customer id.

## Common mistakes

:::mistake{id=MC160}
**Putting the foreign key on the parent table of a one-to-many relationship.**
:::

## Practice

::exercise{id=j6-l2.1-predict-actions}

::exercise{id=j6-l2.1-write-violation}

## Further reading

- **PostgreSQL 18 documentation** `[I69]` on constraints.
- **Java SE 25 API** `[I75]` on `PreparedStatement`.

## How you'll be assessed

- The **predict** exercise checks that you can read a rejection (*identifying*).
- The **write** exercise checks that you can diagnose a rejection (*implementation*).
""")


# ====================================================================== j6-l2.2
TRANSFER_GOOD = """
String transfer(int from, int to, double amount) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        db.setAutoCommit(false);
        try {
            Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", java.math.BigDecimal.valueOf(amount), from);
            Db.update(db, "UPDATE accounts SET balance = balance + ? WHERE id = ?", java.math.BigDecimal.valueOf(amount), to);
            db.commit();
            String fromBalance = Db.one(db, "SELECT balance FROM accounts WHERE id = ?", from);
            String toBalance = Db.one(db, "SELECT balance FROM accounts WHERE id = ?", to);
            return fromBalance + "|" + toBalance;
        } catch (SQLException e) {
            db.rollback();
            return e.getSQLState();
        }
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

TRANSFER_WRONG = """
String transfer(int from, int to, double amount) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", java.math.BigDecimal.valueOf(amount), from);
        Db.update(db, "UPDATE accounts SET balance = balance + ? WHERE id = ?", java.math.BigDecimal.valueOf(amount), to);
        String fromBalance = Db.one(db, "SELECT balance FROM accounts WHERE id = ?", from);
        return fromBalance;
    } catch (SQLException e) {
        return e.getSQLState();
    }
}
"""


ex22.method(
    "write",
    "j6-l2.2-write-transfer",
    "One all-or-nothing transfer",
    ["o1"],
    ["J6.06"],
    ["IMPL"],
    "Write the transfer as a single transaction: debit the source account, credit the destination account, commit; if any statement fails, roll back and say so.",
    [("transfer", [("from", "int"), ("to", "int"), ("amount", "double")], "String")],
    {"transfer": f_transfer},
    [("transfer", (1, 2, 100.0), "a transfer between two open accounts"),
     ("transfer", (3, 1, 10.0), "an overdraft is rejected"),
     ("transfer", (2, 1, 50.0), "a transfer between two open accounts")],
    [("transfer", (5, 4, 25.0), "a small transfer"),
     ("transfer", (2, 5, 300.5), "a transfer that drains an account"),
     ("transfer", (1, 2, 1200.0), "a transfer that drains the source"),
     ("transfer", (4, 3, 5.0), "a transfer between two open accounts"),
     ("transfer", (5, 4, 50.0), "a small transfer")],
    starter="""
String transfer(int from, int to, double amount) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", java.math.BigDecimal.valueOf(amount), from);
        Db.update(db, "UPDATE accounts SET balance = balance + ? WHERE id = ?", java.math.BigDecimal.valueOf(amount), to);
        String fromBalance = Db.one(db, "SELECT balance FROM accounts WHERE id = ?", from);
        return fromBalance;
    } catch (SQLException e) {
        return e.getSQLState();
    }
}
""",
    solution=TRANSFER_GOOD,
    wrongs={"no-transaction": TRANSFER_WRONG},
    hints=["Turn auto-commit off before the first statement, and commit or roll back around them.", "Which side can break the balance?"],
    misconceptions=(),
    difficulty=3,
)


_OPEN_REPORT = """
        return "accounts=" + Db.one(db, "SELECT COUNT(*) FROM accounts WHERE id = 9") + " transactions=" + Db.one(db, "SELECT COUNT(*) FROM transactions WHERE id = 9");
"""

OPEN_GOOD = """
String openAccount(int customerId, double balance) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        db.setAutoCommit(false);
        try {
            Db.update(db, "INSERT INTO accounts VALUES (9, ?, ?, 'open', '2025-01-01')", customerId, balance);
            Db.update(db, "INSERT INTO transactions VALUES (9, 9, 'deposit', ?, '2025-01-02 09:00:00')", balance);
            db.commit();
        } catch (SQLException e) {
            db.rollback();
        }
""" + _OPEN_REPORT + """    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

OPEN_BAD = """
String openAccount(int customerId, double balance) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        try {
            Db.update(db, "INSERT INTO accounts VALUES (9, ?, ?, 'open', '2025-01-01')", customerId, balance);
            Db.update(db, "INSERT INTO transactions VALUES (9, 9, 'deposit', ?, '2025-01-02 09:00:00')", balance);
        } catch (SQLException e) {
            // the first statement was already saved by auto-commit
        }
""" + _OPEN_REPORT + """    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

OPEN_NO_CHECK = """
String openAccount(int customerId, double balance) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        db.setAutoCommit(false);
        try {
            Db.update(db, "INSERT INTO accounts VALUES (9, ?, ?, 'open', '2025-01-01')", customerId, balance);
            db.commit();
            Db.update(db, "INSERT INTO transactions VALUES (9, 9, 'deposit', ?, '2025-01-02 09:00:00')", balance);
            db.commit();
        } catch (SQLException e) {
            db.rollback();
        }
""" + _OPEN_REPORT + """    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""


ex22.method(
    "debug",
    "j6-l2.2-debug-commit",
    "A change that can be half saved",
    ["o2"],
    ["J6.06"],
    ["DEBUG"],
    "The starter opens an account and its first deposit, but auto-commit saves the account before the deposit is tried, so a rejected deposit leaves an account without a transaction. Make the two statements one transaction so a failure leaves nothing behind.",
    [("openAccount", [("customerId", "int"), ("balance", "double")], "String")],
    {"openAccount": f_open},
    [("openAccount", (2, 100.0), "a valid account and its opening deposit"),
     ("openAccount", (99, 100.0), "an invalid customer"),
     ("openAccount", (2, 0.0), "an invalid opening balance")],
    [("openAccount", (5, 20.0), "a valid account and its opening deposit"),
     ("openAccount", (98, 20.0), "an invalid customer"),
     ("openAccount", (7, 3.0), "a valid account and its opening deposit"),
     ("openAccount", (5, 0.0), "an invalid opening balance"),
     ("openAccount", (99, 5.0), "an invalid customer")],
    starter=OPEN_BAD,
    solution=OPEN_GOOD,
    wrongs={"commit-between": OPEN_NO_CHECK, "autocommit": OPEN_BAD},
    hints=["Where does an automatic commit end in the learner's code?", "What happens to a second statement that fails, when the first is already committed?"],
    misconceptions=(),
    difficulty=3,
)


l6_l2_2 = Lesson("j6-l2.2", "Transactions: all or nothing", ["J6.06"], [
    ("o1", "Wrap a multi-step change in a transaction and commit or roll back"),
    ("o2", "Explain what ACID means for a bank transfer"),
    ("o3", "Predict what a second connection sees before and after a commit"),
], ["j6-l2.1"], 50, ["I70", "I71", "I76", "I77"], """## Before you start

You should be able to write statements that can fail, and you should know that a failed statement reports a SQLState.

## Explanation

A **transaction** is a bundle of statements that either all happen or none happen. Without a transaction each statement commits on its own, so a two-statement change can be saved half way.

`COMMIT` makes a transaction permanent; `ROLLBACK` cancels it. Turning **auto-commit** off before the first statement is the usual way to open one.

## Worked examples

### Example 1: a transfer.

```java
connection.setAutoCommit(false);
UPDATE accounts SET balance = balance - ? WHERE id = ?;
UPDATE accounts SET balance = balance + ? WHERE id = ?;
COMMIT;
```

### Example 2: what happens when the second statement fails.

The first statement has already run; without a transaction the credit survives a rejected debit.

## Predict, then run

::exercise{id=j6-l2.2-predict-visibility}

## Where this is used

- Every transfer, every deposit, every fee that must not half land.

## Common mistakes

:::mistake{id=MC159}
**Thinking that a failed statement undoes earlier statements.**
:::

## Practice

::exercise{id=j6-l2.2-predict-visibility}

::exercise{id=j6-l2.2-write-transfer}

::exercise{id=j6-l2.2-debug-commit}

## Further reading

- **PostgreSQL 18 documentation** `[I70]` on transactions.
- **PostgreSQL 18 documentation** `[I71]` on transaction isolation.

## How you'll be assessed

- The **write** exercise checks that a transfer is atomic (*implementation*).
- The **debug** exercise checks that you can find a missing transaction (*debugging*).
- The **predict** exercise checks that you understand commit and rollback boundaries (*identifying*).
""")


ex22.predict(
    "j6-l2.2-predict-visibility",
    "What a second connection sees",
    ["o3"],
    ["J6.06"],
    "Two connections, one transaction. The first inserts an account and then a transaction that the constraint rejects; the rollback should undo the first statement. Predict what the second connection sees afterwards.",
    """
import java.sql.*;

void main() {
    try (Connection c1 = Db.open(); Connection c2 = Db.open()) {
        Db.reset(c1);
        c1.setAutoCommit(false);
        c2.setAutoCommit(false);
        Db.update(c1, "INSERT INTO accounts VALUES (9, 2, 5.00, 'open', '2025-01-01')");
        try {
            Db.update(c1, "INSERT INTO transactions VALUES (9, 9, 'deposit', 0.00, '2025-01-02 09:00:00')");
        } catch (SQLException e) {
            c1.rollback();
        }
        System.out.println("own accounts=" + Db.one(c1, "SELECT COUNT(*) FROM accounts"));
        System.out.println("accounts=" + Db.one(c2, "SELECT COUNT(*) FROM accounts"));
        System.out.println("transactions=" + Db.one(c2, "SELECT COUNT(*) FROM transactions"));
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
""",
    "own accounts=5\naccounts=5\ntransactions=6\n",
    ["What does a rollback undo?", "What does the second connection see before a commit?"],
    misconceptions=(),
    difficulty=1,
)


# ====================================================================== j6-l2.3
LOST_PROGRAM = """
import java.math.BigDecimal;

static BigDecimal balance(Connection db) throws SQLException {
    try (Statement s = db.createStatement(); ResultSet rs = s.executeQuery("SELECT balance FROM accounts WHERE id = 1")) {
        rs.next();
        return rs.getBigDecimal(1);
    }
}

static void updateBalance(Connection db, BigDecimal value) throws SQLException {
    try (PreparedStatement ps = db.prepareStatement("UPDATE accounts SET balance = ? WHERE id = 1")) {
        ps.setBigDecimal(1, value);
        ps.executeUpdate();
    }
}

void main() {
    try (Connection c1 = Db.open(); Connection c2 = Db.open()) {
        Db.reset(c1);
        c1.setAutoCommit(false);
        c2.setAutoCommit(false);
        BigDecimal firstRead = balance(c1);
        BigDecimal secondRead = balance(c2);
        System.out.println("read " + firstRead + " " + secondRead);
        updateBalance(c1, firstRead.subtract(new BigDecimal("100")));
        c1.commit();
        updateBalance(c2, secondRead.subtract(new BigDecimal("50")));
        c2.commit();
        System.out.println("final " + balance(c1));
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

WITHDRAW_GOOD = """
String withdraw(int id, double amount, double expectedBalance) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        String conflict = "conflict|" + java.math.BigDecimal.valueOf(expectedBalance).setScale(2).toPlainString();
        int changed;
        try {
            changed = Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance = ?", java.math.BigDecimal.valueOf(amount), id, java.math.BigDecimal.valueOf(expectedBalance));
        } catch (SQLException e) {
            if ("23513".equals(e.getSQLState())) {
                return conflict;
            }
            throw e;
        }
        if (changed == 1) {
            return "ok|" + Db.one(db, "SELECT balance FROM accounts WHERE id = ?", id);
        }
        return conflict;
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

WITHDRAW_BAD = """
String withdraw(int id, double amount, double expectedBalance) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", java.math.BigDecimal.valueOf(amount), id);
        return "ok|" + Db.one(db, "SELECT balance FROM accounts WHERE id = ?", id);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""


ex23.predict(
    "j6-l2.3-predict-lost-update",
    "A lost update",
    ["o1"],
    ["J6.07"],
    "The program below reads the same balance twice from two connections, debits once, then debits again from the stale read. Predict the final balance, and explain what went wrong.",
    LOST_PROGRAM,
    "read 1200.00 1200.00\nfinal 1150.00\n",
    ["What does each connection think the balance is?", "Who wrote last, and what does the other connection still believe?"],
    misconceptions=(),
    difficulty=1,
)

ex23.method(
    "write",
    "j6-l2.3-write-optimistic",
    "Optimistic withdrawal",
    ["o2"],
    ["J6.07"],
    ["IMPL"],
    "Write the withdrawal as an optimistic update: it only applies while the balance it expects is still the balance on the row. If not, report a conflict.",
    [("withdraw", [("id", "int"), ("amount", "double"), ("expectedBalance", "double")], "String")],
    {"withdraw": f_withdraw},
    [("withdraw", (1, 100.0, 1200.0), "a withdrawal that matches"),
     ("withdraw", (1, 1200.0, 1200.0), "a withdrawal that drains the account"),
     ("withdraw", (2, 300.5, 300.5), "a withdrawal from another account")],
    [("withdraw", (1, 100.0, 1050.0), "a stale expectation must conflict"),
     ("withdraw", (3, 10.0, 0.0), "an overdraft must not apply"),
     ("withdraw", (99, 10.0, 10.0), "an unknown account"),
     ("withdraw", (4, 780.25, 780.25), "a withdrawal that drains the account"),
     ("withdraw", (5, 50.0, 50.0), "a withdrawal from the last account")],
    starter=WITHDRAW_BAD,
    solution=WITHDRAW_GOOD,
    wrongs={"blind-update": WITHDRAW_BAD},
    hints=["What does the WHERE clause add that a plain UPDATE does not?", "Write the expected balance in the WHERE clause, so the row must still match it."],
    misconceptions=(),
    difficulty=3,
)


ex23.explain(
    "j6-l2.3-explain-migrations",
    "What a migration is",
    ["o3"],
    ["J6.07"],
    "A bank keeps its schema in versioned files. What does a migration do, and who runs it?",
    "A migration is a versioned SQL file that changes the schema. The platform's own migrations are run by the team; learners read them.",
    levels={
        2: ("The answer names the versioned file and what it changes.", [
            "A migration carries an identifier and a sequence of schema changes.",
            "Migrations are applied in order, once each."]),
        1: ("The answer describes a migration without its version discipline.", [
            "The answer describes a one-off SQL script without a version.",
            "The answer forgets that migrations are applied once each."]),
        0: ("The answer treats a migration as an undoable manual change.", [
            "The answer proposes dropping and recreating tables by hand.",
            "The answer says migrations can be freely edited after they have run."]),
    },
)


l6_l2_3 = Lesson("j6-l2.3", "Isolation, lost updates and migrations", ["J6.07"], [
    ("o1", "Predict and reproduce a lost update"),
    ("o2", "Prevent a lost update with an optimistic check or a lock"),
    ("o3", "Explain what Flyway migrations do"),
], ["j6-l2.2"], 45, ["I70", "I71", "I74", "I81"], """## Before you start

You should have written transactions and constraints, and you should know what a lost update is in principle.

## Explanation

A **lost update** happens when two readers read the same stale value and both write back. A transaction with a locking read, or an optimistic check, can stop it.

A **migration** is a versioned SQL file that changes the schema.

## Worked examples

### Example 1: the stale read.

```java
BigDecimal firstRead = read(c1);
BigDecimal secondRead = read(c2);
update(c1, firstRead - 100);
update(c2, secondRead - 50);
```

### Example 2: an optimistic check.

```java
UPDATE accounts SET balance = balance - ? WHERE id = ? AND balance = ?;
```

## Predict, then run

::exercise{id=j6-l2.3-predict-lost-update}

## Where this is used

- Every transfer that could overwrite another transfer's write.

## Common mistakes

- **Optimistic locking without the check** turns a lost update back into a failed write.

## Practice

::exercise{id=j6-l2.3-predict-lost-update}

::exercise{id=j6-l2.3-write-optimistic}

::exercise{id=j6-l2.3-explain-migrations}

## Further reading

- **PostgreSQL 18 documentation** `[I71]` on transaction isolation.

## How you'll be assessed

- The **predict** exercise checks that you can reproduce a lost update (*identifying*).
- The **write** exercise checks that you can prevent one (*implementation*).
- The **explain** exercise checks what a migration is (*explanation*).
""")


print("module 6.2 authored")
