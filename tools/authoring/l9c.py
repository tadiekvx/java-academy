"""Stage 9 authoring: module 9.3 (JVM internals and performance). Real GC, JIT and JFR output captured from this machine."""
import l9common
from l9common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex31 = Exercises("j9-l3.1")
ex32 = Exercises("j9-l3.2")
ex33 = Exercises("j9-l3.3")

REGISTER = {
    "j9-l3.1": ("Memory and garbage collection", ["J9.09"]),
    "j9-l3.2": ("JIT compilation and measuring honestly", ["J9.10"]),
    "j9-l3.3": ("Profiling and memory leaks", ["J9.11"]),
}
MISCS = {
    "MC195": (["J9.09"], "I115", "Setting a variable to null frees the object immediately, and a memory leak is impossible in a garbage-collected language"),
    "MC196": (["J9.10"], "I116", "The first timing of a Java method is its true speed, so one measurement is enough"),
    "MC197": (["J9.11"], "I116", "The slow-looking code is the slow code; profiling is only needed when the fix did not work"),
}
register(REGISTER, MISCS)

# ====================================================================== j9-l3.1
def f_unreach(edges, roots):
    graph, nodes = {}, set(roots)
    for e in edges:
        a, b = e.split(">")
        graph.setdefault(a, []).append(b)
        nodes |= {a, b}
    seen, stack = set(), list(roots)
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(graph.get(n, []))
    return sorted(nodes - seen)


UNREACH_SOL = '''
List<String> unreachable(List<String> edges, List<String> roots) {
    Map<String, List<String>> graph = new HashMap<>();
    Set<String> objects = new TreeSet<>(roots);
    for (String edge : edges) {
        String[] parts = edge.split(">");
        graph.computeIfAbsent(parts[0], k -> new ArrayList<>()).add(parts[1]);
        objects.add(parts[0]);
        objects.add(parts[1]);
    }
    Set<String> marked = new HashSet<>();
    Deque<String> work = new ArrayDeque<>(roots);
    while (!work.isEmpty()) {
        String next = work.pop();
        if (marked.add(next)) {
            work.addAll(graph.getOrDefault(next, List.of()));
        }
    }
    List<String> garbage = new ArrayList<>();
    for (String object : objects) {
        if (!marked.contains(object)) {
            garbage.add(object);
        }
    }
    return garbage;
}
'''
UNREACH_DIRECT = UNREACH_SOL.replace("            work.addAll(graph.getOrDefault(next, List.of()));", "            if (roots.contains(next)) {\n                work.addAll(graph.getOrDefault(next, List.of()));\n            }")
UNREACH_NOROOTS = UNREACH_SOL.replace("new ArrayDeque<>(roots)", "new ArrayDeque<>()")
UNREACH_CYCLE = UNREACH_SOL.replace("        if (marked.add(next)) {\n            work.addAll(graph.getOrDefault(next, List.of()));\n        }", "        marked.add(next);\n        for (String child : graph.getOrDefault(next, List.of())) {\n            if (!marked.contains(child)) {\n                work.push(child);\n            }\n        }")
UNREACH_REFCOUNT = '''
List<String> unreachable(List<String> edges, List<String> roots) {
    Set<String> objects = new TreeSet<>(roots);
    Set<String> referenced = new HashSet<>();
    for (String edge : edges) {
        String[] parts = edge.split(">");
        objects.add(parts[0]);
        objects.add(parts[1]);
        referenced.add(parts[1]);
    }
    List<String> garbage = new ArrayList<>();
    for (String object : objects) {
        if (!referenced.contains(object) && !roots.contains(object)) {
            garbage.add(object);
        }
    }
    return garbage;
}
'''

ex31.method(
    "write", "j9-l3.1-write-unreachable", "What the collector may free", ["o1"], ["J9.09"], ["IMPL"],
    "A garbage collector keeps every object it can reach by following references from the **roots** (local variables, static fields and so on) and may free the rest. Each entry `A>B` means object A holds a reference to object B. Write `unreachable(edges, roots)` returning the objects that cannot be reached from any root, sorted alphabetically. Objects are all the names that appear in `edges` or `roots`. Note that objects which only reference each other, in a cycle, are still unreachable.",
    [("unreachable", [("edges", "List<String>"), ("roots", "List<String>")], "List<String>")], {"unreachable": f_unreach},
    [("unreachable", (["main>list", "list>item", "orphan>item"], ["main"]), "one orphan"), ("unreachable", (["a>b", "b>a"], ["main"]), "a cycle nobody reaches"), ("unreachable", ([], ["x"]), "only a root")],
    [("unreachable", (["main>a", "a>b", "b>c", "x>c"], ["main"]), "a long chain and one orphan"), ("unreachable", (["m>a", "a>m"], ["m"]), "a reachable cycle"), ("unreachable", (["a>b", "c>d"], ["a", "c"]), "two roots"),
     ("unreachable", (["a>b", "b>c"], []), "no roots at all"), ("unreachable", (["r>x", "x>y", "y>z", "z>x", "q>z"], ["r"]), "a cycle reached from a root, and an orphan"), ("unreachable", (["a>a"], []), "a self-reference with no root")],
    starter='''
List<String> unreachable(List<String> edges, List<String> roots) {
    return List.of();
}
''', solution=UNREACH_SOL,
    wrongs={"only-roots-are-followed": UNREACH_DIRECT, "no-roots": UNREACH_NOROOTS, "counts-references-instead": UNREACH_REFCOUNT},
    hints=["Start from the roots and mark everything you can reach.", "An object that something references can still be garbage."],
    misconceptions=("MC195",), difficulty=3,
)

GC_CAP = cap("cap_gc.txt")
CHURN = '''import java.util.ArrayList;
import java.util.List;

public class Churn {
    public static void main(String[] args) {
        List<byte[]> keep = new ArrayList<>();
        long total = 0;
        for (int i = 0; i < 4000; i++) {
            byte[] block = new byte[100_000];
            total += block.length;
            if (i % 40 == 0) {
                keep.add(block);
            }
        }
        System.out.println("allocated=" + total + " kept=" + keep.size());
    }
}'''
ex31.explain(
    "j9-l3.1-explain-gc-log", "Reading a GC log", ["o2"], ["J9.09"],
    "This program allocates 4,000 blocks of 100,000 bytes and keeps every 40th one. Below are the program and the GC log that `-Xlog:gc` produced when it was run with a 64 MB heap (`-Xmx64m`), on this machine.\n\n" + fence(CHURN, "java") + "\n\n" + fence(GC_CAP) + "\n\nExplain: which collector ran, what a line such as `35M->2M(64M) 0,262ms` says, why the number after the arrow grows from 2M to 10M, and what the program's `kept=100` has to do with that final 10M.",
    "G1, the default collector, was used. Each line is a young-generation collection: the heap held 35 MB before it, 2 MB after, with 64 MB of heap in total, and the pause lasted about a quarter of a millisecond. Almost all blocks are garbage the moment the loop moves on, so each collection frees nearly everything. The retained size grows because the program keeps every 40th block: 100 blocks of 100,000 bytes are about 10 MB, matching the 10M after the last collection. That growth is live data, not a leak in the collector.",
    levels={
        2: ("The answer names G1, reads before/after/total and the pause, and explains the growth from the 100 kept blocks.", [
            "G1 (the log says Using G1). 35M->2M(64M) means the heap was 35 MB before the pause and 2 MB after, out of 64 MB, and the pause took about 0.26 ms. Most blocks die at once, so each young collection frees nearly all. The after-size climbs to 10M because 100 kept blocks of 100,000 bytes is about 10 MB of live data.",
            "The collector was G1. Each line shows heap used before and after the pause, the total heap, and the pause time. The leftover grows because kept=100 blocks of ~100 KB each stay reachable, about 10 MB."]),
        1: ("The answer reads the log but does not connect the growth to the kept blocks.", [
            "G1 ran and the heap went from 35M down to 2M each time.",
            "The pauses are short because most memory was freed."]),
        0: ("The answer misreads the log.", [
            "The program leaks memory because the number keeps growing.",
            "The pauses show the program was slow."]),
    },
)

l9_l3_1 = Lesson("j9-l3.1", "Memory and garbage collection", ["J9.09"], [
    ("o1", "Work out which objects a collector can free by following references from the roots"),
    ("o2", "Read a real GC log line and relate the numbers to what the program does"),
], ["j9-l1.1"], 45, ["I115"], """## Before you start

You should know objects, references and `null`, and that Java frees memory automatically.

## Explanation

Java programs allocate objects on the **heap**; local variables and call frames live on each thread's **stack**. You never free an object yourself. The **garbage collector** finds objects that the program can no longer reach and reclaims their memory.

What counts as reachable is defined by the **roots**: local variables on thread stacks, static fields and a few others. An object is live if you can get to it by following references from a root. Everything else may be freed, **even objects that still reference each other**: a cycle that nothing outside points to is garbage. This is why reference counting is not how the JVM works.

G1, the Garbage-First collector, is the default collector, so typically you do not have to do anything to enable it. Most objects die young, so the collector collects the young part of the heap often and cheaply.

You can ask the JVM to log what it does. With `-Xlog:gc` each collection is one line: what kind of pause, how large the heap was before and after the collection, the total heap size, and how long the pause lasted.

## Worked examples

### Example 1: a real log.

The exercise shows the log of a program that allocates 400 MB in 100 KB blocks but keeps only every 40th block. Each young collection frees almost everything, and the live data after each one grows toward 10 MB, the size of the 100 blocks that are kept.

### Example 2: a cycle that is garbage.

`a>b, b>a` with root `main`: neither `a` nor `b` is reachable from `main`, so both can be freed, though each is referenced.

## Where this is used

- Diagnosing pauses and memory growth in any long-running Java service. The first question is always what is still reachable, and why.

## Common mistakes

:::mistake{id=MC195}
**Believing a garbage-collected language cannot leak.** The collector frees unreachable objects only. A forgotten reference in a static list keeps everything it points to alive for ever.
:::

## Practice

::exercise{id=j9-l3.1-write-unreachable}

::exercise{id=j9-l3.1-explain-gc-log}

## Further reading

- **HotSpot GC Tuning Guide, Garbage-First (G1)** `[I115]`.

## How you'll be assessed

- The **write** exercise checks reachability (*implementation*).
- The **explain** exercise checks that you can read a real GC log (*explanation*).

The reading of the log's numbers (heap before and after, total, pause) comes from the log itself and the program, which agree; the course did not check it against the unified-logging documentation.
""")

# ====================================================================== j9-l3.2
def f_median(timings, warmup):
    rest = sorted(timings[warmup:])
    if not rest:
        return -1
    n = len(rest)
    return rest[n // 2] if n % 2 else (rest[n // 2 - 1] + rest[n // 2]) // 2


MED_SOL = '''
long steadyMedian(List<Long> timings, int warmup) {
    if (warmup >= timings.size()) {
        return -1;
    }
    List<Long> rest = new ArrayList<>(timings.subList(warmup, timings.size()));
    Collections.sort(rest);
    int n = rest.size();
    return n % 2 == 1 ? rest.get(n / 2) : (rest.get(n / 2 - 1) + rest.get(n / 2)) / 2;
}
'''
MED_MEAN = MED_SOL.replace("    return n % 2 == 1 ? rest.get(n / 2) : (rest.get(n / 2 - 1) + rest.get(n / 2)) / 2;", "    long sum = 0;\n    for (long t : rest) {\n        sum += t;\n    }\n    return sum / n;")
MED_NO_SORT = MED_SOL.replace("    Collections.sort(rest);\n", "")
MED_NO_WARMUP = MED_SOL.replace("timings.subList(warmup, timings.size())", "timings")
MED_UPPER = MED_SOL.replace("(rest.get(n / 2 - 1) + rest.get(n / 2)) / 2", "rest.get(n / 2)")

ex32.method(
    "write", "j9-l3.2-write-median", "A fairer timing", ["o1"], ["J9.10"], ["IMPL"],
    "Benchmark timings from repeated runs include a slow warm-up while the JIT compiles the code. Write `steadyMedian(timings, warmup)`: ignore the first `warmup` timings, then return the median of the rest (the middle value of the sorted list; for an even count, the average of the two middle values rounded down). If nothing is left after the warm-up, return -1.",
    [("steadyMedian", [("timings", "List<Long>"), ("warmup", "int")], "long")], {"steadyMedian": f_median},
    [("steadyMedian", ([2750, 2143, 1736, 1725, 1728], 2), "the numbers from the lesson"), ("steadyMedian", ([5, 1, 3], 0), "odd count, no warm-up"), ("steadyMedian", ([1, 2], 2), "nothing left")],
    [("steadyMedian", ([9, 1, 8, 2, 7, 3], 0), "even count"), ("steadyMedian", ([100, 10, 11, 12, 13], 1), "a slow first run is ignored"), ("steadyMedian", ([4, 4, 4, 4], 1), "equal values"),
     ("steadyMedian", ([], 0), "no timings"), ("steadyMedian", ([10, 20, 30, 1000000], 0), "an outlier does not move the median"), ("steadyMedian", ([7], 0), "a single run"),
     ("steadyMedian", ([3, 1, 2, 9, 8], 5), "warm-up is all of them"), ("steadyMedian", ([1, 2, 3, 4, 5], 1), "even count after warm-up")],
    starter='''
long steadyMedian(List<Long> timings, int warmup) {
    return 0;
}
''', solution=MED_SOL,
    wrongs={"mean-instead": MED_MEAN, "unsorted": MED_NO_SORT, "keeps-the-warmup": MED_NO_WARMUP, "upper-middle": MED_UPPER},
    hints=["Sort a copy of the remaining values.", "For an even count take both middle values."],
    misconceptions=("MC196",), difficulty=3,
)

WARM = cap("cap_warmup.txt")
COMP = cap("cap_compile.txt")
HOT = '''public class Hot {
    static long work(long n) {
        long sum = 0;
        for (long i = 0; i < n; i++) {
            sum += i % 7;
        }
        return sum;
    }

    public static void main(String[] args) {
        long result = 0;
        for (int round = 0; round < 40; round++) {
            long start = System.nanoTime();
            result += work(5_000_000L);
            long micros = (System.nanoTime() - start) / 1000;
            if (round < 4 || round % 10 == 0) {
                System.out.println("round " + round + ": " + micros + " us");
            }
        }
        System.out.println("result=" + result);
    }
}'''
ex32.explain(
    "j9-l3.2-explain-warmup", "Why the first number is not the speed", ["o2"], ["J9.10"],
    "Below are a small program, the timings it printed on this machine, and the start of the JIT compilation log (`-XX:+PrintCompilation`, filtered to the method `work`).\n\n" + fence(HOT, "java") + "\n\n" + fence(WARM) + "\n\n" + fence(COMP) + "\n\nExplain: how much slower was round 0 than the steady rounds, what the compilation log shows happened to `Hot::work`, why a benchmark that runs the method once would mislead, and what you would do to measure it fairly.",
    "Round 0 took 2750 microseconds against about 1730 in the steady rounds, roughly 1.6 times as long. The log shows the same method compiled several times at different levels (3, then 4), plus notes that earlier compilations were made not entrant: the JVM starts by interpreting and then compiles hot code with increasing optimisation, replacing earlier versions. A single timing therefore measures the interpreter and compiler warming up, not the steady speed. Run the method many times, discard the early runs, and report a robust statistic such as the median of the rest.",
    levels={
        2: ("The answer quantifies the difference, reads the compilation log, and describes a fair measurement.", [
            "Round 0 was 2750 us against about 1730 in later rounds, about 1.6 times slower. The log shows work compiled at level 3 and then level 4, with older versions made not entrant, so the JVM was progressively optimising it. A one-off measurement times the warm-up. I would repeat many times, throw away the first runs and use the median of the rest.",
            "First round is around 60% slower. The JIT compiles Hot::work more than once, moving to a higher level and retiring the older code. So measure after warm-up, many repetitions, and use the median."]),
        1: ("The answer notes the first run is slower without the log or the method.", [
            "The first run is slower because of the JIT.",
            "Run it a few times and average."]),
        0: ("The answer treats the first timing as the speed.", [
            "The program runs at 2750 microseconds, the later numbers are noise.",
            "JIT compilation makes no difference to timing."]),
    },
)

l9_l3_2 = Lesson("j9-l3.2", "JIT compilation and measuring honestly", ["J9.10"], [
    ("o1", "Summarise repeated timings robustly, ignoring warm-up"),
    ("o2", "Explain from a real log why a Java method gets faster after its first runs"),
], ["j9-l3.1"], 40, ["I115"], """## Before you start

You should know what a compiler does and have timed code with `System.nanoTime` (Stage 5).

## Explanation

The JVM does not run your bytecode at full speed from the start. It begins by interpreting it, notices which methods are **hot**, and compiles those to machine code with its just-in-time (JIT) compilers, recompiling at higher optimisation levels as a method keeps being used. This takes time, and the early runs are slower. It is called **warm-up**.

For measurement this has consequences:

- The first timing is not the speed of the code. Run it many times and discard the early runs.
- Use a robust statistic. The mean is dragged by outliers (a garbage collection pause, a busy machine); the **median** is not.
- Measure what you are going to run: the same data size, the same JVM flags, the same machine. A fast result on a toy input does not predict a large one.
- Guessing which code is slow is unreliable; measure first (next lesson).

`-XX:+PrintCompilation` shows the compilations as they happen: each line has a timestamp, a compile id, an optional flag, a compilation level, the method and its size, and sometimes a note such as `made not entrant` when an earlier compiled version has been replaced.

## Worked examples

### Example 1: real timings.

The first round of the exercise program took 2750 microseconds. The steady rounds took about 1730. The same code, the same data.

### Example 2: the median.

For timings 2750, 2143, 1736, 1725, 1728 with the first two discarded, the median of the rest is 1728.

## Where this is used

- Any performance claim: "this change is 20% faster" is meaningful only after warm-up and with repetition. Serious benchmarks use a harness (such as JMH) that does this for you; it is not available in this course's runner.

## Common mistakes

:::mistake{id=MC196}
**Timing a method once and trusting the number.** The first run includes interpretation and compilation. Repeat, discard the warm-up, report a median.
:::

## Practice

::exercise{id=j9-l3.2-write-median}

::exercise{id=j9-l3.2-explain-warmup}

## Further reading

- The JDK tools used here (`java -XX:+PrintCompilation`, `jfr`, `jcmd`) are described in the JDK tools reference. This course did not record that reference as a verified source, so check your JDK's own documentation.

## How you'll be assessed

- The **write** exercise checks robust summarising (*implementation*).
- The **explain** exercise checks that you can read real timings and a compilation log (*explanation*).

The description of the `PrintCompilation` columns is standard HotSpot knowledge and was not taken from a recorded source. The timings are from one run on one machine and will differ on yours.
""")

# ====================================================================== j9-l3.3
def f_grow(snaps):
    parsed = []
    for s in snaps:
        d = {}
        for part in s.split(","):
            if part:
                k, v = part.split("=")
                d[k] = int(v)
        parsed.append(d)
    if len(parsed) < 2:
        return []
    out = []
    for k in parsed[0]:
        if all(k in d for d in parsed) and all(parsed[i][k] < parsed[i + 1][k] for i in range(len(parsed) - 1)):
            out.append(k)
    return sorted(out)


GROW_SOL = '''
List<String> growingClasses(List<String> snapshots) {
    List<Map<String, Integer>> parsed = new ArrayList<>();
    for (String snapshot : snapshots) {
        Map<String, Integer> counts = new HashMap<>();
        for (String part : snapshot.split(",")) {
            if (!part.isEmpty()) {
                String[] pair = part.split("=");
                counts.put(pair[0], Integer.parseInt(pair[1]));
            }
        }
        parsed.add(counts);
    }
    List<String> growing = new ArrayList<>();
    if (parsed.size() < 2) {
        return growing;
    }
    for (String name : parsed.get(0).keySet()) {
        boolean always = true;
        for (int i = 0; i + 1 < parsed.size() && always; i++) {
            Integer now = parsed.get(i).get(name);
            Integer next = parsed.get(i + 1).get(name);
            always = now != null && next != null && now < next;
        }
        if (always) {
            growing.add(name);
        }
    }
    Collections.sort(growing);
    return growing;
}
'''
GROW_ANY = GROW_SOL.replace("always = now != null && next != null && now < next;", "always = now != null && next != null && now <= next;")
GROW_FIRST_LAST = GROW_SOL.replace("for (int i = 0; i + 1 < parsed.size() && always; i++) {", "for (int i = 0; i + 1 < parsed.size() && always; i += parsed.size() - 1) {")
GROW_UNSORTED = GROW_SOL.replace("    Collections.sort(growing);\n", "")
GROW_ONE = GROW_SOL.replace("    if (parsed.size() < 2) {\n        return growing;\n    }\n", "")

ex33.method(
    "write", "j9-l3.3-write-growing", "Spot the leak", ["o1"], ["J9.11"], ["IMPL", "DEBUG"],
    "A heap histogram counts live instances per class. Each snapshot is `Class=count,Class=count,...`, taken at a later time than the one before. A **suspect leak** is a class whose count is present in every snapshot and **strictly increases** from each snapshot to the next. Write `growingClasses(snapshots)` returning the suspects sorted alphabetically (an empty list if there are fewer than two snapshots).",
    [("growingClasses", [("snapshots", "List<String>")], "List<String>")], {"growingClasses": f_grow},
    [("growingClasses", (["Order=10,Session=5,Cache=100", "Order=10,Session=9,Cache=100", "Order=10,Session=14,Cache=100"],), "Session grows"), ("growingClasses", (["A=1"],), "one snapshot"), ("growingClasses", (["A=1,B=2", "A=2,B=2"],), "B is flat")],
    [("growingClasses", (["A=1,B=5", "A=2,B=4", "A=3,B=6"],), "B goes down once"), ("growingClasses", (["A=1", "A=2", "A=2"],), "stops growing"), ("growingClasses", (["A=1,B=1", "A=2", "A=3,B=3"],), "B is missing from one snapshot"),
     ("growingClasses", (["X=1,Y=1,Z=1", "X=2,Y=2,Z=1", "X=3,Y=3,Z=1"],), "two suspects, sorted"), ("growingClasses", ([],), "no snapshots"), ("growingClasses", (["Z=1,A=1", "Z=2,A=2"],), "sorted output"),
     ("growingClasses", (["A=5,B=1", "A=1,B=2", "A=9,B=3"],), "A dips then jumps"),
     ("growingClasses", (["BB=1,Aa=1", "BB=2,Aa=2"],), "two suspects whose hash codes collide, still sorted")],
    starter='''
List<String> growingClasses(List<String> snapshots) {
    return List.of();
}
''', solution=GROW_SOL,
    wrongs={"flat-counts-allowed": GROW_ANY, "only-compares-ends": GROW_FIRST_LAST, "unsorted": GROW_UNSORTED, "one-snapshot-is-enough": GROW_ONE},
    hints=["Compare each snapshot with the next one, not just the first with the last.", "A class that disappears from a snapshot is not growing."],
    misconceptions=("MC197",), difficulty=3,
)

JFR = cap("cap_jfr.txt")
REPORT = cap("cap_report_source.txt")
ex33.explain(
    "j9-l3.3-explain-profile", "Fix what the profile says", ["o2"], ["J9.11"],
    "A colleague says the report is slow and is sure the fix is `fastTotal`, 'the loop over the list'. You record a 6-second Java Flight Recorder profile of this program and count the samples per method of your own class. The program and the result follow.\n\n" + fence(REPORT, "java") + "\n\n" + fence(JFR) + "\n\nExplain what the profile tells you about where the time goes, why the colleague's guess is wrong, what is expensive about the slow method (look at what it does for every index), and what the faster version looks like. Say why you would profile again after the change.",
    "All 531 execution samples had `slowTotal` on their stack and none had `fastTotal`, so essentially all the time is in `slowTotal`. For every index it builds a stream, skips `i` elements and takes one, which makes the method quadratic (the work grows with the square of the list size); `fastTotal` is already a single pass. The fix is to sum in one pass, as `fastTotal` does, or to use a single stream sum. Profile again after the change to confirm that the total time fell and to see what the new hot spot is; guessing, or assuming a fix worked, is how tuning goes wrong.",
    levels={
        2: ("The answer reads the samples, rejects the guess, explains the quadratic cost and the fix, and re-profiles.", [
            "All 531 samples are under slowTotal and none under fastTotal, so the guess is wrong. slowTotal builds a stream, skips i elements and takes one for each index, so it does about n squared work. The fix is a single pass like fastTotal. Then I would profile again to confirm the time fell and see what is hot next.",
            "The profile puts 100% of samples in slowTotal. It re-walks the list from the start for every index (skip(i)), which is quadratic. Replace it with a single loop or one stream sum, then re-measure."]),
        1: ("The answer reads the profile but does not explain the cost or the re-measurement.", [
            "slowTotal is where the time goes, not fastTotal.",
            "The colleague should have measured first."]),
        0: ("The answer follows the guess.", [
            "Optimise fastTotal because loops are slow.",
            "The profile cannot tell us anything about which method is slow."]),
    },
)

l9_l3_3 = Lesson("j9-l3.3", "Profiling and memory leaks", ["J9.11"], [
    ("o1", "Pick out suspect leaks from successive heap histograms"),
    ("o2", "Read a real sampling profile and decide what to change"),
], ["j9-l3.2", "j9-l3.1"], 45, ["I115"], """## Before you start

You should know why timings need warm-up (lesson 9.3.2) and what reachability means (lesson 9.3.1).

## Explanation

Programmers are bad at guessing where a program spends its time. **Profile first.** A **sampling profiler** looks at what the program is doing at regular intervals and counts. The JDK includes one, **Java Flight Recorder** (JFR): start the program with `-XX:StartFlightRecording`, and afterwards read the recording with the `jfr` tool, for example `jfr summary` for the event counts and `jfr print --events jdk.ExecutionSample` for the samples, each with its stack. Counting samples per method of your own code shows which of your methods the time is spent under.

The exercise shows exactly that: a 6-second recording of a program with a slow and a fast method, and the counts.

A **memory leak** in a garbage-collected language is data that is still reachable but no longer needed: for example, entries added to a static map and never removed. The collector cannot free it, because it is reachable. The signature is a class whose live instance count rises across successive heap histograms (`jcmd <pid> GC.class_histogram` prints one) and never falls back. Finding *what holds* the objects then needs a heap dump and a tool; this course only reads histograms.

After any change, **measure again**. A fix you did not measure is a guess.

## Worked examples

### Example 1: the profile.

All 531 samples were under `slowTotal`, and none under `fastTotal`, which the colleague had suspected.

### Example 2: the histogram rule.

`Order=10,Session=5` then `Order=10,Session=9` then `Order=10,Session=14`: `Session` grows at every step, `Order` is constant, so `Session` is the suspect.

## Where this is used

- Every performance bug report and every out-of-memory incident. The stage project asks you to diagnose problems from evidence.

## Common mistakes

:::mistake{id=MC197}
**Optimising the code that looks slow.** Look at the profile, change what it points to, and measure again.
:::

## Practice

::exercise{id=j9-l3.3-write-growing}

::exercise{id=j9-l3.3-explain-profile}

## Further reading

- **HotSpot GC Tuning Guide** `[I115]` for how the collector decides what to free.

## How you'll be assessed

- The **write** exercise checks leak-suspect detection (*implementation*).
- The **explain** exercise checks that you can act on a real profile (*explanation*).

The profile is real, from one recording on one machine. The description of the `jfr` and `jcmd` commands is standard JDK usage and was not taken from a recorded source; a flame-graph viewer is not covered.
""")
print("module 9.3 authored")
