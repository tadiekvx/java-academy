"""Stage 10 project: j10-a1-transfer-service (C). Two-step transfer across services with idempotency and compensation."""
import re
import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-10"
from proj import project

MAIN = "\nvoid main() {\n    // Optional: try your handler here.\n}\n"
SIG = [("handleAll", [("requests", "List<String>")], "List<String>")]
BAD = "400|Bad Request"


def model(requests):
    bal = {"a": 1000, "b": 1000, "c": 1000}
    seen = {}
    out = []

    def state():
        return f"a={bal['a']};b={bal['b']};c={bal['c']}"

    for r in requests:
        p = r.split(" ")
        if len(p) not in (4, 5) or (len(p) == 5 and p[4] != "crash") or not re.fullmatch(r"[0-9]{1,9}", p[3]):
            out.append(BAD)
            continue
        key, frm, to, cents = p[0], p[1], p[2], int(p[3])
        body = (frm, to, cents)
        if key in seen:
            out.append("409|Conflict" if seen[key][0] != body else seen[key][1])
            continue
        if frm not in bal or to not in bal or frm == to or cents <= 0:
            out.append(BAD)
            continue
        if bal[frm] < cents:
            resp = "422|Insufficient funds"
            seen[key] = (body, resp)
            out.append(resp)
            continue
        if len(p) == 5:
            out.append("502|Credit failed, debit reversed")
            continue
        bal[frm] -= cents
        bal[to] += cents
        resp = "200|" + state()
        seen[key] = (body, resp)
        out.append(resp)
    return out


INHERITED = '''
// INHERITED CODE: the transfer endpoint, as found. Requests: "key from to cents" with an optional last word
// "crash", which makes the credit step of that attempt fail (the second service is down).
// Ticket 1001: "Customers are charged twice when their phone retries a transfer."
// Ticket 1002: "When the credit fails the money has gone from the sender and arrived nowhere."

List<String> handleAll(List<String> requests) {
    Map<String, Integer> balance = new TreeMap<>(Map.of("a", 1000, "b", 1000, "c", 1000));
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] p = request.split(" ");
        if ((p.length != 4 && p.length != 5) || (p.length == 5 && !p[4].equals("crash")) || !p[3].matches("[0-9]{1,9}")) {
            out.add("400|Bad Request");
            continue;
        }
        String from = p[1];
        String to = p[2];
        int cents = Integer.parseInt(p[3]);
        if (!balance.containsKey(from) || !balance.containsKey(to) || from.equals(to) || cents <= 0) {
            out.add("400|Bad Request");
            continue;
        }
        if (balance.get(from) < cents) {
            out.add("422|Insufficient funds");
            continue;
        }
        balance.merge(from, -cents, Integer::sum);
        if (p.length == 5) {
            out.add("500|Internal Server Error");
            continue;
        }
        balance.merge(to, cents, Integer::sum);
        out.add("200|a=" + balance.get("a") + ";b=" + balance.get("b") + ";c=" + balance.get("c"));
    }
    return out;
}
'''
FINAL = '''
// The transfer endpoint. Requests: "key from to cents" with an optional last word "crash" (the credit step fails).

List<String> handleAll(List<String> requests) {
    Map<String, Integer> balance = new TreeMap<>(Map.of("a", 1000, "b", 1000, "c", 1000));
    Map<String, String[]> seen = new HashMap<>();
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] p = request.split(" ");
        if ((p.length != 4 && p.length != 5) || (p.length == 5 && !p[4].equals("crash")) || !p[3].matches("[0-9]{1,9}")) {
            out.add("400|Bad Request");
            continue;
        }
        String key = p[0];
        String from = p[1];
        String to = p[2];
        int cents = Integer.parseInt(p[3]);
        String body = from + ">" + to + ":" + cents;
        if (seen.containsKey(key)) {
            String[] first = seen.get(key);
            out.add(first[0].equals(body) ? first[1] : "409|Conflict");
            continue;
        }
        if (!balance.containsKey(from) || !balance.containsKey(to) || from.equals(to) || cents <= 0) {
            out.add("400|Bad Request");
            continue;
        }
        if (balance.get(from) < cents) {
            String response = "422|Insufficient funds";
            seen.put(key, new String[] {body, response});
            out.add(response);
            continue;
        }
        balance.merge(from, -cents, Integer::sum);
        if (p.length == 5) {
            balance.merge(from, cents, Integer::sum);
            out.add("502|Credit failed, debit reversed");
            continue;
        }
        balance.merge(to, cents, Integer::sum);
        String response = "200|a=" + balance.get("a") + ";b=" + balance.get("b") + ";c=" + balance.get("c");
        seen.put(key, new String[] {body, response});
        out.add(response);
    }
    return out;
}
'''


def wrong(old, new, src=FINAL):
    assert old in src, old
    return src.replace(old, new, 1)


WRONGS = {
    "m1-no-conflict-check": wrong('first[0].equals(body) ? first[1] : "409|Conflict"', 'first[1]'),
    "m1-forgets-rejections": wrong('            seen.put(key, new String[] {body, response});\n            out.add(response);\n            continue;\n        }\n        balance.merge(from, -cents', '            out.add(response);\n            continue;\n        }\n        balance.merge(from, -cents'),
    "m1-key-checked-after-validation-and-funds": wrong('        if (seen.containsKey(key)) {\n            String[] first = seen.get(key);\n            out.add(first[0].equals(body) ? first[1] : "409|Conflict");\n            continue;\n        }\n', ''),
    "m2-debit-not-reversed": wrong('            balance.merge(from, cents, Integer::sum);\n            out.add("502', '            out.add("502'),
    "m2-crash-remembered": wrong('            out.add("502|Credit failed, debit reversed");\n            continue;', '            seen.put(key, new String[] {body, "502|Credit failed, debit reversed"});\n            out.add("502|Credit failed, debit reversed");\n            continue;'),
}


def case(name, *reqs):
    return ("handleAll", (list(reqs),), name)


M1V = [case("a retried request", "k1 a b 100", "k1 a b 100"), case("the key reused with another body", "k1 a b 100", "k1 a c 100"), case("a different key", "k1 a b 100", "k2 a b 100")]
M1H = M1V + [
    case("a rejected request is remembered", "k1 a b 5000", "k1 a b 5000", "k2 a b 5"),
    case("a rejected request is remembered even when funds arrive later", "k1 a b 1500", "k2 b a 600", "k1 a b 1500"),
    case("an invalid request does not use up the key", "k1 a a 10", "k1 a b 10"),
    case("a malformed request", "k1 a b", "k1 a b x", "k1 a b 1 crashx"),
    case("a retry after later transfers still answers the first result", "k1 a b 100", "k2 b c 50", "k1 a b 100"),
    case("two retries", "k1 a b 100", "k1 a b 100", "k1 a b 100"),
    case("unknown account and zero amount", "k1 a z 10", "k2 a b 0"),
    case("different amounts under one key", "k1 a b 100", "k1 a b 101", "k1 a b 100"),
]
M2V = [case("a crash is compensated", "k1 a b 100 crash"), case("a retry after the crash works", "k1 a b 100 crash", "k1 a b 100"), case("money is never lost", "k1 a b 100 crash", "k2 b c 10", "k3 c a 5 crash")]
M2H = M2V + M1H + [
    case("a crash on an unaffordable transfer is reported as insufficient", "k1 a b 5000 crash"),
    case("a crash does not use up the key", "k1 a b 100 crash", "k1 a b 100", "k1 a b 100"),
    case("several crashes", "k1 a b 10 crash", "k2 a b 10 crash", "k3 a b 10"),
    case("the retry with a crash after a success is a duplicate", "k1 a b 100", "k1 a b 100 crash"),
]
ms = [
    dict(id="m1", title="Ticket 1001: charged twice", methods=SIG, fns={"handleAll": model}, visible=M1V, hidden=M1H, instructions="""
        **Ticket 1001:** *"Customers are charged twice when their phone retries a transfer."*

        Make `key` an idempotency key (lesson 10.2.2): the first request with a key is processed and its response stored; the same key with the same `from to cents` returns **exactly the stored response** and changes nothing; the same key with a different body is `409|Conflict`. A request that is malformed (`400|Bad Request`) or invalid is not stored, so its key can be used again. An unaffordable transfer is stored (`422|Insufficient funds`), so its retry gives the same answer.
        """),
    dict(id="m2", title="Ticket 1002: money that vanished", methods=SIG, fns={"handleAll": model}, visible=M2V, hidden=M2H, instructions="""
        **Ticket 1002:** *"When the credit fails the money has gone from the sender and arrived nowhere."*

        A request ending in `crash` models the second service failing after the debit. Compensate (lesson 10.2.3): reverse the debit, answer `502|Credit failed, debit reversed`, and do **not** store the key, so that the client's retry of the same request can succeed. Balances must always add up to 3000.
        """),
]
RUBRIC = [
    ("Idempotency", "A retry still moves money twice, or the stored response is rebuilt differently", "Duplicates are caught but the mismatch or rejected cases are wrong", "Every duplicate returns the exact stored response, a reused key with another body is a conflict, and invalid requests leave the key free"),
    ("Failure handling", "The debit is lost on a crash, or the crash blocks the retry", "The debit is reversed but the key is stored", "The debit is compensated, the key is not stored, and the retry succeeds"),
    ("Reasoning about order", "No argument about where a crash could still leave the system wrong", "Notes one crash point", "Identifies the crash points (after debit, after credit, before storing the key) and says what the design does or does not cover"),
    ("Decision record", "Missing, or only describes the code", "States what was done without alternatives", "A short ADR with context, decision (idempotency key plus compensation), and consequences including what a real two-database version would need (outbox, durable key store)"),
]
project("j10-a1-transfer-service", "The transfer that happened twice", "C",
        "Take over a transfer endpoint that double-charges retries and loses money when the second step fails; make it idempotent and compensating, and record the decision.",
        """
        You have inherited a transfer endpoint. A request is `key from to cents`, optionally followed by the word `crash`, which means that in this attempt the second service (the one that credits the receiver) is down.

        Two tickets have come in:

        1. **Ticket 1001**: customers are charged twice when their phone retries.
        2. **Ticket 1002**: when the credit fails, the money is gone.

        Fix them one at a time, running all the checks after each. Then write an ADR (see lesson 10.1.3) for the design you chose. In a real system the debit and the credit would be in two databases; say in the ADR what that would change.
        """, 4, ["j10-l1.3", "j10-l2.2", "j10-l2.3"], ["J10.05", "J10.06", "J10.03"],
        ["The same key and body always return the same response and move money once.",
         "A failed credit leaves every balance as it was, and the client can retry.",
         "The total of all balances never changes."],
        ["Fix one ticket at a time.", "Run all the checks after every change."],
        ["Given a retried request, then the second response equals the first.",
         "Given a key reused with another body, then 409.",
         "Given a crash, then the balances are unchanged and a retry succeeds."],
        ms, RUBRIC,
        "Write an ADR (200 words or fewer) with Title, Status, Context, Decision and Consequences for the design you chose. Say why the key comes from the client, why a crashed attempt does not store its key, what could still go wrong if the process dies between the debit and the compensation, and what an outbox and a durable key store would add in a version with two databases.",
        INHERITED + MAIN, FINAL + MAIN, {k: v + MAIN for k, v in WRONGS.items()})
print("P14 written")
