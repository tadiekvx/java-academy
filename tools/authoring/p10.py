"""Stage 6 projects: j6-p1-brightbank (B) and j6-a1-slow-report (C). Expected values are computed here, not from Java."""
import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-6"
import l6common
from l6common import complete_method_source, CUSTOMERS, ACCOUNTS, TRANSACTIONS, money
from proj import project

MAIN = "\nvoid main() {\n    // Optional: try your methods here.\n}\n"


def full(src):
    return complete_method_source(src) + MAIN


BAL = {a[0]: round(a[2] * 100) for a in ACCOUNTS}
STATUS = {a[0]: a[3] for a in ACCOUNTS}
TOTAL = sum(BAL.values())


def cents(c):
    return money(c)


# ------------------------------------------------------------------ B: Brightbank on a database
def f_open(customer, opening):
    if customer in {c[0] for c in CUSTOMERS} and opening > 0:
        return f"6|{money(opening)}|accounts=6"
    return "rejected|accounts=5"


def f_transfer(src, dst, amount):
    a = round(amount * 100)
    ok = (src != dst and a > 0 and src in BAL and dst in BAL and STATUS[src] == "open"
          and STATUS[dst] == "open" and BAL[src] >= a)
    if ok:
        return f"ok|{cents(BAL[src] - a)}|{cents(BAL[dst] + a)}|tx=8|total={cents(TOTAL)}"
    return f"rejected|tx=6|total={cents(TOTAL)}"


def f_find(part):
    return ",".join(sorted(n for _, n, _ in CUSTOMERS if part.lower() in n.lower()))


OPEN_SOL = '''
String openAccount(int customerId, double opening) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        db.setAutoCommit(false);
        try {
            int id = Integer.parseInt(Db.one(db, "SELECT MAX(id) + 1 FROM accounts"));
            BigDecimal amount = BigDecimal.valueOf(opening);
            Db.update(db, "INSERT INTO accounts VALUES (?, ?, ?, 'open', '2025-01-01')", id, customerId, amount);
            long tx = Long.parseLong(Db.one(db, "SELECT MAX(id) + 1 FROM transactions"));
            Db.update(db, "INSERT INTO transactions VALUES (?, ?, 'deposit', ?, '2025-01-02 09:00:00')", tx, id, amount);
            db.commit();
            return id + "|" + amount.setScale(2).toPlainString() + "|accounts=" + Db.one(db, "SELECT COUNT(*) FROM accounts");
        } catch (SQLException e) {
            db.rollback();
            return "rejected|accounts=" + Db.one(db, "SELECT COUNT(*) FROM accounts");
        }
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
'''
OPEN_STUB = '''
String openAccount(int customerId, double opening) {
    // Milestone 1: insert the account and its opening deposit as one transaction.
    return "";
}
'''
OPEN_WRONG = OPEN_SOL.replace("        db.setAutoCommit(false);\n", "").replace("            db.commit();\n", "").replace("            db.rollback();\n", "")

TRANSFER_SOL = '''
String transfer(int from, int to, double amount) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        db.setAutoCommit(false);
        try {
            BigDecimal value = BigDecimal.valueOf(amount);
            String source = Db.one(db, "SELECT status, balance FROM accounts WHERE id = ?", from);
            String target = Db.one(db, "SELECT status, balance FROM accounts WHERE id = ?", to);
            boolean allowed = from != to && value.signum() > 0
                    && source != null && target != null
                    && source.startsWith("open|") && target.startsWith("open|")
                    && new BigDecimal(source.substring(5)).compareTo(value) >= 0;
            if (!allowed) {
                db.rollback();
                return rejected(db);
            }
            Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", value, from);
            Db.update(db, "UPDATE accounts SET balance = balance + ? WHERE id = ?", value, to);
            long tx = Long.parseLong(Db.one(db, "SELECT MAX(id) + 1 FROM transactions"));
            Db.update(db, "INSERT INTO transactions VALUES (?, ?, 'withdrawal', ?, '2025-02-01 10:00:00')", tx, from, value);
            Db.update(db, "INSERT INTO transactions VALUES (?, ?, 'deposit', ?, '2025-02-01 10:00:00')", tx + 1, to, value);
            db.commit();
            return "ok|" + Db.one(db, "SELECT balance FROM accounts WHERE id = ?", from)
                    + "|" + Db.one(db, "SELECT balance FROM accounts WHERE id = ?", to)
                    + "|tx=" + Db.one(db, "SELECT COUNT(*) FROM transactions")
                    + "|total=" + Db.one(db, "SELECT SUM(balance) FROM accounts");
        } catch (SQLException e) {
            db.rollback();
            return rejected(db);
        }
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}

String rejected(Connection db) throws SQLException {
    return "rejected|tx=" + Db.one(db, "SELECT COUNT(*) FROM transactions")
            + "|total=" + Db.one(db, "SELECT SUM(balance) FROM accounts");
}
'''
TRANSFER_STUB = '''
String transfer(int from, int to, double amount) {
    // Milestone 2: move money between two open accounts in one transaction.
    return "";
}

String rejected(Connection db) throws SQLException {
    return "rejected|tx=" + Db.one(db, "SELECT COUNT(*) FROM transactions")
            + "|total=" + Db.one(db, "SELECT SUM(balance) FROM accounts");
}
'''
TRANSFER_NO_STATUS = TRANSFER_SOL.replace('''                    && source.startsWith("open|") && target.startsWith("open|")\n''', "").replace('source.substring(5)', 'source.substring(source.indexOf(\'|\') + 1)')
TRANSFER_AUTOCOMMIT = TRANSFER_SOL.replace("        db.setAutoCommit(false);\n", "").replace(
    '''            Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", value, from);
            Db.update(db, "UPDATE accounts SET balance = balance + ? WHERE id = ?", value, to);''',
    '''            Db.update(db, "UPDATE accounts SET balance = balance + ? WHERE id = ?", value, to);
            Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", value, from);''').replace(
    "            boolean allowed = ", "            boolean allowed = true || ").replace("                db.rollback();\n                return rejected(db);\n            }\n            Db.update", "                return rejected(db);\n            }\n            Db.update").replace("            db.rollback();\n            return rejected(db);", "            return rejected(db);").replace("            db.commit();\n", "")

FIND_SOL = '''
String findCustomers(String namePart) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        List<String> names = Db.query(db, "SELECT name FROM customers WHERE LOWER(name) LIKE ? ORDER BY name",
                "%" + namePart.toLowerCase() + "%");
        return String.join(",", names);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
'''
FIND_STUB = '''
String findCustomers(String namePart) {
    // Milestone 3: search by part of a name, ignoring case, with a bound parameter.
    return "";
}
'''
FIND_CONCAT = FIND_SOL.replace('"SELECT name FROM customers WHERE LOWER(name) LIKE ? ORDER BY name",\n                "%" + namePart.toLowerCase() + "%"', '"SELECT name FROM customers WHERE LOWER(name) LIKE \'%" + namePart.toLowerCase() + "%\' ORDER BY name"')
FIND_CASE = FIND_SOL.replace("LOWER(name) LIKE ?", "name LIKE ?").replace("namePart.toLowerCase()", "namePart")

SOL_B = full(OPEN_SOL + TRANSFER_SOL + FIND_SOL)
STARTER_B = "// Brightbank, now on a database. The Db helper below opens an in-memory H2 database, resets it to a\n// known fixture (5 customers, 5 accounts, 6 transactions) and runs queries. Don't change it.\n\n" + full(OPEN_STUB + TRANSFER_STUB + FIND_STUB)
WRONGS_B = {
    "m1-no-transaction": full(OPEN_WRONG + TRANSFER_SOL + FIND_SOL),
    "m2-ignores-status": full(OPEN_SOL + TRANSFER_NO_STATUS + FIND_SOL),
    "m2-autocommit-credit-first": full(OPEN_SOL + TRANSFER_AUTOCOMMIT + FIND_SOL),
    "m3-concatenated": full(OPEN_SOL + TRANSFER_SOL + FIND_CONCAT),
    "m3-case-sensitive": full(OPEN_SOL + TRANSFER_SOL + FIND_CASE),
}
OPEN_SIG = [("openAccount", [("customerId", "int"), ("opening", "double")], "String")]
TR_SIG = [("transfer", [("from", "int"), ("to", "int"), ("amount", "double")], "String")]
FIND_SIG = [("findCustomers", [("namePart", "String")], "String")]
ms_b = [
    dict(id="m1", title="Open an account", methods=OPEN_SIG, fns={"openAccount": f_open},
         instructions="""
         Write `openAccount(customerId, opening)`. It inserts a new account (id one higher than the largest existing id, status `open`, balance `opening`) **and** its opening deposit in the `transactions` table, in **one transaction**. If either insert fails (an unknown customer, or an opening amount that is zero or negative), nothing is kept.

         Return `id|balance|accounts=N` when it worked, or `rejected|accounts=N` when it did not, where N is the number of accounts afterwards.
         """,
         visible=[("openAccount", (2, 100.0), "a valid account"), ("openAccount", (99, 100.0), "an unknown customer"), ("openAccount", (1, 0.0), "a zero opening deposit")],
         hidden=[("openAccount", (5, 20.5), "a valid account, cents"), ("openAccount", (1, -5.0), "a negative opening amount"), ("openAccount", (3, 1200.0), "a valid account for another customer"), ("openAccount", (0, 10.0), "customer zero"), ("openAccount", (4, 0.0), "zero for a valid customer")]),
    dict(id="m2", title="Transfer money", methods=TR_SIG, fns={"transfer": f_transfer},
         instructions="""
         Write `transfer(from, to, amount)`. Both accounts must exist and be `open`, they must be different, the amount must be positive and the source balance must cover it. Then, in **one transaction**, take the money from one, give it to the other and record a withdrawal and a deposit.

         Return `ok|fromBalance|toBalance|tx=N|total=T` when it worked, or `rejected|tx=N|total=T` when it did not, where N is the number of transactions afterwards and T the sum of all balances. (`total` shows whether a failed transfer left half a change behind.) The `rejected` helper is given.
         """,
         visible=[("transfer", (1, 2, 100.0), "a valid transfer"), ("transfer", (2, 1, 1000.0), "not enough money"), ("transfer", (1, 3, 10.0), "a closed target")],
         hidden=[("transfer", (4, 5, 780.25), "draining an account"), ("transfer", (1, 1, 10.0), "the same account twice"), ("transfer", (1, 99, 10.0), "an unknown target"), ("transfer", (99, 1, 10.0), "an unknown source"), ("transfer", (3, 1, 0.0), "a closed source"), ("transfer", (2, 4, 0.0), "a zero amount"), ("transfer", (5, 1, 50.01), "one cent too much")]),
    dict(id="m3", title="Search safely", methods=FIND_SIG, fns={"findCustomers": f_find},
         instructions="""
         Write `findCustomers(namePart)`: the names of the customers whose name contains `namePart`, ignoring case, in alphabetical order, joined with commas. Use a **bound parameter**, not string concatenation.
         """,
         visible=[("findCustomers", ("ada",), "lower case"), ("findCustomers", ("ur",), "inside a name"), ("findCustomers", ("zzz",), "no match")],
         hidden=[("findCustomers", ("' OR '1'='1",), "an injection attempt matches nothing"), ("findCustomers", ("o'hara",), "an apostrophe"), ("findCustomers", ("ADA",), "upper case"), ("findCustomers", ("a",), "matches everyone"), ("findCustomers", ("is",), "two names"), ("findCustomers", ("er",), "more than one match")]),
]
rubric_b = [
    ("Transactions", "Statements are saved one by one, so a failure leaves half a change", "Uses a transaction but forgets one failure path", "Every multi-statement change commits together or rolls back, and the checks prove it"),
    ("Validation before writing", "Relies on the database to throw for rules the code could check", "Checks some rules before writing", "Checks the rules first, and the constraints are the safety net"),
    ("Safe queries", "Builds SQL by joining strings", "Uses bound parameters in some places", "Every value is a bound parameter and the injection check passes"),
    ("Design note", "Missing or only describes the code", "Explains the code but not the choices", "Explains what must be atomic and why, and what the database enforces versus the code"),
]
project("j6-p1-brightbank", "Brightbank on a database", "B",
        "Add a database layer to Brightbank: open an account atomically, transfer money safely, and search without injection.",
        """
        Brightbank now keeps its data in a database. The helper at the top of the file creates an in-memory H2 database with five customers, five accounts and six transactions, and gives you `Db.query`, `Db.one` and `Db.update`.

        You will write three operations the way a small banking service would:

        1. **Open an account** and its opening deposit as one transaction.
        2. **Transfer money** between two open accounts, with every rule checked and a failure leaving nothing behind.
        3. **Search customers** with a bound parameter, so a search term can never become SQL.

        Each call starts from a fresh copy of the same data, so the answers are repeatable.
        """, 3, ["j6-l2.2", "j6-l3.1", "j6-l3.3"], ["J6.05", "J6.06", "J6.08", "J6.10"],
        ["Opening an account writes the account and its deposit together or not at all.",
         "A transfer needs two different open accounts, a positive amount and enough money.",
         "Searches use bound parameters."],
        ["Use try-with-resources for the connection.", "No string concatenation inside SQL."],
        ["Given an unknown customer or a zero opening deposit, then nothing is kept.",
         "Given a failed transfer, then no balance or transaction changed.",
         "Given an injection attempt, then no customer matches."],
        ms_b, rubric_b,
        "In 150 words or fewer: Which statements had to be atomic and why? Which rules did your code check, and which did you leave to the database constraints? Where in a real service would the transaction boundary sit?",
        STARTER_B, SOL_B, WRONGS_B)

# ------------------------------------------------------------------ C: inherited report
CITY_OPEN_TOTAL = {}


def f_totals(city):
    rows = []
    for cid, name, c in sorted(CUSTOMERS, key=lambda r: r[1]):
        if city is not None and c != city:
            continue
        total = sum(round(a[2] * 100) for a in ACCOUNTS if a[1] == cid and a[3] == "open")
        rows.append(f"{name}|{money(total)}")
    return rows


INH = '''
List<String> customerTotals(String city) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        List<String> out = new ArrayList<>();
        List<String> customers = city == null
                ? Db.query(db, "SELECT id, name FROM customers ORDER BY name")
                : Db.query(db, "SELECT id, name FROM customers WHERE city = '" + city + "' ORDER BY name");
        for (String row : customers) {
            String[] parts = row.split("\\\\|");
            String total = Db.one(db, "SELECT SUM(balance) FROM accounts WHERE customer_id = ? AND status = 'open'", Integer.parseInt(parts[0]));
            out.add(parts[1] + "|" + total);
        }
        return out;
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
'''
M1 = INH.replace('            out.add(parts[1] + "|" + total);', '            if (total.equals("null")) {\n                total = "0.00";\n            }\n            out.add(parts[1] + "|" + total);')
JOINED = '''
List<String> customerTotals(String city) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        String sql = "SELECT c.name, CAST(COALESCE(SUM(a.balance), 0) AS numeric(12,2)) FROM customers c "
                + "%s JOIN accounts a ON a.customer_id = c.id AND a.status = 'open' "
                + (city == null ? "" : "WHERE c.city = '" + city + "' ")
                + "GROUP BY c.id, c.name ORDER BY c.name";
        return Db.query(db, sql);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
'''
M2 = JOINED % "LEFT"
M2_INNER = JOINED % "INNER"
M3 = '''
List<String> customerTotals(String city) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        String sql = "SELECT c.name, CAST(COALESCE(SUM(a.balance), 0) AS numeric(12,2)) FROM customers c "
                + "LEFT JOIN accounts a ON a.customer_id = c.id AND a.status = 'open' "
                + (city == null ? "" : "WHERE c.city = ? ")
                + "GROUP BY c.id, c.name ORDER BY c.name";
        return city == null ? Db.query(db, sql) : Db.query(db, sql, city);
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}
'''
M3_NULL = M3.replace('(city == null ? "" : "WHERE c.city = ? ")', '"WHERE c.city = ? "').replace("return city == null ? Db.query(db, sql) : Db.query(db, sql, city);", "return Db.query(db, sql, city);")
M1_ZERO = M1.replace('            if (total.equals("null")) {\n                total = "0.00";\n            }\n', '            total = "0.00";\n')
CT_SIG = [("customerTotals", [("city", "String")], "List<String>")]
V = [("customerTotals", (None,), "every customer"), ("customerTotals", ("Cape Town",), "one city"), ("customerTotals", ("Durban",), "a customer with no open account")]
H = [("customerTotals", ("Johannesburg",), "one customer with one account"), ("customerTotals", ("Nowhere",), "an unknown city"), ("customerTotals", ("",), "an empty city"), ("customerTotals", ("cape town",), "case matters"), ("customerTotals", (None,), "every customer again")]
H3 = H + [("customerTotals", ("Cote d'Ivoire",), "a city with an apostrophe"), ("customerTotals", ("' OR '1'='1",), "an injection attempt matches nothing")]
ms_c = [
    dict(id="m1", title="Ticket 611: 'null' in the report", methods=CT_SIG, fns={"customerTotals": f_totals},
         instructions="""
         **Ticket 611:** *"The customer totals report prints `Alan Turing|null` and `Barbara Liskov|null`. A customer with no open account should show `0.00`."*

         Reproduce it with `customerTotals(null)`, find the cause, and make the smallest fix. Don't restructure anything yet.
         """, visible=V, hidden=H),
    dict(id="m2", title="Ticket 612: it is slow", methods=CT_SIG, fns={"customerTotals": f_totals},
         instructions="""
         **Ticket 612:** *"The report takes forever on the real database: it runs one extra query for every customer."* That is the N+1 pattern from the lessons.

         Replace the loop with **one query** that joins customers to their open accounts and groups by customer. Keep every answer the same, including customers with no open account. The check looks for `LEFT JOIN` and `GROUP BY` in your source.
         """, visible=V, hidden=H,
         source_tests=[("one joined, grouped query", ["LEFT JOIN", "GROUP BY"], None)]),
    dict(id="m3", title="Review: do not build SQL from the city", methods=CT_SIG, fns={"customerTotals": f_totals},
         instructions="""
         The reviewer writes:

         > *"The city goes straight into the SQL string. A city like `Cote d'Ivoire` breaks the query, and a crafted value can do worse. Please use a bound parameter."*

         Bind the city as a parameter. `null` must still mean every customer.
         """, visible=V, hidden=H3,
         source_tests=[("no concatenated city", None, ["c.city = '\" + city"])]),
]
rubric_c = [
    ("Reproduce, then fix", "Changed code without reproducing the ticket", "Fixed it but did not show the failing call first", "Reproduced the ticket with a specific call, found the cause, made the smallest fix"),
    ("Removing N+1", "Left the per-customer query in place", "Reduced the queries but changed an answer", "One grouped query, every earlier check still passing"),
    ("Handling review", "Ignored the comment, or broke the null case", "Bound the parameter but changed behaviour", "Bound parameter, null still means all customers, apostrophes work"),
    ("Design note", "Missing or only describes the code", "Describes the changes but not the reasoning", "Explains the three causes and how each fix was kept separate and checked"),
]
project("j6-a1-slow-report", "The slow, wrong report", "C",
        "Take over an inherited JDBC report: fix a wrong 'null', remove an N+1 loop, and answer a review about injection.",
        """
        You have inherited the customer totals report from a developer who has left. It queries the database through JDBC. Three things are wrong with it, and they arrive as two tickets and a code review:

        1. **A wrong answer** (ticket 611).
        2. **A slow report** (ticket 612): one query per customer.
        3. **An unsafe query** (review): the city is joined into the SQL string.

        Fix them one at a time, running all the checks after each, and say in your design note what you would commit separately.
        """, 3, ["j6-l1.3", "j6-l3.1", "j4-l4.2", "j6-l4.2"], ["J6.03", "J6.08", "J6.12"],
        ["A customer with no open account shows `0.00`.", "The report runs one query, not one per customer.",
         "The city is a bound parameter, and `null` still means every customer."],
        ["Fix one ticket at a time.", "Run all the checks after every change."],
        ["Given a customer without open accounts, then the report shows 0.00.",
         "Given the report, then it is one joined, grouped query.",
         "Given a city with an apostrophe, then the report works."],
        ms_c, rubric_c,
        "In 150 words or fewer: What caused the 'null'? Why does a loop of queries get slower with more customers, and how did your query avoid it? Why is a bound parameter safer than a quoted string? What would your commits have been?",
        "// INHERITED CODE: the customer totals report.\n// Ticket 611: customers with no open account print 'null'. Ticket 612: it is slow.\n\n" + full(INH),
        full(M3), {
            "m1-zeroes-everything": full(M1_ZERO),
            "m2-inner-join": full(M2_INNER),
            "m3-still-concatenated": full(M2),
            "m3-null-matches-nothing": full(M3_NULL),
        })
print("P10 written")
