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

List<String> accountsOf(int customerId) {
    try (Connection db = Db.open()) {
        Db.reset(db);
        return Db.query(db, "SELECT id, balance FROM accounts ORDER BY id");
    } catch (SQLException e) {
        throw new RuntimeException(e);
    }
}

void main() {
}
