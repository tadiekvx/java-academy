import java.util.*;

class Account {
    final int id;
    long cents;

    Account(int id, long cents) {
        this.id = id;
        this.cents = cents;
    }
}

class Context {
    private final Map<Integer, Account> managed = new HashMap<>();
    private final Map<Integer, Long> snapshot = new HashMap<>();
    int selects = 0;
    int updates = 0;

    Account find(int id) {
        Account known = managed.get(id);
        if (known != null) {
            return known;
        }
        selects++;
        Account loaded = new Account(id, 120000);
        managed.put(id, loaded);
        snapshot.put(id, loaded.cents);
        return loaded;
    }

    void flush() {
        for (Account account : managed.values()) {
            if (account.cents != snapshot.get(account.id)) {
                updates++;
                snapshot.put(account.id, account.cents);
            }
        }
    }
}

void main() {
    Context context = new Context();
    Account first = context.find(1);
    Account second = context.find(1);
    System.out.println("same instance=" + (first == second));
    System.out.println("selects=" + context.selects);
    first.cents -= 5000;
    System.out.println("seen through second=" + second.cents);
    context.flush();
    System.out.println("updates after first flush=" + context.updates);
    context.flush();
    System.out.println("updates after second flush=" + context.updates);
    context.find(2);
    context.find(2);
    System.out.println("selects now=" + context.selects);
}
