"""Stage 10 authoring: module 10.2 (Distributed systems fundamentals). Plain-Java models; expectations from Python."""
import l10common
from l10common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex21 = Exercises("j10-l2.1")
ex22 = Exercises("j10-l2.2")
ex23 = Exercises("j10-l2.3")
ex24 = Exercises("j10-l2.4")

REGISTER = {
    "j10-l2.1": ("Timeouts, retries and backoff", ["J10.04"]),
    "j10-l2.2": ("Idempotency keys", ["J10.05"]),
    "j10-l2.3": ("Sagas, outbox and delivery guarantees", ["J10.06"]),
    "j10-l2.4": ("Circuit breakers and resilience", ["J10.07"]),
}
MISCS = {
    "MC201": (["J10.04"], "I120", "If a remote call times out, it did not happen, so retrying immediately and without limit is safe"),
    "MC202": (["J10.05"], "I120", "A retried request is harmless as long as the server returns an error to the second copy"),
    "MC203": (["J10.06"], "I121", "A transaction across two services can simply be wrapped in one database transaction"),
    "MC204": (["J10.07"], "I123", "A circuit breaker makes a failing dependency work again; it only hides failures"),
}
register(REGISTER, MISCS)

# ====================================================================== j10-l2.1
def f_backoff(attempts, base, cap_):
    return [min(cap_, base * 2 ** i) for i in range(attempts)]


BACKOFF_SOL = '''
List<Long> backoffDelays(int attempts, long baseMs, long capMs) {
    List<Long> delays = new ArrayList<>();
    long delay = Math.min(capMs, baseMs);
    for (int i = 0; i < attempts; i++) {
        delays.add(delay);
        delay = Math.min(capMs, delay * 2);
    }
    return delays;
}
'''
BACKOFF_NOCAP = BACKOFF_SOL.replace("Math.min(capMs, delay * 2)", "delay * 2")
BACKOFF_LINEAR = BACKOFF_SOL.replace("delay = Math.min(capMs, delay * 2);", "delay = Math.min(capMs, delay + baseMs);")
BACKOFF_FIRST = BACKOFF_SOL.replace("long delay = Math.min(capMs, baseMs);", "long delay = Math.min(capMs, baseMs * 2);")
BACKOFF_OVERFLOW = '''
List<Long> backoffDelays(int attempts, long baseMs, long capMs) {
    List<Long> delays = new ArrayList<>();
    for (int i = 0; i < attempts; i++) {
        delays.add(Math.min(capMs, baseMs * (1 << i)));
    }
    return delays;
}
'''

ex21.method(
    "write", "j10-l2.1-write-backoff", "Waiting longer each time", ["o1"], ["J10.04"], ["IMPL"],
    "A client that retries a failed call should wait longer between attempts, so a struggling server is not hammered. Exponential backoff doubles the wait each time, up to a cap. Write `backoffDelays(attempts, baseMs, capMs)`: the wait before each retry, in milliseconds. The first wait is `baseMs` (but never more than `capMs`), each next one is twice the previous, never more than `capMs`. `attempts` can be large, so take care that nothing overflows.",
    [("backoffDelays", [("attempts", "int"), ("baseMs", "long"), ("capMs", "long")], "List<Long>")], {"backoffDelays": f_backoff},
    [("backoffDelays", (5, 100, 10000), "five doublings"), ("backoffDelays", (4, 500, 1000), "the cap is reached"), ("backoffDelays", (0, 100, 1000), "no attempts")],
    [("backoffDelays", (3, 2000, 1000), "the base is above the cap"), ("backoffDelays", (70, 100, 5000), "many attempts do not overflow"), ("backoffDelays", (1, 250, 10000), "one attempt"),
     ("backoffDelays", (6, 1, 1000000), "small base"), ("backoffDelays", (8, 100, 100), "base equals cap"), ("backoffDelays", (40, 1000, 3000000000), "a large cap")],
    starter='''
List<Long> backoffDelays(int attempts, long baseMs, long capMs) {
    return List.of();
}
''', solution=BACKOFF_SOL,
    wrongs={"no-cap-on-later-waits": BACKOFF_NOCAP, "linear-not-exponential": BACKOFF_LINEAR, "starts-too-late": BACKOFF_FIRST, "shift-overflow": BACKOFF_OVERFLOW},
    hints=["Double the previous wait, then apply the cap.", "`1 << i` overflows for large i."],
    misconceptions=("MC201",), difficulty=3,
)


def f_retry(outcomes, max_attempts):
    for i in range(max_attempts):
        if i < len(outcomes) and outcomes[i] == "ok":
            return f"ok@{i + 1}"
    return f"failed@{max_attempts}"


RETRY_SOL = '''
String callWithRetries(List<String> outcomes, int maxAttempts) {
    for (int attempt = 1; attempt <= maxAttempts; attempt++) {
        String outcome = attempt <= outcomes.size() ? outcomes.get(attempt - 1) : "fail";
        if (outcome.equals("ok")) {
            return "ok@" + attempt;
        }
    }
    return "failed@" + maxAttempts;
}
'''
RETRY_OFFBYONE = RETRY_SOL.replace("attempt <= maxAttempts", "attempt < maxAttempts")
RETRY_ZERO_BASED = RETRY_SOL.replace('return "ok@" + attempt;', 'return "ok@" + (attempt - 1);')
RETRY_FOREVER = RETRY_SOL.replace('return "failed@" + maxAttempts;', 'return "failed@" + outcomes.size();')
RETRY_MISSING_OK = RETRY_SOL.replace('outcomes.get(attempt - 1) : "fail"', 'outcomes.get(attempt - 1) : "ok"')

ex21.method(
    "write", "j10-l2.1-write-retries", "Give up at some point", ["o1"], ["J10.04"], ["IMPL"],
    "`outcomes` lists what each attempt of a call would do (`ok` or `fail`); attempts beyond the list always fail. Write `callWithRetries(outcomes, maxAttempts)`: try up to `maxAttempts` times and stop at the first `ok`. Return `ok@N` with the attempt number N (counting from 1), or `failed@M` where M is `maxAttempts`.",
    [("callWithRetries", [("outcomes", "List<String>"), ("maxAttempts", "int")], "String")], {"callWithRetries": f_retry},
    [("callWithRetries", (["fail", "fail", "ok"], 5), "succeeds on the third try"), ("callWithRetries", (["fail", "fail", "fail"], 3), "gives up"), ("callWithRetries", (["ok"], 1), "first time")],
    [("callWithRetries", (["fail", "fail", "ok"], 2), "success would come one attempt too late"), ("callWithRetries", ([], 4), "no outcomes always fail"), ("callWithRetries", (["fail", "ok"], 0), "no attempts allowed"),
     ("callWithRetries", (["fail"], 3), "attempts past the list fail"), ("callWithRetries", (["ok", "fail"], 5), "stops at the first success"), ("callWithRetries", (["fail", "fail", "fail", "fail", "ok"], 5), "last allowed attempt")],
    starter='''
String callWithRetries(List<String> outcomes, int maxAttempts) {
    return "";
}
''', solution=RETRY_SOL,
    wrongs={"one-attempt-short": RETRY_OFFBYONE, "zero-based-number": RETRY_ZERO_BASED, "reports-the-wrong-count": RETRY_FOREVER, "missing-outcomes-succeed": RETRY_MISSING_OK},
    hints=["Count attempts from 1.", "What happens past the end of the list?"],
    misconceptions=("MC201",), difficulty=2,
)

ex21.explain(
    "j10-l2.1-explain-retries", "What a timeout does not tell you", ["o2"], ["J10.04"],
    "A payments client sends `POST /payments` and its 2-second timeout expires. Explain what the client does and does not know, why 'just retry' can be harmful, why retries without a limit or backoff can turn a small outage into a big one, and what you would set as the retry policy.",
    "A timeout means no answer arrived in time; the request may have been lost before arriving, may be still running, or may have completed with only the answer lost, so the client cannot tell whether the payment happened. A blind retry of a non-idempotent call can charge twice (Stage 7). If many clients retry at once without limit or delay, they multiply the load on a server that is already struggling and keep it down. A sound policy bounds the number of attempts, waits with exponential backoff (usually with some randomness so clients do not retry in step), retries only calls that are safe to repeat or carry an idempotency key, and has a deadline overall.",
    levels={
        2: ("The answer separates 'no answer' from 'did not happen', warns about duplicate effects and retry storms, and gives a bounded policy with idempotency.", [
            "A timeout only says no reply came in time; the payment may have happened and the reply been lost, so the client does not know. Retrying a non-idempotent POST could charge twice. Unbounded immediate retries from many clients multiply the load and keep the server down. I would limit attempts, back off exponentially with jitter, set an overall deadline and send an idempotency key so repeating is safe.",
            "The client knows nothing about whether it was applied. Blind retry risks a double payment, and a crowd of retrying clients is a retry storm. Policy: a few attempts, exponential backoff, a deadline, and an idempotency key on the payment."]),
        1: ("The answer gives some of the risks or a policy without the reasons.", [
            "The payment might have gone through, so retrying could double charge.",
            "Retry three times with a delay."]),
        0: ("The answer treats a timeout as a failure to apply.", [
            "The payment did not happen because it timed out, so retry as fast as possible until it works.",
            "Increase the timeout to ten minutes."]),
    },
)

l10_l2_1 = Lesson("j10-l2.1", "Timeouts, retries and backoff", ["J10.04"], [
    ("o1", "Compute backoff delays and a bounded retry loop"),
    ("o2", "Explain what a timeout does and does not tell a client, and design a retry policy"),
], ["j7-l1.2", "j7-l1.3"], 40, ["I120", "I84"], """## Before you start

You should know idempotent methods and status codes (Stage 7).

## Explanation

Inside one process a call either returns or throws. Between machines there is a third outcome: **nothing comes back**. The request may never have arrived, the server may be slow, or it may have done the work and the reply was lost. A **timeout** only says you stopped waiting. The client cannot know which of those happened.

That is why retrying is dangerous for operations that are not idempotent (lesson 7.1.2): if the first attempt did take effect, the second may do the work twice. And retrying carelessly can make an outage worse: if a thousand clients immediately retry a struggling server, the retries are extra load that keeps it down (a *retry storm*).

A sound retry policy therefore has these parts:

- **A limit** on attempts, and an overall **deadline**.
- **Backoff**: wait longer between attempts, commonly by doubling up to a cap (**exponential backoff**), usually with some randomness (**jitter**) so clients do not retry in step.
- **Safety**: retry only calls that are safe to repeat, or that carry an idempotency key (next lesson).

## Worked examples

### Example 1: backoff.

Base 100 ms, cap 10 000 ms: waits of 100, 200, 400, 800, 1600 ms. With a cap of 1 000 ms and base 500: 500, 1000, 1000, 1000.

### Example 2: giving up.

Outcomes `fail, fail, ok` with at most 2 attempts gives `failed@2`: the success would have come one attempt too late.

## Where this is used

- Every client of a network service: HTTP clients, database drivers, message consumers. Most libraries have these settings; the defaults are rarely right for your case.

## Common mistakes

:::mistake{id=MC201}
**Treating a timeout as proof that nothing happened.** It proves only that you stopped waiting. Retrying a non-idempotent call without protection can repeat its effect.
:::

## Practice

::exercise{id=j10-l2.1-write-backoff}

::exercise{id=j10-l2.1-write-retries}

::exercise{id=j10-l2.1-explain-retries}

## Further reading

- **RFC 9110, HTTP Semantics** `[I84]`, on idempotent methods.
- **Idempotency-Key header (Internet-Draft)** `[I120]`, on making a retry safe.

## How you'll be assessed

- The **write** exercises check backoff and the retry loop (*implementation*).
- The **explain** exercise checks that you can design a policy (*explanation*).

Jitter and the term "retry storm" are standard practice and are not taken from a recorded source in this course.
""")

# ====================================================================== j10-l2.2
START = {"a": 1000, "b": 1000, "c": 1000}


def f_apply(requests):
    bal = dict(START)
    seen = {}
    out = []
    for r in requests:
        key, frm, to, cents = r.split(":")
        body = (frm, to, int(cents))
        if key in seen:
            old_body, old_result = seen[key]
            out.append("conflict" if old_body != body else "dup:" + old_result)
            continue
        if frm not in bal or to not in bal or frm == to or body[2] <= 0:
            out.append("invalid")
            continue
        if bal[frm] < body[2]:
            seen[key] = (body, "rejected")
            out.append("rejected")
            continue
        bal[frm] -= body[2]
        bal[to] += body[2]
        seen[key] = (body, "applied")
        out.append("applied")
    out.append(f"a={bal['a']};b={bal['b']};c={bal['c']}")
    return out


APPLY_SOL = '''
List<String> processTransfers(List<String> requests) {
    Map<String, Integer> balance = new TreeMap<>(Map.of("a", 1000, "b", 1000, "c", 1000));
    Map<String, String[]> seen = new HashMap<>();
    List<String> results = new ArrayList<>();
    for (String request : requests) {
        String[] p = request.split(":");
        String key = p[0];
        String body = p[1] + ">" + p[2] + ":" + Integer.parseInt(p[3]);
        int cents = Integer.parseInt(p[3]);
        if (seen.containsKey(key)) {
            String[] old = seen.get(key);
            results.add(old[0].equals(body) ? "dup:" + old[1] : "conflict");
            continue;
        }
        if (!balance.containsKey(p[1]) || !balance.containsKey(p[2]) || p[1].equals(p[2]) || cents <= 0) {
            results.add("invalid");
            continue;
        }
        if (balance.get(p[1]) < cents) {
            seen.put(key, new String[] {body, "rejected"});
            results.add("rejected");
            continue;
        }
        balance.merge(p[1], -cents, Integer::sum);
        balance.merge(p[2], cents, Integer::sum);
        seen.put(key, new String[] {body, "applied"});
        results.add("applied");
    }
    results.add("a=" + balance.get("a") + ";b=" + balance.get("b") + ";c=" + balance.get("c"));
    return results;
}
'''
APPLY_NOKEYS = APPLY_SOL.replace("        if (seen.containsKey(key)) {", "        if (false) {")
APPLY_NO_CONFLICT = APPLY_SOL.replace('old[0].equals(body) ? "dup:" + old[1] : "conflict"', '"dup:" + old[1]')
APPLY_FORGET_REJECT = APPLY_SOL.replace('            seen.put(key, new String[] {body, "rejected"});\n', "")
APPLY_RECORD_INVALID = APPLY_SOL.replace('            results.add("invalid");', '            seen.put(key, new String[] {body, "invalid"});\n            results.add("invalid");')
APPLY_KEY_PER_ACCOUNT = APPLY_SOL.replace('seen.containsKey(key)', 'seen.containsKey(key + p[1])').replace('seen.get(key)', 'seen.get(key + p[1])').replace('seen.put(key, ', 'seen.put(key + p[1], ')

ex22.method(
    "write", "j10-l2.2-write-idempotent", "Apply each request once", ["o1"], ["J10.05"], ["IMPL", "DEBUG"],
    "Accounts a, b and c start with 1000 each. A request is `key:from:to:cents`. Process them in order. A key seen before with the **same** from, to and cents is a duplicate: answer `dup:` followed by the result of the first time, and change nothing. A key seen before with a different body is `conflict`. A new request for an unknown or identical account, or with `cents` zero or less, is `invalid` (and its key is not remembered). If `from` lacks the money the result is `rejected` (the key *is* remembered). Otherwise move the money: `applied`. Return one result per request, then a final element with the balances as `a=..;b=..;c=..`.",
    [("processTransfers", [("requests", "List<String>")], "List<String>")], {"processTransfers": f_apply},
    [("processTransfers", (["k1:a:b:100", "k1:a:b:100"],), "a retried request"), ("processTransfers", (["k1:a:b:100", "k1:a:c:100"],), "the key reused for another body"), ("processTransfers", (["k1:a:b:5000"],), "not enough money")],
    [("processTransfers", (["k1:a:b:100", "k2:a:b:100", "k1:a:b:100", "k2:a:b:100"],), "two keys, both retried"), ("processTransfers", (["k1:a:b:5000", "k1:a:b:5000"],), "a rejected request retried"), ("processTransfers", (["k1:a:a:10", "k1:a:b:10"],), "an invalid request does not use up the key"),
     ("processTransfers", (["k1:a:z:10"],), "an unknown account"), ("processTransfers", (["k1:a:b:0", "k2:b:c:-5"],), "amounts must be positive"), ("processTransfers", (["x:a:b:100", "y:b:c:100", "x:a:b:100", "x:a:b:101"],), "duplicate, then conflict"),
     ("processTransfers", (["k1:a:b:1000", "k2:a:b:1", "k1:a:b:1000"],), "funds run out, the duplicate still answers"), ("processTransfers", ([],), "no requests"), ("processTransfers", (["k1:a:b:100", "k1:b:c:100"],), "the same key from another account")],
    starter='''
List<String> processTransfers(List<String> requests) {
    return List.of();
}
''', solution=APPLY_SOL,
    wrongs={"ignores-keys": APPLY_NOKEYS, "no-conflict-check": APPLY_NO_CONFLICT, "forgets-rejections": APPLY_FORGET_REJECT, "remembers-invalid-requests": APPLY_RECORD_INVALID, "key-is-per-account": APPLY_KEY_PER_ACCOUNT},
    hints=["Remember the body and the result for every key you accepted.", "Check the key before you look at the balances."],
    misconceptions=("MC202",), difficulty=4,
)

ex22.explain(
    "j10-l2.2-explain-keys", "Designing the idempotency key", ["o2"], ["J10.05"],
    "You are designing `POST /transfers` for a mobile app on a bad network. Describe how an idempotency key should work: who creates it, what the server stores, what it answers to a duplicate, what it answers when the same key arrives with a different body, and how long it should remember keys. Why can the server not use the transfer's amount and accounts as the key?",
    "The client creates a unique key (for example a random UUID) for each intended operation and sends it with every attempt of that operation, in an Idempotency-Key header. The server stores, for each key, a fingerprint of the request body and the result; the first request is processed and its result stored. A repeat with the same key and body returns the stored result without redoing the work. The same key with a different body is a misuse and is refused (the draft standard describes a 422 problem response; some designs use 409). Keys must be remembered for at least as long as clients may retry, which is a design choice. Amount and accounts cannot be the key because two different, legitimate transfers can have the same amount between the same accounts, and they must both happen.",
    levels={
        2: ("The answer covers who makes the key, what is stored, the duplicate answer, the mismatch answer, retention and why content is not the key.", [
            "The client generates a unique key per intended transfer and resends it on every retry. The server stores the key with the request body and the result. A duplicate with the same body returns the stored result and does nothing; the same key with a different body is rejected (422 or 409). Keys are kept at least as long as retries could occur. The content cannot be the key because two real transfers of the same amount between the same accounts must both be applied.",
            "Key from the client, such as a UUID, in a header. Server saves key, body hash and response; replays the response for a duplicate; refuses a key reused with another body. Keep keys for the retry window. Using amount and accounts would merge separate identical transfers."]),
        1: ("The answer names the key and the duplicate handling without the mismatch or the reason against content keys.", [
            "The client sends a unique key and the server ignores repeats.",
            "Store the key in a table."]),
        0: ("The answer lets the server invent the key or ignores repeats.", [
            "The server generates the key when it receives the request.",
            "Using the amount as the key is fine."]),
    },
)

l10_l2_2 = Lesson("j10-l2.2", "Idempotency keys", ["J10.05"], [
    ("o1", "Process requests so that a repeated key never repeats the effect"),
    ("o2", "Design an idempotency-key protocol and justify its details"),
], ["j10-l2.1"], 45, ["I120", "I84"], """## Before you start

You should know why POST is not idempotent (lesson 7.1.2) and why retries are needed (lesson 10.2.1).

## Explanation

Retries are necessary and `POST` is not idempotent, so a new technique is needed to make a retried `POST` harmless. The usual one is an **idempotency key**.

The client creates a unique key for each *intended* operation and sends it with every attempt of that operation. The server remembers, for each key, what it did. The Internet-Draft for an `Idempotency-Key` header field describes the idea: the key carries a value that MUST be unique and MUST NOT be reused with another request that has a different payload. (It is a draft, not yet a standard, and details such as the error status may differ between APIs.)

So the server's rules are:

1. First time a key is seen: do the work, store the key, the request body and the result.
2. Same key, same body: return the stored result; do not do the work again.
3. Same key, different body: refuse, because the client has made a mistake.
4. A request that is invalid before any work is done need not use up the key.

Two cautions. The key must come from the client, one per intended operation (a content-derived key would merge two real, identical transfers). And the server must store the key and the effect **together**, in one transaction, or a crash between them brings the duplicate back; lesson 10.2.3 returns to this.

## Worked examples

### Example 1: a retried request.

`k1:a:b:100` twice: the first is `applied`, the second is `dup:applied`, and the balances show only one transfer.

### Example 2: a misused key.

`k1:a:b:100` then `k1:a:c:100`: `conflict`.

## Where this is used

- Payment APIs, order creation, anything a mobile client retries over a bad connection. The stage project builds one.

## Common mistakes

:::mistake{id=MC202}
**Answering the retry with an error.** If the first request succeeded, a duplicate should receive the first result, not a failure, or the client will think the operation failed and may try something else.
:::

## Practice

::exercise{id=j10-l2.2-write-idempotent}

::exercise{id=j10-l2.2-explain-keys}

## Further reading

- **The Idempotency-Key HTTP Header Field (Internet-Draft)** `[I120]`.
- **RFC 9110, HTTP Semantics** `[I84]`.

## How you'll be assessed

- The **write** exercise checks the protocol (*implementation, debugging*).
- The **explain** exercise checks that you can design and justify it (*explanation*).

Because the specification is a draft, the course teaches the idea and the rules above, not an exact wire format.
""")

# ====================================================================== j10-l2.3
def f_saga(steps, fail_at):
    out = []
    for i, s in enumerate(steps):
        if i == fail_at:
            out.append("fail:" + s)
            for done in reversed(steps[:i]):
                out.append("undo:" + done)
            return out
        out.append("do:" + s)
    return out


SAGA_SOL = '''
List<String> sagaTrace(List<String> steps, int failAt) {
    List<String> trace = new ArrayList<>();
    for (int i = 0; i < steps.size(); i++) {
        if (i == failAt) {
            trace.add("fail:" + steps.get(i));
            for (int done = i - 1; done >= 0; done--) {
                trace.add("undo:" + steps.get(done));
            }
            return trace;
        }
        trace.add("do:" + steps.get(i));
    }
    return trace;
}
'''
SAGA_FORWARD = SAGA_SOL.replace("for (int done = i - 1; done >= 0; done--) {", "for (int done = 0; done < i; done++) {")
SAGA_UNDO_FAILED = SAGA_SOL.replace('            for (int done = i - 1; done >= 0; done--) {', '            for (int done = i; done >= 0; done--) {')
SAGA_NO_UNDO = SAGA_SOL.replace('                trace.add("undo:" + steps.get(done));', '                // forgotten')
SAGA_KEEPS_GOING = SAGA_SOL.replace("            return trace;\n        }\n        trace.add", "        }\n        trace.add")
STEPS = ["reserve", "debit", "credit", "notify"]

ex23.method(
    "write", "j10-l2.3-write-saga", "Undo what was done", ["o1"], ["J10.06"], ["IMPL"],
    "A saga runs a list of steps in order; each step is its own local transaction. If step number `failAt` (counting from 0; -1 or a number past the end means nothing fails) fails, the saga stops and **compensates** the steps that had succeeded, in **reverse** order. Write `sagaTrace(steps, failAt)` returning the events: `do:NAME` for a step that worked, `fail:NAME` for the failing step, then `undo:NAME` for each earlier step, last first. The failing step itself is not undone.",
    [("sagaTrace", [("steps", "List<String>"), ("failAt", "int")], "List<String>")], {"sagaTrace": f_saga},
    [("sagaTrace", (STEPS, -1), "nothing fails"), ("sagaTrace", (STEPS, 2), "the third step fails"), ("sagaTrace", (STEPS, 0), "the first step fails")],
    [("sagaTrace", (STEPS, 3), "the last step fails"), ("sagaTrace", (STEPS, 9), "a failure index past the end"), ("sagaTrace", ([], 0), "no steps"),
     ("sagaTrace", (["only"], 0), "a single failing step"), ("sagaTrace", (["a", "b"], 1), "two steps"), ("sagaTrace", (STEPS, -5), "a negative index means no failure")],
    starter='''
List<String> sagaTrace(List<String> steps, int failAt) {
    return List.of();
}
''', solution=SAGA_SOL,
    wrongs={"undoes-in-order": SAGA_FORWARD, "undoes-the-failed-step": SAGA_UNDO_FAILED, "no-compensation": SAGA_NO_UNDO, "carries-on-after-failure": SAGA_KEEPS_GOING},
    hints=["Compensate from the step before the failure down to the first.", "What should happen to the steps after the failing one?"],
    misconceptions=("MC203",), difficulty=3,
)

ex23.explain(
    "j10-l2.3-explain-outbox", "Saving and announcing", ["o2"], ["J10.06"],
    "The accounts service must update a balance in its database and then publish a `TransferCompleted` event to a message broker. The developer writes: save the balance, commit, then publish. Explain what can go wrong if the process crashes between the commit and the publish, and how the transactional outbox pattern fixes it. Then say what delivery guarantee the outbox gives the consumers, and what they must do about it.",
    "If the process crashes after the commit and before the publish, the balance has changed but no event is ever sent, so other services never learn of it. Writing the event first and then updating the balance has the opposite problem. The outbox pattern stores the message in an outbox table in the same database transaction that updates the business data, so both happen or neither does; a separate process reads the outbox and publishes the messages to the broker, marking them sent. If that process crashes after publishing but before marking, it will publish again, so delivery is at least once. Consumers must therefore be idempotent, for example by recording the ids of events they have processed, which is the idempotency-key idea again.",
    levels={
        2: ("The answer explains the lost event, the single-transaction outbox, the relay, at-least-once delivery and idempotent consumers.", [
            "A crash between commit and publish leaves the data changed and the event never sent. With an outbox the event is inserted into an outbox table in the same transaction as the balance update, so both or neither; a relay process publishes from the table and marks rows sent. If it crashes after publishing but before marking it publishes again, so delivery is at least once and consumers must be idempotent, for instance by storing processed event ids.",
            "Without it, the update and the message can disagree. The outbox ties the message to the same database transaction and a relay sends it afterwards. That gives at-least-once delivery, so consumers must detect duplicates."]),
        1: ("The answer names the outbox without explaining the delivery guarantee or the consumer duty.", [
            "The outbox saves the message with the data in one transaction.",
            "Consumers need to handle duplicates."]),
        0: ("The answer treats the broker as part of the database transaction.", [
            "Wrap the database update and the broker publish in one transaction and it is atomic.",
            "Publish twice to be safe, nothing else is needed."]),
    },
)

l10_l2_3 = Lesson("j10-l2.3", "Sagas, outbox and delivery guarantees", ["J10.06"], [
    ("o1", "Trace a saga and its compensations"),
    ("o2", "Explain the outbox pattern and what at-least-once delivery demands of consumers"),
], ["j10-l2.2", "j6-l2.2"], 45, ["I121", "I122", "I120"], """## Before you start

You should know database transactions (Stage 6) and idempotency keys (lesson 10.2.2).

## Explanation

Inside one database a transaction makes several changes all-or-nothing (Stage 6). Across two services, each with its own database, there is no single transaction that covers both. Two patterns fill the gap.

A **saga** is a reliably coordinated sequence of local transactions. The coordination, which often uses asynchronous messaging, ensures that the saga finishes: either all steps complete, or, if a local transaction fails because it violates a business rule, the changes made by the completed steps are undone by **compensating transactions**. Sagas are coordinated by choreography (each step publishes events that trigger the next) or by orchestration (an orchestrator tells participants what to do). Note that a compensation is a new business action (refund the debit), not a rollback; between the step and its compensation other parties may have seen the intermediate state.

The **transactional outbox** solves the "save, then announce" problem. The service stores the message in its database as part of the same transaction that updates the business entities; a separate process then sends the messages to the broker. The data and the message cannot disagree, but the relay may send a message twice, so delivery is **at least once** and consumers must be idempotent.

## Worked examples

### Example 1: a saga that fails at the third step.

Steps `reserve, debit, credit, notify`, failing at `credit`: `do:reserve, do:debit, fail:credit, undo:debit, undo:reserve`.

### Example 2: the outbox.

One transaction: update the balance, insert `TransferCompleted` into the outbox table. A relay publishes and marks the row. If it crashes in between, the event is published again.

## Where this is used

- Any workflow across services: orders, bookings, payments. The stage project asks you to compensate a failed transfer.

## Common mistakes

:::mistake{id=MC203}
**Wrapping two services in one transaction.** There is none. Use a saga with compensations, and make every step and every consumer idempotent.
:::

## Practice

::exercise{id=j10-l2.3-write-saga}

::exercise{id=j10-l2.3-explain-outbox}

## Further reading

- **Pattern: Saga** `[I121]`.
- **Pattern: Transactional outbox** `[I122]`.

## How you'll be assessed

- The **write** exercise checks the order of compensations (*implementation*).
- The **explain** exercise checks the outbox and its delivery guarantee (*explanation*).

The term "at-least-once" is standard messaging vocabulary, and the retry-after-crash reasoning is derived from the pattern's description rather than quoted from it.
""")

# ====================================================================== j10-l2.4
def f_breaker(results, threshold, cooldown):
    out, state, fails, remaining = [], "closed", 0, 0
    for r in results:
        if state == "open":
            out.append("rejected")
            remaining -= 1
            if remaining == 0:
                state = "half"
            continue
        if r == "ok":
            out.append("ok")
            state, fails = "closed", 0
        else:
            out.append("fail")
            if state == "half":
                state, remaining = "open", cooldown
            else:
                fails += 1
                if fails >= threshold:
                    state, remaining = "open", cooldown
        if state == "open" and remaining == 0:
            state = "half"
    return out


BREAKER_SOL = '''
List<String> breakerOutcomes(List<String> results, int threshold, int cooldown) {
    List<String> out = new ArrayList<>();
    String state = "closed";
    int failures = 0;
    int remaining = 0;
    for (String result : results) {
        if (state.equals("open")) {
            out.add("rejected");
            remaining--;
            if (remaining == 0) {
                state = "half";
            }
            continue;
        }
        if (result.equals("ok")) {
            out.add("ok");
            state = "closed";
            failures = 0;
        } else {
            out.add("fail");
            if (state.equals("half")) {
                state = "open";
                remaining = cooldown;
            } else {
                failures++;
                if (failures >= threshold) {
                    state = "open";
                    remaining = cooldown;
                }
            }
        }
        if (state.equals("open") && remaining == 0) {
            state = "half";
        }
    }
    return out;
}
'''
BREAKER_NO_RESET = BREAKER_SOL.replace('            state = "closed";\n            failures = 0;\n        } else {', '            state = "closed";\n        } else {')
BREAKER_HALF_CLOSES = BREAKER_SOL.replace('            if (state.equals("half")) {\n                state = "open";\n                remaining = cooldown;\n            } else {', '            if (state.equals("half")) {\n                state = "closed";\n            } else {')
BREAKER_LATE = BREAKER_SOL.replace("failures >= threshold", "failures > threshold")
BREAKER_FOREVER = BREAKER_SOL.replace('            if (remaining == 0) {\n                state = "half";\n            }\n            continue;', '            continue;')
B1 = ["fail", "fail", "fail", "ok", "ok", "ok", "ok", "fail"]

ex24.method(
    "write", "j10-l2.4-write-breaker", "A circuit breaker's decisions", ["o1"], ["J10.07"], ["IMPL"],
    "`results` is what each call to a dependency **would** return, `ok` or `fail`. The breaker starts closed and lets calls through. After `threshold` consecutive failures it opens: the next `cooldown` calls are answered `rejected` without calling the dependency (their result is not used). It then becomes half-open: the next call is let through, and if it is `ok` the breaker closes (and the failure count starts again), if it fails the breaker opens again for another `cooldown` calls. A success while closed resets the failure count. Write `breakerOutcomes(results, threshold, cooldown)` returning `ok`, `fail` or `rejected` for each call.",
    [("breakerOutcomes", [("results", "List<String>"), ("threshold", "int"), ("cooldown", "int")], "List<String>")], {"breakerOutcomes": f_breaker},
    [("breakerOutcomes", (B1, 3, 2), "trips, rejects, recovers"), ("breakerOutcomes", (["ok", "ok"], 3, 2), "never trips"), ("breakerOutcomes", (["fail", "ok", "fail", "ok", "fail"], 2, 1), "failures not in a row")],
    [("breakerOutcomes", (["fail", "fail", "fail", "fail", "fail", "fail", "ok"], 2, 2), "the half-open call fails and re-opens"), ("breakerOutcomes", (["fail"] * 10, 3, 3), "a dependency that stays down"), ("breakerOutcomes", ([], 3, 2), "no calls"),
     ("breakerOutcomes", (["fail", "fail", "ok", "ok", "ok", "fail", "fail", "ok"], 2, 1), "trips twice"), ("breakerOutcomes", (["fail", "ok", "fail", "ok"], 1, 2), "threshold of one"), ("breakerOutcomes", (["fail", "fail", "x", "ok", "ok", "ok"], 2, 1), "a probe that is not ok counts as a failure")],
    starter='''
List<String> breakerOutcomes(List<String> results, int threshold, int cooldown) {
    return List.of();
}
''', solution=BREAKER_SOL,
    wrongs={"success-does-not-reset": BREAKER_NO_RESET, "never-reopens": BREAKER_HALF_CLOSES, "trips-one-late": BREAKER_LATE, "stays-open-for-ever": BREAKER_FOREVER},
    hints=["Keep three pieces of state: the mode, the failure count and the calls left to reject.", "What does the half-open call decide?"],
    misconceptions=("MC204",), difficulty=4,
)

ex24.explain(
    "j10-l2.4-explain-breaker", "Why stop calling", ["o2"], ["J10.07"],
    "The accounts service calls a currency-rates service on every request, with a 3-second timeout. The rates service becomes very slow. Within a minute the accounts service is also unusable. Explain why that cascade happens, how a circuit breaker (together with a fallback such as the last known rate) changes it, and what a team must still do about the open breaker.",
    "Each request waits up to 3 seconds for the slow dependency, holding a thread and a connection, so under load all the accounts service's threads end up waiting and it cannot serve anything, even requests that do not need rates: the failure spreads. A circuit breaker counts failures; once they reach a threshold it trips and further calls fail immediately without calling the dependency, so the accounts service stays responsive. A fallback such as the last known rate lets it keep serving degraded results. Periodically the breaker lets a trial call through and closes if it succeeds. The team must still alert on the open breaker (the problem is hidden from users, not solved) and fix or scale the dependency.",
    levels={
        2: ("The answer explains thread exhaustion, the fail-fast breaker and fallback, the trial call, and the need to alert.", [
            "Every request blocks for up to 3 seconds on the slow service, so threads and connections fill with waiting calls and the whole accounts service stalls: a cascading failure. A breaker trips after enough failures, so calls fail at once instead of waiting; with a fallback like the last known rate the service keeps working in a degraded way. It lets a trial call through after a cooldown and closes again if it works. The breaker only hides the problem, so you must alert and repair the rates service.",
            "Slow calls tie up all the threads so everything stops. The breaker rejects calls immediately while open, the fallback gives a stale rate, and a half-open probe checks recovery. We still have to be told it tripped and fix the dependency."]),
        1: ("The answer describes the breaker without the cascade or the follow-up.", [
            "The breaker stops calls to the failing service.",
            "Use a fallback rate."]),
        0: ("The answer treats a longer timeout or more threads as the solution.", [
            "Raise the timeout to 30 seconds so it has time to answer.",
            "Add more threads so there are enough to wait."]),
    },
)

l10_l2_4 = Lesson("j10-l2.4", "Circuit breakers and resilience", ["J10.07"], [
    ("o1", "Simulate the decisions of a circuit breaker"),
    ("o2", "Explain how one slow dependency takes a service down and how a breaker and fallback limit the damage"),
], ["j10-l2.1"], 40, ["I123"], """## Before you start

You should know timeouts and retries (lesson 10.2.1) and the thread costs in Stage 9.

## Explanation

When a service you depend on is slow, the damage spreads. Each of your requests waits for it, holding a thread and a connection. Under load all your threads end up waiting, and you cannot serve anything, even requests that do not need that dependency. A failure in one place has become a failure in all (a **cascading failure**).

A **circuit breaker** wraps a protected call and monitors for failures. Once the failures reach a threshold, the breaker trips and all further calls return an error immediately, without making the protected call. Usually a monitor alert is wanted as well. After a cooldown the breaker allows a trial call (**half-open**); if it succeeds the breaker closes again, and if it fails the breaker stays open for another cooldown.

The breaker protects *you* and the struggling dependency: you stop wasting threads and it gets room to recover. It does not make the dependency work. Pair it with a **fallback** (a cached value, a default, a clear "temporarily unavailable") and an alert, and keep timeouts short so a slow call counts as a failure early. A **bulkhead** is the related idea of limiting how many threads any one dependency may use, so it cannot take them all.

## Worked examples

### Example 1: the sequence.

Results `fail, fail, fail, ok, ok, ok, ok, fail` with threshold 3 and cooldown 2: `fail, fail, fail, rejected, rejected, ok, ok, fail`. The two `ok` results at positions 3 and 4 (counting from 0) were never used, because the breaker was open; the call at position 5 was the half-open trial.

### Example 2: the numbers in this course.

Stage 9 showed what a thread waiting costs; a breaker is how you refuse to pay it for a dependency that is down.

## Where this is used

- Every client of a remote service, in libraries such as Resilience4j or built into service meshes. This course models the decision; it does not use a library.

## Common mistakes

:::mistake{id=MC204}
**Thinking a breaker repairs the dependency.** It limits the damage and gives it room to recover. Someone still has to notice and fix the cause.
:::

## Practice

::exercise{id=j10-l2.4-write-breaker}

::exercise{id=j10-l2.4-explain-breaker}

## Further reading

- **Circuit Breaker, M. Fowler** `[I123]`.

## How you'll be assessed

- The **write** exercise checks the breaker's state machine (*implementation*).
- The **explain** exercise checks the cascade and the remedy (*explanation*).

The half-open behaviour described here is the common design; the cited article describes the basic trip behaviour and the alert, and implementations differ in details. Bulkheads are named from general practice, not from a recorded source.
""")
print("module 10.2 authored")
