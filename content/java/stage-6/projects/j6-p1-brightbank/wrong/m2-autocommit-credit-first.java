import java.math.BigDecimal;
import java.sql.*;
import java.util.*;

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

String transfer(int from, int to, double amount) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        try {
            BigDecimal value = BigDecimal.valueOf(amount);
            String source = Db.one(db, "SELECT status, balance FROM accounts WHERE id = ?", from);
            String target = Db.one(db, "SELECT status, balance FROM accounts WHERE id = ?", to);
            boolean allowed = true || from != to && value.signum() > 0
                    && source != null && target != null
                    && source.startsWith("open|") && target.startsWith("open|")
                    && new BigDecimal(source.substring(5)).compareTo(value) >= 0;
            if (!allowed) {
                return rejected(db);
            }
            Db.update(db, "UPDATE accounts SET balance = balance + ? WHERE id = ?", value, to);
            Db.update(db, "UPDATE accounts SET balance = balance - ? WHERE id = ?", value, from);
            long tx = Long.parseLong(Db.one(db, "SELECT MAX(id) + 1 FROM transactions"));
            Db.update(db, "INSERT INTO transactions VALUES (?, ?, 'withdrawal', ?, '2025-02-01 10:00:00')", tx, from, value);
            Db.update(db, "INSERT INTO transactions VALUES (?, ?, 'deposit', ?, '2025-02-01 10:00:00')", tx + 1, to, value);
            return "ok|" + Db.one(db, "SELECT balance FROM accounts WHERE id = ?", from)
                    + "|" + Db.one(db, "SELECT balance FROM accounts WHERE id = ?", to)
                    + "|tx=" + Db.one(db, "SELECT COUNT(*) FROM transactions")
                    + "|total=" + Db.one(db, "SELECT SUM(balance) FROM accounts");
        } catch (SQLException e) {
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

void main() {
    // Optional: try your methods here.
}
