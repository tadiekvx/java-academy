"""Stage 9 project: j9-a1-concurrent-bank (C). Seeded race and deadlock; a daemon-thread runner reports a deadlock as "timeout"."""
import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-9"
from proj import project

MAIN = "\nvoid main() {\n    // Optional: try the driver methods here.\n}\n"
INIT = 1_000_000

HELPERS = '''
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
'''
INHERITED_BANK = '''
// INHERITED CODE: the bank's account store.
// Ticket 901: "The transfer counter on the dashboard is lower than the number of transfers we made."
// Ticket 902: "Transfers freeze when customers pay each other at the same time."

class Bank {
    private final long[] balances;
    private final Object[] locks;
    private long transfers;

    Bank(int accounts, long initial) {
        balances = new long[accounts];
        locks = new Object[accounts];
        for (int i = 0; i < accounts; i++) {
            balances[i] = initial;
            locks[i] = new Object();
        }
    }

    void transfer(int from, int to, long amount) {
        synchronized (locks[from]) {
            synchronized (locks[to]) {
                balances[from] -= amount;
                balances[to] += amount;
            }
        }
        transfers++;
    }

    long balance(int account) {
        return balances[account];
    }

    long transfers() {
        return transfers;
    }
}
'''
FINAL_BANK = '''
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
            synchronized (locks[second]) {
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
'''


def wrong(old, new, src):
    assert old in src, old
    return src.replace(old, new, 1)


SOLUTION = FINAL_BANK + HELPERS + MAIN
STARTER = INHERITED_BANK + HELPERS + MAIN
AFTER_M1 = wrong("        int first = Math.min(from, to);\n        int second = Math.max(from, to);", "        int first = from;\n        int second = to;", FINAL_BANK)
WRONGS = {
    "m1-volatile-counter": wrong("private long transfers;", "private volatile long transfers;", INHERITED_BANK) + HELPERS + MAIN,
    "m2-lock-order-follows-the-arguments": AFTER_M1 + HELPERS + MAIN,
    "m3-lock-order-follows-the-arguments": AFTER_M1 + HELPERS + MAIN,
    "m3-locks-only-the-lower-account": wrong("            synchronized (locks[second]) {\n                balances[from] -= amount;\n                balances[to] += amount;\n            }", "            {\n                balances[from] -= amount;\n                balances[to] += amount;\n            }", FINAL_BANK) + HELPERS + MAIN,
}


def same(t, p):
    return f"a={INIT - t * p};b={INIT + t * p};transfers={t * p}"


def opposite(pairs, p):
    return f"a={INIT};b={INIT};transfers={2 * pairs * p}"


def ring(n, p):
    return "balances=" + ",".join([str(INIT)] * n) + f";transfers={n * p}"


def case(m, args, name):
    return (m, args, name)


M1V = [case("sameDirection", (4, 50000), "four threads"), case("sameDirection", (2, 100000), "two busy threads"), case("sameDirection", (1, 1000), "one thread")]
M1H = M1V + [case("sameDirection", (8, 20000), "eight threads"), case("sameDirection", (0, 100), "no threads"), case("sameDirection", (3, 0), "no work"),
             case("sameDirection", (6, 30000), "six threads"), case("sameDirection", (16, 5000), "sixteen threads")]
M2V = [case("oppositeDirections", (1, 50000), "one pair, opposite directions"), case("oppositeDirections", (2, 30000), "two pairs"), case("oppositeDirections", (1, 100), "a short run")]
M2H = M2V + M1H + [case("oppositeDirections", (4, 20000), "four pairs"), case("oppositeDirections", (0, 100), "no pairs"), case("oppositeDirections", (1, 1), "one transfer each"),
                   case("oppositeDirections", (3, 40000), "three pairs")]
M3V = [case("ring", (4, 20000), "a ring of four"), case("ring", (2, 30000), "a ring of two"), case("ring", (3, 10000), "a ring of three")]
M3H = M3V + M2H + [case("ring", (8, 15000), "a ring of eight"), case("ring", (5, 20000), "a ring of five"), case("ring", (1, 1000), "one account transferring to itself"), case("ring", (6, 0), "no work")]
FNS = {"sameDirection": same, "oppositeDirections": opposite, "ring": ring}
MS = [("sameDirection", [("threads", "int"), ("perThread", "int")], "String"), ("oppositeDirections", [("pairs", "int"), ("perThread", "int")], "String"), ("ring", [("accounts", "int"), ("perThread", "int")], "String")]
ms = [
    dict(id="m1", title="Ticket 901: the lost count", methods=MS, fns=FNS, visible=M1V, hidden=M1H, instructions="""
        **Ticket 901:** *"The transfer counter on the dashboard is lower than the number of transfers we made."*

        `sameDirection(threads, perThread)` makes every thread move one unit from account 0 to account 1, `perThread` times. The balances come out right (they are protected by locks) but `transfers` is wrong. Find the cause and fix it with the right tool from lesson 9.1.3. Remember that `volatile` is not the answer to this one (lesson 9.1.4).
        """),
    dict(id="m2", title="Ticket 902: the frozen payments", methods=MS, fns=FNS, visible=M2V, hidden=M2H, instructions="""
        **Ticket 902:** *"Transfers freeze when customers pay each other at the same time."*

        `oppositeDirections` runs transfers from 0 to 1 and from 1 to 0 together. A run that does not finish is reported as `timeout`. Work out why, using what you saw in the thread dump of lesson 9.1.5, and remove the deadlock **without** giving up the per-account locks (no single global lock).
        """),
    dict(id="m3", title="Review: does it hold for a ring", methods=MS, fns=FNS, visible=M3V, hidden=M3H, instructions="""
        The reviewer writes:

        > *"I tried your fix with `ring(n, k)`: account i pays account i+1, and the last pays the first. Please make sure it works with any number of accounts."*

        Check that your lock order is a rule that works for any pair of accounts, not a trick for two. Every earlier check must still pass.
        """),
]
RUBRIC = [
    ("Diagnosis", "Changed code without finding the cause", "Found the cause of one problem by reasoning only", "Explained both causes from evidence: the lost increments of an unprotected counter and the cycle of lock waits, citing the shape of the dump"),
    ("Right tool", "Used volatile for the counter, or a global lock for the deadlock", "A correct fix that is heavier than needed", "An atomic for the counter and a global lock order for the deadlock, keeping per-account locks"),
    ("Evidence of correctness", "No reasoning about why the fix is complete", "Argued for the cases tested", "Argued why the lock order prevents any cycle for any set of accounts, not only the ones in the checks"),
    ("Honesty about testing", "Claims the code is proven thread-safe because the checks pass", "Notes the checks are probabilistic", "States that passing checks do not prove absence of a race and says what was done to make the code safe by construction"),
]
project("j9-a1-concurrent-bank", "The bank that froze", "C",
        "Take over a bank's account store with a lost-update race and a deadlock: diagnose both, fix them with the right tools, and show the fix works for any number of accounts.",
        """
        You have inherited a bank's in-memory account store. It uses a lock for each account, and customers complain about two things: a dashboard count that is too low, and payments that sometimes freeze.

        The drivers at the bottom of the file start several threads against a `Bank` and report the result. Your job is to change only the `Bank` class:

        1. **Ticket 901**: a counter that loses updates.
        2. **Ticket 902**: a deadlock when two customers pay each other.
        3. **Review**: show the fix works for a ring of accounts, not only two.

        Passing the checks is evidence, not proof: a race can pass any number of runs. Your design note says why the fixed code is safe by construction.
        """, 3, ["j9-l1.3", "j9-l1.4", "j9-l1.5"], ["J9.02", "J9.03", "J9.05"],
        ["The transfer counter equals the number of transfers made.",
         "Opposite and circular transfers always finish.",
         "No balance is ever wrong, and the sum of all balances never changes."],
        ["Change only the Bank class.", "Keep one lock per account: do not replace them with one global lock.", "Run all the checks after every change."],
        ["Given 4 threads transferring in one direction, then the counter equals 4 times the transfers per thread.",
         "Given transfers in opposite directions, then the run finishes within the time limit.",
         "Given a ring of accounts, then every balance is unchanged."],
        ms, RUBRIC,
        "In 200 words or fewer: What caused each ticket, and what in the code or in a thread dump would show it? Why did you choose an atomic for the counter and a lock order for the deadlock, and why is `volatile` or a single global lock the wrong answer in each case? Argue why your lock order cannot form a cycle for any set of accounts. Say honestly what the checks can and cannot prove.",
        STARTER, SOLUTION, WRONGS)
print("P13 written")
