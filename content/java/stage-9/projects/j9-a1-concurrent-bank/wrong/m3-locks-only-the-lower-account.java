// The bank's account store.

class Bank {
    private final long[] balances;
    private final Object[] locks;
    private final AtomicLong transfers = new AtomicLong();

    Bank(int accounts, long initial) {
        balances = new long[accounts];
        locks = new Object[accounts];
        for (int i = 0; i < accounts; i++) {
            balances[i] = initial;
            locks[i] = new Object();
        }
    }

    void transfer(int from, int to, long amount) {
        int first = Math.min(from, to);
        int second = Math.max(from, to);
        synchronized (locks[first]) {
            {
                balances[from] -= amount;
                balances[to] += amount;
            }
        }
        transfers.incrementAndGet();
    }

    long balance(int account) {
        return balances[account];
    }

    long transfers() {
        return transfers.get();
    }
}

// ---------------------------------------------------------------------------------------------
// The drivers call Bank from several threads. Don't change them. A run that does not finish within
// 1.5 seconds (a deadlock) is reported as "timeout" instead of hanging.
// ---------------------------------------------------------------------------------------------

String runAll(List<Runnable> tasks) throws InterruptedException {
    List<Thread> threads = new ArrayList<>();
    for (Runnable task : tasks) {
        Thread thread = new Thread(task);
        thread.setDaemon(true);
        threads.add(thread);
    }
    for (Thread thread : threads) {
        thread.start();
    }
    long deadline = System.nanoTime() + 1_500_000_000L;
    for (Thread thread : threads) {
        thread.join(Math.max(1, (deadline - System.nanoTime()) / 1_000_000));
        if (thread.isAlive()) {
            return "timeout";
        }
    }
    return "finished";
}

Runnable repeat(Bank bank, int from, int to, int times) {
    return () -> {
        for (int i = 0; i < times; i++) {
            bank.transfer(from, to, 1);
        }
    };
}

String sameDirection(int threads, int perThread) throws Exception {
    Bank bank = new Bank(2, 1_000_000);
    List<Runnable> tasks = new ArrayList<>();
    for (int t = 0; t < threads; t++) {
        tasks.add(repeat(bank, 0, 1, perThread));
    }
    return runAll(tasks).equals("timeout") ? "timeout" : "a=" + bank.balance(0) + ";b=" + bank.balance(1) + ";transfers=" + bank.transfers();
}

String oppositeDirections(int pairs, int perThread) throws Exception {
    Bank bank = new Bank(2, 1_000_000);
    List<Runnable> tasks = new ArrayList<>();
    for (int p = 0; p < pairs; p++) {
        tasks.add(repeat(bank, 0, 1, perThread));
        tasks.add(repeat(bank, 1, 0, perThread));
    }
    return runAll(tasks).equals("timeout") ? "timeout" : "a=" + bank.balance(0) + ";b=" + bank.balance(1) + ";transfers=" + bank.transfers();
}

String ring(int accounts, int perThread) throws Exception {
    Bank bank = new Bank(accounts, 1_000_000);
    List<Runnable> tasks = new ArrayList<>();
    for (int i = 0; i < accounts; i++) {
        tasks.add(repeat(bank, i, (i + 1) % accounts, perThread));
    }
    if (runAll(tasks).equals("timeout")) {
        return "timeout";
    }
    List<String> balances = new ArrayList<>();
    for (int i = 0; i < accounts; i++) {
        balances.add(String.valueOf(bank.balance(i)));
    }
    return "balances=" + String.join(",", balances) + ";transfers=" + bank.transfers();
}

void main() {
    // Optional: try the driver methods here.
}
