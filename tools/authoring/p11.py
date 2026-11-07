"""Stage 7 projects: j7-p1-brightbank-api (B) and j7-a1-inherited-api (C).
A plain-Java request handler models the API layer; Spring cannot run in the single-file runner.
Expected values come from the Python models below, not from the Java."""
import re
import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-7"
from proj import project

MAIN = "\nvoid main() {\n    // Optional: try your handler here.\n}\n"
SIG = [("handleAll", [("requests", "List<String>")], "List<String>")]
NF, MNA, BR = "404|Not Found", "405|Method Not Allowed", "400|Bad Request"


# ------------------------------------------------------------------ Python models
def valid_pair(body):
    f = body.split(";")
    return (f[0], f[1]) if len(f) == 2 and f[0].strip() != "" and re.fullmatch(r"[0-9]{1,9}", f[1]) else None


def model_b(requests):
    acc = {1: ("Ada Lovelace", 120000), 2: ("Grace Hopper", 30050)}
    nxt, out = 3, []
    for r in requests:
        parts = r.split(" ", 2)
        method = parts[0]
        path = parts[1] if len(parts) > 1 else ""
        body = parts[2] if len(parts) > 2 else ""
        p = path.split("/")
        if len(p) < 2 or p[0] != "" or p[1] != "accounts":
            out.append(NF); continue
        if len(p) == 2:
            if method == "GET":
                out.append("200|" + ",".join(str(i) for i in sorted(acc)))
            elif method == "POST":
                v = valid_pair(body)
                if not v:
                    out.append(BR)
                else:
                    acc[nxt] = (v[0], int(v[1])); out.append(f"201|/accounts/{nxt}"); nxt += 1
            else:
                out.append(MNA)
            continue
        if not re.fullmatch(r"[0-9]+", p[2]):
            out.append(NF); continue
        i = int(p[2])
        if len(p) == 3:
            if method == "GET":
                out.append(f"200|{i};{acc[i][0]};{acc[i][1]}" if i in acc else NF)
            elif method == "DELETE":
                if i in acc:
                    del acc[i]; out.append("204|")
                else:
                    out.append(NF)
            elif method == "PUT":
                v = valid_pair(body)
                if not v:
                    out.append(BR)
                else:
                    created = i not in acc
                    acc[i] = (v[0], int(v[1])); nxt = max(nxt, i + 1)
                    out.append(f"{201 if created else 200}|{i};{v[0]};{acc[i][1]}")
            else:
                out.append(MNA)
            continue
        if len(p) == 4 and p[3] == "deposit":
            if method != "POST":
                out.append(MNA)
            elif i not in acc:
                out.append(NF)
            elif not re.fullmatch(r"[0-9]{1,9}", body) or int(body) <= 0:
                out.append(BR)
            else:
                acc[i] = (acc[i][0], acc[i][1] + int(body)); out.append(f"200|{acc[i][1]}")
            continue
        out.append(NF)
    return out


def model_c(requests):
    acc = {1: ("Ada Lovelace", 120000), 2: ("Grace Hopper", 30050)}
    nxt, out = 3, []
    for r in requests:
        parts = r.split(" ", 2)
        method, path = parts[0], parts[1]
        body = parts[2] if len(parts) > 2 else ""
        if path == "/accounts":
            if method == "GET":
                out.append("200|" + ",".join(str(i) for i in sorted(acc)))
            elif method == "POST":
                v = valid_pair(body)
                if not v:
                    out.append(BR)
                else:
                    acc[nxt] = (v[0], int(v[1])); out.append(f"201|/accounts/{nxt}"); nxt += 1
            else:
                out.append(MNA)
        elif re.fullmatch(r"/accounts/[0-9]+", path):
            i = int(path.split("/")[2])
            if method == "GET":
                out.append(f"200|{i};{acc[i][0]};{acc[i][1]}" if i in acc else NF)
            else:
                out.append(MNA)
        else:
            out.append(NF)
    return out


# ------------------------------------------------------------------ Java: B solution
B_SOL = '''
// Brightbank's API layer as a plain-Java request handler. Each request is "METHOD path body" (the body may be absent).
// Each response is "status|body". Two accounts exist at the start; money is whole cents.

List<String> handleAll(List<String> requests) {
    Map<Integer, String[]> accounts = new TreeMap<>();
    accounts.put(1, new String[] {"Ada Lovelace", "120000"});
    accounts.put(2, new String[] {"Grace Hopper", "30050"});
    int[] nextId = {3};
    List<String> responses = new ArrayList<>();
    for (String request : requests) {
        responses.add(handle(request, accounts, nextId));
    }
    return responses;
}

String handle(String request, Map<Integer, String[]> accounts, int[] nextId) {
    String[] parts = request.split(" ", 3);
    String method = parts[0];
    String path = parts.length > 1 ? parts[1] : "";
    String body = parts.length > 2 ? parts[2] : "";
    String[] p = path.split("/", -1);
    if (p.length < 2 || !p[0].isEmpty() || !p[1].equals("accounts")) {
        return "404|Not Found";
    }
    if (p.length == 2) {
        return switch (method) {
            case "GET" -> "200|" + String.join(",", accounts.keySet().stream().map(String::valueOf).toList());
            case "POST" -> create(body, accounts, nextId);
            default -> "405|Method Not Allowed";
        };
    }
    if (!p[2].matches("[0-9]+")) {
        return "404|Not Found";
    }
    int id = Integer.parseInt(p[2]);
    if (p.length == 3) {
        return switch (method) {
            case "GET" -> accounts.containsKey(id) ? "200|" + describe(id, accounts) : "404|Not Found";
            case "DELETE" -> accounts.remove(id) != null ? "204|" : "404|Not Found";
            case "PUT" -> replace(id, body, accounts, nextId);
            default -> "405|Method Not Allowed";
        };
    }
    if (p.length == 4 && p[3].equals("deposit")) {
        return method.equals("POST") ? deposit(id, body, accounts) : "405|Method Not Allowed";
    }
    return "404|Not Found";
}

String[] parseAccount(String body) {
    String[] fields = body.split(";", -1);
    if (fields.length != 2 || fields[0].isBlank() || !fields[1].matches("[0-9]{1,9}")) {
        return null;
    }
    return fields;
}

String describe(int id, Map<Integer, String[]> accounts) {
    return id + ";" + accounts.get(id)[0] + ";" + accounts.get(id)[1];
}

String create(String body, Map<Integer, String[]> accounts, int[] nextId) {
    String[] fields = parseAccount(body);
    if (fields == null) {
        return "400|Bad Request";
    }
    int id = nextId[0]++;
    accounts.put(id, new String[] {fields[0], String.valueOf(Integer.parseInt(fields[1]))});
    return "201|/accounts/" + id;
}

String replace(int id, String body, Map<Integer, String[]> accounts, int[] nextId) {
    String[] fields = parseAccount(body);
    if (fields == null) {
        return "400|Bad Request";
    }
    boolean created = !accounts.containsKey(id);
    accounts.put(id, new String[] {fields[0], String.valueOf(Integer.parseInt(fields[1]))});
    nextId[0] = Math.max(nextId[0], id + 1);
    return (created ? "201|" : "200|") + describe(id, accounts);
}

String deposit(int id, String body, Map<Integer, String[]> accounts) {
    if (!accounts.containsKey(id)) {
        return "404|Not Found";
    }
    if (!body.matches("[0-9]{1,9}") || Integer.parseInt(body) <= 0) {
        return "400|Bad Request";
    }
    long balance = Long.parseLong(accounts.get(id)[1]) + Integer.parseInt(body);
    accounts.get(id)[1] = String.valueOf(balance);
    return "200|" + balance;
}
'''
B_STARTER = '''
// Brightbank's API layer as a plain-Java request handler. Each request is "METHOD path body" (the body may be absent).
// Each response is "status|body". Two accounts exist at the start: 1 = Ada Lovelace (120000 cents) and
// 2 = Grace Hopper (30050 cents). Requests are handled in order against the same data.
//
// Milestone 1: routing and reads.   Milestone 2: create and delete.   Milestone 3: replace and deposit.

List<String> handleAll(List<String> requests) {
    List<String> responses = new ArrayList<>();
    for (String request : requests) {
        responses.add("404|Not Found");
    }
    return responses;
}
'''


def wrong(old, new, source=B_SOL):
    assert old in source, old
    return source.replace(old, new, 1)


B_WRONGS = {
    "m1-no-405": wrong('default -> "405|Method Not Allowed";\n        };\n    }\n    if (!p[2]', 'default -> "404|Not Found";\n        };\n    }\n    if (!p[2]'),
    "m1-nonnumeric-id-crashes": wrong('    if (!p[2].matches("[0-9]+")) {\n        return "404|Not Found";\n    }\n', ""),
    "m2-create-is-200": wrong('return "201|/accounts/" + id;', 'return "200|/accounts/" + id;'),
    "m2-blank-owner-accepted": wrong("fields[0].isBlank() || ", ""),
    "m2-delete-is-200": wrong('accounts.remove(id) != null ? "204|"', 'accounts.remove(id) != null ? "200|"'),
    "m2-id-reused-after-delete": wrong("int id = nextId[0]++;", "int id = accounts.size() + 3;"),
    "m3-put-always-201": wrong('(created ? "201|" : "200|")', '"201|"'),
    "m3-negative-deposit-accepted": wrong(' || Integer.parseInt(body) <= 0', ""),
    "m3-put-collides-with-next-id": wrong("    nextId[0] = Math.max(nextId[0], id + 1);\n", ""),
}


def seq(*requests):
    return (list(requests),)


def case(f, name, *requests):
    return ("handleAll", (list(requests),), name)


R1 = [
    ("reads", ["GET /accounts", "GET /accounts/1", "GET /accounts/2"]),
    ("missing", ["GET /accounts/9", "GET /accounts/abc", "GET /customers", "GET /accounts/"]),
    ("wrong method", ["DELETE /accounts", "PUT /accounts", "POST /accounts/1", "PATCH /accounts/1", "POST /accounts/1/deposit x"]),
]
R1_HIDDEN = R1 + [
    ("sub-resource path", ["GET /accounts/1/deposit", "GET /accounts/1/other", "GET /accounts/1/deposit/"]),
    ("empty and odd paths", ["GET ", "GET /", "GET /accounts/007"]),
    ("many reads", ["GET /accounts", "GET /accounts/1", "GET /accounts/9", "DELETE /accounts"]),
]
R2 = [
    ("create one", ["POST /accounts Alan Turing;500", "GET /accounts", "GET /accounts/3"]),
    ("bad bodies", ["POST /accounts ;5", "POST /accounts Alan;abc", "POST /accounts Alan", "POST /accounts Alan;1;2", "POST /accounts"]),
    ("delete", ["DELETE /accounts/1", "GET /accounts", "DELETE /accounts/1", "GET /accounts/1"]),
]
R2_HIDDEN = R2 + [
    ("ids are not reused", ["POST /accounts A;1", "DELETE /accounts/3", "POST /accounts B;2", "GET /accounts"]),
    ("a failed create takes no id", ["POST /accounts ;1", "POST /accounts C;3", "GET /accounts"]),
    ("zero balance", ["POST /accounts Zed;0", "GET /accounts/3"]),
    ("too big a number", ["POST /accounts Big;1234567890", "GET /accounts"]),
    ("delete twice", ["DELETE /accounts/2", "DELETE /accounts/2"]),
]
R3 = [
    ("replace and create", ["PUT /accounts/1 Ada L;7", "PUT /accounts/10 New Person;9", "GET /accounts"]),
    ("deposit", ["POST /accounts/1/deposit 500", "POST /accounts/1/deposit 25", "GET /accounts/1"]),
    ("deposit errors", ["POST /accounts/9/deposit 5", "POST /accounts/1/deposit 0", "POST /accounts/1/deposit abc", "POST /accounts/1/deposit -5"]),
]
R3_HIDDEN = R3 + [
    ("bad replace", ["PUT /accounts/1 ;5", "PUT /accounts/1 X;y", "PUT /accounts/1"]),
    ("the next id follows a replace", ["PUT /accounts/5 Five;5", "POST /accounts Six;6", "GET /accounts"]),
    ("deposit on a deleted account", ["DELETE /accounts/2", "POST /accounts/2/deposit 5"]),
    ("deposit method", ["GET /accounts/1/deposit", "PUT /accounts/1/deposit 5"]),
    ("replace keeps leading digits out", ["PUT /accounts/2 Grace;00042", "GET /accounts/2"]),
]


def build_tests(rows, model):
    return [("handleAll", (reqs,), name) for name, reqs in rows]


def ms_b():
    ms = []
    for mid, title, text, vis, hid in [
        ("m1", "Routing and reads", """
         Make `handleAll` answer these, one response per request, in order:

         - `GET /accounts` → `200|1,2` (the ids, comma separated, ascending).
         - `GET /accounts/{id}` → `200|id;owner;cents`, or `404|Not Found` when there is no such account.
         - A path that is not an accounts path, or has a non-numeric id, or has extra segments that do not exist → `404|Not Found`.
         - A path that exists but with a method it does not support → `405|Method Not Allowed`.

         The paths that exist are `/accounts`, `/accounts/{id}` and `/accounts/{id}/deposit`. Use the routing you wrote in lesson 7.1.4.
         """, R1, R1_HIDDEN),
        ("m2", "Create and delete", """
         - `POST /accounts owner;cents` creates an account with the next free id (3, then 4, ...) and answers `201|/accounts/ID`.
         - A body that is not `owner;cents`, a blank owner, or cents that are not 1 to 9 digits → `400|Bad Request`, and no id is used up.
         - `DELETE /accounts/{id}` → `204|` (nothing after the bar), or `404|Not Found`.
         - Ids are never reused.
         """, R2, R2_HIDDEN),
        ("m3", "Replace and deposit", """
         - `PUT /accounts/{id} owner;cents` replaces the account (`200|id;owner;cents`) or creates it with that id (`201|id;owner;cents`). The next id for a `POST` must stay above every id in use.
         - `POST /accounts/{id}/deposit cents` adds the cents (1 to 9 digits, above zero) and answers `200|newBalance`. An unknown account is `404|Not Found`, a bad amount `400|Bad Request`.
         - Any other method on `/accounts/{id}/deposit` is `405|Method Not Allowed`.
         """, R3, R3_HIDDEN),
    ]:
        ms.append(dict(id=mid, title=title, methods=SIG, fns={"handleAll": model_b}, instructions=text,
                       visible=build_tests(vis, model_b), hidden=build_tests(hid, model_b)))
    return ms


RUBRIC_B = [
    ("Correct HTTP semantics", "Status codes are wrong or inconsistent", "Mostly right, with confusion between 400, 404 and 405", "Every status follows RFC 9110 and the task, including 201, 204 and 405"),
    ("Routing", "Paths are matched with string checks that break on odd input", "Works for normal paths", "A clear routing structure that treats unknown paths, bad ids and wrong methods differently"),
    ("Validation and state", "Bad input changes state, or ids are reused", "Bad input is rejected, but one state rule is missed", "Failed requests change nothing, and ids stay unique"),
    ("Design note", "Missing or only describes the code", "Explains the code but not the choices", "Explains how each response maps to the lessons' rules and what the real Spring annotations would be"),
]
project("j7-p1-brightbank-api", "Brightbank's REST API", "B",
        "Build the request handling of a small accounts API in plain Java: routing, status codes, validation and state.",
        """
        Brightbank needs an HTTP API for its accounts. In this course the platform cannot run Spring, so you write the part Spring's controllers would do: look at each request (`METHOD path body`), decide what it means, change the data and return `status|body`.

        1. **Routing and reads**: tell a missing resource (404) from a wrong method (405).
        2. **Create and delete**: validate input, answer 201 and 204 honestly, and never reuse an id.
        3. **Replace and deposit**: the idempotent PUT and the non-idempotent POST.

        Requests in one call are handled in order, against the same data, which starts with two accounts.
        """, 4, ["j7-l1.4", "j7-l3.1", "j7-l3.2", "j7-l3.3"], ["J7.02", "J7.03", "J7.04", "J7.08", "J7.09"],
        ["Every response status is the one RFC 9110 and the task describe.",
         "Unknown paths, bad ids and wrong methods get different responses.",
         "A rejected request changes no data."],
        ["Plain Java only: no framework is available.", "Handle requests in the order given."],
        ["Given a missing account, then 404; given a wrong method on an existing path, then 405.",
         "Given a bad body, then 400 and no id is used.",
         "Given a repeated PUT, then the account is unchanged by the repeat."],
        ms_b(), RUBRIC_B,
        "In 150 words or fewer: Which of your responses did you have to decide between 400, 404 and 405, and how did you choose? Write the Spring annotations you would use for the `PUT /accounts/{id}` and `POST /accounts/{id}/deposit` handlers, and say which of the two a client may safely retry and why.",
        B_STARTER + MAIN, B_SOL + MAIN, {k: v + MAIN for k, v in B_WRONGS.items()})

# ------------------------------------------------------------------ C: inherited API
C_INHERITED = '''
// INHERITED CODE: the request handler of an older accounts API. Each request is "METHOD path body".
// Ticket 701: "Creating an account answers 200. Clients expect 201."
// Ticket 702: "Asking for an account that does not exist crashes with a 500."

List<String> handleAll(List<String> requests) {
    Map<Integer, String[]> accounts = new TreeMap<>();
    accounts.put(1, new String[] {"Ada Lovelace", "120000"});
    accounts.put(2, new String[] {"Grace Hopper", "30050"});
    int nextId = 3;
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] parts = request.split(" ", 3);
        String method = parts[0];
        String path = parts[1];
        String body = parts.length > 2 ? parts[2] : "";
        try {
            if (path.equals("/accounts") && method.equals("GET")) {
                out.add("200|" + String.join(",", accounts.keySet().stream().map(String::valueOf).toList()));
            } else if (path.equals("/accounts") && method.equals("POST")) {
                String[] f = body.split(";", -1);
                if (f.length != 2 || f[0].isBlank() || !f[1].matches("[0-9]{1,9}")) {
                    out.add("400|Bad Request");
                } else {
                    accounts.put(nextId, new String[] {f[0], String.valueOf(Integer.parseInt(f[1]))});
                    out.add("200|/accounts/" + nextId);
                    nextId++;
                }
            } else if (path.startsWith("/accounts/") && method.equals("GET")) {
                int id = Integer.parseInt(path.substring("/accounts/".length()));
                String[] a = accounts.get(id);
                out.add("200|" + id + ";" + a[0] + ";" + a[1]);
            } else {
                out.add("404|Not Found");
            }
        } catch (Exception e) {
            out.add("500|Internal Server Error");
        }
    }
    return out;
}
'''
C_FINAL = '''
// The request handler of the accounts API. Each request is "METHOD path body".

List<String> handleAll(List<String> requests) {
    Map<Integer, String[]> accounts = new TreeMap<>();
    accounts.put(1, new String[] {"Ada Lovelace", "120000"});
    accounts.put(2, new String[] {"Grace Hopper", "30050"});
    int nextId = 3;
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] parts = request.split(" ", 3);
        String method = parts[0];
        String path = parts[1];
        String body = parts.length > 2 ? parts[2] : "";
        if (path.equals("/accounts")) {
            if (method.equals("GET")) {
                out.add("200|" + String.join(",", accounts.keySet().stream().map(String::valueOf).toList()));
            } else if (method.equals("POST")) {
                String[] f = body.split(";", -1);
                if (f.length != 2 || f[0].isBlank() || !f[1].matches("[0-9]{1,9}")) {
                    out.add("400|Bad Request");
                } else {
                    accounts.put(nextId, new String[] {f[0], String.valueOf(Integer.parseInt(f[1]))});
                    out.add("201|/accounts/" + nextId);
                    nextId++;
                }
            } else {
                out.add("405|Method Not Allowed");
            }
        } else if (path.matches("/accounts/[0-9]{1,9}")) {
            int id = Integer.parseInt(path.substring("/accounts/".length()));
            if (!method.equals("GET")) {
                out.add("405|Method Not Allowed");
            } else if (!accounts.containsKey(id)) {
                out.add("404|Not Found");
            } else {
                out.add("200|" + id + ";" + accounts.get(id)[0] + ";" + accounts.get(id)[1]);
            }
        } else {
            out.add("404|Not Found");
        }
    }
    return out;
}
'''
C_WRONGS = {
    "m1-still-200": wrong('out.add("201|/accounts/" + nextId);', 'out.add("200|/accounts/" + nextId);', C_FINAL),
    "m2-missing-is-200": wrong('} else if (!accounts.containsKey(id)) {\n                out.add("404|Not Found");', '} else if (!accounts.containsKey(id)) {\n                out.add("200|");', C_FINAL),
    "m2-bad-id-crashes": wrong('path.matches("/accounts/[0-9]{1,9}")', 'path.startsWith("/accounts/")', C_FINAL),
    "m3-wrong-method-is-404": wrong('out.add("405|Method Not Allowed");\n            }\n        } else if', 'out.add("404|Not Found");\n            }\n        } else if', C_FINAL),
    "m3-wrong-method-on-item-is-404": wrong('if (!method.equals("GET")) {\n                out.add("405|Method Not Allowed");', 'if (!method.equals("GET")) {\n                out.add("404|Not Found");', C_FINAL),
}
C1 = [("create", ["POST /accounts Alan Turing;500", "GET /accounts"]), ("created id in the response", ["POST /accounts Zed;5", "POST /accounts Amy;6"]), ("bad body", ["POST /accounts ;5", "POST /accounts Zed;abc"])]
C1H = C1 + [("create then read", ["POST /accounts Alan;9", "GET /accounts/3"]), ("blank owner", ["POST /accounts   ;5"]), ("reads still work", ["GET /accounts", "GET /accounts/1"])]
C2 = [("missing account", ["GET /accounts/9"]), ("non-numeric id", ["GET /accounts/abc"]), ("extra segment", ["GET /accounts/1/deposit"])]
C2H = C2 + C1H + [("a huge id", ["GET /accounts/12345678901234"]), ("empty id", ["GET /accounts/"]), ("two missing", ["GET /accounts/3", "GET /accounts/4"])]
C3 = [("delete the collection", ["DELETE /accounts"]), ("delete an account", ["DELETE /accounts/1"]), ("post to an account", ["POST /accounts/1 x;1"])]
C3H = C3 + C2H + [("put on a missing account", ["PUT /accounts/9 x;1"]), ("patch", ["PATCH /accounts"]), ("delete a missing account", ["DELETE /accounts/9"]), ("unknown path", ["GET /nothing", "DELETE /nothing"])]
ms_c = []
for mid, title, text, vis, hid in [
    ("m1", "Ticket 701: created is 201", """
     **Ticket 701:** *"Creating an account answers `200`. Clients expect `201 Created` with the new address."*

     Reproduce it with `POST /accounts Alan Turing;500`, find the cause and make the smallest fix. Leave everything else as it is.
     """, C1, C1H),
    ("m2", "Ticket 702: a missing account is a 404", """
     **Ticket 702:** *"Asking for an account that does not exist, or for `/accounts/abc`, crashes with a 500."*

     A missing resource is a `404 Not Found`. Fix the cause (not by hiding it behind a catch-all), and keep every earlier answer the same.
     """, C2, C2H),
    ("m3", "Review: 405 for the wrong method", """
     The reviewer writes:

     > *"`DELETE /accounts/1` answers 404, as if the address did not exist. It exists; it just does not allow that method. RFC 9110 has a status for this."*

     A known path with a method it does not support answers `405|Method Not Allowed`. The known paths are `/accounts` (GET, POST) and `/accounts/{id}` (GET). Anything else is still a 404.
     """, C3, C3H)]:
    ms_c.append(dict(id=mid, title=title, methods=SIG, fns={"handleAll": model_c}, instructions=text,
                     visible=build_tests(vis, model_c), hidden=build_tests(hid, model_c)))
RUBRIC_C = [
    ("Reproduce, then fix", "Changed code without reproducing the ticket", "Fixed it but did not show the failing request first", "Reproduced each ticket with a specific request, found the cause, made the smallest fix"),
    ("Fixing the cause", "Hid the crash behind a catch-all or a default value", "Fixed the symptom for one input", "Fixed the cause, so bad ids and missing accounts are both 404"),
    ("Handling review", "Ignored the comment, or broke an earlier answer", "Added 405 but changed another response", "405 for known paths, 404 for unknown ones, every earlier check still passing"),
    ("Design note", "Missing or only describes the code", "Describes the changes but not the reasoning", "Explains the difference between 404 and 405 and why a catch-all 500 hides bugs"),
]
project("j7-a1-inherited-api", "The API that cried 500", "C",
        "Take over an inherited request handler: fix a wrong status, a crash that should be a 404, and answer a review about 405.",
        """
        You have inherited the request handler of an older accounts API. Two tickets and a review are waiting, and each is a mistake about HTTP: the wrong success status, an error reported as a server failure, and a missing method check.

        Fix them one at a time, running all the checks after each, and say in your design note what you would commit separately.
        """, 3, ["j7-l1.3", "j7-l1.4", "j7-l3.2"], ["J7.03", "J7.04", "J7.09"],
        ["Creating an account answers 201 with its address.",
         "A missing account, or a malformed id, answers 404 and never 500.",
         "A known path with an unsupported method answers 405."],
        ["Fix one ticket at a time.", "Run all the checks after every change."],
        ["Given a created account, then the status is 201.",
         "Given an unknown account or id, then 404.",
         "Given DELETE on a known path, then 405."],
        ms_c, RUBRIC_C,
        "In 150 words or fewer: What did each ticket's wrong response actually tell a client? Why is a catch-all that turns every exception into a 500 a problem? What is the difference between 404 and 405, and what header does a 405 need? What would your commits have been?",
        C_INHERITED + MAIN, C_FINAL + MAIN, {k: v + MAIN for k, v in C_WRONGS.items()})
print("P11 written")
