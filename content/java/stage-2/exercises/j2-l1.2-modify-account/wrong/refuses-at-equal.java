class Account {
    int balance;
    Account(int balance) { this.balance = balance; }
    void deposit(int amount) { balance += amount; }
    boolean withdraw(int amount) {
        if (amount >= balance) return false;
        balance -= amount;
        return true;
    }
}

String run(int start, int[] amounts) {
    Account acct = new Account(start);
    int ok = 0;
    for (int a : amounts) {
        if (a >= 0) acct.deposit(a);
        else if (acct.withdraw(-a)) ok++;
    }
    return acct.balance + "," + ok;
}

void main() {
}
