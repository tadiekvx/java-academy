class InsufficientFundsException extends Exception {
    private final int shortBy;

    InsufficientFundsException(int shortBy) {
        super("short by " + shortBy);
        this.shortBy = shortBy;
    }

    int shortBy() {
        return shortBy;
    }
}

class Wallet {
    private int balance;

    Wallet(int balance) {
        this.balance = balance;
    }

    void spend(int amount) throws InsufficientFundsException {
        balance -= amount;
        if (balance < 0) {
            throw new InsufficientFundsException(-balance);
        }
    }

    int balance() {
        return balance;
    }
}

String run(int start, int[] amounts) {
    Wallet w = new Wallet(start);
    StringBuilder out = new StringBuilder();
    for (int a : amounts) {
        try {
            w.spend(a);
            out.append("ok ");
        } catch (InsufficientFundsException e) {
            out.append(e.getMessage()).append(" ");
        }
    }
    return out + "balance " + w.balance();
}

void main() {
}
