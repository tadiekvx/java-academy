"""Stage 12 authoring: module 12.1 (Observability and troubleshooting). Incident data is a constructed teaching fixture and is labelled as such."""
import json
import math
import re
import l12common
from l12common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex11 = Exercises("j12-l1.1")
ex12 = Exercises("j12-l1.2")
ex13 = Exercises("j12-l1.3")
ex14 = Exercises("j12-l1.4")

REGISTER = {
    "j12-l1.1": ("Structured logs and the three signals", ["J12.01"]),
    "j12-l1.2": ("SLIs, SLOs and percentiles", ["J12.02"]),
    "j12-l1.3": ("Tracing", ["J12.03"]),
    "j12-l1.4": ("Reading an incident", ["J12.04"]),
}
MISCS = {
    "MC214": (["J12.01"], "I125", "Logs, metrics and traces are three names for the same thing, so one of them is enough"),
    "MC215": (["J12.02"], "I124", "The average latency tells you how users experience the service, so it is the right number for an objective"),
    "MC216": (["J12.03"], "I125", "A slow request is slow in its root span, so the root span's duration shows where to look"),
    "MC217": (["J12.04"], "I124", "During an incident the first job is to find the root cause and fix the code"),
}
register(REGISTER, MISCS)

# ====================================================================== j12-l1.1
def j(s):
    return json.dumps(s, ensure_ascii=False, separators=(",", ":"))


def f_slog(level, message, fields):
    parts = [f'"level":{j(level)}', f'"message":{j(message)}']
    for f in fields:
        k, v = f.split("=", 1)
        parts.append(f"{j(k)}:{v if re.fullmatch(r'-?[0-9]+', v) else j(v)}")
    return "{" + ",".join(parts) + "}"


SLOG_SOL = '''
String structuredLog(String level, String message, List<String> fields) {
    StringBuilder out = new StringBuilder("{\\"level\\":" + quote(level) + ",\\"message\\":" + quote(message));
    for (String field : fields) {
        int equals = field.indexOf('=');
        String key = field.substring(0, equals);
        String value = field.substring(equals + 1);
        out.append(",").append(quote(key)).append(":").append(value.matches("-?[0-9]+") ? value : quote(value));
    }
    return out.append("}").toString();
}

String quote(String text) {
    return "\\"" + text.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\"") + "\\"";
}
'''
SLOG_ALL_STRINGS = SLOG_SOL.replace('value.matches("-?[0-9]+") ? value : quote(value)', 'quote(value)')
SLOG_NO_ESCAPE = SLOG_SOL.replace('return "\\"" + text.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\"") + "\\"";', 'return "\\"" + text + "\\"";')
SLOG_SPLIT_ALL = SLOG_SOL.replace("int equals = field.indexOf('=');", "int equals = field.lastIndexOf('=');")
SLOG_ORDER = SLOG_SOL.replace('"{\\"level\\":" + quote(level) + ",\\"message\\":" + quote(message)', '"{\\"message\\":" + quote(message) + ",\\"level\\":" + quote(level)')

ex11.method(
    "write", "j12-l1.1-write-structured", "A log line a machine can read", ["o1"], ["J12.01"], ["IMPL"],
    "Free-text logs are hard to search. A structured log line is one JSON object per event. Write `structuredLog(level, message, fields)` returning an object with `level` first, `message` second, then one member per field in order. Each field is `key=value` (split at the **first** `=`). A value that is a whole number (optionally with a leading minus) is written as a JSON number, anything else as a string. Escape `\"` and `\\` in strings. No spaces in the output.",
    [("structuredLog", [("level", "String"), ("message", "String"), ("fields", "List<String>")], "String")], {"structuredLog": f_slog},
    [("structuredLog", ("INFO", "transfer applied", ["account=7", "cents=500"]), "numbers stay numbers"), ("structuredLog", ("WARN", "slow query", ["table=transactions", "ms=2100"]), "a string and a number"), ("structuredLog", ("INFO", "started", []), "no fields")],
    [("structuredLog", ("ERROR", 'said "no"', ["who=ada"]), "quotes in the message"), ("structuredLog", ("INFO", "x", ["path=C:\\temp"]), "a backslash in a value"), ("structuredLog", ("INFO", "x", ["expr=a=b"]), "an equals sign in a value"),
     ("structuredLog", ("INFO", "x", ["delta=-5", "id=007"]), "negative and zero-padded numbers"), ("structuredLog", ("INFO", "x", ["empty="]), "an empty value is a string"), ("structuredLog", ("INFO", "café", ["city=Zürich"]), "non-ASCII text is kept"),
     ("structuredLog", ("INFO", "x", ["ratio=1.5"]), "a decimal is treated as a string here")],
    starter='''
String structuredLog(String level, String message, List<String> fields) {
    return "";
}
''', solution=SLOG_SOL,
    wrongs={"everything-is-a-string": SLOG_ALL_STRINGS, "no-escaping": SLOG_NO_ESCAPE, "splits-at-the-last-equals": SLOG_SPLIT_ALL, "message-first": SLOG_ORDER},
    hints=["Build the text by appending pieces in order.", "Check the value with a regular expression for a whole number."],
    misconceptions=("MC214",), difficulty=3,
)

STARTUP = cap("cap_startup.txt")
ex11.explain(
    "j12-l1.1-explain-signals", "Three signals, one incident", ["o2"], ["J12.01"],
    "These are real startup lines from this platform's backend:\n\n" + fence(STARTUP) + "\n\nAnswer: (1) The OpenTelemetry documentation names three signals: traces, metrics and logs. Give each in one sentence, and say which of the three these lines are. (2) What is hard about finding, say, every start that took more than two seconds from lines like these, and how would a structured log line change that? (3) A customer reports that their transfer 'took ages at 14:02'. Say what you would look at in each of the three signals and in what order.",
    "(1) A trace is the path of a request through your application; a metric is a measurement captured at runtime; a log is a recording of an event. These lines are logs. (2) Each line is free text: the start duration is buried in a sentence ('Started AcademyApplication in 1.431 seconds'), so a search must parse text and breaks if the wording changes. A structured line has a named field (for example duration_ms=1431) that a tool can filter and compare directly. (3) Start with metrics to see whether latency or errors rose around 14:02 and for how many users; then use a trace of one slow request to see which step was slow; then read the logs of that component at that time for the cause.",
    levels={
        2: ("The answer defines all three signals, identifies the lines as logs, explains the parsing problem and the structured fix, and orders the three signals for the investigation.", [
            "A trace follows one request through the system, a metric is a measurement over time, a log records an event; these are logs. Searching for slow starts means parsing prose, which breaks when the wording changes; a field like duration_ms can be filtered. For the 14:02 complaint: metrics first (did latency rise, how widely), then a trace of a slow request to find the slow step, then the logs for that component for the reason.",
            "Traces: request path. Metrics: runtime measurements. Logs: event records, which is what we have here. Free text must be parsed; structured fields are queryable. Order: metrics, trace, logs."]),
        1: ("The answer defines the signals but not the investigation, or the reverse.", [
            "Logs, metrics and traces are the three signals and these are logs.",
            "Look at the logs at 14:02."]),
        0: ("The answer treats the signals as the same.", [
            "They are all just logs.",
            "Metrics are enough for everything."]),
    },
)

l12_l1_1 = Lesson("j12-l1.1", "Structured logs and the three signals", ["J12.01"], [
    ("o1", "Write structured log lines with typed fields"),
    ("o2", "Say what traces, metrics and logs are for, and plan an investigation using all three"),
], ["j8-l1.4", "j10-l2.1"], 40, ["I125", "I98"], """## Before you start

You should have used logging (Stage 4) and know what must never be logged (lesson 8.1.4).

## Explanation

Once a service is running in production you cannot attach a debugger. What you can do is **observe** it: ask questions about its behaviour from the data it emits. The OpenTelemetry project names three kinds of signal:

- **Traces**: the path of a request through your application.
- **Metrics**: a measurement captured at runtime.
- **Logs**: a recording of an event.

They answer different questions. Metrics tell you *that* something changed and how big it is (latency rose, errors rose). Traces tell you *where* in a request the time or the failure was. Logs tell you *why*, in the detail of one event.

For logs to be useful at scale they should be **structured**: one machine-readable record per event (commonly a JSON object) with named fields, rather than a sentence from which a person extracts numbers. A structured line is searchable and countable: you can filter by `account`, compare `ms` with a threshold, and group by `status`. Everything from lesson 8.1.4 still applies: never put secrets in the fields.

## Worked examples

### Example 1: free text and structured.

Free text: `Started AcademyApplication in 1.431 seconds`. Structured: `{"level":"INFO","message":"started","app":"academy","ms":1431}`.

### Example 2: this platform's own log.

The exercise shows the real startup lines of this platform's backend. They are useful to a person reading a terminal and awkward for a machine.

## Where this is used

- Every production service. A log pipeline, a metrics dashboard and a tracing tool together are what "observability" means in practice.

## Common mistakes

:::mistake{id=MC214}
**Treating logs, metrics and traces as interchangeable.** Each answers a different question. Counting errors by grepping logs is slow and costly; a metric does it directly.
:::

## Practice

::exercise{id=j12-l1.1-write-structured}

::exercise{id=j12-l1.1-explain-signals}

## Further reading

- **OpenTelemetry, signals** `[I125]`.
- **OWASP Logging Cheat Sheet** `[I98]`.

## How you'll be assessed

- The **write** exercise checks structured output (*implementation*).
- The **explain** exercise checks that you can use the three signals (*explanation*).

The one-line definitions of the signals are from the OpenTelemetry page; the idea of which signal answers which question (that, where, why) is common practice, not a quotation.
""")

# ====================================================================== j12-l1.2
def f_pct(values, p):
    if not values:
        return -1
    s = sorted(values)
    rank = max(1, math.ceil(p * len(s) / 100))
    return s[min(len(s), rank) - 1]


PCT_SOL = '''
int percentile(List<Integer> values, int p) {
    if (values.isEmpty()) {
        return -1;
    }
    List<Integer> sorted = new ArrayList<>(values);
    Collections.sort(sorted);
    int rank = Math.max(1, (int) Math.ceil(p * sorted.size() / 100.0));
    return sorted.get(Math.min(sorted.size(), rank) - 1);
}
'''
PCT_FLOOR = PCT_SOL.replace("(int) Math.ceil(p * sorted.size() / 100.0)", "p * sorted.size() / 100")
PCT_UNSORTED = PCT_SOL.replace("    Collections.sort(sorted);\n", "")
PCT_MEAN = '''
int percentile(List<Integer> values, int p) {
    if (values.isEmpty()) {
        return -1;
    }
    long sum = 0;
    for (int v : values) {
        sum += v;
    }
    return (int) (sum / values.size());
}
'''
PCT_NO_CLAMP = PCT_SOL.replace("    int rank = Math.max(1, (int) Math.ceil(p * sorted.size() / 100.0));\n    return sorted.get(Math.min(sorted.size(), rank) - 1);", "    int rank = (int) Math.ceil(p * sorted.size() / 100.0);\n    return sorted.get(rank - 1);")
LAT = [120, 118, 125, 130, 122, 119, 121, 124, 123, 4800]

ex12.method(
    "write", "j12-l1.2-write-percentile", "The slow tail", ["o1"], ["J12.02"], ["IMPL"],
    "Latency is better described by percentiles than by the average. Using the **nearest-rank** method, the p-th percentile of n values is the value at position `ceil(p * n / 100)` (counting from 1, at least 1) in the sorted list. Write `percentile(values, p)` for p from 0 to 100; an empty list gives -1.",
    [("percentile", [("values", "List<Integer>"), ("p", "int")], "int")], {"percentile": f_pct},
    [("percentile", (LAT, 50), "the median"), ("percentile", (LAT, 95), "the 95th percentile"), ("percentile", (LAT, 99), "the 99th percentile")],
    [("percentile", (LAT, 100), "the maximum"), ("percentile", (LAT, 0), "p0 is the minimum"), ("percentile", ([], 50), "no data"), ("percentile", ([7], 99), "one value"),
     ("percentile", ([5, 1, 4, 2, 3], 40), "five values at p40"), ("percentile", ([1, 2, 3, 4], 50), "even count, nearest rank"), ("percentile", (list(range(1, 101)), 95), "a hundred values"),
     ("percentile", ([10, 10, 10, 500], 75), "a tail value just outside p75")],
    starter='''
int percentile(List<Integer> values, int p) {
    return 0;
}
''', solution=PCT_SOL,
    wrongs={"rounds-down": PCT_FLOOR, "not-sorted": PCT_UNSORTED, "the-average": PCT_MEAN, "no-clamp-at-zero": PCT_NO_CLAMP},
    hints=["Sort a copy first.", "Use the ceiling of p times n over 100, and never go below the first position."],
    misconceptions=("MC215",), difficulty=3,
)


def f_budget(slo_permille, total, failed):
    allowed = total * (1000 - slo_permille) // 1000
    return allowed - failed


BUD_SOL = '''
long errorBudgetLeft(int sloPermille, long total, long failed) {
    long allowed = total * (1000 - sloPermille) / 1000;
    return allowed - failed;
}
'''
BUD_PCT = BUD_SOL.replace("total * (1000 - sloPermille) / 1000", "total * sloPermille / 1000")
BUD_ROUND = BUD_SOL.replace("total * (1000 - sloPermille) / 1000", "(total * (1000 - sloPermille) + 999) / 1000")
BUD_NO_SUB = BUD_SOL.replace("    return allowed - failed;", "    return allowed;")
BUD_INT = BUD_SOL.replace("long allowed = total * (1000 - sloPermille) / 1000;", "int allowed = (int) (total * (1000 - sloPermille)) / 1000;")

ex12.method(
    "write", "j12-l1.2-write-budget", "How much failure is allowed", ["o1"], ["J12.02"], ["IMPL"],
    "An SLO of 99.9 percent of requests succeeding gives an **error budget** of 0.1 percent: the failures you can afford. The SLO is given in permille (99.9 percent is 999, 99 percent is 990). Write `errorBudgetLeft(sloPermille, total, failed)`: the number of failures allowed, `total * (1000 - sloPermille) / 1000` rounded down, minus the failures so far. A negative result means the budget is spent.",
    [("errorBudgetLeft", [("sloPermille", "int"), ("total", "long"), ("failed", "long")], "long")], {"errorBudgetLeft": f_budget},
    [("errorBudgetLeft", (999, 1000000, 400), "a healthy month"), ("errorBudgetLeft", (999, 1000000, 1500), "overspent"), ("errorBudgetLeft", (990, 10000, 0), "nothing failed yet")],
    [("errorBudgetLeft", (999, 1999, 1), "rounds the allowance down"), ("errorBudgetLeft", (1000, 500000, 0), "a perfect SLO has no budget"), ("errorBudgetLeft", (999, 0, 0), "no traffic"),
     ("errorBudgetLeft", (999, 5000000000, 4000000), "large numbers need a long"), ("errorBudgetLeft", (950, 100, 5), "exactly spent"), ("errorBudgetLeft", (0, 1000, 1000), "an SLO of nothing")],
    starter='''
long errorBudgetLeft(int sloPermille, long total, long failed) {
    return 0;
}
''', solution=BUD_SOL,
    wrongs={"uses-the-slo-not-the-gap": BUD_PCT, "rounds-up": BUD_ROUND, "forgets-the-failures": BUD_NO_SUB, "int-overflow": BUD_INT},
    hints=["The budget is the share of requests that may fail.", "Do the multiplication as long values."],
    misconceptions=("MC215",), difficulty=3,
)

ex12.explain(
    "j12-l1.2-explain-slo", "Choosing the measure", ["o2"], ["J12.02"],
    "Over a minute, 10 requests took 120, 118, 125, 130, 122, 119, 121, 124, 123 and 4800 milliseconds. Compute the average and the 95th percentile (nearest rank), and say what each tells a team. Then explain what an SLI, an SLO and an error budget are, using the definitions in the SRE book, write one SLO for Brightbank's transfer endpoint, and say what a team should do when the budget is nearly spent.",
    "The average is (120+118+125+130+122+119+121+124+123+4800)/10 = 590.2 ms, a number that no request actually experienced, because one slow outlier drags it up. The 95th percentile by nearest rank is the 10th value of the sorted list, 4800 ms, which shows the slow tail a real user hit; percentiles describe what users experience at the slow end. An SLI is a carefully defined quantitative measure of the level of service (latency, error rate, throughput); an SLO is a target for that measure (SLI <= target); the error budget is the amount of failure the SLO allows. An example SLO: 99.9 percent of POST /transfers requests succeed, and 99 percent complete within 500 ms, measured over 30 days. When the budget is nearly spent the team slows risky releases and spends effort on reliability until it recovers.",
    levels={
        2: ("The answer computes both numbers, interprets them, defines SLI/SLO/budget, gives a concrete SLO and says what to do as the budget runs out.", [
            "The average is 590.2 ms but nobody saw that; the p95 (10th of 10 values) is 4800 ms, which exposes the slow tail. An SLI is a measure such as latency or error rate, an SLO is a target for it, and the error budget is how much failure the SLO permits. For transfers: 99.9 percent succeed and 99 percent finish within 500 ms over 30 days. When the budget is nearly gone we slow releases and fix reliability first.",
            "Average 590.2 ms hides the problem; p95 is 4800 ms. SLI: what you measure. SLO: the target. Error budget: allowed failures. Example: 99.9% of transfers succeed over 30 days. If the budget is nearly spent, pause risky changes and work on stability."]),
        1: ("The answer computes the numbers or defines the terms but not both.", [
            "The p95 is 4800 and the average is 590.",
            "An SLO is a target for an SLI."]),
        0: ("The answer prefers the average or confuses the terms.", [
            "The average is the fairest number for users.",
            "An SLA, SLO and SLI are the same."]),
    },
)

l12_l1_2 = Lesson("j12-l1.2", "SLIs, SLOs and percentiles", ["J12.02"], [
    ("o1", "Compute a percentile and an error budget"),
    ("o2", "Explain why percentiles beat averages, and define an SLO with its budget"),
], ["j12-l1.1"], 40, ["I124"], """## Before you start

You should know what a median is (lesson 9.3.2) and what a status code means (Stage 7).

## Explanation

"Is the service healthy?" needs a precise answer. The SRE book gives the vocabulary.

An **SLI** (service level indicator) is a carefully defined quantitative measure of some aspect of the level of service provided: request latency, error rate (often a fraction of all requests) and throughput are the common ones. An **SLO** (service level objective) is a target value or range of values for a service level, measured by an SLI; a natural form is SLI ≤ target, or a lower bound ≤ SLI ≤ an upper bound. An example: "99.9 percent of requests succeed" or "the 99th percentile of latency is below 500 ms".

Averages are a poor SLI for latency. A single slow request can drag the average up to a value that **no request actually experienced**, and a mostly fast service can hide a slow tail in a good average. **Percentiles** describe the tail: the p95 is the value 95 percent of the requests were at or below. With the nearest-rank method used here, the p-th percentile of n sorted values is the value at position ceil(p × n / 100).

An SLO implies an **error budget**: the failure it allows. At 99.9 percent, 1 request in 1,000 may fail. The budget turns reliability into a number a team can spend: while there is budget, ship; when it is nearly spent, slow down risky changes and invest in reliability.

## Worked examples

### Example 1: the slow tail.

Ten latencies of about 120 ms and one of 4,800 ms: the average is 590.2 ms, a number nobody experienced; the p95 is 4,800 ms.

### Example 2: a budget.

At 99.9 percent over 1,000,000 requests the allowance is 1,000 failures. With 400 so far, 600 are left.

## Where this is used

- Dashboards, alerts and release decisions. Alert on a symptom that threatens an SLO, not on every blip.

## Common mistakes

:::mistake{id=MC215}
**Reporting average latency.** It is easy to compute and describes almost nobody. Report percentiles, and say which.
:::

## Practice

::exercise{id=j12-l1.2-write-percentile}

::exercise{id=j12-l1.2-write-budget}

::exercise{id=j12-l1.2-explain-slo}

## Further reading

- **Site Reliability Engineering, Service Level Objectives** `[I124]`.

## How you'll be assessed

- The **write** exercises check the two calculations (*implementation*).
- The **explain** exercise checks the argument and an SLO of your own (*explanation*).

The error-budget idea and the nearest-rank formula are standard; the definitions of SLI and SLO are from the cited chapter, while "error budget" is used here as common practice without a quotation.
""")

# ====================================================================== j12-l1.3
def f_self(spans):
    rows = {}
    order = []
    for s in spans:
        sid, parent, start, end = s.split(":")
        rows[sid] = (parent, int(end) - int(start))
        order.append(sid)
    kids = {}
    for sid, (parent, d) in rows.items():
        kids[parent] = kids.get(parent, 0) + d
    return [f"{sid}={rows[sid][1] - kids.get(sid, 0)}" for sid in order]


SELF_SOL = '''
List<String> selfTimes(List<String> spans) {
    Map<String, Integer> duration = new LinkedHashMap<>();
    Map<String, Integer> childTotal = new HashMap<>();
    for (String span : spans) {
        String[] p = span.split(":");
        int length = Integer.parseInt(p[3]) - Integer.parseInt(p[2]);
        duration.put(p[0], length);
        childTotal.merge(p[1], length, Integer::sum);
    }
    List<String> out = new ArrayList<>();
    for (Map.Entry<String, Integer> entry : duration.entrySet()) {
        out.add(entry.getKey() + "=" + (entry.getValue() - childTotal.getOrDefault(entry.getKey(), 0)));
    }
    return out;
}
'''
SELF_TOTAL = SELF_SOL.replace("(entry.getValue() - childTotal.getOrDefault(entry.getKey(), 0))", "entry.getValue()")
SELF_FIRST_CHILD = SELF_SOL.replace("childTotal.merge(p[1], length, Integer::sum);", "childTotal.putIfAbsent(p[1], length);")
SELF_SORTED = SELF_SOL.replace("new LinkedHashMap<>()", "new TreeMap<>()")
SELF_ABS = SELF_SOL.replace('(entry.getValue() - childTotal.getOrDefault(entry.getKey(), 0))', 'Math.abs(entry.getValue() - childTotal.getOrDefault(entry.getKey(), 0))')
TRACE = ["root:-:0:1000", "auth:root:10:60", "transfer:root:60:960", "debit:transfer:70:130", "credit:transfer:140:900", "notify:transfer:905:950"]

ex13.method(
    "write", "j12-l1.3-write-self-times", "Where did the time go", ["o1"], ["J12.03"], ["IMPL"],
    "A trace is a tree of **spans**. Each is `id:parent:start:end` in milliseconds (the root's parent is `-`). A span's **self time** is its duration minus the total duration of its direct children (the time spent in the span itself, not waiting for children; children never overlap in these traces). Write `selfTimes(spans)` returning `id=self` for each span, in the order given.",
    [("selfTimes", [("spans", "List<String>")], "List<String>")], {"selfTimes": f_self},
    [("selfTimes", (TRACE,), "a transfer request"), ("selfTimes", (["only:-:5:15"],), "a single span"), ("selfTimes", (["a:-:0:100", "b:a:10:60"],), "one child")],
    [("selfTimes", (["a:-:0:100", "b:a:0:30", "c:a:30:100"],), "children fill the parent"), ("selfTimes", (["r:-:0:10", "x:r:0:0"],), "a zero-length child"), ("selfTimes", ([],), "no spans"),
     ("selfTimes", (["a:-:0:100", "b:a:10:50", "c:b:20:40"],), "three levels"), ("selfTimes", (["leaf:p:5:9", "p:-:0:20"],), "a child listed before its parent"), ("selfTimes", (["r:-:0:100", "a:r:0:10", "b:r:10:20", "c:r:20:30", "d:r:30:40"],), "four children")],
    starter='''
List<String> selfTimes(List<String> spans) {
    return List.of();
}
''', solution=SELF_SOL,
    wrongs={"reports-total-time": SELF_TOTAL, "only-the-first-child": SELF_FIRST_CHILD, "sorted-by-id": SELF_SORTED},
    hints=["Add up the durations of the spans that name each span as their parent.", "A span may appear before its parent in the list."],
    misconceptions=("MC216",), difficulty=3,
)

ex13.explain(
    "j12-l1.3-explain-trace", "Reading a trace", ["o2"], ["J12.03"],
    "This is a trace for one slow `POST /transfers` request. It is a constructed teaching example (not captured from a real system); times are in milliseconds from the start of the request.\n\n" + fence("\n".join(TRACE)) + "\n\nUsing self times, say where the time went, which span you would investigate first and why the root span's duration alone would not tell you that. What would you ask next about that span, and which other signal would you consult?",
    "The root takes 1000 ms. Its direct child 'transfer' takes 900 ms and 'auth' 50 ms, so the root's own time is 50 ms. Within 'transfer' (900 ms) the children are debit 60, credit 760 and notify 45, which leaves 35 ms of its own. The self time of 'credit' is 760 ms (it has no children in the trace), so most of the request is spent inside the credit step itself, not in a deeper call. The root's duration shows only that the request was slow; self times show where. Next I would ask what the credit step is doing for 760 ms (a remote call, a slow query, a lock), look at that component's metrics (latency, connections in use) and its logs for the same time and request id.",
    levels={
        2: ("The answer computes self times, identifies credit (760 ms) as the place, explains the limits of the root duration, and names follow-up questions and signals.", [
            "Root self time is 50, transfer 35, auth 50, debit 60, notify 45 and credit 760. The credit span has 760 ms of its own, so I would investigate that first. The root duration (1000 ms) only says the request was slow; it does not say where. I would ask what credit is waiting for (remote call, query, lock) and check its metrics and logs for the same time and request id.",
            "The time is in credit: 760 ms self time out of 1000. Root duration cannot show that because it includes all its children. Next: what is credit doing, with the metrics for its dependency and the logs for that request."]),
        1: ("The answer finds credit as slow without self-time reasoning or follow-up.", [
            "The credit span is the slowest.",
            "Look at the logs."]),
        0: ("The answer blames the root or auth.", [
            "The root span is slow so the problem is in the root.",
            "Auth is first so it must be the cause."]),
    },
)

l12_l1_3 = Lesson("j12-l1.3", "Tracing", ["J12.03"], [
    ("o1", "Compute self times from a trace's spans"),
    ("o2", "Use a trace to decide where to investigate a slow request"),
], ["j12-l1.1"], 35, ["I125"], """## Before you start

You should know the three signals (lesson 12.1.1).

## Explanation

A **trace** is the path of a request through your application (and, in a distributed system, across services). It is made of **spans**: one per unit of work, such as an incoming request, a database call or a call to another service. Each span has a start, an end and a parent, so a trace is a tree.

The question a trace answers is *where*. A span's duration includes all the work of its children, so the root span's duration only says that the request was slow. What you need is each span's **self time**: its duration minus the time spent in its children. The span with the largest self time is where the time is spent.

To tie the three signals together, the trace identifier is put on the log lines of the request, so that from a slow trace you can open the logs of exactly that request, and from a metric that rose you can find example traces.

## Worked examples

### Example 1: the exercise trace.

The request takes 1000 ms, the transfer span 900 ms, but the credit span, with no children of its own, has 760 ms self time: the investigation starts there.

### Example 2: this platform.

It has no tracing. Adding it is a library and configuration job, which this course does not cover.

## Where this is used

- Any system where a request crosses several components. Tracing tools draw the tree and highlight self time for you.

## Common mistakes

:::mistake{id=MC216}
**Reading the root span's duration as the diagnosis.** It includes everything below it. Look for the span with large self time.
:::

## Practice

::exercise{id=j12-l1.3-write-self-times}

::exercise{id=j12-l1.3-explain-trace}

## Further reading

- **OpenTelemetry, signals** `[I125]`.

## How you'll be assessed

- The **write** exercise checks self-time arithmetic (*implementation*).
- The **explain** exercise checks that you can read a trace (*explanation*).

The trace is a constructed teaching example. No tracing tool was run for this course, and the advice to put the trace id on log lines is common practice without a recorded source.
""")

# ====================================================================== j12-l1.4
def f_breach(series, threshold, minutes):
    run = 0
    for i, v in enumerate(series):
        run = run + 1 if v > threshold else 0
        if run >= minutes:
            return i - minutes + 1
    return -1


BREACH_SOL = '''
int firstBreach(List<Integer> series, int threshold, int minutes) {
    int run = 0;
    for (int i = 0; i < series.size(); i++) {
        run = series.get(i) > threshold ? run + 1 : 0;
        if (run >= minutes) {
            return i - minutes + 1;
        }
    }
    return -1;
}
'''
BREACH_AT_LEAST = BREACH_SOL.replace("series.get(i) > threshold", "series.get(i) >= threshold")
BREACH_NO_RESET = BREACH_SOL.replace("run = series.get(i) > threshold ? run + 1 : 0;", "run = series.get(i) > threshold ? run + 1 : run;")
BREACH_END = BREACH_SOL.replace("return i - minutes + 1;", "return i;")
BREACH_FIRST = BREACH_SOL.replace("        if (run >= minutes) {", "        if (series.get(i) > threshold) {")
CONN = [3, 3, 4, 6, 9, 10, 10, 10]
P95 = [120, 118, 125, 300, 900, 4800, 6200, 7000]

ex14.method(
    "write", "j12-l1.4-write-breach", "When did it start", ["o1"], ["J12.04"], ["IMPL", "DEBUG"],
    "An alert should fire when a metric is **above** a threshold for several samples in a row, not on one blip. Samples are one per minute. Write `firstBreach(series, threshold, minutes)`: the index (from 0) of the first sample of the first run of at least `minutes` consecutive samples **strictly above** the threshold, or -1 if there is none.",
    [("firstBreach", [("series", "List<Integer>"), ("threshold", "int"), ("minutes", "int")], "int")], {"firstBreach": f_breach},
    [("firstBreach", (CONN, 8, 3), "connections in use"), ("firstBreach", (P95, 1000, 2), "p95 latency"), ("firstBreach", ([1, 2, 3], 10, 1), "never above")],
    [("firstBreach", ([9, 1, 9, 9, 9], 5, 3), "an earlier blip does not count"), ("firstBreach", ([5, 5, 5], 5, 1), "equal is not above"), ("firstBreach", ([6, 6], 5, 3), "too short"),
     ("firstBreach", ([], 5, 1), "no samples"), ("firstBreach", ([9, 9, 1, 9, 9, 9], 5, 3), "the run is broken then restarts"), ("firstBreach", ([9], 5, 1), "a single sample"),
     ("firstBreach", ([1, 9, 9, 9, 9], 5, 2), "a longer run starts at its first sample")],
    starter='''
int firstBreach(List<Integer> series, int threshold, int minutes) {
    return -1;
}
''', solution=BREACH_SOL,
    wrongs={"at-or-above": BREACH_AT_LEAST, "run-is-not-reset": BREACH_NO_RESET, "reports-the-end": BREACH_END, "fires-on-a-blip": BREACH_FIRST},
    hints=["Count the current run, and reset it when a sample is not above the threshold.", "Report where the run started, not where it was detected."],
    misconceptions=("MC217",), difficulty=3,
)

INCIDENT = """CONSTRUCTED TEACHING FIXTURE (not captured from a real system)

Timeline: v2 of the accounts service was deployed at minute 3.
minute  connections_in_use(max 10)  p95_ms  error_rate_%
0       3                           120     0
1       3                           118     0
2       4                           125     0
3       6                           300     1
4       9                           900     3
5       10                          4800    22
6       10                          6200    41
7       10                          7000    47

Log excerpts (wording invented for practice):
12:03 INFO  deploy complete version=v2
12:04 WARN  slow query ms=2100 sql="SELECT * FROM transactions WHERE account_id = ?" rows=48211
12:05 ERROR connection not available pool=main timeout_ms=30000
12:06 ERROR connection not available pool=main timeout_ms=30000
12:07 ERROR connection not available pool=main timeout_ms=30000"""
ex14.explain(
    "j12-l1.4-explain-incident", "Diagnose and respond", ["o2"], ["J12.04"],
    "Read the fixture below (it is a constructed teaching example) and write a short incident note.\n\n" + fence(INCIDENT) + "\n\nInclude: (1) the minute the problem started and how you know; (2) the most likely chain of causes, from the change to the user-visible errors; (3) what you would do **first** to stop the harm, and why that comes before fixing the code; (4) the follow-up fix; (5) one thing to add so that you find out sooner next time.",
    "(1) The deploy at minute 3 coincides with the first change: connections in use start rising at minute 3 (6) and p95 begins to climb (300 ms), reaching the maximum of 10 connections at minute 5, when errors jump to 22 percent. (2) v2 runs a slow query (2100 ms, scanning 48,211 rows, probably without a useful index on account_id); each slow query holds a database connection for seconds, so the pool of 10 is used up; new requests cannot get a connection, wait until the timeout and fail, so latency and errors rise together. (3) First roll back to v1, because users are being harmed now and a rollback is quick and known; finding the cause with the system down is slower and riskier. (4) Then fix the query (an index on account_id or a better query), test it with realistic data volume, and release it with a smoke test. (5) Add an alert on connection-pool usage (for example above 80 percent for 3 minutes) or on p95 latency, and a slow-query log or test, so the problem is seen at minute 3 or 4, not after users complain.",
    levels={
        2: ("The answer dates the start, gives a coherent cause chain, mitigates first by rollback, names the real fix and an earlier alert.", [
            "Started at minute 3 with the v2 deploy: connections and p95 begin to rise. v2's slow query (2.1 s over 48k rows) holds connections; the pool of 10 fills by minute 5, new requests time out and error. First action: roll back to v1 to stop users being hurt, since that is quick and certain. Then fix the query (index on account_id), test at realistic volume and redeploy. Add an alert on pool usage or p95 so it is caught at minute 3-4.",
            "The change was the v2 deploy at minute 3. Slow SQL ties up connections until the pool hits 10/10, then requests fail waiting for a connection. Mitigate with a rollback first, then fix the query/index and test with realistic data. Alert on pool saturation and latency."]),
        1: ("The answer finds the cause but starts by fixing code, or has no alert.", [
            "The slow query in v2 used up the connection pool. Fix the query.",
            "Roll back."]),
        0: ("The answer blames the wrong thing.", [
            "The database is too small, so add more connections and restart.",
            "Users are making too many requests."]),
    },
)

l12_l1_4 = Lesson("j12-l1.4", "Reading an incident", ["J12.04"], [
    ("o1", "Find when a metric first stayed above its threshold"),
    ("o2", "Diagnose a constructed incident from metrics and logs and respond in the right order"),
], ["j12-l1.2", "j9-l3.3"], 45, ["I124", "I125"], """## Before you start

You should know the three signals and what an SLO is (lessons 12.1.1 and 12.1.2), and how a connection pool runs out (Stage 6).

## Explanation

An **incident** is an event that harms users or threatens an SLO. Two skills matter, and they are different.

**Mitigation** stops the harm: roll back the last change, switch off a feature flag, add capacity, fail over. **Diagnosis** finds the cause so it can be fixed properly. The order is almost always mitigate first: users are being hurt now, a rollback is quick and known, and a diagnosis done under pressure on a failing system is slow and risky. Fix the code afterwards, with a test.

Diagnosis works like this:

1. **What changed?** Compare the timeline of the metrics with deployments, configuration changes and traffic. A deploy a minute before the first symptom is the first suspect.
2. **Where is the pressure?** Utilisation metrics (connections in use, CPU, memory, queue lengths) show a resource that is full; latency and error metrics show the consequence.
3. **What do the logs say?** Read the log lines of the affected component for the same minutes; they supply the reason that the metrics only hint at.
4. **Form one explanation, test it** (a trace, a query plan, a thread dump from Stage 9), then act.

Afterwards write a **post-incident review**: a blameless account of the timeline, the cause, what went well and badly, and the follow-up actions with owners. The review's purpose is to improve the system and the process, not to find someone to blame.

## Worked examples

### Example 1: the exercise incident.

A deploy at minute 3; connections in use climb to the maximum by minute 5; p95 and errors follow. Logs show a slow query and "connection not available". Rollback first; fix the query; add an alert.

### Example 2: when did it start.

A series `[3,3,4,6,9,10,10,10]` with threshold 8 for 3 minutes first breaches at index 4 (minute 4, the first of the run 9, 10, 10... starting at the sample above 8).

## Where this is used

- On-call work. The practice is to rehearse: seeded incidents with only logs and metrics available are the best training.

## Common mistakes

:::mistake{id=MC217}
**Starting with the root cause while users are failing.** Stop the harm first, by the quickest safe means, then find the cause with the pressure off.
:::

## Practice

::exercise{id=j12-l1.4-write-breach}

::exercise{id=j12-l1.4-explain-incident}

## Further reading

- **Site Reliability Engineering, Service Level Objectives** `[I124]`.
- **OpenTelemetry, signals** `[I125]`.

## How you'll be assessed

- The **write** exercise checks alert logic (*implementation, debugging*).
- The **explain** exercise checks your diagnosis and response (*explanation*).

The incident is a constructed teaching fixture, labelled as such; its numbers and log wording were invented for practice and are not from any real system. The advice on the order of mitigation and diagnosis is widely accepted practice without a recorded source.
""")
print("module 12.1 authored")
