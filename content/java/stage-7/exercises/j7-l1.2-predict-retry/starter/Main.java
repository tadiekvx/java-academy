class Bank {
    int balance = 100;

    void put(int value) {
        balance = value;
    }

    void post(int amount) {
        balance += amount;
    }
}

void main() {
    Bank replaced = new Bank();
    replaced.put(150);
    replaced.put(150);
    Bank added = new Bank();
    added.post(50);
    added.post(50);
    System.out.println("after two PUTs=" + replaced.balance);
    System.out.println("after two POSTs=" + added.balance);
}
