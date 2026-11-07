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
            text.append(line).append("\n");
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
        int interest = (balance() * percent + 99) / 100;
        if (interest > 0) {
            deposit(interest);
        }
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
