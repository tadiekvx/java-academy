"""Shared authoring helpers for Stage 6 content (module scripts, not part of the product).

One SQL/JDBC exercise is one compact Java source file. The shared fixture and row helpers are
copied into every file; lesson scripts supply the learner's method, the expected values come from
this module's Python data, never from running the Java solution.
"""
import build

build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-6"
from build import Lesson, Exercises, q, code  # noqa: E402
import outline  # noqa: E402

register = outline.register

CUSTOMERS = [
    (1, "Ada Lovelace", "Cape Town"),
    (2, "Grace Hopper", "Johannesburg"),
    (3, "Alan Turing", None),
    (4, "Edsger Dijkstra", "Cape Town"),
    (5, "Barbara Liskov", "Durban"),
]
ACCOUNTS = [
    (1, 1, 1200.00, "open", "2024-01-10"),
    (2, 2, 300.50, "open", "2024-02-01"),
    (3, 3, 0.00, "closed", "2024-03-15"),
    (4, 4, 780.25, "open", "2024-04-20"),
    (5, 1, 50.00, "open", "2024-05-05"),
]
TRANSACTIONS = [
    (1, 1, "deposit", 500.00, "2025-01-02 09:00:00"),
    (2, 1, "withdrawal", 200.00, "2025-01-05 11:30:00"),
    (3, 1, "deposit", 100.00, "2025-01-09 16:45:00"),
    (4, 2, "deposit", 300.50, "2025-01-03 10:15:00"),
    (5, 4, "deposit", 780.25, "2025-01-04 14:00:00"),
    (6, 5, "deposit", 50.00, "2025-01-06 08:20:00"),
]
CENTS = lambda text: int(round(float(text) * 100))
CENTS_BY = {row[0]: row[2] for row in ACCOUNTS}


def money(value):
    """Format an amount (float or cents) with two decimal places."""
    cents = int(round(float(value) * 100)) if not isinstance(value, int) else int(value)
    sign = "-" if cents < 0 else ""
    value = abs(cents)
    return f"{sign}{value // 100}.{value % 100:02d}"


def account_balance(account_id):
    for aid, _, balance, _, _ in ACCOUNTS:
        if aid == account_id:
            return money(CENTS(str(balance)))
    return None


def customer_name(customer_id):
    for cid, name, _ in CUSTOMERS:
        if cid == customer_id:
            return name
    return None


def accounts_of(customer_id):
    return sorted(a for a in ACCOUNTS if a[1] == customer_id)


def transactions_of(account_id):
    return sorted(t for t in TRANSACTIONS if t[1] == account_id)


def customers_in(city):
    if city is None:
        return sorted(name for _, name, c in CUSTOMERS if c is None)
    return sorted(name for _, name, c in CUSTOMERS if c == city)


def account_counts():
    counts = {}
    for _, cid, _, _, _ in ACCOUNTS:
        counts[cid] = counts.get(cid, 0) + 1
    return [(cid, name, counts.get(cid, 0)) for cid, name, _ in CUSTOMERS]


def account_totals_by_customer():
    return [(cid, name, sum(CENTS(str(a[2])) for a in ACCOUNTS if a[1] == cid)) for cid, name, _ in CUSTOMERS]


DB_HELPERS = r'''
final class Db {
    static final String URL = "jdbc:h2:mem:stage6;DB_CLOSE_DELAY=-1";

    static Connection open() throws SQLException {
        return DriverManager.getConnection(URL);
    }

    static void reset(Connection db) throws SQLException {
        try (Statement s = db.createStatement()) {
            s.execute("DROP ALL OBJECTS");
            s.execute("CREATE TABLE customers (id integer PRIMARY KEY, name varchar(100) NOT NULL, city varchar(100))");
            s.execute("CREATE TABLE accounts (id integer PRIMARY KEY, customer_id integer NOT NULL REFERENCES customers(id), balance numeric(12,2) NOT NULL CHECK (balance >= 0), status varchar(20) NOT NULL DEFAULT 'open', opened_on date NOT NULL)");
            s.execute("CREATE TABLE transactions (id bigint PRIMARY KEY, account_id integer NOT NULL REFERENCES accounts(id), kind varchar(20) NOT NULL CHECK (kind IN ('deposit', 'withdrawal')), amount numeric(12,2) NOT NULL CHECK (amount > 0), occurred_at timestamp NOT NULL)");
            s.execute("INSERT INTO customers VALUES (1, 'Ada Lovelace', 'Cape Town'), (2, 'Grace Hopper', 'Johannesburg'), (3, 'Alan Turing', NULL), (4, 'Edsger Dijkstra', 'Cape Town'), (5, 'Barbara Liskov', 'Durban')");
            s.execute("INSERT INTO accounts VALUES (1, 1, 1200.00, 'open', '2024-01-10'), (2, 2, 300.50, 'open', '2024-02-01'), (3, 3, 0.00, 'closed', '2024-03-15'), (4, 4, 780.25, 'open', '2024-04-20'), (5, 1, 50.00, 'open', '2024-05-05')");
            s.execute("INSERT INTO transactions VALUES (1, 1, 'deposit', 500.00, '2025-01-02 09:00:00'), (2, 1, 'withdrawal', 200.00, '2025-01-05 11:30:00'), (3, 1, 'deposit', 100.00, '2025-01-09 16:45:00'), (4, 2, 'deposit', 300.50, '2025-01-03 10:15:00'), (5, 4, 'deposit', 780.25, '2025-01-04 14:00:00'), (6, 5, 'deposit', 50.00, '2025-01-06 08:20:00')");
        }
    }

    static List<String> query(Connection db, String sql, Object... params) throws SQLException {
        List<String> rows = new ArrayList<>();
        try (PreparedStatement ps = db.prepareStatement(sql)) {
            for (int i = 0; i < params.length; i++) {
                ps.setObject(i + 1, params[i]);
            }
            try (ResultSet rs = ps.executeQuery()) {
                int columns = rs.getMetaData().getColumnCount();
                while (rs.next()) {
                    StringBuilder row = new StringBuilder();
                    for (int c = 1; c <= columns; c++) {
                        if (c > 1) {
                            row.append('|');
                        }
                        row.append(rs.getString(c));
                    }
                    rows.add(row.toString());
                }
            }
        }
        return rows;
    }

    static List<String> value(Connection db, String sql, Object... params) throws SQLException {
        return query(db, sql, params);
    }

    static String one(Connection db, String sql, Object... params) throws SQLException {
        List<String> rows = query(db, sql, params);
        return rows.isEmpty() ? null : rows.getFirst();
    }

    static String DbState(Connection db, String sql) {
        try {
            update(db, sql);
            return "ok";
        } catch (SQLException e) {
            return e.getSQLState();
        }
    }

    static int update(Connection db, String sql, Object... params) throws SQLException {
        try (PreparedStatement ps = db.prepareStatement(sql)) {
            for (int i = 0; i < params.length; i++) {
                ps.setObject(i + 1, params[i]);
            }
            return ps.executeUpdate();
        }
    }
}
'''

IMPORTS = "import java.math.BigDecimal;\nimport java.sql.*;\nimport java.util.*;\n"


def sql_file(method_source, main_call, extra=""):
    """Complete compact source: imports, shared fixture helpers, the learner method, main."""
    parts = [IMPORTS, DB_HELPERS]
    if extra.strip():
        parts.append("\n" + extra.strip("\n") + "\n")
    parts.append("\n" + method_source.strip("\n") + "\n\nvoid main() {\n    System.out.println(" + main_call + ");\n}\n")
    return "\n".join(parts)


def run_sql(method_body, sql, args=()):
    """A method body that runs one query through the shared fixture helper and returns rows."""
    return method_body.format(sql=sql, args=list(args))


def java_list(values):
    return "[" + ", ".join('"%s"' % v for v in values) + "]"


def customer_city(customer_id):
    for cid, _, city in CUSTOMERS:
        if cid == customer_id:
            return city
    return None


def normalise_program(source):
    """Hoist imports to the top, add the shared Db fixture when the program uses it, and qualify DbState."""
    import re
    lines = source.strip("\n").split("\n")
    imports = [l for l in lines if l.startswith("import ")]
    body = "\n".join(l for l in lines if not l.startswith("import ")).strip("\n")
    uses_db = re.search(r"\bDb\.|\bDbState\(", body) is not None
    if uses_db:
        imports = IMPORTS.strip().split("\n") + imports
        if "final class Db" not in body:
            body = DB_HELPERS.strip("\n") + "\n\n" + body
    body = re.sub(r"(?<!String )(?<![.\w])DbState\(", "Db.DbState(", body)
    seen, unique = set(), []
    for l in imports:
        if l not in seen:
            seen.add(l)
            unique.append(l)
    return "\n".join(unique) + ("\n\n" if unique else "") + body + "\n"


_original_predict = build.Exercises.predict


def _predict(self, id, title, assesses, concepts, prompt, program, expected, hints, *a, **k):
    return _original_predict(self, id, title, assesses, concepts, prompt, normalise_program(program), expected, hints, *a, **k)


build.Exercises.predict = _predict


def complete_method_source(source):
    """A method-exercise file: imports, the shared Db fixture, then the learner's methods."""
    import re
    lines = source.strip("\n").split("\n")
    imports = IMPORTS.strip().split("\n") + [l for l in lines if l.startswith("import ")]
    body = "\n".join(l for l in lines if not l.startswith("import ")).strip("\n")
    if "final class Db" not in body:
        body = DB_HELPERS.strip("\n") + "\n\n" + body
    body = re.sub(r"(?<!String )(?<![.\w])DbState\(", "Db.DbState(", body)
    seen, unique = set(), []
    for l in imports:
        if l not in seen:
            seen.add(l)
            unique.append(l)
    return "\n".join(unique) + "\n\n" + body + "\n"


_original_method = build.Exercises.method
_METHOD_ARGS = ["type", "id", "title", "assesses", "concepts", "evidence", "prompt", "methods", "fns",
                "visible", "hidden", "starter", "solution", "wrongs"]


def _method(self, *a, **k):
    a = list(a)
    for name in ("starter", "solution", "wrongs"):
        index = _METHOD_ARGS.index(name)
        if name in k:
            k[name] = _fix(name, k[name])
        elif index < len(a):
            a[index] = _fix(name, a[index])
    return _original_method(self, *a, **k)


def _fix(name, value):
    if name == "wrongs":
        return {key: complete_method_source(text) for key, text in value.items()}
    return complete_method_source(value)


build.Exercises.method = _method
