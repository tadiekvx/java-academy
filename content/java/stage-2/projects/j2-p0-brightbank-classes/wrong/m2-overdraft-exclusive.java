// Brightbank, now with a class. Money is whole pence in an int.

record Transaction(int amount) {}

class Account {
    private final int overdraftLimit;
    private int balance;
    private final List<Transaction> history = new ArrayList<>();

    Account(int overdraftLimit) {
        this.overdraftLimit = overdraftLimit;
    }

    void deposit(int amount) {
        balance += amount;
        history.add(new Transaction(amount));
    }

    boolean withdraw(int amount) {
        if (balance - amount <= -overdraftLimit) {
            return false;
        }
        balance -= amount;
        history.add(new Transaction(-amount));
        return true;
    }

    int balance() {
        return balance;
    }

    List<Transaction> history() {
        return new ArrayList<>(history);
    }
}

// ---------------------------------------------------------------------------------------------
// The checks call these. They show how your class will be used. Don't change them.
// ---------------------------------------------------------------------------------------------

String m1(int[] amounts) {
    Account account = new Account(0);
    for (int amount : amounts) {
        account.deposit(amount);
    }
    return "balance=" + account.balance();
}

String m2(int overdraft, int[] amounts) {
    Account account = new Account(overdraft);
    int refused = 0;
    for (int amount : amounts) {
        if (amount >= 0) {
            account.deposit(amount);
        } else if (!account.withdraw(-amount)) {
            refused++;
        }
    }
    return "balance=" + account.balance() + " refused=" + refused;
}

String m3(int[] amounts) {
    Account account = new Account(0);
    for (int amount : amounts) {
        if (amount > 0) {
            account.deposit(amount);
        }
    }
    int before = account.history().size();
    List<Transaction> copy = account.history();
    try {
        copy.clear();
    } catch (UnsupportedOperationException e) {
        // a read-only list is fine too
    }
    return "history=" + before + " afterTamper=" + account.history().size();
}

void main() {
    // Optional: try your class out here.
}
