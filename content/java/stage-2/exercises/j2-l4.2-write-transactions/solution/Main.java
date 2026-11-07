sealed interface Txn permits Deposit, Withdrawal, Fee {}

record Deposit(int amount) implements Txn {}
record Withdrawal(int amount) implements Txn {}
record Fee(int percent) implements Txn {}

int apply(Txn t, int balance) {
    return switch (t) {
        case Deposit d -> balance + d.amount();
        case Withdrawal w -> balance - w.amount();
        case Fee f -> balance - balance * f.percent() / 100;
    };
}

int run(String[] specs) {
    int balance = 0;
    for (String s : specs) {
        String[] p = s.split(":");
        int n = Integer.parseInt(p[1]);
        Txn t;
        if (p[0].equals("d")) {
            t = new Deposit(n);
        } else if (p[0].equals("w")) {
            t = new Withdrawal(n);
        } else {
            t = new Fee(n);
        }
        balance = apply(t, balance);
    }
    return balance;
}

void main() {
}
