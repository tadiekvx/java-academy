"""Stage 12 capstone: j12-a1-capstone (C). One API handler that grows through four changes: a requirement, reliability, operability, an incident."""
import re
import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-12"
from proj import project

MAIN = "\nvoid main() {\n    // Optional: try your handler here.\n}\n"
SIG_H = [("handleAll", [("requests", "List<String>")], "List<String>")]
SIG_A = [("auditLines", [("requests", "List<String>")], "List<String>")]
USERS = {"ada", "grace", "tess"}
OWNERS = {"1": "ada", "2": "grace", "3": "ada"}


def model(requests):
    bal = {"1": 1000, "2": 1000, "3": 1000}
    seen, out = {}, []
    for r in requests:
        t = r.split(" ")
        if len(t) < 3:
            out.append("400|Bad Request"); continue
        actor, method, path = t[0], t[1], t[2]
        if path == "/health":
            out.append("200|ok" if method == "GET" else "405|Method Not Allowed"); continue
        if actor not in USERS:
            out.append("401|Unauthorized"); continue
        if re.fullmatch(r"/accounts/[0-9]{1,9}", path):
            if method != "GET":
                out.append("405|Method Not Allowed"); continue
            i = str(int(path.split("/")[2]))
            if i not in OWNERS:
                out.append("404|Not Found")
            elif actor == "tess" or OWNERS[i] == actor:
                out.append(f"200|{i};{OWNERS[i]};{bal[i]}")
            else:
                out.append("403|Forbidden")
            continue
        if path == "/transfers":
            if method != "POST":
                out.append("405|Method Not Allowed"); continue
            b = t[3:]
            if len(b) not in (4, 5) or (len(b) == 5 and b[4] != "crash") or not re.fullmatch(r"[0-9]{1,9}", b[3]):
                out.append("400|Bad Request"); continue
            key, frm, to, cents = b[0], b[1], b[2], int(b[3])
            body = (frm, to, cents)
            if key in seen:
                out.append("409|Conflict" if seen[key][0] != body else seen[key][1]); continue
            if frm not in bal or to not in bal or frm == to or cents <= 0:
                out.append("400|Bad Request"); continue
            if actor != "tess" and OWNERS[frm] != actor:
                out.append("403|Forbidden"); continue
            if bal[frm] < cents:
                resp = "422|Insufficient funds"
                seen[key] = (body, resp); out.append(resp); continue
            if len(b) == 5:
                out.append("502|Credit failed, debit reversed"); continue
            bal[frm] -= cents
            bal[to] += cents
            resp = "200|" + ";".join(f"{k}:{bal[k]}" for k in sorted(bal))
            seen[key] = (body, resp); out.append(resp); continue
        out.append("404|Not Found")
    return out


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def audit(requests):
    res = model(requests)
    lines = []
    for r, resp in zip(requests, res):
        t = r.split(" ")
        a, m, p = (t + ["", "", ""])[:3]
        lines.append('{"actor":"%s","method":"%s","path":"%s","status":%s}' % (esc(a), esc(m), esc(p), resp.split("|")[0]))
    return lines


FINAL = '''
// Brightbank's API handler. Request: "actor METHOD path [body words]". Actor "-" means nobody is signed in.
// Users: ada and grace (customers) and tess (a teller). Accounts 1 (ada), 2 (grace), 3 (ada) start at 1000.

List<String> handleAll(List<String> requests) {
    Map<String, String> owners = new HashMap<>(Map.of("1", "ada", "2", "grace", "3", "ada"));
    Map<String, Integer> balance = new TreeMap<>(Map.of("1", 1000, "2", 1000, "3", 1000));
    Set<String> users = Set.of("ada", "grace", "tess");
    Map<String, String[]> seen = new HashMap<>();
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        out.add(handle(request, owners, balance, users, seen));
    }
    return out;
}

String handle(String request, Map<String, String> owners, Map<String, Integer> balance, Set<String> users, Map<String, String[]> seen) {
    String[] t = request.split(" ", -1);
    if (t.length < 3) {
        return "400|Bad Request";
    }
    String actor = t[0];
    String method = t[1];
    String path = t[2];
    if (path.equals("/health")) {
        return method.equals("GET") ? "200|ok" : "405|Method Not Allowed";
    }
    if (!users.contains(actor)) {
        return "401|Unauthorized";
    }
    if (path.matches("/accounts/[0-9]{1,9}")) {
        if (!method.equals("GET")) {
            return "405|Method Not Allowed";
        }
        String id = String.valueOf(Integer.parseInt(path.substring("/accounts/".length())));
        if (!owners.containsKey(id)) {
            return "404|Not Found";
        }
        if (actor.equals("tess") || owners.get(id).equals(actor)) {
            return "200|" + id + ";" + owners.get(id) + ";" + balance.get(id);
        }
        return "403|Forbidden";
    }
    if (path.equals("/transfers")) {
        if (!method.equals("POST")) {
            return "405|Method Not Allowed";
        }
        return transfer(actor, Arrays.copyOfRange(t, 3, t.length), owners, balance, seen);
    }
    return "404|Not Found";
}

String transfer(String actor, String[] b, Map<String, String> owners, Map<String, Integer> balance, Map<String, String[]> seen) {
    if ((b.length != 4 && b.length != 5) || (b.length == 5 && !b[4].equals("crash")) || !b[3].matches("[0-9]{1,9}")) {
        return "400|Bad Request";
    }
    String key = b[0];
    String from = b[1];
    String to = b[2];
    int cents = Integer.parseInt(b[3]);
    String body = from + ">" + to + ":" + cents;
    if (seen.containsKey(key)) {
        String[] first = seen.get(key);
        return first[0].equals(body) ? first[1] : "409|Conflict";
    }
    if (!balance.containsKey(from) || !balance.containsKey(to) || from.equals(to) || cents <= 0) {
        return "400|Bad Request";
    }
    if (!actor.equals("tess") && !owners.get(from).equals(actor)) {
        return "403|Forbidden";
    }
    if (balance.get(from) < cents) {
        String response = "422|Insufficient funds";
        seen.put(key, new String[] {body, response});
        return response;
    }
    if (b.length == 5) {
        return "502|Credit failed, debit reversed";
    }
    balance.merge(from, -cents, Integer::sum);
    balance.merge(to, cents, Integer::sum);
    List<String> parts = new ArrayList<>();
    for (Map.Entry<String, Integer> entry : balance.entrySet()) {
        parts.add(entry.getKey() + ":" + entry.getValue());
    }
    String response = "200|" + String.join(";", parts);
    seen.put(key, new String[] {body, response});
    return response;
}

List<String> auditLines(List<String> requests) {
    List<String> responses = handleAll(requests);
    List<String> lines = new ArrayList<>();
    for (int i = 0; i < requests.size(); i++) {
        String[] t = requests.get(i).split(" ", -1);
        String actor = t.length > 0 ? t[0] : "";
        String method = t.length > 1 ? t[1] : "";
        String path = t.length > 2 ? t[2] : "";
        String status = responses.get(i).substring(0, responses.get(i).indexOf('|'));
        lines.add("{\\"actor\\":" + quote(actor) + ",\\"method\\":" + quote(method) + ",\\"path\\":" + quote(path) + ",\\"status\\":" + status + "}");
    }
    return lines;
}

String quote(String text) {
    return "\\"" + text.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\"") + "\\"";
}
'''
INHERITED = '''
// INHERITED CODE: the account API of the partner company Brightbank has bought, as found.
// Request: "actor METHOD path [body words]". Actor "-" means nobody is signed in.
// Users: ada and grace (customers) and tess (a teller). Accounts 1 (ada), 2 (grace), 3 (ada) start at 1000.
//
// Your job over four changes (see the milestones): add transfers, make them reliable, make the service
// observable, and handle the incident that follows.

List<String> handleAll(List<String> requests) {
    Map<String, String> owners = Map.of("1", "ada", "2", "grace", "3", "ada");
    Map<String, Integer> balance = new TreeMap<>(Map.of("1", 1000, "2", 1000, "3", 1000));
    Set<String> users = Set.of("ada", "grace", "tess");
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        try {
            String[] t = request.split(" ", -1);
            if (t.length < 3) {
                out.add("400|Bad Request");
            } else if (!users.contains(t[0])) {
                out.add("401|Unauthorized");
            } else if (t[2].matches("/accounts/[0-9]{1,9}")) {
                if (!t[1].equals("GET")) {
                    out.add("405|Method Not Allowed");
                } else {
                    String id = String.valueOf(Integer.parseInt(t[2].substring("/accounts/".length())));
                    if (!owners.containsKey(id)) {
                        out.add("404|Not Found");
                    } else if (t[0].equals("tess") || owners.get(id).equals(t[0])) {
                        out.add("200|" + id + ";" + owners.get(id) + ";" + balance.get(id));
                    } else {
                        out.add("403|Forbidden");
                    }
                }
            } else {
                out.add("404|Not Found");
            }
        } catch (Exception e) {
            out.add("500|Internal Server Error");
        }
    }
    return out;
}

List<String> auditLines(List<String> requests) {
    return new ArrayList<>();
}
'''


def wrong(old, new, src=FINAL):
    assert old in src, old
    return src.replace(old, new, 1)


WRONGS = {
    "m1-any-customer-moves-any-money": wrong('    if (!actor.equals("tess") && !owners.get(from).equals(actor)) {\n        return "403|Forbidden";\n    }\n', ''),
    "m1-funds-not-checked": wrong('    if (balance.get(from) < cents) {', '    if (false) {'),
    "m1-same-account-allowed": wrong(' || from.equals(to)', ''),
    "m2-no-key-memory": wrong('    if (seen.containsKey(key)) {', '    if (false) {'),
    "m2-crash-loses-the-debit": wrong('    if (b.length == 5) {\n        return "502|Credit failed, debit reversed";\n    }\n    balance.merge(from, -cents, Integer::sum);', '    balance.merge(from, -cents, Integer::sum);\n    if (b.length == 5) {\n        return "502|Credit failed, debit reversed";\n    }'),
    "m2-crash-is-remembered": wrong('    if (b.length == 5) {\n        return "502|Credit failed, debit reversed";\n    }', '    if (b.length == 5) {\n        seen.put(key, new String[] {body, "502|Credit failed, debit reversed"});\n        return "502|Credit failed, debit reversed";\n    }'),
    "m3-health-needs-a-login": wrong('    if (path.equals("/health")) {\n        return method.equals("GET") ? "200|ok" : "405|Method Not Allowed";\n    }\n    if (!users.contains(actor)) {\n        return "401|Unauthorized";\n    }', '    if (!users.contains(actor)) {\n        return "401|Unauthorized";\n    }\n    if (path.equals("/health")) {\n        return method.equals("GET") ? "200|ok" : "405|Method Not Allowed";\n    }'),
    "m3-audit-line-has-the-body": wrong(',\\"status\\":" + status + "}"', ',\\"status\\":" + status + ",\\"body\\":" + quote(requests.get(i)) + "}"'),
    "m3-audit-unescaped": wrong('quote(path)', '"\\"" + path + "\\""'),
    "m4-oversized-amount-crashes": wrong('!b[3].matches("[0-9]{1,9}")', '!b[3].matches("[0-9]+")'),
}


def case(m, name, *reqs):
    return (m, (list(reqs),), name)


H = "handleAll"
M1V = [case(H, "own money, enough funds", "ada POST /transfers k1 1 2 100"), case(H, "someone else's money", "ada POST /transfers k1 2 1 100"), case(H, "not enough money", "ada POST /transfers k1 1 2 5000")]
M1H = M1V + [
    case(H, "a teller may move any money", "tess POST /transfers k1 2 3 50"), case(H, "unknown account", "ada POST /transfers k1 1 9 10"), case(H, "same account", "ada POST /transfers k1 1 1 10"),
    case(H, "zero amount", "ada POST /transfers k1 1 2 0"), case(H, "malformed body", "ada POST /transfers k1 1 2", "ada POST /transfers k1 1 2 x"), case(H, "balances accumulate", "ada POST /transfers a 1 2 100", "grace POST /transfers b 2 3 300", "ada GET /accounts/2"),
    case(H, "nobody signed in", "- POST /transfers k1 1 2 10"), case(H, "wrong method", "ada GET /transfers"), case(H, "reads as before", "ada GET /accounts/1", "ada GET /accounts/2", "ada GET /accounts/9", "tess GET /accounts/2"),
]
M2V = [case(H, "a retried transfer", "ada POST /transfers k1 1 2 100", "ada POST /transfers k1 1 2 100"), case(H, "a crash is compensated", "ada POST /transfers k1 1 2 100 crash", "ada GET /accounts/1"), case(H, "retry after a crash", "ada POST /transfers k1 1 2 100 crash", "ada POST /transfers k1 1 2 100")]
M2H = M2V + M1H + [
    case(H, "a key reused with another body", "ada POST /transfers k1 1 2 100", "ada POST /transfers k1 1 3 100"), case(H, "a rejected transfer is remembered", "ada POST /transfers k1 1 2 5000", "ada POST /transfers k1 1 2 5000"),
    case(H, "an invalid request leaves the key free", "ada POST /transfers k1 1 1 10", "ada POST /transfers k1 1 2 10"), case(H, "forbidden does not use up the key", "ada POST /transfers k1 2 1 10", "grace POST /transfers k1 2 1 10"),
    case(H, "several retries and crashes", "ada POST /transfers a 1 2 10 crash", "ada POST /transfers a 1 2 10", "ada POST /transfers a 1 2 10", "ada POST /transfers b 1 3 10 crash"),
]
AUD = "auditLines"
A_REQ = ["ada GET /accounts/1", "- GET /accounts/1", "ada POST /transfers k1 1 2 100", 'ada GET /acc"ounts', "", "grace GET /health"]
M3V = [case(AUD, "audit lines for a few requests", *A_REQ), case(H, "health needs no login", "- GET /health"), case(H, "health is read-only", "ada POST /health")]
M3H = M3V + M2H + [
    case(AUD, "no requests", ), case(AUD, "a path with a backslash", "ada GET /a\\b"), case(AUD, "bodies are not logged", "ada POST /transfers secret-key 1 2 5"),
    case(AUD, "every status is a number", "ada DELETE /accounts/1", "mallory GET /accounts/1", "tess POST /transfers k 1 2 10 crash"), case(H, "health with odd methods", "- DELETE /health", "tess GET /health"),
]
M4V = [case(H, "an enormous amount", "ada POST /transfers k1 1 2 99999999999"), case(H, "a negative amount", "ada POST /transfers k1 1 2 -5"), case(H, "the largest accepted amount", "tess POST /transfers k1 1 2 999999999")]
M4H = M4V + M3H + [
    case(H, "an amount that overflows an int", "ada POST /transfers k1 1 2 2147483648"), case(H, "ten digits", "ada POST /transfers k1 1 2 1000000000"), case(H, "garbage after valid requests", "ada GET /accounts/1", "ada POST /transfers k1 1 2 99999999999999999999", "ada GET /accounts/1"),
    case(AUD, "the oversized request is logged as a 400", "ada POST /transfers k1 1 2 99999999999"),
]
FNS = {"handleAll": model, "auditLines": audit}
MS_ALL = SIG_H + SIG_A
ms = []
for mid, title, text, vis, hid in [
    ("m1", "Change 1: a new requirement", """
         The partner's API can only read accounts. Product now wants **transfers**: `actor POST /transfers key from to cents`. Rules, in this order: a malformed body (four words, or five with the last one `crash`, and `cents` 1 to 9 digits) is `400|Bad Request`; unknown or identical accounts or an amount of zero is `400|Bad Request`; the actor must own the `from` account, or be the teller `tess`, otherwise `403|Forbidden`; not enough money is `422|Insufficient funds`; otherwise move the money and answer `200|` followed by all balances as `id:balance` separated by `;` in id order. Other methods on `/transfers` are `405|Method Not Allowed`. (Ignore `crash` and repeated keys for now; later changes handle them.)
         """, M1V, M1H),
    ("m2", "Change 2: make it reliable", """
         Apply lessons 10.2.2 and 10.2.3. The `key` is an idempotency key: the first request with a key is processed and its response stored; the same key with the same body returns the stored response; the same key with a different body is `409|Conflict`. Invalid, forbidden and malformed requests are not stored. A transfer ending in `crash` (the credit step fails) must leave the balances unchanged, answer `502|Credit failed, debit reversed`, and must **not** store the key.
         """, M2V, M2H),
    ("m3", "Change 3: make it observable", """
         Apply lessons 12.1.1 and 8.1.4. First, `GET /health` answers `200|ok` for **anybody**, signed in or not; other methods on it are `405|Method Not Allowed`. Second, `auditLines(requests)` returns one structured JSON line per request, after handling them in order: `{"actor":"ada","method":"GET","path":"/accounts/1","status":200}` with no spaces, exactly those four members in that order, the status as a number, and `"` and `\\` escaped inside the strings. Missing parts of a short request are empty strings. **Never log the body**: transfer keys and amounts do not belong in an audit line.
         """, M3V, M3H),
    ("m4", "Change 4: the incident", """
         At 03:12 the on-call phone rings: `POST /transfers` with an amount of `99999999999` made the service answer `500` and fill the logs with stack traces; at 03:20 someone found that it is the same for any amount with more than nine digits. The cause is in the input check. Fix it so that any amount that is not 1 to 9 digits is a `400|Bad Request`, keep every earlier behaviour, and then answer the questions in the design note. Do not hide the failure behind a catch-all.
         """, M4V, M4H)]:
    ms.append(dict(id=mid, title=title, methods=MS_ALL, fns=FNS, instructions=text, visible=vis, hidden=hid))
RUBRIC = [
    ("Correctness and tests", "Changes break earlier behaviour, or only the visible checks pass", "All checks pass but the changes were made in one step", "Each change made separately with all checks run after it; the code handles the cases the hidden checks probe"),
    ("Security and reliability", "Ownership, idempotency or compensation is missing or inconsistent", "Each present but a gap remains (a stored key on a crash, a body in a log)", "Ownership is checked before funds, keys are stored only for definite outcomes, a crash is compensated, and nothing sensitive is logged"),
    ("Operability", "Health and audit lines are missing or leak data", "They work but are not structured or escaped", "A health endpoint with no login, structured audit lines with escaping, and the incident fixed at its cause"),
    ("Written justification", "Missing, or repeats the code", "Describes what was done without alternatives or evidence", "ADRs for the two significant decisions, a blameless post-incident review with timeline, cause, fix and follow-ups, and honest limits of the model"),
]
project("j12-a1-capstone", "Capstone: take over, change, operate", "C",
        "Take over an acquired company's API and carry it through four changes: a new requirement, reliability, observability and a production incident; then justify your decisions in writing.",
        """
        This is the last project. There is no tutorial for it. You inherit a small account API from a company Brightbank has acquired. It reads accounts and nothing more. Over four changes you will make it do what the business needs and then deal with the consequences:

        1. A **new requirement**: transfers between accounts.
        2. **Reliability**: retries must not repeat a transfer; a failed credit must not lose money.
        3. **Observability**: a health endpoint and structured audit lines that leak nothing.
        4. An **incident**: an input that crashes the service.

        Change one thing at a time and run all the checks after each. Your written note is part of the assessment: two decision records and a post-incident review. The platform cannot run a real service, a database or a pipeline, so the project models the API logic; say in your note what a real deployment would add.
        """, 8, ["j7-l3.2", "j8-l2.3", "j10-l2.2", "j10-l2.3", "j12-l1.1", "j12-l1.4"], ["J7.09", "J8.07", "J10.05", "J10.06", "J12.01", "J12.04"],
        ["Transfers follow the rules of the first change, then the reliability rules, then the observability rules.",
         "An oversized amount is a 400, never a 500.",
         "Nothing sensitive is written to an audit line."],
        ["Change one thing at a time.", "Run all the checks after every change.", "Do not catch everything and hide it."],
        ["Given another customer's account, then 403.",
         "Given a retried transfer, then the same response and one effect.",
         "Given a crash, then the balances are unchanged and a retry works.",
         "Given an amount with ten digits, then 400."],
        ms, RUBRIC,
        "Write (400 words or fewer, three parts). (1) Two short ADRs (Title, Status, Context, Decision, Consequences): one for how you made transfers safe to retry, one for your choice of what the audit line contains and omits. (2) A blameless post-incident review of change 4: timeline (03:12, 03:20, your fix), cause, why the checks of the earlier changes did not catch it, what you fixed, and two follow-up actions with an owner each (for example an alert, a test). (3) Three things this model does not cover that a real deployment of this API would need (name at least one from each of Stage 8, Stage 10 and Stage 11).",
        INHERITED + MAIN, FINAL + MAIN, {k: v + MAIN for k, v in WRONGS.items()})
print("P16 written")
