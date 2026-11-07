"""Stage 6 authoring: module 6.1 (Relational thinking and SQL), lessons 6.1.1-6.1.4."""
import textwrap

import l6common
from l6common import (Lesson, Exercises, q, register, sql_file, DB_HELPERS, IMPORTS, CUSTOMERS, ACCOUNTS,
                     TRANSACTIONS, accounts_of, transactions_of, customers_in, account_balance, customer_name,
                     customer_city, money, CENTS)
import build  # noqa: E402

build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-6"
ex11 = Exercises("j6-l1.1")
ex12 = Exercises("j6-l1.2")
ex13 = Exercises("j6-l1.3")
ex14 = Exercises("j6-l1.4")


def full(method_source, main_call):
    return sql_file(method_source, main_call)


def program(main_body):
    """A complete runnable source: imports, shared Db fixture, then the main program."""
    return IMPORTS + "\n" + DB_HELPERS + "\n" + textwrap.dedent(main_body).strip("\n") + "\n"


REGISTER = {
    "j6-l1.1": ("Tables, keys and relationships", ["J6.01"]),
    "j6-l1.2": ("Selecting and filtering with NULL", ["J6.02"]),
    "j6-l1.3": ("Joins, aggregates and subqueries", ["J6.03"]),
    "j6-l1.4": ("Writing data, indexes and query plans", ["J6.04"]),
}
MISCS = {
    "MC157": (["J6.02"], "I69", "SQL uses three-valued logic, so `city = NULL` compares against the unknown value and never becomes true"),
    "MC158": (["J6.03"], "I72", "A many-to-many relationship is modelled by repeating one entity's column instead of joining through a junction table"),
}
register(REGISTER, MISCS)


# ====================================================================== j6-l1.1
ex11.predict(
    "j6-l1.1-predict-relationships",
    "What the keys guarantee",
    ["o3"],
    ["J6.01"],
    "The program below creates a small bank schema in an in-memory database, puts five customers and five accounts in it, and prints what it found. Predict the output exactly.",
    program("""
void main() {
    try (Connection db = Db.open()) {
        Db.reset(db);
        System.out.println("customers=5");
        System.out.println("customers with accounts=" + Db.one(db, "SELECT COUNT(DISTINCT customer_id) FROM accounts"));
        System.out.println("ada accounts=" + String.join(",", Db.query(db, "SELECT id FROM accounts WHERE customer_id = 1 ORDER BY id")));
        System.out.println("orphan insert=" + Db.DbState(db, "INSERT INTO accounts VALUES (9, 99, 0, 'open', '2025-01-01')"));
        System.out.println("duplicate customer=" + Db.DbState(db, "INSERT INTO customers VALUES (1, 'Ada Lovelace', 'Cape Town')"));
        System.out.println("balance sum=" + Db.one(db, "SELECT SUM(balance) FROM accounts"));
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""),
    "customers=5\ncustomers with accounts=4\nada accounts=1,5\norphan insert=23506\nduplicate customer=23505\nbalance sum=2330.75\n",
    ["What does the primary key of customers guarantee about Ada Lovelace?", "Why does the orphan insert get SQLState 23506?"],
    misconceptions=(),
    difficulty=1,
)

ACCOUNTS_OF_SOURCE = """
List<String> accountsOf(int customerId) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT id, balance FROM accounts WHERE customer_id = ? ORDER BY id", customerId);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

ACCOUNTS_OF_WRONG_NO_WHERE = """
List<String> accountsOf(int customerId) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT id, balance FROM accounts ORDER BY id");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

ACCOUNTS_OF_WRONG_WRONG_ORDER = """
List<String> accountsOf(int customerId) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT id, balance FROM accounts WHERE customer_id = ? ORDER BY balance ASC", customerId);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""


def f_accounts_of(*args):
    customer_id = args[0]
    return [f"{aid}|{money(CENTS(str(balance)))}" for aid, _, balance, _, _ in accounts_of(customer_id)]


ex11.method(
    "write",
    "j6-l1.1-write-accounts-of",
    "One customer's accounts",
    ["o1"],
    ["J6.01"],
    ["IMPL"],
    "Write the query that returns every account of one customer, as `id|balance`, ordered by account id. Use the foreign key column.",
    [("accountsOf", [("customerId", "int")], "List<String>")],
    {"accountsOf": f_accounts_of},
    [("accountsOf", (1,), "one customer with two accounts"),
     ("accountsOf", (2,), "one customer with one account"),
     ("accountsOf", (99,), "no such customer")],
    [("accountsOf", (3,), "one closed account"),
     ("accountsOf", (4,), "one open account"),
     ("accountsOf", (5,), "no such customer"),
     ("accountsOf", (0,), "no such customer"),
     ("accountsOf", (2,), "one customer with one account")],
    starter="""
List<String> accountsOf(int customerId) {
    return List.of();
}
""",
    solution=ACCOUNTS_OF_SOURCE,
    wrongs={"no-where": ACCOUNTS_OF_WRONG_NO_WHERE, "wrong-order": ACCOUNTS_OF_WRONG_WRONG_ORDER},
    hints=["Write the filter on the foreign key column customer_id.", "Return the columns in the order the reader expects: id and balance."],
    misconceptions=(),
    difficulty=2,
)

ex11.explain(
    "j6-l1.1-explain-normalise",
    "Why a join table",
    ["o2"],
    ["J6.01"],
    "A bank wants customers and tags. Is two one-to-many relationships enough, or does the relationship itself have to be a join table?",
    "The answer should put the relationship in its own table.\n\n- **One-to-many:** the many side keeps a foreign key to the one side.\n- **Many-to-many:** a junction table with one foreign key to each side and a primary key that pairs the two values.",
    levels={
        2: ("The answer names the foreign key and the join table, and explains why.", [
            "A customer owns accounts: accounts.customer_id references customers.id.",
            "For many-to-many, a junction table with both foreign keys and a composite primary key."]),
        1: ("The answer gets one of the two halves right, or is vague about duplicates.", [
            "The answer names the foreign key but calls it a many-to-many.",
            "The answer proposes a join table but forgets the unique pair."]),
        0: ("The answer repeats one side instead of joining.", [
            "The answer stores the customer name inside the account row.",
            "The answer proposes two one-to-many joins for a many-to-many."]),
    },
)


l6_l1_1 = Lesson("j6-l1.1", "Tables, keys and relationships", ["J6.01"], [
    ("o1", "Model a one-to-many relationship with a primary key and a foreign key, and explain why a many-to-many relationship needs a join table"),
    ("o2", "Explain first normal form by keeping one value per column, and say what a primary, foreign or candidate key guarantees"),
    ("o3", "Read a small schema and predict which rows a query can return, including which rows a foreign key rejects"),
], ["j3-l1.1"], 45, ["I69", "I72"], """## Before you start

You should have met lists and maps, and you should know what it means to pass a variable into a method. A database table is a kind of list, and a relationship between two tables is a kind of pointer.

## Explanation

A **table** holds a set of rows. The **primary key** is the column that identifies each row uniquely, and a **foreign key** is a column that points at a primary key in another table.

A **one-to-many** relationship means one customer and many accounts. The many side keeps a foreign key back to the customer, so the account row knows who it belongs to.

## Worked examples

### Example 1: one customer, many accounts.

```sql
CREATE TABLE customers (id integer PRIMARY KEY, name varchar(100) NOT NULL);
CREATE TABLE accounts (id integer PRIMARY KEY, customer_id integer NOT NULL REFERENCES customers(id), balance numeric(12,2) NOT NULL);
```

### Example 2: many customers, many tags.

When both sides can have many of the other, one-to-many stops being enough. Add a **join table** with one foreign key to each side, plus a primary key that makes a pair unique.

```sql
CREATE TABLE account_tags (account_id integer NOT NULL REFERENCES accounts(id), tag text NOT NULL, PRIMARY KEY (account_id, tag));
```

## Predict, then run

::exercise{id=j6-l1.1-predict-relationships}

## Where this is used

- Banking: a customer owns accounts, an account owns transactions.

## Common mistakes

:::mistake{id=MC158}
**Normalising a many-to-many relationship by repeating one side.**
:::

## Practice

::exercise{id=j6-l1.1-predict-relationships}

::exercise{id=j6-l1.1-write-accounts-of}

::exercise{id=j6-l1.1-explain-normalise}

## Further reading

- **PostgreSQL 18 documentation** `[I69]` on constraints.
- **PostgreSQL 18 documentation** `[I72]` on table expressions.

## How you'll be assessed

- The **predict** exercise checks that you can read keys and relationships (*identifying*).
- The **write** exercise checks that you can write a query that picks one customer's accounts (*implementation*).
- The **explain** exercise checks that you can argue for a normal form (*explanation*).
""")


# ====================================================================== j6-l1.2
ex12.predict(
    "j6-l1.2-predict-null",
    "What does a query with NULL return",
    ["o2", "o3"],
    ["J6.02"],
    "The program below runs four queries over the small bank fixture: an equality against the NULL city, an `IS NULL` check, a `NOT IN` whose subquery contains that NULL, and two count queries. Predict the exact output.",
    program("""
void main() {
    try (Connection db = Db.open()) {
        Db.reset(db);
        System.out.println("equal null=" + Db.one(db, "SELECT COUNT(*) FROM customers WHERE city = NULL"));
        System.out.println("is null=" + Db.one(db, "SELECT COUNT(*) FROM customers WHERE city IS NULL"));
        System.out.println("not in=" + Db.one(db, "SELECT COUNT(*) FROM customers WHERE city NOT IN (SELECT city FROM customers)"));
        System.out.println("count rows=" + Db.one(db, "SELECT COUNT(*) FROM customers"));
        System.out.println("count named=" + Db.one(db, "SELECT COUNT(*), COUNT(city) FROM customers"));
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""),
    "equal null=0\nis null=1\nnot in=0\ncount rows=5\ncount named=5|4\n",
    ["Why does `city = NULL` return nothing?", "What does `COUNT(city)` count?"],
    misconceptions=(),
    difficulty=1,
)

CUSTOMERS_IN_SOURCE = """
List<String> customersIn(String city) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        if (city == null) {
            return Db.query(db, "SELECT name FROM customers WHERE city IS NULL ORDER BY name");
        }
        return Db.query(db, "SELECT name FROM customers WHERE city = ? ORDER BY name", city);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

CUSTOMERS_IN_WRONG_NULL = """
List<String> customersIn(String city) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT name FROM customers WHERE city = ? ORDER BY name", city);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

CUSTOMERS_IN_WRONG_COLUMN = """
List<String> customersIn(String city) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT name FROM customers WHERE name = ? ORDER BY name", city);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""


def f_customers_in(*args):
    return customers_in(args[0])


ex12.method(
    "write",
    "j6-l1.2-write-filter",
    "Finding customers by city",
    ["o1"],
    ["J6.02"],
    ["IMPL"],
    "Write the query that returns the names of the customers in one city, in alphabetical order. If the city is null, return the customers whose city is null.",
    [("customersIn", [("city", "String")], "List<String>")],
    {"customersIn": f_customers_in},
    [("customersIn", ("Cape Town",), "two customers"),
     ("customersIn", ("Durban",), "one customer"),
     ("customersIn", (None,), "customers without a city"),
     ("customersIn", ("",), "no customers")],
    [("customersIn", ("Johannesburg",), "one customer"),
     ("customersIn", ("Nowhere",), "no customers"),
     ("customersIn", (None,), "customers without a city"),
     ("customersIn", ("cape town",), "the comparison is case sensitive"),
     ("customersIn", ("Cape Town",), "two customers")],
    starter="""
List<String> customersIn(String city) {
    return List.of();
}
""",
    solution=CUSTOMERS_IN_SOURCE,
    wrongs={"null-ignored": CUSTOMERS_IN_WRONG_NULL, "wrong-column": CUSTOMERS_IN_WRONG_COLUMN},
    hints=["Use `IS NULL` when the needle is the null value, and a bound parameter when it is a value.", "Remember to order the result."],
    misconceptions=(),
    difficulty=2,
)


l6_l1_2 = Lesson("j6-l1.2", "Selecting and filtering with NULL", ["J6.02"], [
    ("o1", "Write a SELECT with a WHERE filter, a bound parameter and an ORDER BY"),
    ("o2", "Explain three-valued logic and predict what a query with NULL returns"),
    ("o3", "Predict how COUNT and NOT IN treat NULL"),
], ["j6-l1.1"], 40, ["I69", "I76"], """## Before you start

You should have met tables and keys in the previous lesson, and you should be able to write a method that takes a parameter.

## Explanation

A **filter** keeps the rows where its condition is **true**. Comparing a column to the value NULL gives an **unknown** answer, not false, so the row is dropped.

## Worked examples

### Example 1: find a customer's city.

```sql
SELECT name FROM customers WHERE city = ? ORDER BY name;
```

### Example 2: find the customers whose city is unknown.

```sql
SELECT name FROM customers WHERE city IS NULL ORDER BY name;
```

## Predict, then run

::exercise{id=j6-l1.2-predict-null}

## Where this is used

- Every search box, filter and report that asks "is this value present?".

## Common mistakes

:::mistake{id=MC157}
**Writing `= NULL` to find missing values.**
:::

## Practice

::exercise{id=j6-l1.2-predict-null}

::exercise{id=j6-l1.2-debug-not-in}

::exercise{id=j6-l1.2-write-filter}

## Further reading

- **PostgreSQL 18 documentation** `[I69]` on `NOT NULL`.
- **Java SE 25 API** `[I76]` on the auto-commit default of a connection.

## How you'll be assessed

- The **predict** exercises check your reading of NULL (*identifying*).
- The **write** exercise checks that you can filter correctly (*implementation*).
""")


# ====================================================================== j6-l1.3
JOINS_PROGRAM = """
import java.sql.*;
import java.util.*;

void main() {
    try (Connection db = Db.open()) {
        Db.reset(db);
        System.out.println("counts");
        for (String row : Db.query(db, "SELECT c.id, c.name, COUNT(a.id) FROM customers c LEFT JOIN accounts a ON a.customer_id = c.id GROUP BY c.id, c.name ORDER BY c.id")) {
            System.out.println("customer " + row);
        }
        System.out.println("totals");
        for (String row : Db.query(db, "SELECT c.id, SUM(a.balance) FROM customers c LEFT JOIN accounts a ON a.customer_id = c.id GROUP BY c.id ORDER BY c.id")) {
            System.out.println("customer " + row);
        }
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

JOINS_EXPECTED = """counts
customer 1|Ada Lovelace|2
customer 2|Grace Hopper|1
customer 3|Alan Turing|1
customer 4|Edsger Dijkstra|1
customer 5|Barbara Liskov|0
totals
customer 1|1250.00
customer 2|300.50
customer 3|0.00
customer 4|780.25
customer 5|null
"""

SUMMARY_SOURCE = """
List<String> accountSummary(String city) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        String sql = "SELECT c.name, COUNT(a.id), CAST(COALESCE(SUM(a.balance), 0) AS numeric(12,2)) AS total FROM customers c LEFT JOIN accounts a ON a.customer_id = c.id";
        if (city != null) {
            sql = sql + " WHERE c.city = ?";
        }
        sql = sql + " GROUP BY c.id, c.name ORDER BY c.id";
        Object[] params = city == null ? new Object[0] : new Object[] {city};
        return Db.query(db, sql, params);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

SUMMARY_SOURCE_BAD = """
List<String> accountSummary(String city) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        String sql = "SELECT c.name, COUNT(a.id), SUM(a.balance) FROM customers c JOIN accounts a ON a.customer_id = c.id GROUP BY c.id, c.name ORDER BY c.id";
        if (city != null) {
            sql = sql + " WHERE c.city = ?";
        }
        sql = sql + " GROUP BY c.id, c.name ORDER BY c.id";
        Object[] params = city == null ? new Object[0] : new Object[] {city};
        return Db.query(db, sql, params);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""


def f_summary(*args):
    city = args[0]
    rows = []
    for cid, name, _ in CUSTOMERS:
        if city is not None and customer_city(cid) != city:
            continue
        accounts = [a for a in ACCOUNTS if a[1] == cid]
        total = sum(CENTS(str(a[2])) for a in accounts)
        rows.append(f"{name}|{len(accounts)}|{money(total)}")
    return rows


ex13.predict(
    "j6-l1.3-predict-joins",
    "Reading a grouped join",
    ["o1"],
    ["J6.03"],
    "The program below prints how many accounts each customer holds and what those accounts total. Predict the exact output, including what a customer without accounts contributes.",
    program(JOINS_PROGRAM),
    JOINS_EXPECTED,
    ["Why does Barbara Liskov appear with count 0?", "Why does the second line show null for a customer without accounts?"],
    misconceptions=(),
    difficulty=1,
)

ex13.method(
    "write",
    "j6-l1.3-write-summary",
    "Money per customer",
    ["o1", "o2"],
    ["J6.03"],
    ["IMPL"],
    "Write the query that returns one line per customer: `name|count|total`. Use a left join, group by customer, and treat a customer with no accounts as having zero total.",
    [("accountSummary", [("city", "String")], "List<String>")],
    {"accountSummary": f_summary},
    [("accountSummary", (None,), "all customers"),
     ("accountSummary", ("Cape Town",), "one city"),
     ("accountSummary", ("Durban",), "one customer, no accounts")],
    [("accountSummary", ("Johannesburg",), "one customer, one account"),
     ("accountSummary", ("Nowhere",), "no customers"),
     ("accountSummary", ("",), "no customers"),
     ("accountSummary", ("Durban",), "one customer, no accounts"),
     ("accountSummary", ("Alan Turing",), "one customer, one closed account")],
    starter=SUMMARY_SOURCE_BAD,
    solution=SUMMARY_SOURCE,
    wrongs={"inner-join": SUMMARY_SOURCE_BAD},
    hints=["Which join keeps the customers that have no accounts?", "How do you make a customer with no accounts contribute zero?"],
    misconceptions=(),
    difficulty=3,
)


CUSTOMER_TOTALS_BUGGY = """
List<String> customerTotals() {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT c.name, SUM(a.balance) FROM customers c JOIN accounts a ON a.customer_id = c.id JOIN transactions t ON t.account_id = a.id GROUP BY c.id, c.name ORDER BY c.id");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

CUSTOMER_TOTALS_GOOD = """
List<String> customerTotals() {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT c.name, SUM(a.balance) FROM customers c JOIN accounts a ON a.customer_id = c.id GROUP BY c.id, c.name ORDER BY c.id");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""


def f_customer_totals(*args):
    rows = []
    for cid, name, _ in CUSTOMERS:
        accounts = [a for a in ACCOUNTS if a[1] == cid]
        if not accounts:
            continue
        total = sum(CENTS(str(a[2])) for a in accounts)
        rows.append(f"{name}|{money(total)}")
    return rows


ex13.method(
    "debug",
    "j6-l1.3-debug-duplicates",
    "A join that multiplies",
    ["o3"],
    ["J6.03"],
    ["DEBUG"],
    "The report joins accounts to transactions and sums the balance once per transaction. Predict the total for a customer with several transactions, then fix the query so each account is counted once.",
    [("customerTotals", [], "List<String>")],
    {"customerTotals": f_customer_totals},
    [("customerTotals", (), "Ada, who has two accounts and three transactions")],
    [("customerTotals", (), "Ada, who has two accounts and three transactions"),
     ("customerTotals", (), "Grace, who has one account"),
     ("customerTotals", (), "Alan, whose only account is closed")],
    starter=CUSTOMER_TOTALS_BUGGY,
    solution=CUSTOMER_TOTALS_GOOD,
    wrongs={"transactions-join": CUSTOMER_TOTALS_BUGGY},
    hints=["Why does Ada appear with a total that is three times too large?", "What does the join multiply?"],
    misconceptions=(),
    difficulty=3,
)


l6_l1_3 = Lesson("j6-l1.3", "Joins, aggregates and subqueries", ["J6.03"], [
    ("o1", "Write a join and choose between inner and left join"),
    ("o2", "Write GROUP BY with aggregates and HAVING, and tell COUNT(*) from COUNT(column)"),
    ("o3", "Use a subquery so a query does not multiply rows"),
], ["j6-l1.2"], 50, ["I72"], """## Before you start

You should have written filters and seen that a join combines two tables. You should know what grouping means from maps, in the grouping sense.

## Explanation

A **join** makes one row per combination of matches, so a many-to-many join multiplies rows. An **inner join** keeps only combinations where both sides matched; a **left join** keeps every row of the left side, filling unmatched columns with NULL.

An **aggregate** collapses rows into a group: `COUNT`, `SUM`, `AVG`. `HAVING` filters on the group after it has been formed.

## Worked examples

### Example 1: total money per customer, including customers with no accounts.

```sql
SELECT c.name, COUNT(a.id), CAST(COALESCE(SUM(a.balance), 0) AS numeric(12,2)) AS total
FROM customers c LEFT JOIN accounts a ON a.customer_id = c.id
GROUP BY c.id, c.name;
```

### Example 2: a subquery counts transactions without joining.

```sql
SELECT account_id, SUM(amount) FROM transactions GROUP BY account_id;
```

## Predict, then run

::exercise{id=j6-l1.3-predict-joins}

## Where this is used

- A report that goes one level up: which customers have spent what.

## Common mistakes

- **Filtering before grouping.** A `WHERE` clause filters rows before aggregation; `HAVING` filters groups after.

## Practice

::exercise{id=j6-l1.3-predict-joins}

::exercise{id=j6-l1.3-write-summary}

::exercise{id=j6-l1.3-debug-duplicates}

## Further reading

- **PostgreSQL 18 documentation** `[I72]` on join types and the `ON` condition.

## How you'll be assessed

- The **predict** exercise checks your reading of joins (*identifying*).
- The **write** exercise checks that you can group and aggregate (*implementation*).
- The **debug** exercise checks that you can stop rows from being multiplied (*debugging*).
""")


# ====================================================================== j6-l1.4
CHARGE_SOURCE = """
String chargeFee(int accountId, double fee) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        int changed = Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", java.math.BigDecimal.valueOf(fee), accountId);
        if (changed == 0) {
            return "missing";
        }
        return accountId + "|" + Db.one(db, "SELECT balance FROM accounts WHERE id = ?", accountId);
    } catch (SQLException e) {
        return e.getSQLState();
    }
}
"""

CHARGE_WRONG = """
String chargeFee(int accountId, double fee) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        Db.update(db, "UPDATE accounts SET balance = balance + ? WHERE id = ?", java.math.BigDecimal.valueOf(fee), accountId);
        return accountId + "|" + Db.one(db, "SELECT balance FROM accounts WHERE id = ?", accountId);
    } catch (SQLException e) {
        return e.getSQLState();
    }
}
"""


def f_charge(*args):
    account_id, fee = args
    if account_id == 99:
        return "missing"
    balances = {1: 1200.00, 2: 300.50, 3: 0.00, 4: 780.25, 5: 50.00}
    current = balances[account_id]
    new_balance = round(float(current) * 100) - round(float(fee) * 100)
    if new_balance < 0:
        return "23513"
    return f"{account_id}|{money(new_balance)}"


ex14.method(
    "write",
    "j6-l1.4-write-fee",
    "Charging a fee",
    ["o1", "o3"],
    ["J6.04"],
    ["IMPL"],
    "Write the statement that charges a fee from one account and reports the new balance. If the account does not exist, or the fee would overdraw it, report that.",
    [("chargeFee", [("accountId", "int"), ("fee", "double")], "String")],
    {"chargeFee": f_charge},
    [("chargeFee", (1, 100.0), "a fee that leaves the account open"),
     ("chargeFee", (3, 0.01), "a fee the balance cannot cover"),
     ("chargeFee", (99, 10.0), "an account that does not exist")],
    [("chargeFee", (1, 1200.0), "a fee that drains the account"),
     ("chargeFee", (5, 50.0), "a fee that drains the last account"),
     ("chargeFee", (2, 0.5), "a small fee"),
     ("chargeFee", (4, 780.25), "a fee that drains another account"),
     ("chargeFee", (3, 0.0), "a zero fee")],
    starter="""
String chargeFee(int accountId, double fee) {
    return "todo";
}
""",
    solution=CHARGE_SOURCE,
    wrongs={"no-where": CHARGE_WRONG},
    hints=["What does the WHERE clause add to an UPDATE?", "How do you report a balance that cannot be covered?"],
    misconceptions=(),
    difficulty=2,
)


DELETE_SOURCE = """
List<String> deleteAccount(int accountId) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        try {
            Db.update(db, "DELETE FROM accounts WHERE id = ?", accountId);
            Db.update(db, "DELETE FROM transactions WHERE account_id = ?", accountId);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return Db.query(db, "SELECT id, balance FROM accounts ORDER BY id");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

DELETE_SOURCE_GOOD = """
List<String> deleteAccount(int accountId) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        try {
            Db.update(db, "DELETE FROM transactions WHERE account_id = ?", accountId);
            Db.update(db, "DELETE FROM accounts WHERE id = ?", accountId);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return Db.query(db, "SELECT id, balance FROM accounts ORDER BY id");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""


def f_delete(*args):
    account_id = args[0]
    remaining = []
    for aid, _, balance, _, _ in sorted(l6common.ACCOUNTS):
        if aid == account_id:
            continue
        remaining.append(f"{aid}|{money(l6common.CENTS(str(balance)))}")
    return remaining


ex14.method(
    "debug",
    "j6-l1.4-debug-delete",
    "Deleting in the wrong order",
    ["o1"],
    ["J6.04"],
    ["DEBUG"],
    "The delete statements have the foreign key backwards: the account is deleted before the transactions that reference it. Write the delete so it removes the child rows first.",
    [("deleteAccount", [("accountId", "int")], "List<String>")],
    {"deleteAccount": f_delete},
    [("deleteAccount", (2,), "deleting an account that other transactions reference"),
     ("deleteAccount", (99,), "deleting an unknown account"),
     ("deleteAccount", (5,), "deleting the account that belongs to Ada again"),
     ("deleteAccount", (0,), "deleting an unknown account")],
    [("deleteAccount", (2,), "deleting an account that other transactions reference"),
     ("deleteAccount", (99,), "deleting an unknown account"),
     ("deleteAccount", (5,), "deleting the account that belongs to Ada again"),
     ("deleteAccount", (1,), "deleting the first account"),
     ("deleteAccount", (4,), "deleting a middle account")],
    starter=DELETE_SOURCE,
    solution=DELETE_SOURCE_GOOD,
    wrongs={"transactions-only": """
List<String> deleteAccount(int accountId) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        Db.update(db, "DELETE FROM transactions WHERE account_id = ?", accountId);
        return Db.query(db, "SELECT id, balance FROM accounts ORDER BY id");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""},
    hints=["Which side is the child, and which side is the parent?", "What happens when you delete a parent that children still point at?"],
    misconceptions=(),
    difficulty=3,
)


ex14.explain(
    "j6-l1.4-explain-plan",
    "Reading a query plan",
    ["o2"],
    ["J6.04"],
    "A bank runs a report over a payments table with 50,000 rows. The mentor asks: what does this `EXPLAIN (ANALYZE, BUFFERS)` output tell you, and what would you change? The plan shows a sequential scan that removes 49,900 rows before the join, and after an index the same query is a bitmap heap scan.",
    "A sequential scan reads every row and filters; an index lets the planner read only the rows that match. `EXPLAIN` prints the plan, `ANALYZE` runs it and adds actual numbers, and `BUFFERS` reports disk reads.",
    levels={
        2: ("The answer names the scan, the filter and the cost, and says what an index changes.", [
            "Without the index the plan is a sequential scan that filters a customer id and removes most rows.",
            "With the index the plan is a bitmap heap scan on the index column."]),
        1: ("The answer names the plan but not what the numbers mean.", [
            "The answer quotes the plan without explaining the rows removed by the filter.",
            "The answer says an index always helps without saying when it does not."]),
        0: ("The answer reads the plan as a list of rows rather than a strategy.", [
            "The answer reads the numbers as a histogram instead of a scan strategy.",
            "The answer ignores the execution time and buffer counts."]),
    },
)


l6_l1_4 = Lesson("j6-l1.4", "Writing data, indexes and query plans", ["J6.04"], [
    ("o1", "Write an UPDATE or DELETE that affects exactly the rows the WHERE names"),
    ("o2", "Predict how an index changes a query plan, and read EXPLAIN output"),
    ("o3", "Write an UPDATE that a CHECK constraint rejects, and read the SQLState"),
], ["j6-l1.3"], 45, ["I73", "I74", "I75"], """## Before you start

You should be able to write filters and you should know that a failed statement leaves the previous state alone.

## Explanation

`UPDATE`, `DELETE` and `INSERT` are statements like any other; only their effect differs. The discipline is that every one of them says exactly which rows it means.

An **index** stores an ordered copy of selected columns. The planner reads the index instead of scanning a whole table. `EXPLAIN` prints the plan, `ANALYZE` runs the statement, and `BUFFERS` reports disk reads.

## Worked examples

### Example 1: charging a fee.

```java
UPDATE accounts SET balance = balance - ? WHERE id = ?;
SELECT balance FROM accounts WHERE id = ?;
```

### Example 2: reading a plan.

```
Seq Scan on payments (cost=0.00..944.00 rows=100 width=18) (actual time=0.006..1.095 rows=100.00)
  Filter: (customer_id = 42)
  Rows Removed by Filter: 49900
  Buffers: shared hit=319
```

## Predict, then run

::exercise{id=j6-l1.4-write-fee}

## Where this is used

- Every fee, transfer, status change and backfill.

## Common mistakes

- **An UPDATE or DELETE without a WHERE clause** affects every row in the table.

## Practice

::exercise{id=j6-l1.4-write-fee}

::exercise{id=j6-l1.4-debug-delete}

::exercise{id=j6-l1.4-explain-plan}

## Further reading

- **PostgreSQL 18 documentation** `[I73]` on `EXPLAIN`.
- **PostgreSQL 18 documentation** `[I74]` on `INSERT` and `RETURNING`.

## How you'll be assessed

- The **write** exercise checks that a `WHERE` names the row (*implementation*).
- The **debug** exercise checks that you can find a missing `WHERE` (*debugging*).
- The **explain** exercise checks that you can read a plan (*explanation*).
""")


# ---- j6-l1.2 debug: NOT IN over a column that contains NULL (expected values computed here)
_CITIES_WITH_CUSTOMERS = {c for _, _, c in CUSTOMERS if c is not None}


def _branches_head(sub):
    return """
List<String> citiesWithoutCustomers(List<String> branches) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        Db.update(db, "CREATE TABLE branches (city varchar(100) PRIMARY KEY)");
        for (String branch : branches) {
            Db.update(db, "INSERT INTO branches VALUES (?)", branch);
        }
        return Db.query(db, "%s ORDER BY city");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
""" % sub


def f_cities_without(*args):
    return sorted(b for b in args[0] if b not in _CITIES_WITH_CUSTOMERS)


ex12.method(
    "debug",
    "j6-l1.2-debug-not-in",
    "A NOT IN that breaks on NULL",
    ["o3"],
    ["J6.02"],
    ["DEBUG"],
    "A report lists the branch cities in which the bank has no customer. It uses `NOT IN` over `customers.city`, and it returns nothing even for a city that has no customers. One customer's city is NULL. Diagnose and fix it.",
    [("citiesWithoutCustomers", [("branches", "List<String>")], "List<String>")],
    {"citiesWithoutCustomers": f_cities_without},
    [("citiesWithoutCustomers", (["Cape Town", "Kimberley", "Pretoria"],), "two cities without customers"),
     ("citiesWithoutCustomers", ([],), "no branches"),
     ("citiesWithoutCustomers", (["Durban"],), "a city that has a customer")],
    [("citiesWithoutCustomers", (["Nowhere", "Durban"],), "one unknown city"),
     ("citiesWithoutCustomers", (["Johannesburg", "Cape Town"],), "every city has customers"),
     ("citiesWithoutCustomers", (["Pretoria"],), "one city without customers"),
     ("citiesWithoutCustomers", (["Kimberley", "Bloemfontein", "Durban"],), "two cities without customers, in order"),
     ("citiesWithoutCustomers", (["cape town"],), "the comparison is case sensitive")],
    starter=_branches_head("SELECT city FROM branches WHERE city NOT IN (SELECT city FROM customers)"),
    solution=_branches_head("SELECT city FROM branches WHERE city NOT IN (SELECT city FROM customers WHERE city IS NOT NULL)"),
    wrongs={"in-instead": _branches_head("SELECT city FROM branches WHERE city IN (SELECT city FROM customers)"),
            "original": _branches_head("SELECT city FROM branches WHERE city NOT IN (SELECT city FROM customers)")},
    hints=["What does `x NOT IN (a, b, NULL)` evaluate to when x is not a or b?", "Remove the NULLs from the subquery, or use NOT EXISTS."],
    misconceptions=(),
    difficulty=3,
)


print("module 6.1 authored")
