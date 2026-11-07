// Brightbank, now with a class. Money is whole pence in an int.
// In Stage 1 an account was an int[] of transactions plus loose methods. Now the data and the rules live together.
// The class below compiles but its methods are stubs. Each milestone tells you what to write.

record Transaction(int amount) {}

class Account {
    // Step 1: what does an account remember? (fields)

    Account(int overdraftLimit) {
        // Step 2: store the overdraft limit
    }

    void deposit(int amount) {
    }

    boolean withdraw(int amount) {
        return false;
    }

    int balance() {
        return 0;
    }

    List<Transaction> history() {
        return List.of();
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
