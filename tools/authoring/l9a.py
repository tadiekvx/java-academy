"""Stage 9 authoring: module 9.1 (Concurrency fundamentals). All exercises are deterministic: joins, latches or pure models."""
import l9common
from l9common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex11 = Exercises("j9-l1.1")
ex12 = Exercises("j9-l1.2")
ex13 = Exercises("j9-l1.3")
ex14 = Exercises("j9-l1.4")
ex15 = Exercises("j9-l1.5")

REGISTER = {
    "j9-l1.1": ("Threads and the cost of sharing", ["J9.01"]),
    "j9-l1.2": ("Races: make one happen", ["J9.02"]),
    "j9-l1.3": ("synchronized, locks and atomics", ["J9.03"]),
    "j9-l1.4": ("Visibility and the Java Memory Model", ["J9.04"]),
    "j9-l1.5": ("Deadlock: reproduce and diagnose", ["J9.05"]),
}
MISCS = {
    "MC187": (["J9.01"], "I116", "Starting a thread and then reading its result right away is fine, because the thread will have finished by then"),
    "MC188": (["J9.02"], "I111", "If a concurrent program passed its tests, it has no race; a race always shows up as a crash"),
    "MC189": (["J9.03"], "I116", "synchronized on any object protects the data, so a new lock object per call is fine"),
    "MC190": (["J9.04"], "I111", "volatile makes compound operations such as count++ atomic"),
    "MC191": (["J9.05"], "I111", "A deadlock is a slow program; it will finish if you wait long enough"),
}
register(REGISTER, MISCS)

# ====================================================================== j9-l1.1
PARTIAL_PROGRAM = '''
void main() throws Exception {
    int[] partial = new int[3];
    Thread[] workers = new Thread[3];
    for (int w = 0; w < 3; w++) {
        final int id = w;
        workers[w] = new Thread(() -> {
            int last = id == 2 ? 100 : (id + 1) * 33;
            int sum = 0;
            for (int n = id * 33 + 1; n <= last; n++) {
                sum += n;
            }
            partial[id] = sum;
        });
        workers[w].start();
    }
    for (Thread worker : workers) {
        worker.join();
    }
    System.out.println("partials=" + Arrays.toString(partial));
    System.out.println("total=" + (partial[0] + partial[1] + partial[2]));
}
'''
# Derived by hand: 1..33 = 561, 34..66 = 1650, 67..100 = 2839, and 561 + 1650 + 2839 = 5050 (the sum 1..100).
ex11.predict(
    "j9-l1.1-predict-partials", "Three workers, no sharing", ["o1"], ["J9.01"],
    "Three threads each add up their own range of 1 to 100 and store the result in their own slot of an array. The main thread waits for all three. Predict the exact output.",
    PARTIAL_PROGRAM, "partials=[561, 1650, 2839]\ntotal=5050\n",
    ["Which numbers does the third worker add, and why does it stop at 100?", "Why can the main thread safely read the array after the loop of joins?"],
    misconceptions=("MC187",), difficulty=1,
)

PSUM_SOL = '''
long parallelSum(int[] data, int threads) throws InterruptedException {
    int parts = Math.max(1, threads);
    long[] partial = new long[parts];
    Thread[] workers = new Thread[parts];
    int chunk = (data.length + parts - 1) / parts;
    for (int w = 0; w < parts; w++) {
        final int id = w;
        workers[w] = new Thread(() -> {
            long sum = 0;
            for (int i = id * chunk; i < Math.min(data.length, (id + 1) * chunk); i++) {
                sum += data[i];
            }
            partial[id] = sum;
        });
        workers[w].start();
    }
    long total = 0;
    for (int w = 0; w < parts; w++) {
        workers[w].join();
        total += partial[w];
    }
    return total;
}
'''
PSUM_NOJOIN = PSUM_SOL.replace("        workers[w].join();\n", "")
PSUM_FLOOR = PSUM_SOL.replace("int chunk = (data.length + parts - 1) / parts;", "int chunk = data.length / parts;")
PSUM_INT = PSUM_SOL.replace("    long total = 0;", "    int total = 0;")

ex11.method(
    "write", "j9-l1.1-write-parallel-sum", "Add it up with threads", ["o2"], ["J9.01"], ["IMPL"],
    "Write `parallelSum(data, threads)`: split the array into `threads` consecutive chunks (the last may be shorter; treat fewer than 1 thread as 1), give each chunk to its own `Thread` that writes its subtotal into its own slot of a `long[]`, wait for every thread with `join`, and return the total as a `long`. No variable may be written by more than one thread.",
    [("parallelSum", [("data", "int[]"), ("threads", "int")], "long")], {"parallelSum": lambda d, t: sum(d)},
    [("parallelSum", ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3), "ten numbers, three threads"), ("parallelSum", ([5], 4), "more threads than numbers"), ("parallelSum", ([], 2), "no numbers")],
    [("parallelSum", ([2000000000, 2000000000], 2), "the total needs a long"), ("parallelSum", ([1, 1, 1, 1, 1, 1, 1], 7), "one number each"), ("parallelSum", ([3, 4, 5], 0), "zero threads is one"),
     ("parallelSum", (list(range(1, 1001)), 8), "a thousand numbers"), ("parallelSum", ([-5, 5, -5, 5, -5], 2), "negative numbers"), ("parallelSum", ([7, 7, 7, 7, 7, 7, 7, 7, 7], 4), "a remainder")],
    starter='''
long parallelSum(int[] data, int threads) throws InterruptedException {
    return 0;
}
''', solution=PSUM_SOL,
    wrongs={"does-not-wait": PSUM_NOJOIN, "drops-the-remainder": PSUM_FLOOR, "int-total": PSUM_INT},
    source_tests=[("waits for the workers with join", ["join"], None), ("uses Thread", ["new Thread"], None)],
    hints=["Start all the threads before you wait for any of them.", "Compute the chunk size so that the last chunk takes the remainder."],
    misconceptions=("MC187",), difficulty=3,
)

ex11.explain(
    "j9-l1.1-explain-threads", "What threads cost and what sharing costs", ["o1"], ["J9.01"],
    "A colleague says 'more threads always means faster'. Using the parallel-sum idea, explain what has to be true for extra threads to help, what each thread costs, and why giving each thread its own slot (instead of one shared total) matters.",
    "Threads help when the work can be split into independent parts and there are enough processor cores; each thread has costs (a stack, scheduling, startup and the wait to join), so tiny tasks or too many threads can be slower than one thread. Threads that write the same variable need coordination, which costs time and risks bugs; giving each thread its own slot means no coordination until the final join, which is the cheapest way to share work.",
    levels={
        2: ("The answer names independence and core count, the per-thread costs, and the no-sharing advantage.", [
            "Extra threads help only if the work splits into independent pieces and there are cores to run them. Each thread costs memory for a stack, startup time and scheduling, so for small jobs it is slower. Separate slots avoid locking: each thread writes only its own, and the join gives the main thread a safe view at the end.",
            "No. The pieces must be independent and the machine needs spare cores. Threads are not free (stack, creation, context switches). Own slots mean there is nothing to coordinate until join."]),
        1: ("The answer names a cost or a condition, not both, or does not explain the slots.", [
            "Threads cost memory so too many are bad.",
            "It only helps with more cores."]),
        0: ("The answer agrees with the colleague.", [
            "Yes, more threads is always faster because more work happens at once.",
            "Sharing one total is simpler, so it is better."]),
    },
)

l9_l1_1 = Lesson("j9-l1.1", "Threads and the cost of sharing", ["J9.01"], [
    ("o1", "Explain when extra threads help, what they cost and why unshared work is cheapest"),
    ("o2", "Split work across threads that never write the same variable, and join them"),
], ["j5-l1.1"], 40, ["I116", "I111"], """## Before you start

You should know arrays and loops, and that a program normally runs one statement at a time.

## Explanation

A **thread** is an independent path of execution inside a program. Starting several lets work happen at the same time on several processor cores, or lets one thread wait (for a file, for the network) while another runs.

Threads are not free. Each has its own stack and must be scheduled, and starting and waiting for them takes time. The gain is real only when the work divides into independent parts and there are cores to run them.

The hard part is not starting threads, it is **sharing**. As soon as two threads touch the same variable and one of them writes, you need coordination (the rest of this stage). The cheapest design shares nothing while the work runs: each thread writes only its own result, and the main thread combines the results after waiting for them. `Thread.join` makes the caller wait until the thread has finished, and per the Java Language Specification starting a thread synchronizes-with that thread's first action, so a started thread sees what its starter wrote before the start.

## Worked examples

### Example 1: three workers.

The predict exercise splits 1 to 100 into three ranges. Each worker writes `partial[id]`; the main thread reads the array only after joining all three.

### Example 2: what goes wrong without join.

If the main thread added up the array right after starting the threads, it would likely read zeros, because the workers have not run yet. Starting a thread does not wait for it.

## Where this is used

- Report builders, batch jobs, any CPU-bound loop over a large collection. Higher-level tools (executors, parallel streams) automate exactly this split-and-combine.

## Common mistakes

:::mistake{id=MC187}
**Reading a worker's result right after `start()`.** The thread may not have run. Wait with `join` (or use a future, next module) before reading.
:::

## Practice

::exercise{id=j9-l1.1-predict-partials}

::exercise{id=j9-l1.1-write-parallel-sum}

::exercise{id=j9-l1.1-explain-threads}

## Further reading

- **Java SE 25 API, `Thread`** `[I116]`.
- **Java Language Specification, chapter 17** `[I111]`.

## How you'll be assessed

- The **predict** exercise checks that you can follow workers and a join (*identifying*).
- The **write** exercise checks that you can split and combine work (*implementation*).
- The **explain** exercise checks the cost-benefit argument (*explanation*).
""")

# ====================================================================== j9-l1.2
LOST_PROGRAM = '''
void main() throws Exception {
    int[] counter = {0};
    CountDownLatch bothHaveRead = new CountDownLatch(2);
    Runnable increment = () -> {
        int seen = counter[0];
        bothHaveRead.countDown();
        try {
            bothHaveRead.await();
        } catch (InterruptedException e) {
            return;
        }
        counter[0] = seen + 1;
    };
    Thread a = new Thread(increment);
    Thread b = new Thread(increment);
    a.start();
    b.start();
    a.join();
    b.join();
    System.out.println("two increments, counter=" + counter[0]);
}
'''
ex12.predict(
    "j9-l1.2-predict-lost-update", "A race you can count on", ["o1"], ["J9.02"],
    "Two threads each add one to a shared counter that starts at 0: each reads it, then writes back what it read plus one. A latch makes sure both threads have read before either writes. Predict the exact output.",
    PARTIAL_PROGRAM.split("void main")[0] + LOST_PROGRAM, "two increments, counter=1\n",
    ["What value has each thread read when it reaches the latch?", "What does each thread then write?"],
    misconceptions=("MC188",), difficulty=1,
)


def f_schedule(schedule):
    counter, local = 0, {}
    for step in schedule:
        t, act = step.split(":")
        if act == "read":
            local[t] = counter
        else:
            counter = local.get(t, 0) + 1
    return counter


SCHED_SOL = '''
int finalValue(List<String> schedule) {
    int counter = 0;
    Map<String, Integer> seen = new HashMap<>();
    for (String step : schedule) {
        String[] parts = step.split(":");
        if (parts[1].equals("read")) {
            seen.put(parts[0], counter);
        } else {
            counter = seen.getOrDefault(parts[0], 0) + 1;
        }
    }
    return counter;
}
'''
SCHED_COUNT = '''
int finalValue(List<String> schedule) {
    int writes = 0;
    for (String step : schedule) {
        if (step.endsWith(":write")) {
            writes++;
        }
    }
    return writes;
}
'''
SCHED_SHARED_LOCAL = SCHED_SOL.replace("Map<String, Integer> seen = new HashMap<>();", "int[] last = {0};").replace("seen.put(parts[0], counter);", "last[0] = counter;").replace("counter = seen.getOrDefault(parts[0], 0) + 1;", "counter = last[0] + 1;")
SCHED_FIRST_READ = SCHED_SOL.replace("seen.put(parts[0], counter);", "seen.putIfAbsent(parts[0], counter);")

ex12.method(
    "write", "j9-l1.2-write-schedule", "Simulate an interleaving", ["o2"], ["J9.02"], ["IMPL"],
    "A schedule lists the steps the threads take in order, as `thread:read` or `thread:write`. Every thread runs the same code: `read` copies the shared counter (initially 0) into the thread's private variable, `write` stores that private value plus one into the counter. A `write` with no earlier `read` by that thread uses 0, and a thread may read again. Write `finalValue(schedule)`, the counter after all the steps.",
    [("finalValue", [("schedule", "List<String>")], "int")], {"finalValue": f_schedule},
    [("finalValue", (["A:read", "A:write", "B:read", "B:write"],), "one after the other"), ("finalValue", (["A:read", "B:read", "A:write", "B:write"],), "both read first"), ("finalValue", ([],), "nothing happens")],
    [("finalValue", (["A:read", "B:read", "C:read", "A:write", "B:write", "C:write"],), "three threads all lose"), ("finalValue", (["A:read", "A:write", "A:read", "A:write"],), "one thread twice"),
     ("finalValue", (["A:read", "B:read", "A:write", "B:read", "B:write"],), "B reads again after A wrote"), ("finalValue", (["A:write"],), "a write without a read"),
     ("finalValue", (["A:read", "A:write", "B:read", "A:read", "A:write", "B:write"],), "mixed"), ("finalValue", (["A:read", "B:read", "B:write", "A:write"],), "A writes last with an old value"),
     ("finalValue", (["A:read", "B:read", "B:write", "C:read", "A:write"],), "each thread keeps its own read")],
    starter='''
int finalValue(List<String> schedule) {
    return 0;
}
''', solution=SCHED_SOL,
    wrongs={"counts-the-writes": SCHED_COUNT, "one-shared-private-variable": SCHED_SHARED_LOCAL, "keeps-only-the-first-read": SCHED_FIRST_READ},
    hints=["Each thread needs its own private value.", "A later read replaces the earlier one."],
    misconceptions=("MC188",), difficulty=3,
)

ex12.explain(
    "j9-l1.2-explain-race", "Why the test passed", ["o2"], ["J9.02"],
    "A team's test starts two threads that each increment a shared counter a thousand times and asserts the total is 2000. It passes on every developer machine and on the build server for a month, then fails once in production. Explain what a race condition is, why the test passed, and how you would test for it more reliably.",
    "A race condition is a bug whose outcome depends on how the threads' steps interleave. The increment is a read, an add and a write; if two threads interleave, one update is lost. The test passed because the interleavings that lose an update are rare at that scale (a thousand quick increments often finish within one thread's time slice), and a passing test only shows one interleaving worked. To test reliably, force the bad interleaving with latches (as in the exercise), use many more iterations and threads, and above all prove the code safe by construction (a lock or an atomic) rather than by testing.",
    levels={
        2: ("The answer defines the race, explains why passing proves little, and offers forced interleaving or construction-based safety.", [
            "A race is when the result depends on the order the threads interleave. count++ is read, add, write, so two threads can both read the same value and one update is lost. A thousand increments is so short that the threads may run one after another, so the test passes by luck. I would force the bad order with a latch, use more threads and iterations, and fix the code with an atomic or a lock so it is safe by design.",
            "The bug exists only for some interleavings. The test hit lucky ones, because a short loop can finish inside one time slice. A passing test does not show absence of a race. Use latches to force the interleaving and make the counter atomic."]),
        1: ("The answer defines the race without explaining the passing test, or the other way round.", [
            "A race is when threads interfere with each other.",
            "The test was too small."]),
        0: ("The answer says passing tests show there is no race.", [
            "If it passed for a month the code is correct and production was a freak event.",
            "Races always crash the program, so a pass means there is none."]),
    },
)

l9_l1_2 = Lesson("j9-l1.2", "Races: make one happen", ["J9.02"], [
    ("o1", "Predict the outcome of a forced interleaving"),
    ("o2", "Explain why a race can hide from tests and show up later"),
], ["j9-l1.1"], 40, ["I111"], """## Before you start

You should be able to run two threads and join them (lesson 9.1.1).

## Explanation

A **race condition** is a bug where the result depends on the relative timing of threads. The classic case is a **lost update**. `counter++` looks like one step but is three: read the value, add one, write it back. If two threads read the same value before either writes, both write the same new value and one increment disappears.

Races are hard because they are not reliable. Whether the bad interleaving happens depends on the scheduler, the number of cores, the load on the machine and the speed of the code. A test that passes a thousand times has shown only that those thousand interleavings were fine.

So make the race happen on purpose. In the exercise program a **latch** (`CountDownLatch`) holds both threads until each has read the counter. Now the lost update is not a matter of luck: both threads certainly read 0, both certainly write 1, and the counter ends at 1.

The practical lesson is to make code **safe by construction** (a lock, an atomic, immutability) instead of trying to prove it safe by testing.

## Worked examples

### Example 1: forcing the lost update.

Two increments, final value 1. Remove the latch and the result is usually 2, until it is not.

### Example 2: reading a schedule.

`A:read, B:read, A:write, B:write` ends at 1. `A:read, A:write, B:read, B:write` ends at 2. The simulation exercise lets you try many.

## Where this is used

- Every shared counter, cache, balance or flag in a multi-threaded program. The stage project has a seeded race for you to find.

## Common mistakes

:::mistake{id=MC188}
**Concluding there is no race because the tests pass.** A race is a property of the interleavings the code allows, not of the ones you happened to see.
:::

## Practice

::exercise{id=j9-l1.2-predict-lost-update}

::exercise{id=j9-l1.2-write-schedule}

::exercise{id=j9-l1.2-explain-race}

## Further reading

- **Java Language Specification, chapter 17** `[I111]`.

## How you'll be assessed

- The **predict** exercise checks that you can follow a forced lost update (*identifying*).
- The **write** exercise checks that you can simulate interleavings (*implementation*).
- The **explain** exercise checks that you understand why tests can miss races (*explanation*).
""")

# ====================================================================== j9-l1.3
LOCK_SOL = '''
long countWithLock(int threads, int perThread) throws InterruptedException {
    Object lock = new Object();
    long[] counter = {0};
    Thread[] workers = new Thread[threads];
    for (int t = 0; t < threads; t++) {
        workers[t] = new Thread(() -> {
            for (int i = 0; i < perThread; i++) {
                synchronized (lock) {
                    counter[0]++;
                }
            }
        });
        workers[t].start();
    }
    for (Thread worker : workers) {
        worker.join();
    }
    return counter[0];
}
'''
LOCK_PLAIN = LOCK_SOL.replace("                synchronized (lock) {\n                    counter[0]++;\n                }\n", "                counter[0]++;\n")
LOCK_NEW_EACH = LOCK_SOL.replace("synchronized (lock)", "synchronized (new Object())")
LOCK_NOJOIN = LOCK_SOL.replace("    for (Thread worker : workers) {\n        worker.join();\n    }\n", "")

ex13.method(
    "write", "j9-l1.3-write-lock", "A counter behind a lock", ["o1"], ["J9.03"], ["IMPL"],
    "Write `countWithLock(threads, perThread)`: start `threads` threads that each add one to a shared counter `perThread` times, protected with a `synchronized` block on one shared lock object. Wait for all threads and return the counter. The answer is always `threads * perThread`.",
    [("countWithLock", [("threads", "int"), ("perThread", "int")], "long")], {"countWithLock": lambda t, p: t * p},
    [("countWithLock", (2, 1000), "two threads"), ("countWithLock", (4, 50000), "four threads"), ("countWithLock", (1, 10), "one thread")],
    [("countWithLock", (8, 25000), "eight threads"), ("countWithLock", (4, 200000), "many increments"), ("countWithLock", (0, 100), "no threads"),
     ("countWithLock", (3, 0), "no work"), ("countWithLock", (6, 30000), "six threads"), ("countWithLock", (2, 150000), "two busy threads")],
    starter='''
long countWithLock(int threads, int perThread) throws InterruptedException {
    return 0;
}
''', solution=LOCK_SOL,
    wrongs={"no-lock": LOCK_PLAIN, "a-new-lock-each-time": LOCK_NEW_EACH, "does-not-wait": LOCK_NOJOIN},
    source_tests=[("uses a synchronized block", ["synchronized ("], None), ("does not create the lock inside the block", None, ["synchronized (new "])],
    hints=["All threads must lock the **same** object.", "Put only the increment inside the block."],
    misconceptions=("MC189",), difficulty=3,
)

ATOMIC_SOL = '''
long countWithAtomic(int threads, int perThread) throws InterruptedException {
    AtomicLong counter = new AtomicLong();
    Thread[] workers = new Thread[threads];
    for (int t = 0; t < threads; t++) {
        workers[t] = new Thread(() -> {
            for (int i = 0; i < perThread; i++) {
                counter.incrementAndGet();
            }
        });
        workers[t].start();
    }
    for (Thread worker : workers) {
        worker.join();
    }
    return counter.get();
}
'''
ATOMIC_READ_WRITE = ATOMIC_SOL.replace("counter.incrementAndGet();", "counter.set(counter.get() + 1);")
ATOMIC_NOJOIN = ATOMIC_SOL.replace("    for (Thread worker : workers) {\n        worker.join();\n    }\n", "")
ATOMIC_ONE_THREAD = ATOMIC_SOL.replace("int t = 0; t < threads; t++", "int t = 0; t < Math.min(threads, 1); t++")

ex13.method(
    "write", "j9-l1.3-write-atomic", "The same counter, lock-free", ["o1"], ["J9.03"], ["IMPL"],
    "Write `countWithAtomic(threads, perThread)` with the same behaviour, but use an `AtomicLong` and its `incrementAndGet` method instead of a lock. (Hint: `counter.set(counter.get() + 1)` is a read and a write, so it is a race again.)",
    [("countWithAtomic", [("threads", "int"), ("perThread", "int")], "long")], {"countWithAtomic": lambda t, p: t * p},
    [("countWithAtomic", (2, 1000), "two threads"), ("countWithAtomic", (4, 50000), "four threads"), ("countWithAtomic", (1, 10), "one thread")],
    [("countWithAtomic", (8, 25000), "eight threads"), ("countWithAtomic", (4, 200000), "many increments"), ("countWithAtomic", (0, 100), "no threads"),
     ("countWithAtomic", (3, 0), "no work"), ("countWithAtomic", (6, 30000), "six threads")],
    starter='''
long countWithAtomic(int threads, int perThread) throws InterruptedException {
    return 0;
}
''', solution=ATOMIC_SOL,
    wrongs={"read-then-write": ATOMIC_READ_WRITE, "does-not-wait": ATOMIC_NOJOIN, "only-one-thread": ATOMIC_ONE_THREAD},
    source_tests=[("uses AtomicLong", ["AtomicLong"], None), ("uses an atomic update", ["incrementAndGet"], None)],
    hints=["The atomic class does the read-add-write as one step.", "Why is get() followed by set() not the same?"],
    misconceptions=("MC189",), difficulty=2,
)

ex13.explain(
    "j9-l1.3-explain-tools", "Lock, atomic or neither", ["o2"], ["J9.03"],
    "For each situation say whether you would use a `synchronized` block (or a `ReentrantLock`), an atomic class, or no coordination at all, and why: (a) a request counter incremented by many threads; (b) moving money between two accounts, which must change two balances together; (c) a list of results that each worker thread builds privately and the main thread reads after joining.",
    "(a) An atomic: one variable, one update, and the atomic classes support lock-free thread-safe updates of single variables. (b) A lock: two variables must change together, which an atomic on each cannot guarantee; hold a lock around both changes (and, with more than one lock, take them in a fixed order, next lessons). (c) None: no data is shared while the workers run, and join gives the reader a safe view afterwards.",
    levels={
        2: ("The answer chooses correctly for all three with the reason (single variable, multi-variable invariant, no sharing).", [
            "(a) AtomicLong or LongAdder: a single variable updated in one step, no lock needed. (b) A lock around both balance changes, because the two variables must change together and atomics on each cannot ensure that. (c) Nothing: each worker owns its list and join makes the results visible, so there is no sharing to protect.",
            "Counter: atomic. Transfer: synchronized or a ReentrantLock covering both accounts, since it is a multi-variable invariant. Private result lists: no coordination, thread confinement plus join."]),
        1: ("The answer chooses correctly for two of the three or gives no reasons.", [
            "Atomic for the counter and a lock for the transfer.",
            "Use synchronized everywhere to be safe."]),
        0: ("The answer misjudges the cases.", [
            "No coordination is needed for any of them as long as the code is fast.",
            "An atomic is enough for the money transfer."]),
    },
)

l9_l1_3 = Lesson("j9-l1.3", "synchronized, locks and atomics", ["J9.03"], [
    ("o1", "Make a shared counter correct with a lock and with an atomic"),
    ("o2", "Choose between a lock, an atomic and no coordination"),
], ["j9-l1.2"], 45, ["I116", "I111"], """## Before you start

You should have seen a lost update (lesson 9.1.2).

## Explanation

Three tools stop races.

A **`synchronized` block** takes the monitor of an object. Only one thread at a time can hold a given monitor, so code inside blocks that lock the same object cannot interleave. Unlocking a monitor synchronizes-with later locking of it (Java Language Specification, chapter 17), so what one thread wrote inside the block is visible to the next thread that locks. All threads must use the **same** lock object: `synchronized (new Object())` locks something nobody else shares.

A **`ReentrantLock`** has the same basic behaviour and semantics as the implicit monitor lock, with extended capabilities (such as trying to take the lock without waiting). You must unlock it yourself, in a `finally`.

The **atomic classes** in `java.util.concurrent.atomic` are a small toolkit supporting lock-free thread-safe programming on single variables: `incrementAndGet` does read, add and write as one indivisible step. They suit one variable. They cannot make two variables change together.

The rule of thumb: no sharing needs no tool; one variable suits an atomic; an invariant across several variables needs a lock held around all the changes.

## Worked examples

### Example 1: the lock.

```java
synchronized (lock) {
    counter[0]++;
}
```

### Example 2: the atomic.

```java
counter.incrementAndGet();
```

`counter.set(counter.get() + 1)` is two operations and is a race again.

## Where this is used

- Counters and statistics (atomics), balances and caches (locks), and everywhere data is built privately and merged (nothing).

## Common mistakes

:::mistake{id=MC189}
**Locking a different object each time.** A lock only excludes threads that use the same one. `synchronized (new Object())` protects nothing.
:::

## Practice

::exercise{id=j9-l1.3-write-lock}

::exercise{id=j9-l1.3-write-atomic}

::exercise{id=j9-l1.3-explain-tools}

## Further reading

- **Java SE 25 API, `java.util.concurrent.atomic`** `[I116]`.
- **Java Language Specification, chapter 17** `[I111]`.

## How you'll be assessed

- The **write** exercises check the two fixes (*implementation*). They also check your source, because a race cannot be detected reliably by running it.
- The **explain** exercise checks the choice of tool (*explanation*).
""")

# ====================================================================== j9-l1.4
VOL = {
    "stop-flag": "yes",
    "counter-increment": "no",
    "check-then-act": "no",
    "publish-immutable-object": "yes",
    "update-two-fields-together": "no",
}


def f_vol(op):
    return VOL.get(op, "unknown")


VOL_SOL = '''
String volatileEnough(String operation) {
    return switch (operation) {
        case "stop-flag", "publish-immutable-object" -> "yes";
        case "counter-increment", "check-then-act", "update-two-fields-together" -> "no";
        default -> "unknown";
    };
}
'''
VOL_ALL_YES = VOL_SOL.replace('case "counter-increment", "check-then-act", "update-two-fields-together" -> "no";', 'case "counter-increment", "check-then-act", "update-two-fields-together" -> "yes";')
VOL_COUNTER = VOL_SOL.replace('case "stop-flag", "publish-immutable-object" -> "yes";', 'case "stop-flag", "publish-immutable-object", "counter-increment" -> "yes";').replace('case "counter-increment", "check-then-act"', 'case "check-then-act"')
VOL_DEFAULT = VOL_SOL.replace('default -> "unknown";', 'default -> "no";')
VOL_FLAG = VOL_SOL.replace('case "stop-flag", "publish-immutable-object" -> "yes";', 'case "publish-immutable-object" -> "yes";').replace('case "counter-increment",', 'case "stop-flag", "counter-increment",')

ex14.method(
    "write", "j9-l1.4-write-volatile", "Is volatile enough", ["o1"], ["J9.04"], ["IMPL"],
    "A `volatile` variable gives **visibility** (a write is seen by later reads in other threads) but not **atomicity** of compound actions. Write `volatileEnough(operation)` returning `yes` when declaring the shared variable `volatile` is enough and `no` when it is not, for: `stop-flag` (one thread sets a boolean, another loops until it sees it), `publish-immutable-object` (one thread assigns a reference to an object that is never changed, others read it), `counter-increment` (`count++`), `check-then-act` (`if (x == null) x = create();`), `update-two-fields-together`. Anything else is `unknown`.",
    [("volatileEnough", [("operation", "String")], "String")], {"volatileEnough": f_vol},
    [("volatileEnough", ("stop-flag",), "the classic use"), ("volatileEnough", ("counter-increment",), "volatile does not make ++ atomic"), ("volatileEnough", ("something-else",), "not listed")],
    [("volatileEnough", ("publish-immutable-object",), "an immutable object"), ("volatileEnough", ("check-then-act",), "two steps"), ("volatileEnough", ("update-two-fields-together",), "an invariant over two fields"),
     ("volatileEnough", ("",), "empty"), ("volatileEnough", ("STOP-FLAG",), "exact names")],
    starter='''
String volatileEnough(String operation) {
    return "";
}
''', solution=VOL_SOL,
    wrongs={"volatile-fixes-everything": VOL_ALL_YES, "counter-is-fine": VOL_COUNTER, "unknown-means-no": VOL_DEFAULT, "flag-needs-more": VOL_FLAG},
    hints=["Visibility is about seeing a write; atomicity is about doing several steps as one.", "Which operations are a single read or a single write?"],
    misconceptions=("MC190",), difficulty=2,
)

ex14.explain(
    "j9-l1.4-explain-visibility", "Why a flag might never be seen", ["o2"], ["J9.04"],
    "A worker thread runs `while (running) { work(); }` where `running` is an ordinary `boolean` field. The main thread later sets `running = false`, but the worker sometimes keeps going for ever. Explain why this can happen in terms of the Java memory model's happens-before relation, and what changing the field to `volatile` guarantees.",
    "Without synchronization there is no happens-before edge between the main thread's write and the worker's reads, so the memory model does not require the worker ever to see the new value; the compiler or hardware may keep reading a stale copy. Declaring the field volatile makes a write to it synchronize-with all subsequent reads of it by any thread, which creates the happens-before edge, so the worker will see the update. It does not make compound actions atomic.",
    levels={
        2: ("The answer names the missing happens-before edge, says the stale read is allowed, and states what volatile provides and does not.", [
            "There is no happens-before relationship between the write and the worker's reads, so the worker may keep seeing the old value and the JVM is allowed to cache it. A volatile write synchronizes-with later reads of that variable, so the worker is guaranteed to see the change. It only gives visibility, not atomic compound updates.",
            "Plain fields give no visibility guarantee across threads. volatile creates the happens-before edge from the write to subsequent reads, so the loop ends. It does not make count++ safe."]),
        1: ("The answer says volatile fixes visibility without the memory-model reasoning.", [
            "The worker has a cached copy; volatile forces it to read the real one.",
            "Make the flag volatile."]),
        0: ("The answer misattributes the cause.", [
            "The main thread did not run long enough to set the flag.",
            "Booleans are not thread safe so the value is corrupted."]),
    },
)

l9_l1_4 = Lesson("j9-l1.4", "Visibility and the Java Memory Model", ["J9.04"], [
    ("o1", "Decide whether volatile is enough for a given shared-variable use"),
    ("o2", "Explain a visibility bug with the happens-before relation"),
], ["j9-l1.3"], 40, ["I111"], """## Before you start

You should know what a race is and what a lock does (lessons 9.1.2 and 9.1.3).

## Explanation

Races are about interleaving. A second problem is **visibility**: whether one thread ever sees what another wrote. Processors and the JVM may keep values in registers and caches and reorder operations, as long as a single thread cannot tell. For other threads, what is guaranteed is defined by the **Java memory model**, in chapter 17 of the language specification.

Its key idea is **happens-before**: if one action happens-before another, the first is visible to and ordered before the second. Within one thread, program order gives happens-before. Between threads you need a synchronization action that creates the edge. The specification lists these: unlocking a monitor synchronizes-with later locking of it; a write to a volatile variable synchronizes-with all subsequent reads of that variable by any thread; starting a thread synchronizes-with its first action.

So a plain `boolean` flag has no guaranteed visibility; a `volatile` one does. But `volatile` gives only visibility and ordering. It does not make `count++` atomic, because that is still read, add, write by separate steps; use an atomic or a lock for that.

## Worked examples

### Example 1: the stop flag.

`volatile boolean running` lets one thread stop another reliably. One writer, one-step reads and writes: exactly the case it was made for.

### Example 2: where volatile is not enough.

`volatile int count; count++` still loses updates. `if (x == null) x = create();` can create twice. An invariant over two fields needs a lock.

## Where this is used

- Shutdown flags, configuration references that are replaced wholesale, and as the building block of the `java.util.concurrent` classes.

## Common mistakes

:::mistake{id=MC190}
**Making a counter `volatile` to make it thread-safe.** The increment is three steps. Use an atomic.
:::

## Practice

::exercise{id=j9-l1.4-write-volatile}

::exercise{id=j9-l1.4-explain-visibility}

## Further reading

- **Java Language Specification, chapter 17** `[I111]`.

## How you'll be assessed

- The **write** exercise checks when volatile suffices (*implementation*).
- The **explain** exercise checks the memory-model reasoning (*explanation*).

A visibility bug cannot be reproduced reliably, which is why this lesson asks you to reason about it instead of running it.
""")

# ====================================================================== j9-l1.5
def f_deadlock(waits):
    graph = {}
    for e in waits:
        a, b = e.split(">")
        graph.setdefault(a, set()).add(b)
    nodes = set(graph) | {b for v in graph.values() for b in v}

    def reaches(start):
        seen, stack = set(), list(graph.get(start, ()))
        while stack:
            n = stack.pop()
            if n == start:
                return True
            if n in seen:
                continue
            seen.add(n)
            stack.extend(graph.get(n, ()))
        return False

    return sorted(n for n in nodes if reaches(n))


DL_SOL = '''
List<String> findDeadlock(List<String> waits) {
    Map<String, Set<String>> graph = new HashMap<>();
    Set<String> nodes = new TreeSet<>();
    for (String edge : waits) {
        String[] parts = edge.split(">");
        graph.computeIfAbsent(parts[0], k -> new HashSet<>()).add(parts[1]);
        nodes.add(parts[0]);
        nodes.add(parts[1]);
    }
    List<String> stuck = new ArrayList<>();
    for (String start : nodes) {
        Set<String> seen = new HashSet<>();
        Deque<String> stack = new ArrayDeque<>(graph.getOrDefault(start, Set.of()));
        boolean cycle = false;
        while (!stack.isEmpty() && !cycle) {
            String next = stack.pop();
            if (next.equals(start)) {
                cycle = true;
            } else if (seen.add(next)) {
                stack.addAll(graph.getOrDefault(next, Set.of()));
            }
        }
        if (cycle) {
            stuck.add(start);
        }
    }
    return stuck;
}
'''
DL_ANY_WAIT = DL_SOL.replace("        if (cycle) {\n            stuck.add(start);\n        }", "        if (graph.containsKey(start)) {\n            stuck.add(start);\n        }")
DL_ONLY_TWO = DL_SOL.replace("            if (next.equals(start)) {\n                cycle = true;\n            } else if (seen.add(next)) {\n                stack.addAll(graph.getOrDefault(next, Set.of()));\n            }", "            if (next.equals(start)) {\n                cycle = true;\n            }")
DL_ALL_NODES = DL_SOL.replace("        if (cycle) {\n            stuck.add(start);\n        }", "        stuck.add(start);")
DL_SELF = DL_SOL.replace("        Deque<String> stack = new ArrayDeque<>(graph.getOrDefault(start, Set.of()));", "        Deque<String> stack = new ArrayDeque<>(graph.getOrDefault(start, Set.of()));\n        stack.remove(start);")

ex15.method(
    "write", "j9-l1.5-write-find-deadlock", "Which threads are stuck", ["o1"], ["J9.05"], ["IMPL"],
    "Each entry `T1>T2` says thread T1 is waiting for a lock that thread T2 holds. A set of threads is deadlocked when each waits, directly or through others, for the next, round to itself. Write `findDeadlock(waits)` returning the names of every thread that lies on such a cycle, sorted alphabetically (an empty list if there is none). A thread that merely waits for a deadlocked thread is **not** itself in the cycle.",
    [("findDeadlock", [("waits", "List<String>")], "List<String>")], {"findDeadlock": f_deadlock},
    [("findDeadlock", (["A>B", "B>A"],), "the classic pair"), ("findDeadlock", (["A>B", "B>C"],), "a chain, no cycle"), ("findDeadlock", ([],), "nobody waits")],
    [("findDeadlock", (["A>B", "B>C", "C>A"],), "three threads"), ("findDeadlock", (["D>A", "A>B", "B>A"],), "D waits for a deadlocked thread but is not in the cycle"), ("findDeadlock", (["A>A"],), "a thread waiting for itself"),
     ("findDeadlock", (["A>B", "B>A", "C>D", "D>C"],), "two separate deadlocks"), ("findDeadlock", (["A>B", "B>C", "C>B", "A>C"],), "a cycle with a tail"), ("findDeadlock", (["X>Y", "Y>Z", "Z>X", "Z>W"],), "a cycle with an exit"),
     ("findDeadlock", (["A>B", "C>B"],), "two waiters on one holder")],
    starter='''
List<String> findDeadlock(List<String> waits) {
    return List.of();
}
''', solution=DL_SOL,
    wrongs={"anyone-who-waits": DL_ANY_WAIT, "only-direct-pairs": DL_ONLY_TWO, "everyone-is-stuck": DL_ALL_NODES, "ignores-self-waits": DL_SELF},
    hints=["A thread is on a cycle if you can follow the waits from it and come back to it.", "Be careful not to follow a path for ever: remember where you have been."],
    misconceptions=("MC191",), difficulty=4,
)

DUMP = cap("cap_deadlock.txt")
DLSRC = cap("cap_deadlock_source.txt")
ex15.explain(
    "j9-l1.5-explain-dump", "Reading a thread dump", ["o2"], ["J9.05"],
    "This program deadlocks every time (a latch makes sure both threads hold their first lock before asking for the second). Its source and the deadlock section of a real thread dump, taken with `jcmd <pid> Thread.print` while it was stuck, follow.\n\n" + fence(DLSRC, "java") + "\n\n" + fence(DUMP) + "\n\nAnswer: which two threads are deadlocked, which lock each holds and wants, which line of the source each is stuck on, and how to remove the deadlock without removing the locks.",
    "The threads transfer-A-to-B and transfer-B-to-A are deadlocked. Each holds one monitor and waits for the one the other holds: transfer-A-to-B holds the lock on ACCOUNT_A (…dc8) and waits for ACCOUNT_B (…dd8), transfer-B-to-A the opposite. Both are stuck at the inner synchronized(to) on line 26. The fix is a global lock order: always take the locks in the same order whatever the direction of the transfer (for example by account id), so no thread can hold the second lock while waiting for the first.",
    levels={
        2: ("The answer names both threads, the lock each holds and wants, the line, and proposes a consistent lock order.", [
            "transfer-A-to-B and transfer-B-to-A. The first holds the lock at ...dc8 (ACCOUNT_A) and waits for ...dd8; the second holds ...dd8 and waits for ...dc8. Both are blocked on line 26, the inner synchronized. Fix: acquire the two locks in a fixed global order, such as by account id, in both directions.",
            "The dump says it found one deadlock between the two transfer threads: each locked its from-account and is waiting for the other's. They wait at Deadlock.transfer line 26. Always lock the lower-numbered account first so the cycle cannot form."]),
        1: ("The answer identifies the deadlock but not the fix, or the fix but not the evidence.", [
            "The two transfer threads are deadlocked on each other's locks.",
            "Use a lock order."]),
        0: ("The answer misreads the dump.", [
            "The program is slow because it waits for a latch.",
            "Only one thread is blocked, the other is fine."]),
    },
)

l9_l1_5 = Lesson("j9-l1.5", "Deadlock: reproduce and diagnose", ["J9.05"], [
    ("o1", "Find the threads on a wait-for cycle"),
    ("o2", "Diagnose a deadlock from a real thread dump and fix it with a lock order"),
], ["j9-l1.3"], 45, ["I111", "I116"], """## Before you start

You should know how `synchronized` blocks work (lesson 9.1.3).

## Explanation

A **deadlock** is a set of threads each waiting for a lock another in the set holds, so none can proceed. It is not slowness: the threads wait for ever. The conditions are mutual exclusion, holding one lock while waiting for another, no way to take a lock back, and a cycle of waiting. Break any one and the deadlock cannot happen.

The practical fix is to break the cycle with a **global lock order**: every thread that needs several locks takes them in the same order. For a transfer between two accounts, lock the account with the lower id first, whichever direction the money goes.

The JDK shows you the problem. `jcmd <pid> Thread.print` (or `jstack`) prints every thread's stack, and when it finds a deadlock among Java monitors it reports it, naming the threads and the locks, as in the real dump in the exercise. To reproduce a deadlock for a lesson without relying on luck, the program uses a latch so that both threads certainly hold their first lock before either asks for the second.

## Worked examples

### Example 1: the real dump.

The exercise shows the program and the dump that `jcmd` printed for it: "Found one Java-level deadlock", the two threads, and the monitor each is waiting for and holds.

### Example 2: the cycle as a graph.

`A>B, B>A` is a cycle of two. `D>A, A>B, B>A` has a cycle (A and B) and a thread D waiting on it; D is blocked but not part of the cycle.

## Where this is used

- Any code that locks two things: transfers, lock-protected caches that call each other, database row locks. The stage project has one to fix.

## Common mistakes

:::mistake{id=MC191}
**Treating a hang as slowness.** A deadlock never finishes. Take a thread dump, look for the cycle, then fix the lock order.
:::

## Practice

::exercise{id=j9-l1.5-write-find-deadlock}

::exercise{id=j9-l1.5-explain-dump}

## Further reading

- **Java Language Specification, chapter 17** `[I111]` on monitors and locking.
- **Java SE 25 API, `Thread`** `[I116]`.

## How you'll be assessed

- The **write** exercise checks cycle detection (*implementation*).
- The **explain** exercise checks that you can read a real dump (*explanation*).

The four conditions for deadlock are standard operating-system theory and are not taken from a source recorded for this course.
""")
print("module 9.1 authored")
