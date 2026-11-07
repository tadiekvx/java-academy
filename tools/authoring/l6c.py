"""Stage 6 authoring: module 6.3 (JDBC): connections, PreparedStatement, mapping, resources."""
import l6common
from l6common import Lesson, Exercises, q, register, sql_file, DB_HELPERS, IMPORTS, CUSTOMERS, ACCOUNTS, TRANSACTIONS, accounts_of, money, accounts_of, customers_in, customer_city
import build  # noqa: E402

build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-6"
ex31 = Exercises("j6-l3.1")
ex32 = Exercises("j6-l3.2")
ex33 = Exercises("j6-l3.3")


def full(method_source, main_call):
    return sql_file(method_source, main_call)


def program(main_body):
    return IMPORTS + "\n" + DB_HELPERS + "\n" + main_body.strip("\n") + "\n"


REGISTER = {
    "j6-l3.1": ("Connections and PreparedStatement", ["J6.08"]),
    "j6-l3.2": ("Mapping rows and repositories", ["J6.09"]),
    "j6-l3.3": ("Transactions and resource management in JDBC", ["J6.10"]),
}
MISCS = {
    "MC161": (["J6.08"], "I82", "SQL injection is stopped by escaping quotes inside the query string"),
    "MC162": (["J6.10"], "I76", "A JDBC connection is closed by the database server only when the application closes it"),
}
register(REGISTER, MISCS)


# ====================================================================== j6-l3.1
ex31.predict(
    "j6-l3.1-predict-injection",
    "What an interpolated query does",
    ["o1"],
    ["J6.08"],
    "The program below builds one query by string concatenation and one through a bound parameter, over the same value. Predict what each returns.",
    program("""
import java.sql.*;
import java.util.*;

void main() {
    try (Connection db = Db.open()) {
        Db.reset(db);
        String sneaky = "Ada' OR '1'='1";
        List<String> interpolated = new ArrayList<>();
        try (Statement s = db.createStatement(); ResultSet rs = s.executeQuery("SELECT name FROM customers WHERE name = '" + sneaky + "'")) {
            while (rs.next()) {
                interpolated.add(rs.getString(1));
            }
        }
        List<String> bound = Db.query(db, "SELECT name FROM customers WHERE name = ?", sneaky);
        System.out.println("interpolated=" + interpolated.size());
        System.out.println("bound=" + bound.size());
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""),
    "interpolated=5\nbound=0\n",
    ["What does the interpolated query do that the bound parameter does not?", "Why is the result of the safe query zero rows?"],
    misconceptions=(),
    difficulty=1,
)

SEARCH_SOURCE = """
List<String> findCustomers(String prefix) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT name FROM customers WHERE name LIKE ? ORDER BY name", prefix + "%");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

SEARCH_F = lambda *args: sorted(n for n in [c[1] for c in CUSTOMERS if c[1] is not None and c[1].startswith(args[0])] if n)


ex31.method(
    "write",
    "j6-l3.1-write-search",
    "Searching by name",
    ["o1", "o2"],
    ["J6.08"],
    ["IMPL"],
    "Write the query that returns the customer names starting with the given prefix, in alphabetical order.",
    [("findCustomers", [("prefix", "String")], "List<String>")],
    {"findCustomers": SEARCH_F},
    [("findCustomers", ("Ada",), "one customer"),
     ("findCustomers", ("Grace",), "one customer"),
     ("findCustomers", ("",), "all customers")],
    [("findCustomers", ("Al",), "two customers"),
     ("findCustomers", ("E",), "one customer"),
     ("findCustomers", ("B",), "one customer"),
     ("findCustomers", ("Z",), "no customers"),
     ("findCustomers", ("A",), "one customer")],
    starter="""
List<String> findCustomers(String prefix) {
    return List.of();
}
""",
    solution=SEARCH_SOURCE,
    wrongs={"interpolated": """
List<String> findCustomers(String prefix) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT name FROM customers WHERE name = '" + prefix + "' ORDER BY name");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""},
    hints=["Bind the prefix as a parameter instead of putting it in the SQL string.", "How would the query read with a pattern?"],
    misconceptions=(),
    difficulty=2,
)


ex31.explain(
    "j6-l3.1-explain-injection",
    "Why parameters are the fix",
    ["o1"],
    ["J6.08"],
    "A bank logs every search term. Why is the query that concatenates the search term into the SQL string a security hole, and why is the parameterised query not?",
    "SQL injection lets untrusted data become SQL. The fix is a parameterised query; escaping quotes is not enough.",
    levels={
        2: ("The answer names the hole and the parameterised fix, and is precise about escaping.", [
            "A value that is concatenated can close the string and start a new statement.",
            "A parameter is bound as data, never as SQL."]),
        1: ("The answer names the fix but not the hole.", [
            "The answer says to use parameters without saying why.",
            "Use a PreparedStatement instead of building the string; that is what the docs recommend."]),
        0: ("The answer suggests escaping quotes as the fix.", [
            "The answer proposes single-quote escaping as sufficient.",
            "Replace every single quote in the search term by two quotes before building the string, and the query is safe."]),
    },
)


l6_l3_1 = Lesson("j6-l3.1", "Connections and PreparedStatement", ["J6.08"], [
    ("o1", "Write a query with a bound parameter, and explain why it stops SQL injection"),
    ("o2", "Open a connection with DriverManager and close it in the right order"),
], ["j6-l2.3"], 45, ["I78", "I82", "I76"], """## Before you start

You should have written queries with filters, and you should know what an injection is in principle.

## Explanation

A **prepared statement** keeps the SQL fixed and binds the values as parameters. The database sees a template with placeholders, so a value can never become SQL syntax.

A **connection pool** hands out connections instead of opening one per request.

## Worked examples

### Example 1: the safe query.

```java
PreparedStatement ps = db.prepareStatement("SELECT name FROM customers WHERE name = ?");
ps.setString(1, sneaky);
```

### Example 2: the same query interpolated.

```java
Statement s = db.createStatement();
ResultSet rs = s.executeQuery("SELECT name FROM customers WHERE name = '" + sneaky + "'");
```

## Predict, then run

::exercise{id=j6-l3.1-predict-injection}

## Where this is used

- Every search box, every report with a parameter.

## Common mistakes

:::mistake{id=MC161}
**Stopping injection by escaping quotes in the query string.**
:::

## Practice

::exercise{id=j6-l3.1-predict-injection}

::exercise{id=j6-l3.1-write-search}

::exercise{id=j6-l3.1-explain-injection}

## Further reading

- **OWASP** `[I82]` on SQL injection.
- **Java SE 25 API** `[I78]` on `DriverManager`.

## How you'll be assessed

- The **predict** exercise checks that you can see what interpolation does (*identifying*).
- The **write** exercise checks that you can bind a parameter (*implementation*).
- The **explain** exercise checks the defence (*explanation*).
""")


# ====================================================================== j6-l3.2
ACCOUNT_ROWS_SOURCE = """
List<String> accountRows(int accountId) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        List<String> rows = Db.query(db, "SELECT a.id, c.name, c.city, a.balance FROM accounts a JOIN customers c ON c.id = a.customer_id WHERE a.id = ? ORDER BY a.id", accountId);
        if (rows.isEmpty()) {
            return List.of();
        }
        String row = rows.get(0);
        String[] parts = row.split("\\\\|");
        String city = parts[2].equals("null") ? "unknown" : parts[2];
        return List.of(parts[0] + "|" + parts[1] + "|" + city + "|" + parts[3]);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

ACCOUNT_ROWS_SOURCE_BAD = """
List<String> accountRows(int accountId) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT a.id, a.balance FROM accounts a ORDER BY a.id");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""


def f_account_row(*args):
    aid = args[0]
    for a in l6common.ACCOUNTS:
        if a[0] == aid:
            name = l6common.customer_name(a[1]) or "unknown"
            city = l6common.customer_city(a[1]) or "unknown"
            return [f"{aid}|{name}|{city}|{l6common.money(l6common.CENTS(str(a[2])))}"]
    return []


ex32.method(
    "write",
    "j6-l3.2-write-map",
    "Mapping a join onto a row",
    ["o1"],
    ["J6.09"],
    ["IMPL"],
    "Write the mapping that turns one joined row into the string `account|customer|city|balance`. A customer whose city is unknown becomes the word unknown.",
    [("accountRows", [("accountId", "int")], "List<String>")],
    {"accountRows": f_account_row},
    [("accountRows", (1,), "the accounts with their customer"),
     ("accountRows", (3,), "an account whose customer has no city"),
     ("accountRows", (99,), "an account that does not exist")],
    [("accountRows", (2,), "an account with a customer from a known city"),
     ("accountRows", (4,), "an account with a customer from a known city"),
     ("accountRows", (5,), "an account with a customer from a known city"),
     ("accountRows", (1,), "an account with a customer from a known city"),
     ("accountRows", (3,), "an account whose customer has no city")],
    starter="""
List<String> accountRows(int accountId) {
    return List.of();
}
""",
    solution=ACCOUNT_ROWS_SOURCE,
    wrongs={"no-join": ACCOUNT_ROWS_SOURCE_BAD},
    hints=["Which columns does the row have, and in what order do you build the string?", "How do you spell a null city in the output?"],
    misconceptions=(),
    difficulty=2,
)


ex32.explain(
    "j6-l3.2-explain-repository",
    "Where the SQL lives",
    ["o2"],
    ["J6.09"],
    "A team asks you to add a new report. What should you add, and where should the query live?",
    "A repository owns the queries for one concept.",
    levels={
        2: ("The answer names the repository and keeps the rest of the app free of SQL.", [
            "One repository per concept, with the queries inside it.",
            "Add a method to the account repository that runs the new query and returns domain objects; the caller never sees SQL."]),
        1: ("The answer names a repository but leaks a query elsewhere.", [
            "The answer allows a query in the calling code.",
            "Write the new query in the report class that needs it, and keep the repository for the old ones."]),
        0: ("The answer puts the SQL back into the domain model.", [
            "The answer suggests the domain object runs a query.",
            "Give the Account class a method that opens a connection and loads its own transactions."]),
    },
)


l6_l3_2 = Lesson("j6-l3.2", "Mapping rows and repositories", ["J6.09"], [
    ("o1", "Map a ResultSet row onto a domain object, and keep SQL out of the domain model"),
    ("o2", "Keep the query inside the repository, and use generated keys when inserting"),
], ["j6-l3.1"], 45, ["I77", "I79", "I78"], """## Before you start

You should have written a query with a join, and you should know what a record is.

## Explanation

A **repository** hides the SQL behind a method. The rest of the app should not know which table holds the data.

## Worked examples

### Example 1: mapping a join.

```java
String row = accountId + "|" + customer + "|" + city + "|" + balance;
```

### Example 2: generated keys.

```java
PreparedStatement ps = db.prepareStatement("INSERT INTO savings (customer_id, balance) VALUES (?, ?)", Statement.RETURN_GENERATED_KEYS);
```

## Predict, then run

::exercise{id=j6-l3.2-write-map}

## Where this is used

- Any place that turns a row into an object without leaking SQL into the design.

## Common mistakes

- **Leaking the query into the domain model.**

## Practice

::exercise{id=j6-l3.2-write-map}

::exercise{id=j6-l3.2-explain-repository}

## Further reading

- **Jakarta Persistence 3.2** `[I79]` on entities.

## How you'll be assessed

- The **write** exercise checks that you can map a row (*implementation*).
- The **explain** exercise checks that the SQL lives in a repository (*explanation*).
""")


# ====================================================================== j6-l3.3
PAY_SOURCE = """
String transferJdbc(int from, int to, double amount) {
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

def f_transfer(*args):
    source, target, amount = args
    from_cents = round(float(BAL[source]) * 100) if source in BAL else None
    to_cents = round(float(BAL[target]) * 100) if target in BAL else None
    if from_cents is None or to_cents is None or from_cents - round(float(amount) * 100) < 0:
        return "23513"
    return l6common.money(from_cents - round(float(amount) * 100)) + "|" + l6common.money(to_cents + round(float(amount) * 100))


BAL = {1: 1200.00, 2: 300.50, 3: 0.00, 4: 780.25, 5: 50.00}
PAY_F = f_transfer

SAFE_QUERY = """
String rowCount(String table) {
    if (!List.of("customers", "accounts", "transactions").contains(table)) {
        return "unknown";
    }
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.one(db, "SELECT COUNT(*) FROM " + table);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
"""

SAFE_QUERY_LEAK = """
String rowCount(String table) throws SQLException {
    if (!List.of("customers", "accounts", "transactions").contains(table)) {
        return "unknown";
    }
    Connection db = Db.open();
    Db.reset(db);
    return Db.one(db, "SELECT COUNT(*) FROM " + table);
}
"""

SAFE_QUERY_MANUAL = """
String rowCount(String table) throws SQLException {
    if (!List.of("customers", "accounts", "transactions").contains(table)) {
        return "unknown";
    }
    Connection db = Db.open();
    Db.reset(db);
    String value = Db.one(db, "SELECT COUNT(*) FROM " + table);
    db.close();
    return value;
}
"""

_ROW_COUNTS = {"customers": len(CUSTOMERS), "accounts": len(ACCOUNTS), "transactions": len(TRANSACTIONS)}


def f_row_count(*args):
    return str(_ROW_COUNTS.get(args[0], "unknown"))


ex33.method(
    "write",
    "j6-l3.3-write-transfer-jdbc",
    "A transfer through a connection",
    ["o1"],
    ["J6.10"],
    ["IMPL"],
    "Write the transfer as a JDBC transaction: auto-commit off, two statements, commit; on failure roll back.",
    [("transferJdbc", [("from", "int"), ("to", "int"), ("amount", "double")], "String")],
    {"transferJdbc": PAY_F},
    [("transferJdbc", (1, 2, 100.0), "a transfer between two open accounts"),
     ("transferJdbc", (3, 1, 10.0), "an overdraft is rejected"),
     ("transferJdbc", (2, 1, 50.0), "a transfer between two open accounts")],
    [("transferJdbc", (5, 4, 25.0), "a small transfer"),
     ("transferJdbc", (2, 5, 300.5), "a transfer that drains an account"),
     ("transferJdbc", (1, 2, 1200.0), "a transfer that drains the source"),
     ("transferJdbc", (4, 3, 5.0), "a transfer between two open accounts"),
     ("transferJdbc", (5, 4, 50.0), "a small transfer")],
    starter="""
String transferJdbc(int from, int to, double amount) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", java.math.BigDecimal.valueOf(amount), from);
        Db.update(db, "UPDATE accounts SET balance = balance + ? WHERE id = ?", java.math.BigDecimal.valueOf(amount), to);
        return "committed";
    } catch (SQLException e) {
        return e.getSQLState();
    }
}
""",
    solution=PAY_SOURCE,
    wrongs={"no-transaction": """
String transferJdbc(int from, int to, double amount) {
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
"""},
    hints=["Turn auto-commit off before the first statement, and commit or roll back around them.", "Which side can break the balance?"],
    misconceptions=(),
    difficulty=3,
)


ex33.method(
    "debug",
    "j6-l3.3-debug-leak",
    "A connection left open",
    ["o2"],
    ["J6.10"],
    ["DEBUG"],
    "The helper counts the rows of a table, but it never closes the connection it opens, so every call leaks one database session. Fix it so the connection is closed even when a statement fails, using try-with-resources, and keep the check that only known tables are counted.",
    [("rowCount", [("table", "String")], "String")],
    {"rowCount": f_row_count},
    [("rowCount", ("customers",), "a known table"),
     ("rowCount", ("transactions",), "a known table with more rows"),
     ("rowCount", ("branches",), "an unknown table")],
    [("rowCount", ("accounts",), "a known table"),
     ("rowCount", ("customers; DROP TABLE accounts",), "an injection attempt is refused"),
     ("rowCount", ("ACCOUNTS",), "names are matched exactly"),
     ("rowCount", ("",), "an empty name"),
     ("rowCount", ("transactions",), "a known table with more rows")],
    starter=SAFE_QUERY_LEAK,
    solution=SAFE_QUERY,
    wrongs={"manual-close": SAFE_QUERY_MANUAL},
    hints=["Which resource does the helper own, and when does try-with-resources close it?", "Why does an unclosed connection keep a database session alive?"],
    misconceptions=(),
    difficulty=3,
    source_tests=[("closes the connection with try-with-resources", ["try (Connection db = Db.open()"], ["db.close();"])],
)


l6_l3_3 = Lesson("j6-l3.3", "Transactions and resource management in JDBC", ["J6.10"], [
    ("o1", "Commit or roll back a JDBC transaction around failing statements"),
    ("o2", "Close connections and statements in the right order"),
], ["j6-l2.2"], 45, ["I76", "I77", "I78"], """## Before you start

You should have written a transaction, and you should know what a connection is.

## Explanation

A **connection** wraps a session. Resources that belong to the session — statements and result sets — are closed before the connection. An **unclosed connection** holds a session open.

## Worked examples

### Example 1: closing in the right order.

```java
try (Connection db = Db.open()) {
    try (Statement s = db.createStatement()) {
        // ...
    }
}
```

### Example 2: rolling back.

```java
db.setAutoCommit(false);
// statements
db.rollback();
```

## Predict, then run

::exercise{id=j6-l3.3-write-transfer-jdbc}

## Where this is used

- Every service that talks to the database.

## Common mistakes

- **Closing the connection before the statement.**

## Practice

::exercise{id=j6-l3.3-write-transfer-jdbc}

::exercise{id=j6-l3.3-debug-leak}

## Further reading

- **Java SE 25 API** `[I76]` on `Connection`.

## How you'll be assessed

- The **write** exercise checks that a transaction is committed or rolled back (*implementation*).
- The **debug** exercise checks that you close what you open (*debugging*).
""")


print("module 6.3 authored")
