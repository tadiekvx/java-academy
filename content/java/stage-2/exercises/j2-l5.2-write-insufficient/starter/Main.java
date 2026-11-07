class Wallet {
    private int balance;

    Wallet(int balance) {
        this.balance = balance;
    }

    void spend(int amount) {
        balance -= amount;
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
