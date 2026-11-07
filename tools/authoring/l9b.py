"""Stage 9 authoring: module 9.2 (Modern concurrency). Deterministic by design: results do not depend on scheduling."""
from collections import Counter
import l9common
from l9common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex21 = Exercises("j9-l2.1")
ex22 = Exercises("j9-l2.2")
ex23 = Exercises("j9-l2.3")

REGISTER = {
    "j9-l2.1": ("Executors and futures", ["J9.06"]),
    "j9-l2.2": ("Concurrent collections", ["J9.07"]),
    "j9-l2.3": ("Virtual threads, scoped values and structured concurrency", ["J9.08"]),
}
MISCS = {
    "MC192": (["J9.06"], "I112", "Creating a new Thread for every task is the normal way to run many tasks; an executor adds nothing"),
    "MC193": (["J9.07"], "I114", "A concurrent map makes any sequence of its operations atomic, including contains-then-put"),
    "MC194": (["J9.08"], "I108", "Virtual threads make CPU-bound code faster, and should be pooled like platform threads"),
}
register(REGISTER, MISCS)

# ====================================================================== j9-l2.1
CF_PROGRAM = '''
void main() {
    CompletableFuture<Integer> a = CompletableFuture.supplyAsync(() -> 20);
    CompletableFuture<Integer> b = CompletableFuture.supplyAsync(() -> 22);
    int total = a.thenCombine(b, Integer::sum).thenApply(x -> x * 2).join();
    System.out.println("total=" + total);
    String outcome = CompletableFuture.<String>supplyAsync(() -> {
        throw new IllegalStateException("boom");
    }).exceptionally(e -> "recovered:" + e.getClass().getSimpleName()).join();
    System.out.println(outcome);
    System.out.println("done=" + a.isDone() + "," + b.isDone());
}
'''
# total: (20 + 22) * 2 = 84. An exception thrown inside supplyAsync reaches exceptionally wrapped in a CompletionException.
ex21.predict(
    "j9-l2.1-predict-futures", "Composing futures", ["o1"], ["J9.06"],
    "Two futures compute 20 and 22 in the background. The first chain adds them and doubles the result. The second future fails with an exception and a recovery step handles it. Predict the exact output. (Think about what type of exception the recovery function actually receives from a failed `supplyAsync`.)",
    CF_PROGRAM, "total=84\nrecovered:CompletionException\ndone=true,true\n",
    ["What do `thenCombine` and `thenApply` do with the two results?", "Does `join()` return before or after the computation has finished?"],
    misconceptions=("MC192",), difficulty=2,
)


def wrap32(x):
    return ((x + 2**31) % 2**32) - 2**31


SQ_SOL = '''
List<Integer> parallelSquares(List<Integer> values, int threads) throws Exception {
    try (ExecutorService pool = Executors.newFixedThreadPool(Math.max(1, threads))) {
        List<Future<Integer>> futures = new ArrayList<>();
        for (int value : values) {
            futures.add(pool.submit(() -> value * value));
        }
        List<Integer> squares = new ArrayList<>();
        for (Future<Integer> future : futures) {
            squares.add(future.get());
        }
        return squares;
    }
}
'''
SQ_SEQ = '''
List<Integer> parallelSquares(List<Integer> values, int threads) throws Exception {
    List<Integer> squares = new ArrayList<>();
    for (int value : values) {
        squares.add(value * value);
    }
    return squares;
}
'''
SQ_DROP = SQ_SOL.replace("for (Future<Integer> future : futures) {", "for (Future<Integer> future : futures.subList(0, Math.max(0, futures.size() - 1))) {")
SQ_ABS = SQ_SOL.replace("() -> value * value", "() -> Math.abs(value) + value * 0 + (value * value - Math.abs(value))")

ex21.method(
    "write", "j9-l2.1-write-squares", "Fan out and collect", ["o2"], ["J9.06"], ["IMPL"],
    "Write `parallelSquares(values, threads)`: submit one task per value to a fixed pool of `threads` threads (at least 1) using an `ExecutorService`, collect the `Future` results, and return the squares **in the order of the input**. Close the executor when you are done (it is `AutoCloseable`, so try-with-resources works). The square is an ordinary `int` product.",
    [("parallelSquares", [("values", "List<Integer>"), ("threads", "int")], "List<Integer>")], {"parallelSquares": lambda v, t: [wrap32(x * x) for x in v]},
    [("parallelSquares", ([1, 2, 3, 4], 2), "four values"), ("parallelSquares", ([], 3), "no values"), ("parallelSquares", ([-3, 5], 1), "one thread")],
    [("parallelSquares", (list(range(1, 21)), 4), "twenty values keep their order"), ("parallelSquares", ([50000], 2), "an int overflow wraps"), ("parallelSquares", ([7, 7, 7], 0), "zero threads means one"),
     ("parallelSquares", (list(range(100, 0, -1)), 8), "descending input"), ("parallelSquares", ([0, -1, 1], 3), "zero and negatives")],
    starter='''
List<Integer> parallelSquares(List<Integer> values, int threads) throws Exception {
    return List.of();
}
''', solution=SQ_SOL,
    wrongs={"sequential": SQ_SEQ, "drops-the-last": SQ_DROP},
    source_tests=[("uses an ExecutorService", ["ExecutorService"], None), ("submits tasks and reads futures", ["submit", ".get()"], None)],
    hints=["Submit every task first; only then call get() on the futures, in order.", "ExecutorService is AutoCloseable."],
    misconceptions=("MC192",), difficulty=3,
)

ex21.explain(
    "j9-l2.1-explain-executors", "Why not just new Thread", ["o2"], ["J9.06"],
    "A service handles each incoming task with `new Thread(task).start()`. Explain three problems with this once the load grows, and how an `ExecutorService` addresses each. Say what `Future.get()` gives you that a bare thread does not, and what happens if you forget to shut an executor down.",
    "Creating a thread per task is expensive and unbounded: a burst can create thousands of threads and exhaust memory, there is no queue or limit, and results and exceptions are lost because Runnable returns nothing. An ExecutorService reuses a fixed number of threads, queues extra tasks, and returns a Future per task: get() waits for the result and rethrows a task's exception wrapped in an ExecutionException. An executor that is never shut down keeps its worker threads alive, so the program may not exit; ExecutorService can be shut down (shutdown lets submitted tasks finish) and is AutoCloseable.",
    levels={
        2: ("The answer gives three problems with per-task threads, matches each executor feature, and explains get() and shutdown.", [
            "Thread per task is costly to create, unbounded (a burst can run out of memory) and gives no way to return a value or an exception. An executor reuses a fixed set of threads, queues the rest, and returns a Future: get() waits for the result and rethrows failures as ExecutionException. If you never shut it down its worker threads keep the program alive, so use shutdown or try-with-resources.",
            "Creation cost, no limit and no results. A pool bounds the threads and queues work, and futures carry the value or the error. Forgetting to close leaves non-daemon workers running."]),
        1: ("The answer names some problems or features without linking them.", [
            "Executors reuse threads, which is faster.",
            "Futures let you get a result."]),
        0: ("The answer sees no benefit.", [
            "new Thread is simpler and just as good.",
            "Executors are only for very large programs."]),
    },
)

l9_l2_1 = Lesson("j9-l2.1", "Executors and futures", ["J9.06"], [
    ("o1", "Predict the result of a chain of CompletableFutures, including a failure"),
    ("o2", "Run tasks on an ExecutorService and collect their results in order"),
], ["j9-l1.3"], 45, ["I112", "I113"], """## Before you start

You should know how to start and join threads and what a race is (module 9.1).

## Explanation

Starting a `Thread` per task does not scale: threads are expensive, there is no limit, and a `Runnable` cannot return a value. An **`ExecutorService`** separates *what to run* from *how to run it*. It manages termination and can produce a **`Future`** to track the result of each asynchronous task. It can be shut down, after which it rejects new tasks: `shutdown()` lets submitted tasks finish, `shutdownNow()` tries to stop the ones executing. It is `AutoCloseable`, so a try-with-resources block waits for the tasks and cleans up.

`Future.get()` waits for the task and returns its result, or throws an `ExecutionException` wrapping what the task threw.

A **`CompletableFuture`** is a Future that may be explicitly completed and supports dependent functions and actions that trigger on completion: `supplyAsync` starts a computation, `thenApply` transforms the result, `thenCombine` joins two futures, `exceptionally` recovers from a failure, and `join` waits. Chaining describes a dataflow without blocking at every step. When several threads try to complete one future, only one succeeds.

## Worked examples

### Example 1: results in input order.

Submit all the tasks first, then call `get()` on the futures in the order you submitted them. The work runs in parallel, the results come back in order.

### Example 2: a chain.

`a.thenCombine(b, Integer::sum).thenApply(x -> x * 2).join()` with 20 and 22 is 84.

## Where this is used

- Parallel report builders, calling several services at once, any job that can be split. Spring and most libraries run their asynchronous work on executors.

## Common mistakes

:::mistake{id=MC192}
**Spawning a thread per task.** Use an executor: it bounds the threads, queues the rest and carries results and failures back.
:::

## Practice

::exercise{id=j9-l2.1-predict-futures}

::exercise{id=j9-l2.1-write-squares}

::exercise{id=j9-l2.1-explain-executors}

## Further reading

- **Java SE 25 API, `ExecutorService`** `[I112]`.
- **Java SE 25 API, `CompletableFuture`** `[I113]`.

## How you'll be assessed

- The **predict** exercise checks future composition (*identifying*).
- The **write** exercise checks fan-out and ordered collection (*implementation*). It also checks your source, because the result looks the same without any parallelism.
- The **explain** exercise checks the case for executors (*explanation*).
""")

# ====================================================================== j9-l2.2
def f_wc(words, threads):
    c = Counter(words)
    return ",".join(f"{w}={c[w]}" for w in sorted(c))


WC_SOL = '''
String wordCounts(List<String> words, int threads) throws InterruptedException {
    ConcurrentHashMap<String, Integer> counts = new ConcurrentHashMap<>();
    int parts = Math.max(1, threads);
    Thread[] workers = new Thread[parts];
    for (int w = 0; w < parts; w++) {
        final int id = w;
        workers[w] = new Thread(() -> {
            for (int i = id; i < words.size(); i += parts) {
                counts.merge(words.get(i), 1, Integer::sum);
            }
        });
        workers[w].start();
    }
    for (Thread worker : workers) {
        worker.join();
    }
    List<String> parts2 = new ArrayList<>();
    for (String word : new TreeSet<>(counts.keySet())) {
        parts2.add(word + "=" + counts.get(word));
    }
    return String.join(",", parts2);
}
'''
WC_CHECK_THEN_PUT = WC_SOL.replace("counts.merge(words.get(i), 1, Integer::sum);", "String word = words.get(i);\n                if (counts.containsKey(word)) {\n                    counts.put(word, counts.get(word) + 1);\n                } else {\n                    counts.put(word, 1);\n                }")
WC_HASHMAP = WC_SOL.replace("ConcurrentHashMap<String, Integer> counts = new ConcurrentHashMap<>();", "Map<String, Integer> counts = new HashMap<>();")
WC_UNSORTED = WC_SOL.replace("new TreeSet<>(counts.keySet())", "counts.keySet()")
WC_ONE_THREAD_ONLY = WC_SOL.replace("for (int i = id; i < words.size(); i += parts) {", "for (int i = id; i < words.size(); i += parts + parts) {")
_BIG = ["a", "b", "a", "c", "b", "a"] * 60

ex22.method(
    "write", "j9-l2.2-write-word-counts", "Counting words from several threads", ["o1"], ["J9.07"], ["IMPL"],
    "Write `wordCounts(words, threads)`: worker threads share one `ConcurrentHashMap<String, Integer>`; worker `w` handles the words at positions `w`, `w + threads`, `w + 2*threads`, and so on, and counts each word with the **atomic** `merge` method. After joining the workers, return `word=count` pairs sorted by word and joined with commas (an empty string if there are no words).",
    [("wordCounts", [("words", "List<String>"), ("threads", "int")], "String")], {"wordCounts": f_wc},
    [("wordCounts", (["b", "a", "b"], 2), "three words"), ("wordCounts", ([], 3), "none"), ("wordCounts", (["x"], 4), "more threads than words")],
    [("wordCounts", (_BIG, 4), "many words, four threads"), ("wordCounts", (_BIG, 8), "many words, eight threads"), ("wordCounts", (["same"] * 300, 6), "one very hot key"),
     ("wordCounts", (["b", "a", "c"], 1), "one thread"), ("wordCounts", (["a", "A", "a"], 2), "case matters"), ("wordCounts", (["q"] * 7, 0), "zero threads means one")],
    starter='''
String wordCounts(List<String> words, int threads) throws InterruptedException {
    return "";
}
''', solution=WC_SOL,
    wrongs={"check-then-put": WC_CHECK_THEN_PUT, "plain-hashmap": WC_HASHMAP, "unsorted": WC_UNSORTED, "skips-words": WC_ONE_THREAD_ONLY},
    source_tests=[("uses ConcurrentHashMap", ["ConcurrentHashMap"], None), ("updates atomically with merge", ["merge"], None)],
    hints=["`merge(key, 1, Integer::sum)` inserts 1 or adds 1, as one atomic step.", "Join all the workers before you read the map."],
    misconceptions=("MC193",), difficulty=3,
)

ex22.explain(
    "j9-l2.2-explain-check-then-act", "Thread-safe parts, unsafe whole", ["o2"], ["J9.07"],
    "A developer writes `if (!cache.containsKey(key)) { cache.put(key, load(key)); }` on a `ConcurrentHashMap` and says 'it is a concurrent map, so this is safe'. Explain what can still go wrong, what the map offers instead, and what it does and does not promise about reads that overlap with updates.",
    "Each call is safe on its own, but the pair is not atomic: two threads can both see the key missing and both call load, so the work is done twice and one result overwrites the other. ConcurrentHashMap provides atomic compound methods (putIfAbsent, computeIfAbsent, compute, merge) that do the check and the update as one step. Its retrievals do not block and may overlap with updates, so a get reflects the most recently completed updates but is not a snapshot of the whole map.",
    levels={
        2: ("The answer explains the check-then-act gap, names an atomic method, and states the retrieval guarantee accurately.", [
            "containsKey and put are each safe but another thread can slip between them, so both threads load and one overwrites the other. Use computeIfAbsent (or putIfAbsent/merge), which do check and update atomically. Reads do not block and can overlap with updates, so they see completed updates but not a frozen snapshot.",
            "The two calls together are not atomic: a race between the check and the put. computeIfAbsent solves it. get never blocks and reflects the latest completed updates."]),
        1: ("The answer names the atomic method without the race, or the race without the fix.", [
            "Use computeIfAbsent instead.",
            "Two threads could both put."]),
        0: ("The answer trusts the concurrent map.", [
            "It is a ConcurrentHashMap so everything done with it is safe.",
            "The only problem is speed."]),
    },
)

l9_l2_2 = Lesson("j9-l2.2", "Concurrent collections", ["J9.07"], [
    ("o1", "Count shared data from several threads with an atomic map update"),
    ("o2", "Explain why a thread-safe collection can still be used unsafely"),
], ["j9-l2.1"], 40, ["I114", "I111"], """## Before you start

You should know `HashMap` from Stage 3 and what a race is.

## Explanation

A plain `HashMap` is not safe to change from several threads: updates can be lost or the map corrupted. `ConcurrentHashMap` is built for it. Retrieval operations (including `get`) generally do not block, so they may overlap with update operations (`put`, `remove`) and reflect the results of the most recently completed updates.

But thread-safe **parts** do not make a thread-safe **whole**. `containsKey` followed by `put` is two calls, and another thread can act between them: the classic **check-then-act** race. The map therefore offers compound operations that do both as one atomic step: `putIfAbsent`, `computeIfAbsent`, `compute` and `merge`.

`merge(word, 1, Integer::sum)` is the idiom for counting: it stores 1 if the word is absent, or applies the function to the old and new value if it is present, atomically. The same idea applies to the atomic classes of lesson 9.1.3.

## Worked examples

### Example 1: counting.

```java
counts.merge(word, 1, Integer::sum);
```

### Example 2: a cache.

```java
cache.computeIfAbsent(key, k -> load(k));
```

loads each key once, even when many threads ask for it together (the function should be short and must not update the same map).

## Where this is used

- Shared caches, registries, per-key statistics. Most "my map loses entries under load" bugs are an unsynchronised `HashMap` or a check-then-act.

## Common mistakes

:::mistake{id=MC193}
**Assuming a concurrent collection makes your own sequences of calls atomic.** Use its compound methods, or a lock around the whole sequence.
:::

## Practice

::exercise{id=j9-l2.2-write-word-counts}

::exercise{id=j9-l2.2-explain-check-then-act}

## Further reading

- **Java SE 25 API, `ConcurrentHashMap`** `[I114]`.

## How you'll be assessed

- The **write** exercise checks atomic counting (*implementation*). It also checks your source, because a race cannot be detected reliably by running it.
- The **explain** exercise checks the check-then-act gap (*explanation*).

The note about the mapping function of `computeIfAbsent` is general guidance and was not taken from a recorded source.
""")

# ====================================================================== j9-l2.3
SCOPED_PROGRAM = '''
static final ScopedValue<String> USER = ScopedValue.newInstance();

void main() {
    System.out.println("bound before=" + USER.isBound());
    ScopedValue.where(USER, "ada").run(() -> {
        System.out.println("inside=" + USER.get());
        ScopedValue.where(USER, "grace").run(() -> System.out.println("inner=" + USER.get()));
        System.out.println("after inner=" + USER.get());
    });
    System.out.println("bound after=" + USER.isBound());
}
'''
ex23.predict(
    "j9-l2.3-predict-scoped", "A value with a lifetime", ["o1"], ["J9.08"],
    "A scoped value is bound to a value only while a block of code runs, and a nested block can bind it again. Predict the exact output.",
    SCOPED_PROGRAM, "bound before=false\ninside=ada\ninner=grace\nafter inner=ada\nbound after=false\n",
    ["Where is `USER` bound, and where is it not?", "What does the value go back to when the inner block ends?"],
    misconceptions=("MC194",), difficulty=2,
)

VT_SOL = '''
long sleepersFinished(int count) throws Exception {
    LongAdder done = new LongAdder();
    try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
        for (int i = 0; i < count; i++) {
            executor.submit(() -> {
                Thread.sleep(20);
                done.increment();
                return null;
            });
        }
    }
    return done.sum();
}
'''
VT_POOL = VT_SOL.replace("Executors.newVirtualThreadPerTaskExecutor()", "Executors.newFixedThreadPool(10)")
VT_NOWAIT = VT_SOL.replace("    try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {", "    ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();\n    {")
VT_SEQ = '''
long sleepersFinished(int count) throws Exception {
    long done = 0;
    for (int i = 0; i < count; i++) {
        Thread.sleep(20);
        done++;
    }
    return done;
}
'''

ex23.method(
    "write", "j9-l2.3-write-virtual", "Ten thousand sleepers", ["o2"], ["J9.08"], ["IMPL"],
    "Each of `count` tasks sleeps for 20 milliseconds and then increments a shared `LongAdder`. Write `sleepersFinished(count)` so that all the tasks run at the same time: create one **virtual thread per task** with `Executors.newVirtualThreadPerTaskExecutor()` (do not pool them), let the try-with-resources close wait for the tasks, and return the adder's sum. For `count` = 10,000 this takes a small fraction of a second; a pool of 10 platform threads would need over 20 seconds.",
    [("sleepersFinished", [("count", "int")], "long")], {"sleepersFinished": lambda n: n},
    [("sleepersFinished", (100,), "a hundred"), ("sleepersFinished", (1000,), "a thousand"), ("sleepersFinished", (0,), "none")],
    [("sleepersFinished", (10000,), "ten thousand"), ("sleepersFinished", (5000,), "five thousand"), ("sleepersFinished", (1,), "one"), ("sleepersFinished", (250,), "two hundred and fifty"),
     ("sleepersFinished", (20000,), "twenty thousand")],
    starter='''
long sleepersFinished(int count) throws Exception {
    return 0;
}
''', solution=VT_SOL,
    wrongs={"ten-platform-threads": VT_POOL, "one-after-another": VT_SEQ, "does-not-wait": VT_NOWAIT},
    source_tests=[("one virtual thread per task", ["newVirtualThreadPerTaskExecutor"], None)],
    hints=["Closing the executor waits for the submitted tasks.", "Virtual threads should not be pooled: one per task."],
    misconceptions=("MC194",), difficulty=3,
)

ex23.explain(
    "j9-l2.3-explain-which-thread", "Platform, virtual, or neither", ["o2"], ["J9.08"],
    "For each workload, say whether you would use platform threads in a fixed pool, virtual threads, or something else, and why: (a) a server making 5,000 concurrent HTTP calls to a slow partner service; (b) rendering 8 large images, each taking seconds of pure computation; (c) passing the signed-in user from a web filter down to a service method and into the child tasks it starts. Also say what state structured concurrency is in with Java 25.",
    "(a) Virtual threads: the tasks spend nearly all their time blocked waiting, virtual threads are cheap and plentiful so one per task, unpooled, is the intended style. (b) A fixed pool of platform threads sized to the number of cores: the work is CPU-bound, virtual threads are not intended for long-running CPU-intensive operations and add nothing. (c) A scoped value: it shares immutable data with callees and child threads for a bounded scope (final in Java 25). Structured concurrency is a preview API in Java 25, needing preview features to be enabled and liable to change, so it should not go into production code on the strength of this course.",
    levels={
        2: ("The answer chooses all three correctly with reasons and states that structured concurrency is a preview in Java 25.", [
            "(a) Virtual threads, one per task: they mostly wait on I/O and are cheap. (b) A fixed pool of platform threads about the number of cores, because virtual threads are not meant for long CPU-bound work. (c) A ScopedValue, bound for the request and visible to callees and child threads. Structured concurrency is still a preview feature in 25, so it needs --enable-preview and may change.",
            "HTTP calls: virtual threads. Image rendering: platform pool sized to the cores. Passing the user: scoped value, which is final in 25. Structured concurrency is preview in 25."]),
        1: ("The answer gets two of three or omits the preview status.", [
            "Virtual threads for the HTTP calls and a pool for the images.",
            "Use virtual threads for everything."]),
        0: ("The answer misjudges the cases.", [
            "Virtual threads make CPU-bound work faster, so use them for the images.",
            "A static field is the best way to pass the user."]),
    },
)

l9_l2_3 = Lesson("j9-l2.3", "Virtual threads, scoped values and structured concurrency", ["J9.08"], [
    ("o1", "Predict how a scoped value is bound and rebound"),
    ("o2", "Choose between platform threads, virtual threads and scoped values for a workload"),
], ["j9-l2.1"], 45, ["I108", "I109", "I110", "I116"], """## Before you start

You should be comfortable with executors (lesson 9.2.1).

## Explanation

**Virtual threads** (final in Java 21, JEP 444) are lightweight threads scheduled by the Java runtime rather than the operating system; a JVM may support millions of them. They let simple thread-per-request code scale: the goal is to enable server applications written in the thread-per-request style to scale with near-optimal hardware utilisation. They suit tasks that spend most of their time **blocked**, often waiting for I/O, and are not intended for long-running CPU-intensive operations. Because they are cheap and plentiful they should **never be pooled**: create a new virtual thread for every task. Platform threads, by contrast, are heavyweight, long-lived and often pooled.

**Scoped values** (final in Java 25, JEP 506) let a method share immutable data with its callees within a thread and with child threads. The lifetime of the shared data is apparent from the structure of the code: the value is bound only while a block runs, and a nested block can bind it again; when the inner block ends, the outer binding is visible again.

**Structured concurrency** (JEP 505) treats related tasks running in different threads as a single unit of work. In Java 25 it is still a **preview API** (the fifth preview), so it needs preview features enabled, may change, and is not used in this course's exercises.

## Worked examples

### Example 1: a virtual thread per task.

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10_000; i++) {
        executor.submit(() -> { Thread.sleep(20); return null; });
    }
}
```

### Example 2: a scoped binding.

`ScopedValue.where(USER, "ada").run(...)` binds `USER` for the run and nowhere else.

## Where this is used

- Web servers that block on databases and remote calls, and request-scoped context such as the signed-in user or a trace id, which used to need a thread-local variable.

## Common mistakes

:::mistake{id=MC194}
**Using virtual threads for CPU-bound work, or pooling them.** They help with waiting, not with computing, and a pool defeats their purpose.
:::

## Practice

::exercise{id=j9-l2.3-predict-scoped}

::exercise{id=j9-l2.3-write-virtual}

::exercise{id=j9-l2.3-explain-which-thread}

## Further reading

- **JEP 444, Virtual Threads** `[I108]`.
- **JEP 506, Scoped Values** `[I109]`.
- **JEP 505, Structured Concurrency (Fifth Preview)** `[I110]`.
- **Java SE 25 API, `Thread`** `[I116]`.

## How you'll be assessed

- The **predict** exercise checks scoped values (*identifying*).
- The **write** exercise checks the virtual-thread-per-task style (*implementation*).
- The **explain** exercise checks the choice of thread type (*explanation*).
""")
print("module 9.2 authored")
