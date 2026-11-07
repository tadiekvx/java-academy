// Brightbank v2: the same rules as stage 1, now as classes.
// Money is whole pence. A transaction is a Deposit or a Withdrawal record (given below).
// The classes at the bottom compile but are stubs that give wrong answers. The brief says what they must do.

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
