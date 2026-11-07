"""Stage 7 authoring: module 7.1 (HTTP and REST fundamentals). Expected values are computed here, not from Java."""
import re
import l7common
from l7common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex11 = Exercises("j7-l1.1")
ex12 = Exercises("j7-l1.2")
ex13 = Exercises("j7-l1.3")
ex14 = Exercises("j7-l1.4")

REGISTER = {
    "j7-l1.1": ("Requests, responses and headers", ["J7.01"]),
    "j7-l1.2": ("Methods, safety and idempotence", ["J7.02"]),
    "j7-l1.3": ("Status codes and problem details", ["J7.03"]),
    "j7-l1.4": ("Resource design and routing", ["J7.04"]),
}
MISCS = {
    "MC166": (["J7.01"], "I84", "A response status code is part of the body, so a client has to read the body to know whether a request worked"),
    "MC167": (["J7.02"], "I84", "POST and PUT are interchangeable ways to save data, so a client may retry either one freely"),
    "MC168": (["J7.03"], "I84", "Any failure can be reported as 200 with an error message in the body, or as a generic 500"),
    "MC169": (["J7.04"], "I84", "A URL names an action, so an API should have addresses like /getAccount and /deleteAccount"),
}
register(REGISTER, MISCS)

# ====================================================================== j7-l1.1
REQUEST_PROGRAM = r'''
void main() {
    String raw = "POST /api/accounts HTTP/1.1\r\nHost: bank.example\r\nContent-Type: application/json\r\nContent-Length: 15\r\n\r\n{\"owner\":\"Ada\"}";
    String[] parts = raw.split("\r\n\r\n", 2);
    String[] head = parts[0].split("\r\n");
    String[] line = head[0].split(" ");
    System.out.println("method=" + line[0]);
    System.out.println("target=" + line[1]);
    System.out.println("version=" + line[2]);
    System.out.println("headers=" + (head.length - 1));
    for (int i = 1; i < head.length; i++) {
        if (head[i].startsWith("Content-Type:")) {
            System.out.println("type=" + head[i].substring("Content-Type:".length()).trim());
        }
    }
    System.out.println("body chars=" + parts[1].length());
    System.out.println("length matches=" + (parts[1].length() == 15));
}
'''
# Derived by hand: the request line splits into POST, /api/accounts, HTTP/1.1; three header lines follow
# (Host, Content-Type, Content-Length); the body {"owner":"Ada"} is 15 characters.
REQUEST_EXPECTED = """method=POST
target=/api/accounts
version=HTTP/1.1
headers=3
type=application/json
body chars=15
length matches=true
"""

ex11.predict(
    "j7-l1.1-predict-request", "Reading a raw request", ["o1"], ["J7.01"],
    "The program below takes a raw HTTP request, exactly as it travels over the connection, and picks it apart. Predict the exact output.",
    REQUEST_PROGRAM, REQUEST_EXPECTED,
    ["Where does the request line end and where do the headers end?", "What separates the headers from the body?"],
    misconceptions=(), difficulty=1,
)


def f_request_line(line):
    parts = line.split(" ")
    if len(parts) == 3 and re.fullmatch(r"[A-Z]+", parts[0]) and parts[1] != "" and parts[2].startswith("HTTP/"):
        return "|".join(parts)
    return "invalid"


REQLINE_SOL = '''
String parseRequestLine(String line) {
    String[] parts = line.split(" ", -1);
    if (parts.length == 3 && parts[0].matches("[A-Z]+") && !parts[1].isEmpty() && parts[2].startsWith("HTTP/")) {
        return String.join("|", parts);
    }
    return "invalid";
}
'''
REQLINE_REGEX = REQLINE_SOL.replace('line.split(" ", -1)', 'line.trim().split("\\\\s+")')
REQLINE_ANYCASE = REQLINE_SOL.replace('parts[0].matches("[A-Z]+")', '!parts[0].isEmpty()')
REQLINE_NOVERSION = REQLINE_SOL.replace(' && parts[2].startsWith("HTTP/")', "")

ex11.method(
    "write", "j7-l1.1-write-requestline", "The request line", ["o1"], ["J7.01"], ["IMPL"],
    "Write `parseRequestLine(line)`. A valid request line is a method of capital letters, a target and a version that starts with `HTTP/`, separated by single spaces. Return `METHOD|target|version`, or `invalid` for anything else.",
    [("parseRequestLine", [("line", "String")], "String")], {"parseRequestLine": f_request_line},
    [("parseRequestLine", ("GET /api/curriculum HTTP/1.1",), "a normal request line"),
     ("parseRequestLine", ("POST /api/accounts HTTP/1.1",), "a POST"),
     ("parseRequestLine", ("GET /x",), "the version is missing")],
    [("parseRequestLine", ("GET  /x HTTP/1.1",), "two spaces are not allowed"),
     ("parseRequestLine", ("get /x HTTP/1.1",), "the method is capitals"),
     ("parseRequestLine", ("",), "an empty line"),
     ("parseRequestLine", ("GET /x HTTP/2",), "another HTTP version"),
     ("parseRequestLine", ("GET /x FTP/1.0",), "not HTTP"),
     ("parseRequestLine", ("G3T /x HTTP/1.1",), "a digit in the method"),
     ("parseRequestLine", ("DELETE /api/accounts/7 HTTP/1.1",), "a longer target")],
    starter='''
String parseRequestLine(String line) {
    return "";
}
''', solution=REQLINE_SOL,
    wrongs={"any-whitespace": REQLINE_REGEX, "any-case-method": REQLINE_ANYCASE, "no-version-check": REQLINE_NOVERSION},
    hints=["How many parts should the line split into?", "Which check rejects `FTP/1.0`?"],
    misconceptions=(), difficulty=2,
)

RESPONSE_CAPTURE = cap("cap_get_curriculum.txt")
ex11.explain(
    "j7-l1.1-explain-response", "Reading a real response", ["o1", "o2"], ["J7.01"],
    "This is the start of a real response from this platform's own API, captured with `curl -i`. Say what the status line tells a client, what two of the headers are for, and why a client should check the status before reading the body.\n\n" + fence(RESPONSE_CAPTURE),
    "The status line gives the protocol version, a three-digit status code and a reason phrase, and the code tells the client whether the request worked. Headers are name/value metadata: Content-Type says how to read the body. A client must check the status first because an error response also has a body, with a different shape.",
    levels={
        2: ("The answer reads the status line, explains two headers and says why status comes first.", [
            "The status line says HTTP/1.1 200, so the request worked. Content-Type: application/json says the body is JSON, and another header describes the connection or cache. A 404 or 500 also has a body, in a different format, so the client checks the status before parsing.",
            "200 means success. Content-Type tells the client how to decode the body and Content-Length or Transfer-Encoding says how much body there is. If it skipped the status it could parse an error page as if it were the data."]),
        1: ("The answer reads the status or a header but not why the status is checked first.", [
            "200 means OK, and Content-Type says it is JSON.",
            "It is a success response with some headers and then JSON."]),
        0: ("The answer treats the status as part of the body or ignores headers.", [
            "The body is what matters, the status and headers are just decoration.",
            "The client reads the JSON to find out whether it worked."]),
    },
)

l7_l1_1 = Lesson("j7-l1.1", "Requests, responses and headers", ["J7.01"], [
    ("o1", "Pick a raw HTTP request apart into request line, headers and body"),
    ("o2", "Read a real response: status line, headers and body"),
], ["j6-l3.2"], 40, ["I84"], """## Before you start

You should be comfortable with strings and splitting text, and you should know what a database row looks like from Stage 6.

## Explanation

HTTP is a text protocol for a client to ask a server for something and for the server to answer. One exchange is a **request** and a **response**.

A request has a **request line** (method, target, version), then **header** lines (a name, a colon, a value), then an empty line, then an optional **body**. A response has a **status line** (version, a three-digit status code, a reason phrase), headers, an empty line and a body.

The status code is how the client learns whether the request worked, so it is read before the body. An error response has a body too, but its shape differs from a success body.

## Worked examples

### Example 1: a request, as it travels.

```text
POST /api/accounts HTTP/1.1
Host: bank.example
Content-Type: application/json
Content-Length: 15

{"owner":"Ada"}
```

### Example 2: a real response from this platform.

Captured with `curl -i` against this platform's own API (the `Set-Cookie` lines were removed and the body was cut for length):

""" + fence(RESPONSE_CAPTURE) + """

## Where this is used

- Every browser, every mobile app and every service-to-service call. A Spring controller is, in the end, code that turns a request like the one above into a response like this one.

## Common mistakes

:::mistake{id=MC166}
**Reading the body to find out whether it worked.** The status code answers that. An error has a body too, and it is not shaped like the data.
:::

## Practice

::exercise{id=j7-l1.1-predict-request}

::exercise{id=j7-l1.1-write-requestline}

::exercise{id=j7-l1.1-explain-response}

## Further reading

- **RFC 9110, HTTP Semantics** `[I84]`, the specification of methods, headers and status codes.

## How you'll be assessed

- The **predict** exercise checks that you can pick a request apart (*identifying*).
- The **write** exercise checks that you can validate a request line (*implementation*).
- The **explain** exercise checks that you can read a real response (*explanation*).
""")

# ====================================================================== j7-l1.2
SAFE = {"GET", "HEAD", "OPTIONS", "TRACE"}
IDEMP = {"PUT", "DELETE"}


def f_properties(method):
    if method in SAFE:
        return "safe+idempotent"
    if method in IDEMP:
        return "idempotent"
    if method in ("POST", "CONNECT"):
        return "neither"
    return "unknown"


PROPS_SOL = '''
String properties(String method) {
    return switch (method) {
        case "GET", "HEAD", "OPTIONS", "TRACE" -> "safe+idempotent";
        case "PUT", "DELETE" -> "idempotent";
        case "POST", "CONNECT" -> "neither";
        default -> "unknown";
    };
}
'''
PROPS_POST_IDEMP = PROPS_SOL.replace('case "PUT", "DELETE" -> "idempotent";', 'case "PUT", "DELETE", "POST" -> "idempotent";').replace('case "POST", "CONNECT" -> "neither";', 'case "CONNECT" -> "neither";')
PROPS_DELETE_NOT = PROPS_SOL.replace('case "PUT", "DELETE" -> "idempotent";', 'case "PUT" -> "idempotent";').replace('case "POST", "CONNECT" -> "neither";', 'case "POST", "CONNECT", "DELETE" -> "neither";')
PROPS_LOWER = PROPS_SOL.replace("switch (method)", "switch (method.toUpperCase())")
PROPS_NO_TRACE = PROPS_SOL.replace('"GET", "HEAD", "OPTIONS", "TRACE"', '"GET", "HEAD", "OPTIONS"')

ex12.method(
    "write", "j7-l1.2-write-properties", "Safe, idempotent, or neither", ["o1"], ["J7.02"], ["IMPL"],
    "Write `properties(method)` for a method name in capitals, following RFC 9110. Return `safe+idempotent` for a safe method, `idempotent` for an idempotent method that is not safe, `neither` for POST and CONNECT, and `unknown` for any other text (including lower case).",
    [("properties", [("method", "String")], "String")], {"properties": f_properties},
    [("properties", ("GET",), "a read"), ("properties", ("PUT",), "replace"), ("properties", ("POST",), "create or process")],
    [("properties", ("DELETE",), "delete is idempotent"), ("properties", ("HEAD",), "safe"), ("properties", ("OPTIONS",), "safe"),
     ("properties", ("TRACE",), "safe"), ("properties", ("CONNECT",), "neither"), ("properties", ("get",), "lower case is unknown"),
     ("properties", ("FETCH",), "not a method"), ("properties", ("",), "empty")],
    starter='''
String properties(String method) {
    return "";
}
''', solution=PROPS_SOL,
    wrongs={"post-idempotent": PROPS_POST_IDEMP, "delete-not-idempotent": PROPS_DELETE_NOT, "case-insensitive": PROPS_LOWER, "forgets-trace": PROPS_NO_TRACE},
    hints=["Which methods does RFC 9110 call safe?", "Which methods are idempotent but not safe?"],
    misconceptions=("MC167",), difficulty=2,
)

RETRY_PROGRAM = '''
class Bank {
    int balance = 100;

    void put(int value) {
        balance = value;
    }

    void post(int amount) {
        balance += amount;
    }
}

void main() {
    Bank replaced = new Bank();
    replaced.put(150);
    replaced.put(150);
    Bank added = new Bank();
    added.post(50);
    added.post(50);
    System.out.println("after two PUTs=" + replaced.balance);
    System.out.println("after two POSTs=" + added.balance);
}
'''
# Derived by hand: put sets the balance to 150 twice (150); post adds 50 twice to 100 (200).
ex12.predict(
    "j7-l1.2-predict-retry", "Sending it twice", ["o2"], ["J7.02"],
    "A client sends a request, gets no answer, and sends the same request again. The model below treats a PUT as 'set the balance to this value' and a POST as 'add this amount'. Predict the exact output.",
    RETRY_PROGRAM, "after two PUTs=150\nafter two POSTs=200\n",
    ["What is the balance after the first PUT, and after the second?", "Which of the two requests would double-charge a customer if a client retried it?"],
    misconceptions=("MC167",), difficulty=1,
)

ex12.explain(
    "j7-l1.2-explain-retry", "Why retries care about the method", ["o2"], ["J7.02"],
    "A mobile app calls `POST /payments` and the connection drops before the response arrives. Explain why the app cannot simply retry, why a retry of `PUT /accounts/7` would be safe, and what an API designer can do so a payment can be retried.",
    "An idempotent method has the same effect when repeated; PUT and DELETE are idempotent, POST is not, so a repeated POST may create a second payment. A PUT sets the state to the representation sent, so repeating it changes nothing further. A designer can make the operation idempotent, for example with a client-chosen request identifier that the server remembers, so a duplicate is recognised.",
    levels={
        2: ("The answer separates idempotent from non-idempotent, explains the double payment and offers a remedy.", [
            "POST is not idempotent: if the first payment went through and only the response was lost, the retry creates a second one. PUT sets the account to the state sent, so doing it twice leaves the same state. To make payments retryable, the client sends a unique request id and the server returns the first result for a repeated id.",
            "A retried POST can charge twice because each POST may create something new. PUT and DELETE are defined as idempotent so repeating them is safe. The fix is an idempotency key: the server stores the key and ignores the duplicate."]),
        1: ("The answer says POST is unsafe to retry without saying why or how to fix it.", [
            "POST can create duplicates, PUT cannot.",
            "You should not retry a POST, but PUT is fine."]),
        0: ("The answer treats methods as interchangeable or blames the network.", [
            "POST and PUT do the same thing, so retrying either is fine.",
            "The network is unreliable, so the app should keep retrying until it succeeds."]),
    },
)

l7_l1_2 = Lesson("j7-l1.2", "Methods, safety and idempotence", ["J7.02"], [
    ("o1", "Classify an HTTP method as safe, idempotent or neither, following RFC 9110"),
    ("o2", "Explain why retrying a request depends on its method"),
], ["j7-l1.1"], 40, ["I84"], """## Before you start

You should be able to read a request line and know what a method is.

## Explanation

The **method** says what the client wants done. RFC 9110 defines properties of methods that matter in practice.

A method is **safe** if its defined semantics are essentially read-only: the client does not ask for, and does not expect, a state change. GET, HEAD, OPTIONS and TRACE are safe.

A method is **idempotent** if the intended effect of several identical requests is the same as the effect of one. PUT, DELETE and all the safe methods are idempotent. POST is not: two identical POSTs may do the work twice.

PUT asks for the target resource's state to be created or replaced with the state in the request, so sending it twice leaves the same state.

These properties are what let a client, a proxy or a load balancer decide whether it may repeat a request after a failure.

## Worked examples

### Example 1: replacing, twice.

`PUT /accounts/7` with `{"owner":"Ada"}` sets the account to that state. A second identical PUT changes nothing more.

### Example 2: adding, twice.

`POST /accounts/7/deposits` with `{"cents":5000}` adds a deposit each time. Two identical POSTs add two deposits.

## Where this is used

- Retry logic in clients and gateways. A safe, idempotent GET may be retried automatically; a POST may not.
- Designing an API: use PUT when the client knows the full state to set, POST when the server creates something.

## Common mistakes

:::mistake{id=MC167}
**Treating POST and PUT as two spellings of "save".** PUT can be repeated safely; POST usually cannot. The difference decides what happens on a retry.
:::

## Practice

::exercise{id=j7-l1.2-write-properties}

::exercise{id=j7-l1.2-predict-retry}

::exercise{id=j7-l1.2-explain-retry}

## Further reading

- **RFC 9110, HTTP Semantics** `[I84]`, sections on safe methods and idempotent methods.

## How you'll be assessed

- The **write** exercise checks that you can classify methods (*implementation*).
- The **predict** exercise checks that you can follow a repeated request (*identifying*).
- The **explain** exercise checks that you can reason about retries (*explanation*).
""")

# ====================================================================== j7-l1.3
def f_status(op, auth, exists, valid):
    if op not in ("GET", "POST", "PUT", "DELETE"):
        return 405
    if not auth:
        return 401
    if op == "GET":
        return 200 if exists else 404
    if op == "DELETE":
        return 204 if exists else 404
    if not valid:
        return 400
    if op == "POST":
        return 409 if exists else 201
    return 200 if exists else 201


STATUS_SOL = '''
int status(String op, boolean authenticated, boolean exists, boolean valid) {
    if (!List.of("GET", "POST", "PUT", "DELETE").contains(op)) {
        return 405;
    }
    if (!authenticated) {
        return 401;
    }
    return switch (op) {
        case "GET" -> exists ? 200 : 404;
        case "DELETE" -> exists ? 204 : 404;
        case "POST" -> !valid ? 400 : exists ? 409 : 201;
        default -> !valid ? 400 : exists ? 200 : 201;
    };
}
'''
STATUS_PUT_ALWAYS_201 = STATUS_SOL.replace("default -> !valid ? 400 : exists ? 200 : 201;", "default -> !valid ? 400 : 201;")
STATUS_DUP_400 = STATUS_SOL.replace("case \"POST\" -> !valid ? 400 : exists ? 409 : 201;", "case \"POST\" -> !valid || exists ? 400 : 201;")
STATUS_DELETE_200 = STATUS_SOL.replace('case "DELETE" -> exists ? 204 : 404;', 'case "DELETE" -> exists ? 200 : 404;')
STATUS_VALID_FIRST = STATUS_SOL.replace("    if (!authenticated) {\n        return 401;\n    }\n", "    if (!authenticated && valid) {\n        return 401;\n    }\n")

ex13.method(
    "write", "j7-l1.3-write-status", "Choosing the status code", ["o1"], ["J7.03"], ["IMPL"],
    "Write `status(op, authenticated, exists, valid)`, the status code an API returns. An op other than GET, POST, PUT or DELETE is `405`. Otherwise, a caller who is not authenticated gets `401`. Then: GET is `200` if the resource exists, else `404`. DELETE is `204` if it exists, else `404`. POST (create): an invalid body is `400`, a resource that already exists is `409`, otherwise `201`. PUT (replace or create): an invalid body is `400`, an existing resource is `200`, a new one is `201`.",
    [("status", [("op", "String"), ("authenticated", "boolean"), ("exists", "boolean"), ("valid", "boolean")], "int")], {"status": f_status},
    [("status", ("GET", True, True, True), "reading something that exists"),
     ("status", ("POST", True, False, True), "creating something new"),
     ("status", ("DELETE", True, False, True), "deleting something that is not there")],
    [("status", ("PUT", True, False, True), "PUT creates"), ("status", ("PUT", True, True, True), "PUT replaces"),
     ("status", ("PUT", True, True, False), "PUT with a bad body"), ("status", ("POST", True, True, True), "a duplicate"),
     ("status", ("POST", True, False, False), "a bad body"), ("status", ("DELETE", True, True, True), "delete works"),
     ("status", ("GET", False, True, True), "not signed in"), ("status", ("PATCH", True, True, True), "an unsupported method"),
     ("status", ("POST", False, False, False), "not signed in beats a bad body")],
    starter='''
int status(String op, boolean authenticated, boolean exists, boolean valid) {
    return 0;
}
''', solution=STATUS_SOL,
    wrongs={"put-always-201": STATUS_PUT_ALWAYS_201, "duplicate-is-400": STATUS_DUP_400, "delete-200": STATUS_DELETE_200, "bad-body-before-auth": STATUS_VALID_FIRST},
    hints=["Which check comes first: the method, then who is asking?", "What does RFC 9110 say a successful DELETE or a created resource returns?"],
    misconceptions=("MC168",), difficulty=3,
)


def json_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def f_problem(status, title, detail):
    return '{"type":"about:blank","title":"%s","status":%d,"detail":"%s"}' % (json_escape(title), status, json_escape(detail))


PROBLEM_SOL = '''
String problemJson(int status, String title, String detail) {
    return "{\\"type\\":\\"about:blank\\",\\"title\\":\\"" + escape(title) + "\\",\\"status\\":" + status
            + ",\\"detail\\":\\"" + escape(detail) + "\\"}";
}

String escape(String text) {
    return text.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\"");
}
'''
PROBLEM_NO_ESCAPE = PROBLEM_SOL.replace("escape(title)", "title").replace("escape(detail)", "detail")
PROBLEM_ORDER = PROBLEM_SOL.replace('''"{\\"type\\":\\"about:blank\\",\\"title\\":\\"" + escape(title) + "\\",\\"status\\":" + status
            + ",\\"detail\\":\\"" + escape(detail) + "\\"}"''', '''"{\\"type\\":\\"about:blank\\",\\"status\\":" + status + ",\\"title\\":\\"" + escape(title)
            + "\\",\\"detail\\":\\"" + escape(detail) + "\\"}"''')
PROBLEM_NO_TYPE = PROBLEM_SOL.replace('\\"type\\":\\"about:blank\\",', "")
PROBLEM_QUOTES_ONLY = PROBLEM_SOL.replace('.replace("\\\\", "\\\\\\\\")', "")

ex13.method(
    "write", "j7-l1.3-write-problem", "A problem detail body", ["o2"], ["J7.03"], ["IMPL"],
    "RFC 9457 defines a JSON error body with `type`, `title`, `status` and `detail`. Write `problemJson(status, title, detail)` returning exactly `{\"type\":\"about:blank\",\"title\":...,\"status\":...,\"detail\":...}` with no spaces, in that order, with `\"` and `\\` escaped inside the two strings. `status` is a JSON number.",
    [("problemJson", [("status", "int"), ("title", "String"), ("detail", "String")], "String")], {"problemJson": f_problem},
    [("problemJson", (404, "Not Found", "No account 7"), "a simple problem"),
     ("problemJson", (400, "Bad Request", "owner must not be blank"), "a validation problem"),
     ("problemJson", (409, "Conflict", "Account 7 already exists"), "a conflict")],
    [("problemJson", (400, "Bad Request", 'Field "owner" is missing'), "quotes are escaped"),
     ("problemJson", (500, "Internal Server Error", "C:\\temp"), "a backslash is escaped"),
     ("problemJson", (404, "Not Found", ""), "an empty detail"),
     ("problemJson", (422, "Unprocessable Content", "Café closed"), "non-ASCII text is kept"),
     ("problemJson", (401, "Unauthorized", 'Say "hello" \\ goodbye'), "both escapes together")],
    starter='''
String problemJson(int status, String title, String detail) {
    return "";
}
''', solution=PROBLEM_SOL,
    wrongs={"no-escaping": PROBLEM_NO_ESCAPE, "wrong-order": PROBLEM_ORDER, "no-type": PROBLEM_NO_TYPE, "quotes-only": PROBLEM_QUOTES_ONLY},
    hints=["Build the string in the order type, title, status, detail.", "Escape the backslash before you escape the quote."],
    misconceptions=("MC168",), difficulty=3,
)

ex13.explain(
    "j7-l1.3-explain-errors", "Honest errors", ["o1", "o2"], ["J7.03"],
    "An API returns `200 OK` with the body `{\"error\":\"account not found\"}` for a missing account, and `500` with a stack trace when the owner field is blank. Say what is wrong with each response, and what each should be.",
    "A missing resource is 404 and a bad request body is a client error, 400: the status code is what generic clients, caches and monitoring read, so it must be truthful. A 500 means the server failed, and a stack trace leaks internals; the body should be a problem detail whose detail helps the client correct the request and whose status matches the HTTP status.",
    levels={
        2: ("The answer fixes both statuses, explains why the status matters and rejects the stack trace.", [
            "The first should be 404 Not Found, because clients and monitoring read the status, not the body. The second is the client's mistake, so 400, not 500. A stack trace shows internals; return a problem detail with a helpful detail instead, using the same status in the body.",
            "200 with an error body hides the failure from every generic client, so use 404. A blank owner is a bad request: 400. A 500 means the server broke, and the trace leaks code. Send application/problem+json with status, title and a detail the client can act on."]),
        1: ("The answer fixes the statuses but not the leak, or gives no reason.", [
            "The first should be 404 and the second 400.",
            "Return the right status codes."]),
        0: ("The answer accepts the responses as they are.", [
            "It is fine because the client can read the error message in the body.",
            "A 500 is right, anything wrong is a server error."]),
    },
)

l7_l1_3 = Lesson("j7-l1.3", "Status codes and problem details", ["J7.03"], [
    ("o1", "Choose the status code for a common API situation"),
    ("o2", "Write an RFC 9457 problem detail body"),
], ["j7-l1.2"], 45, ["I84", "I85"], """## Before you start

You should be able to read a status line and classify a method.

## Explanation

The **status code** is how an API tells every client, cache and monitor what happened, so it has to be truthful. The ones an API uses constantly:

| Code | Meaning (RFC 9110) |
|---|---|
| 200 | success, with a body |
| 201 | created: a new resource exists, identified by a `Location` header or the target URI |
| 204 | success, no content to send |
| 400 | the server cannot or will not process the request because of a client error such as malformed syntax |
| 401 | the request lacks valid authentication credentials |
| 404 | no current representation found (or the server will not say one exists) |
| 405 | the method is known but not supported by the target resource; the response must include an `Allow` header |
| 409 | the request conflicts with the current state of the target resource |

An error also needs a body a client can use. **RFC 9457** defines a **problem detail**: a JSON object with media type `application/problem+json` and members `type`, `title`, `status`, `detail` and `instance`. If `type` is absent it is taken to be `about:blank`. `status` is advisory, and the HTTP response must use the same code. `detail` should help the client correct the problem, not expose debugging information.

## Worked examples

### Example 1: a real error response from this platform.

""" + fence(cap("cap_unauth.txt")) + """

Notice what this real response does and does not do. It has no `WWW-Authenticate` header, although RFC 9110 says a 401 response MUST send one. That is a gap in this platform, and you will meet the reasons in Stage 8. The 404 and 405 below it also use Spring Boot's default JSON error body (`timestamp`, `status`, `error`, `path`), not the problem detail shape.

### Example 2: a problem detail.

```json
{"type":"about:blank","title":"Not Found","status":404,"detail":"No account 7"}
```

## Where this is used

- Every API. Gateways, retries, dashboards and client libraries all react to the status, never to your message text.

## Common mistakes

:::mistake{id=MC168}
**Answering 200 with an error in the body, or 500 for every failure.** The status is the contract. A bad request is the client's error (4xx); only a real server failure is 5xx.
:::

## Practice

::exercise{id=j7-l1.3-write-status}

::exercise{id=j7-l1.3-write-problem}

::exercise{id=j7-l1.3-explain-errors}

## Further reading

- **RFC 9110, HTTP Semantics** `[I84]`, section on status codes.
- **RFC 9457, Problem Details for HTTP APIs** `[I85]`.

## How you'll be assessed

- The **write** exercises check status choice and the problem body (*implementation*).
- The **explain** exercise checks that you can critique a response (*explanation*).
""")

# ====================================================================== j7-l1.4
def f_route(method, path):
    if path == "/accounts":
        return {"GET": "list-accounts", "POST": "create-account"}.get(method, "method-not-allowed")
    m = re.fullmatch(r"/accounts/([0-9]+)", path)
    if m:
        verbs = {"GET": "get-account", "DELETE": "delete-account", "PUT": "replace-account"}
        return verbs[method] + ":" + m.group(1) if method in verbs else "method-not-allowed"
    m = re.fullmatch(r"/accounts/([0-9]+)/transactions", path)
    if m:
        return "list-transactions:" + m.group(1) if method == "GET" else "method-not-allowed"
    return "not-found"


ROUTE_SOL = '''
String route(String method, String path) {
    String[] p = path.split("/", -1);
    if (p.length < 2 || !p[0].isEmpty() || !p[1].equals("accounts")) {
        return "not-found";
    }
    if (p.length == 2) {
        return switch (method) {
            case "GET" -> "list-accounts";
            case "POST" -> "create-account";
            default -> "method-not-allowed";
        };
    }
    if (!p[2].matches("[0-9]+")) {
        return "not-found";
    }
    String id = p[2];
    if (p.length == 3) {
        return switch (method) {
            case "GET" -> "get-account:" + id;
            case "DELETE" -> "delete-account:" + id;
            case "PUT" -> "replace-account:" + id;
            default -> "method-not-allowed";
        };
    }
    if (p.length == 4 && p[3].equals("transactions")) {
        return method.equals("GET") ? "list-transactions:" + id : "method-not-allowed";
    }
    return "not-found";
}
'''
ROUTE_NO_405 = ROUTE_SOL.replace('default -> "method-not-allowed";', 'default -> "not-found";').replace('"list-transactions:" + id : "method-not-allowed"', '"list-transactions:" + id : "not-found"')
ROUTE_NO_DIGITS = ROUTE_SOL.replace('    if (!p[2].matches("[0-9]+")) {\n        return "not-found";\n    }\n', "")
ROUTE_SLASH = ROUTE_SOL.replace('    String[] p = path.split("/", -1);', '    String[] p = (path.endsWith("/") ? path.substring(0, path.length() - 1) : path).split("/", -1);')

ex14.method(
    "write", "j7-l1.4-write-route", "Routing a request", ["o1"], ["J7.04"], ["IMPL"],
    "Write `route(method, path)`, the routing table for an accounts API. `/accounts`: GET is `list-accounts`, POST is `create-account`. `/accounts/{id}` (the id is digits): GET `get-account:ID`, PUT `replace-account:ID`, DELETE `delete-account:ID`. `/accounts/{id}/transactions`: GET `list-transactions:ID`. A known path with another method is `method-not-allowed`. Anything else, including a trailing slash or an id that is not digits, is `not-found`.",
    [("route", [("method", "String"), ("path", "String")], "String")], {"route": f_route},
    [("route", ("GET", "/accounts"), "list"), ("route", ("GET", "/accounts/7"), "one account"), ("route", ("DELETE", "/accounts"), "wrong method on a known path")],
    [("route", ("POST", "/accounts"), "create"), ("route", ("PUT", "/accounts/12"), "replace"), ("route", ("DELETE", "/accounts/12"), "delete"),
     ("route", ("GET", "/accounts/7/transactions"), "a sub-resource"), ("route", ("POST", "/accounts/7/transactions"), "a sub-resource, wrong method"),
     ("route", ("GET", "/accounts/abc"), "an id that is not a number"), ("route", ("GET", "/accounts/"), "a trailing slash"),
     ("route", ("GET", "/customers"), "an unknown collection"), ("route", ("GET", ""), "an empty path"), ("route", ("POST", "/accounts/7"), "POST on one account")],
    starter='''
String route(String method, String path) {
    return "not-found";
}
''', solution=ROUTE_SOL,
    wrongs={"no-405": ROUTE_NO_405, "no-digit-check": ROUTE_NO_DIGITS, "forgives-trailing-slash": ROUTE_SLASH},
    hints=["Split the path on `/` and look at how many parts there are.", "When is a path known but the method wrong, and when is the path unknown?"],
    misconceptions=("MC169",), difficulty=3,
)

ex14.explain(
    "j7-l1.4-explain-design", "Critique an API", ["o2"], ["J7.04"],
    "A team proposes these endpoints: `GET /getAccount?id=7`, `POST /createAccount`, `POST /deleteAccount?id=7`, `GET /accounts/7/getTransactions`. Rewrite them as resource-oriented endpoints, and say what each rewrite gains.",
    "URLs should name resources (nouns) and the method should say the action. The rewrites are GET /accounts/7, POST /accounts, DELETE /accounts/7 and GET /accounts/7/transactions. The method then carries the meaning clients, caches and gateways understand: GET is safe and cacheable, DELETE is idempotent so it can be retried, and POST for creation can answer 201 with a Location.",
    levels={
        2: ("The answer gives all four rewrites and explains what the HTTP method now provides.", [
            "GET /accounts/7, POST /accounts, DELETE /accounts/7 and GET /accounts/7/transactions. The verbs move into the method: GET is safe and cacheable, DELETE can be retried because it is idempotent, and the create can return 201 with a Location header.",
            "Use nouns in the path and let the method be the verb: GET /accounts/7, POST /accounts, DELETE /accounts/7, GET /accounts/7/transactions. Now tools that know HTTP semantics (caches, retries, gateways) can treat each request correctly."]),
        1: ("The answer rewrites some endpoints without saying what is gained.", [
            "GET /accounts/7 and DELETE /accounts/7.",
            "Remove the verbs from the URLs and use nouns."]),
        0: ("The answer keeps the verbs or defends them.", [
            "The names are clear, so they are fine as they are.",
            "Add a version number to each URL."]),
    },
)

l7_l1_4 = Lesson("j7-l1.4", "Resource design and routing", ["J7.04"], [
    ("o1", "Route a method and path to the right handler in a resource-oriented API"),
    ("o2", "Rewrite an action-style API as resources and methods"),
], ["j7-l1.3"], 40, ["I84"], """## Before you start

You should know the HTTP methods and the status codes for a missing resource and a wrong method.

## Explanation

In a **resource-oriented** API the URL names a thing (`/accounts/7`) and the method says what to do with it (GET reads, PUT replaces, DELETE removes, POST creates under a collection). The same address can be read and changed, so the API has few URLs and the HTTP methods carry the verbs.

A **route** is a rule that maps a method and a path to a handler. A request that matches no path is a 404. A path that exists but does not support the method is a 405 (and must say which methods it does allow in an `Allow` header). Segments in curly braces, such as `{id}`, are **path variables**: the part of the URL that identifies one resource.

Sub-resources nest: `/accounts/7/transactions` is the transactions of account 7.

## Worked examples

### Example 1: the routing table of this lesson.

```text
GET    /accounts                    list-accounts
POST   /accounts                    create-account
GET    /accounts/{id}               get-account
PUT    /accounts/{id}               replace-account
DELETE /accounts/{id}               delete-account
GET    /accounts/{id}/transactions  list-transactions
```

### Example 2: a real 404 and a real 405 from this platform.

(The 405 needed a valid CSRF token first. Without one, this platform answers 403 before it looks at the method.)

""" + fence(cap("cap_404.txt")) + "\n\n" + fence(cap("cap_405.txt")) + """

## Where this is used

- Every Spring `@RequestMapping`, `@GetMapping` and `@PathVariable` is this routing table written as annotations. You will meet them in module 7.3.

## Common mistakes

:::mistake{id=MC169}
**Putting the action in the URL** (`/getAccount`, `/deleteAccount`). The method already says the action, and tools that understand HTTP can then cache, retry and secure requests correctly.
:::

## Practice

::exercise{id=j7-l1.4-write-route}

::exercise{id=j7-l1.4-explain-design}

## Further reading

- **RFC 9110, HTTP Semantics** `[I84]`, sections on `404`, `405` and the `Allow` header.

## How you'll be assessed

- The **write** exercise checks that you can implement routing (*implementation*).
- The **explain** exercise checks that you can critique an API design (*explanation*).
""")
print("module 7.1 authored")
