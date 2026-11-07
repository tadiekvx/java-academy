"""Stage 8 authoring: module 8.2 (Authentication and authorisation). Tokens and expectations are built in Python."""
import base64
import binascii
import hashlib
import hmac
import re
import l8common
from l8common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex21 = Exercises("j8-l2.1")
ex22 = Exercises("j8-l2.2")
ex23 = Exercises("j8-l2.3")
ex24 = Exercises("j8-l2.4")
ex25 = Exercises("j8-l2.5")

REGISTER = {
    "j8-l2.1": ("Authentication, sessions and cookies", ["J8.05"]),
    "j8-l2.2": ("Tokens and JWT", ["J8.06"]),
    "j8-l2.3": ("Access control and ownership", ["J8.07"]),
    "j8-l2.4": ("Spring Security: CSRF and CORS", ["J8.08"]),
    "j8-l2.5": ("Lockout and generic responses", ["J8.09"]),
}
MISCS = {
    "MC182": (["J8.05"], "I101", "Every cookie should be hidden from scripts with HttpOnly, so a single-page app can never read any cookie"),
    "MC183": (["J8.06"], "I100", "A signed JWT cannot be abused: the signature makes its contents secret and it can be revoked at any time"),
    "MC184": (["J8.07"], "I104", "If a user is logged in, an endpoint may return any record whose id they ask for"),
    "MC185": (["J8.08"], "I102", "CSRF protection and CORS are the same control, so enabling one makes the other unnecessary"),
    "MC186": (["J8.09"], "I105", "A login error should say exactly what was wrong, so honest users are helped"),
}
register(REGISTER, MISCS)

# ====================================================================== j8-l2.1
SETCOOKIE = cap("cap_setcookie.txt")


def f_cookie(header):
    parts = header.split("; ")
    name = parts[0].split("=", 1)[0]
    attrs = {p.split("=", 1)[0].lower() for p in parts[1:]}
    return f"name={name} httpOnly={'true' if 'httponly' in attrs else 'false'} secure={'true' if 'secure' in attrs else 'false'}"


COOKIE_SOL = '''
String describeCookie(String header) {
    String[] parts = header.split("; ");
    String name = parts[0].split("=", 2)[0];
    boolean httpOnly = false;
    boolean secure = false;
    for (int i = 1; i < parts.length; i++) {
        String attribute = parts[i].split("=", 2)[0].toLowerCase();
        if (attribute.equals("httponly")) {
            httpOnly = true;
        }
        if (attribute.equals("secure")) {
            secure = true;
        }
    }
    return "name=" + name + " httpOnly=" + httpOnly + " secure=" + secure;
}
'''
COOKIE_CASE = COOKIE_SOL.replace(".toLowerCase()", "")
COOKIE_SWAP = COOKIE_SOL.replace('attribute.equals("httponly")', 'attribute.equals("secure")', 1).replace('        if (attribute.equals("secure")) {\n            secure = true;', '        if (attribute.equals("httponly")) {\n            secure = true;', 1)
COOKIE_VALUE_AS_NAME = COOKIE_SOL.replace('header.split("; ");\n    String name = parts[0].split("=", 2)[0];', 'header.split("; ");\n    String name = parts[0];')

ex21.method(
    "write", "j8-l2.1-write-cookie", "Reading a Set-Cookie header", ["o1"], ["J8.05"], ["IMPL"],
    "Write `describeCookie(header)` for the value of a `Set-Cookie` header (attributes are separated by `; `). Return `name=NAME httpOnly=true|false secure=true|false`, where NAME is the cookie name (the part before the first `=`) and attribute names are matched ignoring letter case.",
    [("describeCookie", [("header", "String")], "String")], {"describeCookie": f_cookie},
    [("describeCookie", ("JSESSIONID=ABC123; Path=/; HttpOnly",), "a session cookie"), ("describeCookie", ("XSRF-TOKEN=t0k3n; Path=/",), "a token cookie"), ("describeCookie", ("a=b; Secure; HttpOnly",), "both flags")],
    [("describeCookie", ("sid=1; httponly",), "lower case"), ("describeCookie", ("sid=1; SECURE",), "upper case"), ("describeCookie", ("sid=",), "an empty value"),
     ("describeCookie", ("sid=a=b; Path=/",), "an equals sign in the value"), ("describeCookie", ("sid=1; Max-Age=60; Path=/; Secure",), "several attributes"), ("describeCookie", ("sid=1; HttpOnlyish",), "a similar name")],
    starter='''
String describeCookie(String header) {
    return "";
}
''', solution=COOKIE_SOL,
    wrongs={"case-sensitive": COOKIE_CASE, "flags-swapped": COOKIE_SWAP, "name-includes-value": COOKIE_VALUE_AS_NAME},
    hints=["Split on `; `, then split the first part at the first `=`.", "Compare each attribute name in lower case."],
    misconceptions=("MC182",), difficulty=2,
)

ex21.explain(
    "j8-l2.1-explain-cookies", "Two cookies, two policies", ["o2"], ["J8.05"],
    "These are the `Set-Cookie` headers of a real response from this platform's backend:\n\n" + fence(SETCOOKIE) + "\n\nWhy does the session cookie carry `HttpOnly` while the `XSRF-TOKEN` cookie does not? What attack does `HttpOnly` help against, and what would you add to both cookies before running this over the internet?",
    "HttpOnly tells the browser not to expose the cookie to scripts, so script injected by cross-site scripting cannot read the session identifier. The XSRF-TOKEN cookie is deliberately readable: this platform's single-page front end reads it and sends it back in the X-XSRF-TOKEN header, which is how the CSRF check works, and the token is useless without the matching session. Before internet use, add the Secure attribute so the cookies travel only over TLS (it protects confidentiality only) and serve everything over HTTPS.",
    levels={
        2: ("The answer ties HttpOnly to script access and XSS, explains why the XSRF token must be readable, and adds Secure with HTTPS.", [
            "HttpOnly hides the session cookie from JavaScript, so an XSS bug cannot steal it. The XSRF-TOKEN cookie has to be read by the front end, which copies it into the X-XSRF-TOKEN header; that is the CSRF defence, and a token alone is no use without the session. For the internet both cookies need Secure, with HTTPS, so they are only sent over TLS.",
            "The session id is a credential, so scripts must not see it (HttpOnly protects against XSS theft). The CSRF token is meant for the page's own script to echo back, so it is readable. Add Secure and use TLS."]),
        1: ("The answer explains one cookie but not the other, or omits Secure.", [
            "HttpOnly stops JavaScript reading the session cookie.",
            "The token has to be read by the front end."]),
        0: ("The answer treats the difference as a mistake or irrelevant.", [
            "It is a bug, both cookies should be the same.",
            "HttpOnly stops the cookie being sent over HTTP."]),
    },
)

ex21.explain(
    "j8-l2.1-explain-401-403", "401 or 403", ["o1"], ["J8.05"],
    "Compare these two real responses from this platform. The first is a request with no login to a protected endpoint; the second is a `DELETE` with no CSRF token.\n\n" + fence(cap("cap_unauth_head.txt")) + "\n\n" + fence(cap("cap_csrf403.txt")) + "\n\nExplain the difference between authentication and authorisation, say which status each response uses and why, and say what is missing from the 401 response according to RFC 9110. Use the line `.exceptionHandling(e -> e.authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED)))` from this platform's `SecurityConfig` to explain why.",
    "Authentication is establishing who the caller is; authorisation is deciding what that caller may do. The first request has no identity, so the answer is 401. The second is refused because it lacks the CSRF token, a permission check on the request itself, so the answer is 403. RFC 9110 says a 401 must carry a WWW-Authenticate header, and this response has none: the application configured an HttpStatusEntryPoint, which only sets the status. That is a reasonable choice for a single-page app that handles login itself, but it departs from the RFC.",
    levels={
        2: ("The answer distinguishes the two ideas, assigns 401 and 403 correctly, and explains the missing header from the entry point.", [
            "Authentication is who you are, authorisation is what you may do. No login means no identity, so 401. A request with no CSRF token is refused as not allowed, so 403. RFC 9110 says a 401 must include WWW-Authenticate, and there is none here because the HttpStatusEntryPoint only sets the status code, which suits a SPA that shows its own login form.",
            "401 is for missing or invalid credentials (authentication); 403 is for a known caller who is not allowed or whose request fails a check such as CSRF (authorisation). The 401 lacks the WWW-Authenticate header the RFC requires because the platform's entry point just returns the status."]),
        1: ("The answer assigns the codes without the missing-header point.", [
            "401 means not logged in and 403 means forbidden.",
            "The first one has no login and the second has no token."]),
        0: ("The answer treats the two as the same or reverses them.", [
            "They are the same thing, both mean access denied.",
            "403 means you need to log in and 401 means you are not allowed."]),
    },
)

l8_l2_1 = Lesson("j8-l2.1", "Authentication, sessions and cookies", ["J8.05"], [
    ("o1", "Tell authentication from authorisation and choose 401 or 403"),
    ("o2", "Read cookie attributes and explain why a session cookie is HttpOnly"),
], ["j8-l1.2", "j7-l1.3"], 45, ["I101", "I102", "I106"], """## Before you start

You should know the status codes (Stage 7) and how passwords are stored (lesson 8.1.2).

## Explanation

**Authentication** establishes who the caller is. **Authorisation** decides what that caller may do. Mixing them up causes bugs and wrong status codes: no identity is a 401; a known caller who is not allowed is a 403.

A **session** keeps a login across requests. After a successful login the server creates a session and sends the browser a **cookie** holding an identifier; the browser returns it on every request. The identifier is therefore a credential, so how the cookie is marked matters (RFC 6265):

- `HttpOnly` tells the browser to omit the cookie when scripts ask for cookies, so a cross-site scripting bug cannot read the session id.
- `Secure` limits the cookie to secure channels, typically TLS. It protects the cookie's confidentiality only, and it is independent of `HttpOnly`: a cookie can have both.

This platform uses a session cookie, set by Spring Security. `SecurityConfig` also turns on CSRF protection in single-page-app mode, so a second cookie, `XSRF-TOKEN`, is meant to be read by the front end script.

## Worked examples

### Example 1: the real cookies.

Captured from this platform's backend:

""" + fence(SETCOOKIE) + """

### Example 2: two real refusals.

""" + fence(cap("cap_unauth_head.txt")) + "\n\n" + fence(cap("cap_csrf403.txt")) + """

## Where this is used

- Every login. A web application with a stolen session cookie is the account's owner as far as the server can tell.

## Common mistakes

:::mistake{id=MC182}
**Marking every cookie `HttpOnly`, or none.** The session id must be hidden from scripts; a CSRF token that the front end has to echo back must be readable. Decide per cookie.
:::

## Practice

::exercise{id=j8-l2.1-write-cookie}

::exercise{id=j8-l2.1-explain-cookies}

::exercise{id=j8-l2.1-explain-401-403}

## Further reading

- **RFC 6265, HTTP State Management** `[I101]`.
- **Spring Security, CSRF** `[I102]`.

## How you'll be assessed

- The **write** exercise checks that you can read cookie attributes (*implementation*).
- The **explain** exercises check the cookie policy and the status codes (*explanation*).
""")

# ====================================================================== j8-l2.2
def b64u(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def token(header, payload, secret, sig_from=None):
    h, p = b64u(header.encode()), b64u(payload.encode())
    sig = hmac.new((sig_from or secret).encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{b64u(sig)}"


HS = '{"alg":"HS256","typ":"JWT"}'


def decode(s):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", s):
        raise ValueError
    try:
        return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
    except (binascii.Error, ValueError):
        raise ValueError


def f_verify(tok, secret, now):
    parts = tok.split(".")
    if len(parts) != 3:
        return "malformed"
    try:
        header, payload = decode(parts[0]).decode(), decode(parts[1]).decode()
    except (ValueError, UnicodeDecodeError):
        return "malformed"
    if not re.search(r'"alg"\s*:\s*"HS256"', header):
        return "unsupported-alg"
    try:
        sig = decode(parts[2])
    except ValueError:
        return "malformed"
    want = hmac.new(secret.encode(), f"{parts[0]}.{parts[1]}".encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(sig, want):
        return "bad-signature"
    m = re.search(r'"exp"\s*:\s*(\d+)', payload)
    if not m:
        return "malformed"
    return "expired" if now >= int(m.group(1)) else "valid"


VERIFY_JWT = '''
String verifyToken(String token, String secret, long now) throws Exception {
    String[] parts = token.split("\\\\.", -1);
    if (parts.length != 3) {
        return "malformed";
    }
    String header;
    String payload;
    byte[] signature;
    try {
        header = new String(decode(parts[0]), java.nio.charset.StandardCharsets.UTF_8);
        payload = new String(decode(parts[1]), java.nio.charset.StandardCharsets.UTF_8);
    } catch (IllegalArgumentException e) {
        return "malformed";
    }
    if (!java.util.regex.Pattern.compile("\\"alg\\"\\\\s*:\\\\s*\\"HS256\\"").matcher(header).find()) {
        return "unsupported-alg";
    }
    try {
        signature = decode(parts[2]);
    } catch (IllegalArgumentException e) {
        return "malformed";
    }
    Mac mac = Mac.getInstance("HmacSHA256");
    mac.init(new SecretKeySpec(secret.getBytes(java.nio.charset.StandardCharsets.UTF_8), "HmacSHA256"));
    byte[] expected = mac.doFinal((parts[0] + "." + parts[1]).getBytes(java.nio.charset.StandardCharsets.UTF_8));
    if (!MessageDigest.isEqual(signature, expected)) {
        return "bad-signature";
    }
    java.util.regex.Matcher exp = java.util.regex.Pattern.compile("\\"exp\\"\\\\s*:\\\\s*(\\\\d+)").matcher(payload);
    if (!exp.find()) {
        return "malformed";
    }
    return now >= Long.parseLong(exp.group(1)) ? "expired" : "valid";
}

byte[] decode(String part) {
    if (!part.matches("[A-Za-z0-9_-]+")) {
        throw new IllegalArgumentException("not base64url");
    }
    return Base64.getUrlDecoder().decode(part);
}
'''
JWT_NONE = VERIFY_JWT.replace('        return "unsupported-alg";', '        if (!header.contains("none")) {\n            return "unsupported-alg";\n        }\n        return now >= 0 ? "valid" : "valid";')
JWT_EXP_FIRST = VERIFY_JWT.replace('    if (!MessageDigest.isEqual(signature, expected)) {\n        return "bad-signature";\n    }\n', "").replace('    return now >= Long.parseLong(exp.group(1)) ? "expired" : "valid";', '    if (now >= Long.parseLong(exp.group(1))) {\n        return "expired";\n    }\n    return MessageDigest.isEqual(signature, expected) ? "valid" : "bad-signature";')
JWT_BOUNDARY = VERIFY_JWT.replace("now >= Long.parseLong", "now > Long.parseLong")
JWT_NO_SIGCHECK = VERIFY_JWT.replace('    if (!MessageDigest.isEqual(signature, expected)) {\n        return "bad-signature";\n    }\n', "")
SEC = "k3y-for-tests"
GOOD = token(HS, '{"sub":"ada","exp":2000}', SEC)
h_, p_, s_ = GOOD.split(".")
TAMPERED = h_ + "." + b64u(b'{"sub":"admin","exp":2000}') + "." + s_
NONE = b64u(b'{"alg":"none","typ":"JWT"}') + "." + b64u(b'{"sub":"ada","exp":2000}') + "."
OTHER = token(HS, '{"sub":"ada","exp":2000}', SEC, sig_from="another-secret")
NOEXP = token(HS, '{"sub":"ada"}', SEC)
HS512 = token('{"alg":"HS512","typ":"JWT"}', '{"sub":"ada","exp":2000}', SEC)

ex22.method(
    "write", "j8-l2.2-write-verify", "Verifying a signed token", ["o1"], ["J8.06"], ["IMPL", "MIST"],
    "A token is `header.payload.signature`, each part base64url text; the signature is HMAC-SHA256 of `header.payload` with the shared secret. Write `verifyToken(token, secret, now)` (times are seconds). In this order: not three dot-separated parts, or a header/payload part that is not valid base64url → `malformed`; a header that does not say `\"alg\":\"HS256\"` → `unsupported-alg` (this refuses `none`); a signature that does not match (compare with `MessageDigest.isEqual`) → `bad-signature`; no numeric `exp` claim → `malformed`; `now` at or after `exp` → `expired`; otherwise `valid`.",
    [("verifyToken", [("token", "String"), ("secret", "String"), ("now", "long")], "String")], {"verifyToken": f_verify},
    [("verifyToken", (GOOD, SEC, 1000), "a valid token"), ("verifyToken", (GOOD, SEC, 2000), "the moment it expires"), ("verifyToken", (TAMPERED, SEC, 1000), "a changed payload")],
    [("verifyToken", (GOOD, SEC, 1999), "one second before expiry"), ("verifyToken", (GOOD, SEC, 5000), "long expired"), ("verifyToken", (NONE, SEC, 1000), "algorithm none"),
     ("verifyToken", (OTHER, SEC, 1000), "signed with another secret"), ("verifyToken", ("only.two", SEC, 1000), "two parts"), ("verifyToken", ("a.b.c.d", SEC, 1000), "four parts"),
     ("verifyToken", ("!!!." + p_ + "." + s_, SEC, 1000), "not base64url"), ("verifyToken", (NOEXP, SEC, 1000), "no expiry claim"), ("verifyToken", (HS512, SEC, 1000), "another algorithm"),
     ("verifyToken", (TAMPERED, SEC, 9999), "tampered and expired: the signature is checked first")],
    starter='''
String verifyToken(String token, String secret, long now) throws Exception {
    return "malformed";
}
''', solution=VERIFY_JWT,
    wrongs={"accepts-none": JWT_NONE, "checks-expiry-before-signature": JWT_EXP_FIRST, "off-by-one-expiry": JWT_BOUNDARY, "never-checks-signature": JWT_NO_SIGCHECK},
    source_tests=[("compares signatures with MessageDigest.isEqual", ["MessageDigest.isEqual"], None)],
    hints=["Check things in the order the exercise lists them.", "The HMAC covers the first two parts exactly as they appear, joined by a dot."],
    misconceptions=("MC183",), difficulty=4,
)

ex22.explain(
    "j8-l2.2-explain-session-vs-token", "Session or token", ["o2"], ["J8.06"],
    "Brightbank's web app and a planned mobile app both need to sign customers in. A colleague wants signed JWTs valid for 30 days stored in the browser's local storage, 'because tokens are stateless and scale better'. Argue for the choice you would make for the web app, covering revocation, where the credential is stored, and what the `exp` claim does and does not give you. This platform uses a server session and cookie; say what that trades away.",
    "A JWT is verified by its signature and exp claim alone, which is why no server lookup is needed, but that also means it cannot be revoked before exp unless the server keeps a list, which is state again. A 30-day token is a long-lived bearer credential: whoever copies it is the customer, and local storage is readable by any script on the page, so one XSS bug exposes it. A session cookie can be marked HttpOnly, and logging out or banning a user takes effect at once because the server owns the session. The price of a server session is server-side state to store and share between instances. For the web app a session cookie is the better default; tokens suit cases such as service-to-service calls or a mobile client that needs a different mechanism.",
    levels={
        2: ("The answer covers revocation, storage and exp, and states what the session design costs.", [
            "I would use a session cookie for the web app. A JWT cannot be revoked before exp without keeping server state, which defeats the point, and 30 days is a long time for a stolen token to work. In local storage any injected script can read it, whereas the session cookie can be HttpOnly. The exp claim only stops the token being accepted after that time. The cost of sessions is state on the server that must be shared if there are several instances.",
            "Sessions: logout and bans work immediately, the id is HttpOnly. A long-lived JWT in local storage is exposed to XSS and cannot be cancelled early. exp just limits the lifetime. What the session trades away is statelessness, so sessions need storage and sharing across servers."]),
        1: ("The answer prefers one with only one reason.", [
            "Sessions are safer because they can be revoked.",
            "Tokens are stateless so they scale better."]),
        0: ("The answer treats a signature as confidentiality or ignores storage.", [
            "A signed token is secret so storing it anywhere is fine.",
            "Tokens are always better because they are modern."]),
    },
)

l8_l2_2 = Lesson("j8-l2.2", "Tokens and JWT", ["J8.06"], [
    ("o1", "Verify a signed JWT: structure, algorithm, signature and expiry, in a safe order"),
    ("o2", "Argue sessions against tokens for a given application"),
], ["j8-l2.1"], 50, ["I100", "I107", "I101"], """## Before you start

You should know what a session cookie is and how HMAC-style hashing differs from storing a password.

## Explanation

A **JSON Web Token** (JWT, RFC 7519) is three base64url parts joined by dots: a header, a payload of claims, and a signature. The header carries the algorithm, for example `{"typ":"JWT","alg":"HS256"}`, where HS256 means an HMAC with SHA-256 over `header.payload` using a shared secret.

The signature gives **integrity**: if the payload is changed the signature no longer matches. It does not give **secrecy**: the payload is only encoded, and anyone can read it.

The `exp` claim identifies the time on or after which the token MUST NOT be accepted for processing; the current time must be before it. Implementations may allow a little leeway for clock skew.

Verification must be done in a safe order. Refuse an algorithm you did not choose (a header saying `none` means "no signature"), check the signature, and only then trust the claims. Compare signatures in a way that examines all bytes (`MessageDigest.isEqual`).

The design question is whether to use tokens at all. A token is checked without a server lookup, so it cannot be revoked before `exp` unless the server keeps state; where it is stored in the browser decides what a script can steal. A server session with an `HttpOnly` cookie is the simpler default for a web application.

## Worked examples

### Example 1: the parts of a token.

`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9` is the base64url of `{"alg":"HS256","typ":"JWT"}`.

### Example 2: the order of checks.

A token with a changed payload and an expired `exp` is reported as `bad-signature`, not `expired`: do not look at claims before you trust the signature.

## Where this is used

- APIs called by other programs, and single sign-on. Many frameworks verify tokens for you; this lesson shows what they are doing.

## Common mistakes

:::mistake{id=MC183}
**Thinking a signed token is secret or revocable.** A signature proves it was not changed; it does not hide the contents and does not stop a copied token working until it expires.
:::

## Practice

::exercise{id=j8-l2.2-write-verify}

::exercise{id=j8-l2.2-explain-session-vs-token}

## Further reading

- **RFC 7519, JSON Web Token** `[I100]`.
- **Java Security Standard Algorithm Names** `[I107]` for `HmacSHA256`.

## How you'll be assessed

- The **write** exercise checks safe verification (*implementation*).
- The **explain** exercise checks the session-versus-token argument (*explanation*).
""")

# ====================================================================== j8-l2.3
def f_can(role, user, action, owner):
    if action not in ("read", "write"):
        return False
    if role == "admin":
        return True
    if role == "teller":
        return action == "read"
    if role == "customer":
        return action == "read" and user != "" and user == owner
    return False


CAN_SOL = '''
boolean canAccess(String role, String user, String action, String owner) {
    if (!action.equals("read") && !action.equals("write")) {
        return false;
    }
    return switch (role) {
        case "admin" -> true;
        case "teller" -> action.equals("read");
        case "customer" -> action.equals("read") && !user.isEmpty() && user.equals(owner);
        default -> false;
    };
}
'''
CAN_IDOR = CAN_SOL.replace('action.equals("read") && !user.isEmpty() && user.equals(owner)', 'action.equals("read")')
CAN_ALLOW_UNKNOWN = CAN_SOL.replace("default -> false;", "default -> true;")
CAN_TELLER_WRITE = CAN_SOL.replace('case "teller" -> action.equals("read");', 'case "teller" -> true;')
CAN_EMPTY_USER = CAN_SOL.replace(" && !user.isEmpty()", "")
CAN_CASE = CAN_SOL.replace("switch (role)", "switch (role.toLowerCase())")

ex23.method(
    "write", "j8-l2.3-write-can-access", "Who may do what", ["o1"], ["J8.07"], ["IMPL"],
    "Write `canAccess(role, user, action, owner)`. An `action` other than `read` or `write` is always refused. `admin` may do both. `teller` may only read any account. `customer` may only read an account whose owner is that same (non-empty) user. Any other role is refused (deny by default).",
    [("canAccess", [("role", "String"), ("user", "String"), ("action", "String"), ("owner", "String")], "boolean")], {"canAccess": f_can},
    [("canAccess", ("customer", "ada", "read", "ada"), "own account"), ("canAccess", ("customer", "ada", "read", "grace"), "someone else's account"), ("canAccess", ("teller", "tess", "write", "ada"), "teller cannot write")],
    [("canAccess", ("admin", "root", "write", "ada"), "admin may write"), ("canAccess", ("teller", "tess", "read", "grace"), "teller reads any"), ("canAccess", ("customer", "ada", "write", "ada"), "customers cannot write"),
     ("canAccess", ("visitor", "bob", "read", "bob"), "an unknown role"), ("canAccess", ("customer", "", "read", ""), "empty user and owner"), ("canAccess", ("admin", "root", "delete", "ada"), "an unknown action"),
     ("canAccess", ("Customer", "ada", "read", "ada"), "role names are exact"), ("canAccess", ("customer", "ada", "READ", "ada"), "actions are exact")],
    starter='''
boolean canAccess(String role, String user, String action, String owner) {
    return true;
}
''', solution=CAN_SOL,
    wrongs={"anyone-reads-anything": CAN_IDOR, "unknown-roles-allowed": CAN_ALLOW_UNKNOWN, "teller-may-write": CAN_TELLER_WRITE, "empty-user-matches-empty-owner": CAN_EMPTY_USER, "role-case-folded": CAN_CASE},
    hints=["Start by refusing everything, then allow the cases the rules name.", "What does a customer need to be true about the owner?"],
    misconceptions=("MC184",), difficulty=3,
)


def f_visible(user, role, accounts):
    if role in ("admin", "teller"):
        return [a.split(":")[0] for a in accounts]
    if role == "customer":
        return [a.split(":")[0] for a in accounts if a.split(":")[1] == user]
    return []


VIS_SOL = '''
List<String> visibleAccounts(String user, String role, List<String> accounts) {
    List<String> ids = new ArrayList<>();
    for (String account : accounts) {
        String[] parts = account.split(":");
        boolean allowed = role.equals("admin") || role.equals("teller") || (role.equals("customer") && parts[1].equals(user));
        if (allowed) {
            ids.add(parts[0]);
        }
    }
    return ids;
}
'''
VIS_BUGGY = '''
List<String> visibleAccounts(String user, String role, List<String> accounts) {
    List<String> ids = new ArrayList<>();
    for (String account : accounts) {
        ids.add(account.split(":")[0]);
    }
    return ids;
}
'''
VIS_UNKNOWN = VIS_SOL.replace('role.equals("admin") || role.equals("teller") || (', '!role.isEmpty() || (')
VIS_PREFIX = VIS_SOL.replace("parts[1].equals(user)", "parts[1].startsWith(user)")
VIS_OWNER_ID = VIS_SOL.replace("ids.add(parts[0]);", "ids.add(parts[1]);")

ex23.method(
    "debug", "j8-l2.3-debug-listing", "The list that shows everyone's accounts", ["o2"], ["J8.07"], ["DEBUG"],
    "`visibleAccounts(user, role, accounts)` should return the ids of the accounts a caller may see. Each account is `id:owner`. `admin` and `teller` see all; a `customer` sees only the accounts they own; any other role sees none. The starter returns every id, an insecure direct object reference. Fix it.",
    [("visibleAccounts", [("user", "String"), ("role", "String"), ("accounts", "List<String>")], "List<String>")], {"visibleAccounts": f_visible},
    [("visibleAccounts", ("ada", "customer", ["1:ada", "2:grace", "3:ada"]), "a customer with two accounts"), ("visibleAccounts", ("tess", "teller", ["1:ada", "2:grace"]), "a teller sees all"), ("visibleAccounts", ("mallory", "visitor", ["1:ada"]), "an unknown role")],
    [("visibleAccounts", ("grace", "customer", ["1:ada", "2:grace", "3:ada"]), "another customer"), ("visibleAccounts", ("zed", "customer", ["1:ada"]), "a customer with none"), ("visibleAccounts", ("ad", "customer", ["1:ada", "2:ad"]), "a name that is a prefix of another"),
     ("visibleAccounts", ("root", "admin", []), "no accounts"), ("visibleAccounts", ("ada", "customer", []), "empty list"), ("visibleAccounts", ("bob", "", ["1:bob"]), "empty role")],
    starter=VIS_BUGGY, solution=VIS_SOL,
    wrongs={"original": VIS_BUGGY, "any-role-sees-all": VIS_UNKNOWN, "prefix-match": VIS_PREFIX, "returns-owners": VIS_OWNER_ID},
    hints=["Which condition decides whether an account is included?", "Is `ad` the same user as `ada`?"],
    misconceptions=("MC184",), difficulty=3,
)

ex23.explain(
    "j8-l2.3-explain-idor", "The id in the URL", ["o2"], ["J8.07"],
    "`GET /accounts/7` returns account 7 to any signed-in customer. Customer A notices their account is 7, tries 8, and sees customer B's balance. Name this flaw (with its OWASP Top 10:2025 category), say why hiding or randomising ids is not the fix, and describe the fix, using the guidance 'deny by default' and 'validate the permissions on every request'.",
    "This is an insecure direct object reference, a case of A01 Broken Access Control: the server checks that the caller is signed in (authentication) but not that the account belongs to them (authorisation). Hard-to-guess ids only make the flaw harder to find; the OWASP guidance says to make sure lookup ids cannot be accessed even when guessed. The fix is an ownership check on every request on the server (the caller's identity from the session, compared with the account's owner), refusing by default, with a test that customer A is refused for customer B's account.",
    levels={
        2: ("The answer names the flaw and category, explains why obscure ids do not fix it, and describes a server-side check on every request, deny by default, with a test.", [
            "It is an insecure direct object reference, A01 Broken Access Control. Being signed in proves who the caller is, not that account 7 or 8 is theirs. Random ids only hide the problem, since the id must not matter even if guessed. On every request the server should compare the session's user with the account's owner and refuse by default, and there should be a test that A cannot read B's account.",
            "IDOR under A01 Broken Access Control. The fix is authorisation on the server for each request: look up the account, check its owner is the caller, otherwise 403 (or 404). Secret or random ids are not a defence, and the default must be deny. Add a test with two customers."]),
        1: ("The answer names the flaw or the fix without the other parts.", [
            "It is broken access control. Check who owns the account.",
            "Use random ids so people cannot guess them."]),
        0: ("The answer treats being signed in as sufficient.", [
            "The user is signed in so it is allowed.",
            "The front end should hide the other accounts."]),
    },
)

l8_l2_3 = Lesson("j8-l2.3", "Access control and ownership", ["J8.07"], [
    ("o1", "Write role and ownership rules that deny by default"),
    ("o2", "Find and fix an insecure direct object reference"),
], ["j8-l2.1"], 45, ["I104", "I95"], """## Before you start

You should know the difference between authentication and authorisation (lesson 8.2.1) and how a controller finds a record by id (Stage 7).

## Explanation

**Broken access control** is A01 in the OWASP Top 10:2025: the top category. The most common form in APIs is the **insecure direct object reference** (IDOR): the endpoint takes an id, loads the record, and returns it without asking whether this caller may see it.

The OWASP authorization guidance gives the rules to apply:

- **Enforce least privilege:** give each role only what it needs.
- **Deny by default:** anything not explicitly allowed is refused, including unknown roles and unknown actions.
- **Validate the permissions on every request**, on the server. Hiding a button in the front end is not a control.
- Make sure lookup ids cannot be used even when they are guessed or tampered with. Random ids do not remove the need for the check.

Two kinds of rule are usually combined: a **role** rule (tellers may read any account) and an **ownership** rule (a customer may read only their own). The exercise puts both in one function so you can see the cases that go wrong: the empty user who matches an empty owner, the prefix that matches a longer name, the role nobody planned for.

## Worked examples

### Example 1: the rule table.

`customer` reads own account: allowed. `customer` reads another's: refused. `teller` writes: refused. `visitor` anything: refused.

### Example 2: filter the list as well.

An endpoint that lists accounts is an access-control surface too. Filter on the server by the caller, not by the id they ask for.

## Where this is used

- Every endpoint that returns or changes a record. The project of this stage asks you to audit one.

## Common mistakes

:::mistake{id=MC184}
**Treating "logged in" as "allowed".** Authentication says who the caller is. Each request still needs its own authorisation decision.
:::

## Practice

::exercise{id=j8-l2.3-write-can-access}

::exercise{id=j8-l2.3-debug-listing}

::exercise{id=j8-l2.3-explain-idor}

## Further reading

- **OWASP Authorization Cheat Sheet** `[I104]`.
- **OWASP Top 10:2025, A01** `[I95]`.

## How you'll be assessed

- The **write** and **debug** exercises check the rules (*implementation, debugging*).
- The **explain** exercise checks that you can describe the flaw and its fix (*explanation*).
""")

# ====================================================================== j8-l2.4
SAFE_M = {"GET", "HEAD", "OPTIONS", "TRACE"}


def f_csrf(method, present, matches):
    if method in SAFE_M:
        return "allow"
    return "allow" if present and matches else "reject"


CSRF_SOL = '''
String csrfDecision(String method, boolean tokenPresent, boolean tokenMatches) {
    if (List.of("GET", "HEAD", "OPTIONS", "TRACE").contains(method)) {
        return "allow";
    }
    return tokenPresent && tokenMatches ? "allow" : "reject";
}
'''
CSRF_ALL = CSRF_SOL.replace('return tokenPresent && tokenMatches ? "allow" : "reject";', 'return tokenPresent ? "allow" : "reject";')
CSRF_GET = CSRF_SOL.replace('List.of("GET", "HEAD", "OPTIONS", "TRACE")', 'List.of("HEAD", "OPTIONS", "TRACE")')
CSRF_NEVER = CSRF_SOL.replace('    return tokenPresent && tokenMatches ? "allow" : "reject";', '    return "allow";')
CSRF_LOWER = CSRF_SOL.replace("contains(method)", "contains(method.toUpperCase())")

ex24.method(
    "write", "j8-l2.4-write-csrf", "The CSRF decision", ["o1"], ["J8.08"], ["IMPL"],
    "Browsers attach cookies to cross-site requests automatically, so a session cookie alone cannot prove the request was meant. Spring Security's answer is a CSRF token the page must add itself, in a header. Write `csrfDecision(method, tokenPresent, tokenMatches)` returning `allow` or `reject`: the safe methods GET, HEAD, OPTIONS and TRACE (RFC 9110) are `allow`; any other method is `allow` only if a token is present and matches. Method names are exact capitals.",
    [("csrfDecision", [("method", "String"), ("tokenPresent", "boolean"), ("tokenMatches", "boolean")], "String")], {"csrfDecision": f_csrf},
    [("csrfDecision", ("GET", False, False), "a read needs no token"), ("csrfDecision", ("POST", True, True), "a write with the right token"), ("csrfDecision", ("DELETE", False, False), "a write without a token")],
    [("csrfDecision", ("POST", True, False), "a wrong token"), ("csrfDecision", ("PUT", True, True), "put"), ("csrfDecision", ("HEAD", False, False), "head"),
     ("csrfDecision", ("OPTIONS", False, False), "options"), ("csrfDecision", ("TRACE", False, False), "trace"), ("csrfDecision", ("PATCH", False, True), "patch without a token"),
     ("csrfDecision", ("post", True, True), "lower case is not a known safe method but is not rejected as a method"), ("csrfDecision", ("get", False, False), "lower case get is not the safe GET")],
    starter='''
String csrfDecision(String method, boolean tokenPresent, boolean tokenMatches) {
    return "allow";
}
''', solution=CSRF_SOL,
    wrongs={"only-checks-presence": CSRF_ALL, "get-needs-token": CSRF_GET, "never-rejects": CSRF_NEVER, "case-folds-method": CSRF_LOWER},
    hints=["Which methods never change state?", "A token that is present but wrong must be refused."],
    misconceptions=("MC185",), difficulty=2,
)


def f_cors(origin, allowed):
    return origin != "" and origin in allowed


CORS_SOL = '''
boolean corsAllowed(String origin, List<String> allowedOrigins) {
    return !origin.isEmpty() && allowedOrigins.contains(origin);
}
'''
CORS_WILD = CORS_SOL.replace("allowedOrigins.contains(origin)", "(allowedOrigins.contains(origin) || allowedOrigins.contains(\"*\"))")
CORS_PREFIX = CORS_SOL.replace("allowedOrigins.contains(origin)", "allowedOrigins.stream().anyMatch(origin::startsWith)")
CORS_CASE = CORS_SOL.replace("allowedOrigins.contains(origin)", "allowedOrigins.stream().anyMatch(origin::equalsIgnoreCase)")
CORS_EMPTY = CORS_SOL.replace("!origin.isEmpty() && ", "")

ex24.method(
    "write", "j8-l2.4-write-cors", "Which origins may read the response", ["o1"], ["J8.08"], ["IMPL"],
    "CORS tells a browser which other origins may read a response; it does not authenticate anyone. Write `corsAllowed(origin, allowedOrigins)` returning true only when the request's origin is **exactly** one of the allowed origins. An empty origin is refused. There is no wildcard: `*` in the list allows nothing special here.",
    [("corsAllowed", [("origin", "String"), ("allowedOrigins", "List<String>")], "boolean")], {"corsAllowed": f_cors},
    [("corsAllowed", ("https://bank.example", ["https://bank.example"]), "an allowed origin"), ("corsAllowed", ("https://evil.example", ["https://bank.example"]), "another origin"), ("corsAllowed", ("", ["https://bank.example"]), "no origin")],
    [("corsAllowed", ("https://bank.example.evil.com", ["https://bank.example"]), "a longer host that starts the same"), ("corsAllowed", ("https://bank.example/", ["https://bank.example"]), "a trailing slash is a different string"),
     ("corsAllowed", ("HTTPS://BANK.EXAMPLE", ["https://bank.example"]), "exact comparison"), ("corsAllowed", ("https://any.example", ["*"]), "a wildcard entry"), ("corsAllowed", ("http://bank.example", ["https://bank.example"]), "a different scheme"),
     ("corsAllowed", ("https://a.example", ["https://b.example", "https://a.example"]), "second in the list"), ("corsAllowed", ("", [""]), "empty origin and empty entry")],
    starter='''
boolean corsAllowed(String origin, List<String> allowedOrigins) {
    return true;
}
''', solution=CORS_SOL,
    wrongs={"wildcard-honoured": CORS_WILD, "prefix-match": CORS_PREFIX, "case-insensitive": CORS_CASE, "empty-origin-allowed": CORS_EMPTY},
    hints=["Compare whole strings, not prefixes.", "What should an empty origin get?"],
    misconceptions=("MC185",), difficulty=2,
)

SECURITY_CODE = '''@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    return http
            .authorizeHttpRequests(requests -> requests
                    .requestMatchers(HttpMethod.GET, "/api/curriculum", "/api/lessons/*", "/api/exercises/*", "/api/projects", "/api/projects/*").permitAll()
                    .requestMatchers("/api/auth/register", "/api/auth/login", "/api/auth/me", "/api/auth/csrf").permitAll()
                    .requestMatchers("/api/**").authenticated()
                    .anyRequest().permitAll())
            .csrf(csrf -> csrf.spa())
            .exceptionHandling(e -> e.authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED)))
            .formLogin(AbstractHttpConfigurer::disable)
            .httpBasic(AbstractHttpConfigurer::disable)
            .build();
}'''
ex24.explain(
    "j8-l2.4-explain-chain", "Reading a real security configuration", ["o2"], ["J8.08"],
    "This is a shortened copy of this platform's real `SecurityConfig`.\n\n" + fence(SECURITY_CODE, "java") + "\n\nAnswer: (1) Which requests can an anonymous visitor make? (2) What does `.requestMatchers(\"/api/**\").authenticated()` add, and why does the order of the matchers matter? (3) What does `anyRequest().permitAll()` at the end allow, and is it a good default? (4) What does `csrf.spa()` mean for a front end? (5) Name one change you would make before exposing this to the internet.",
    "(1) Anonymous visitors can GET the curriculum, lessons, exercises and projects, and call the register, login, me and csrf endpoints. (2) Any other /api path needs an authenticated caller; matchers are tried in order, so the specific permitAll rules must come before the general authenticated rule, or they would never apply. (3) Everything outside /api (the front end files) is open; for the API the default is deny-by-authentication, but anyRequest().permitAll() is allow-by-default for any path added outside /api, which is risky. (4) The front end must read the XSRF-TOKEN cookie and send it in the X-XSRF-TOKEN header on writes. (5) For example serve over HTTPS with Secure cookies, or make the final rule anyRequest().authenticated() or denyAll().",
    levels={
        2: ("The answer gets the matchers, the ordering, the permissive default, the SPA token and a sensible hardening step.", [
            "(1) Anonymous users can GET content endpoints and use the auth endpoints. (2) All other /api paths require login; matchers are checked in order so the permitAll rules must come first. (3) permitAll for everything else covers the static front end, but it is allow-by-default, so a new endpoint outside /api would be public; I would prefer authenticated or deny by default. (4) The front end reads the XSRF-TOKEN cookie and echoes it in X-XSRF-TOKEN. (5) Use HTTPS with Secure cookies.",
            "Anonymous: reading content and logging in/registering. The /api/** rule makes everything else need a session, and it comes after the specific rules because the first match wins. The last rule is permissive, so I would tighten it. csrf.spa means the page must send the XSRF token header on writes. Before the internet: TLS, Secure cookies, rate limiting on login."]),
        1: ("The answer gets some parts but misses the ordering or the permissive default.", [
            "Anonymous users can read content and log in, and the rest needs a login.",
            "CSRF is on, so the front end sends a token."]),
        0: ("The answer misreads the configuration.", [
            "Everything needs a login, nothing is public.",
            "CSRF protection is turned off here."]),
    },
)

l8_l2_4 = Lesson("j8-l2.4", "Spring Security: CSRF and CORS", ["J8.08"], [
    ("o1", "Write the CSRF and CORS decisions as rules"),
    ("o2", "Read a real Spring Security filter-chain configuration"),
], ["j8-l2.1", "j7-l3.1"], 45, ["I102", "I106", "I101"], """## Before you start

You should know what a session cookie is (lesson 8.2.1) and the safe HTTP methods (Stage 7).

## Explanation

**Cross-site request forgery (CSRF):** a malicious page makes the victim's browser send a request to your site, and the browser attaches the victim's session cookie automatically. The server cannot tell it from a real request.

Spring Security's defence is the **synchronizer token pattern**: the server issues a random token, and a state-changing request must carry it in a part of the request that the browser does not add by itself, a header or a form field. By default the header is `X-CSRF-TOKEN` or `X-XSRF-TOKEN`. Safe methods (GET, HEAD, OPTIONS, TRACE) do not change state, so they do not need a token; that is why a GET must never change data.

**CORS** is a different control. It tells browsers which other origins may read responses from your API. It does not authenticate anybody and does not replace CSRF protection. Preflight (`OPTIONS`) requests are part of the mechanism.

Both are configured in Spring Security's **filter chain**: a `SecurityFilterChain` bean built from `HttpSecurity`. `authorizeHttpRequests` declares which requests need which authorisation (`anyRequest().authenticated()` requires an authenticated caller for anything not matched earlier). The matchers are tried in order, so specific rules go first.

## Worked examples

### Example 1: this platform's own configuration.

The exercise shows a shortened copy of the real `SecurityConfig`. It makes content and login endpoints public, requires login for everything else under `/api`, and turns CSRF protection on in SPA mode.

### Example 2: the 403 you met in lesson 8.2.1.

A `DELETE` without a CSRF token was answered 403 before the application looked at the method. That is the filter chain working.

## Where this is used

- Every Spring web application. Understanding the chain is how you debug a surprising 401 or 403.

## Common mistakes

:::mistake{id=MC185}
**Treating CORS and CSRF as one control.** CORS decides which origins may read a response; CSRF protection decides whether a state-changing request was meant by the user. You need to think about both.
:::

## Practice

::exercise{id=j8-l2.4-write-csrf}

::exercise{id=j8-l2.4-write-cors}

::exercise{id=j8-l2.4-explain-chain}

## Further reading

- **Spring Security, CSRF** `[I102]`.
- **Spring Security, authorize HTTP requests** `[I106]`.

## How you'll be assessed

- The **write** exercises check the two decisions (*implementation*).
- The **explain** exercise checks that you can read a real configuration (*explanation*).

The CORS rule here is a simplified model. Spring Security's real CORS support has more options, which this course did not verify beyond the existence of preflight handling.
""")

# ====================================================================== j8-l2.5
def f_locked(events, mx, window, now):
    ev = []
    for e in events:
        t, k = e.split(":")
        ev.append((int(t), k))
    start = 0
    for i, (t, k) in enumerate(ev):
        if k == "ok" and t <= now:
            start = i + 1
    fails = [1 for t, k in ev[start:] if k == "fail" and now - window < t <= now]
    return "true" if len(fails) >= mx else "false"


LOCK_SOL = '''
boolean lockedOut(List<String> events, int maxFailures, int windowSeconds, int now) {
    int start = 0;
    for (int i = 0; i < events.size(); i++) {
        String[] e = events.get(i).split(":");
        if (e[1].equals("ok") && Integer.parseInt(e[0]) <= now) {
            start = i + 1;
        }
    }
    int failures = 0;
    for (int i = start; i < events.size(); i++) {
        String[] e = events.get(i).split(":");
        int t = Integer.parseInt(e[0]);
        if (e[1].equals("fail") && t > now - windowSeconds && t <= now) {
            failures++;
        }
    }
    return failures >= maxFailures;
}
'''
LOCK_NO_RESET = LOCK_SOL.replace("            start = i + 1;\n", "")
LOCK_NO_WINDOW = LOCK_SOL.replace(" && t > now - windowSeconds", "")
LOCK_GT = LOCK_SOL.replace("failures >= maxFailures", "failures > maxFailures")
LOCK_FUTURE = LOCK_SOL.replace(" && t <= now) {\n            failures++;", ") {\n            failures++;")
LOCK_WINDOW_EDGE = LOCK_SOL.replace("t > now - windowSeconds", "t >= now - windowSeconds")

ex25.method(
    "write", "j8-l2.5-write-lockout", "Account lockout", ["o1"], ["J8.09"], ["IMPL"],
    "Events for one account arrive in time order as `seconds:fail` or `seconds:ok`. Write `lockedOut(events, maxFailures, windowSeconds, now)`: the account is locked when, counting only events up to `now`, there are at least `maxFailures` failures within the last `windowSeconds` (a failure at time `t` counts if `now - windowSeconds < t <= now`), **since the most recent successful login**. A success clears the count.",
    [("lockedOut", [("events", "List<String>"), ("maxFailures", "int"), ("windowSeconds", "int"), ("now", "int")], "boolean")], {"lockedOut": lambda e, m, w, n: f_locked(e, m, w, n) == "true"},
    [("lockedOut", (["10:fail", "11:fail", "12:fail"], 3, 60, 20), "three quick failures"), ("lockedOut", (["10:fail", "11:fail"], 3, 60, 20), "only two"), ("lockedOut", (["10:fail", "11:fail", "12:ok", "13:fail"], 3, 60, 20), "a success resets")],
    [("lockedOut", (["10:fail", "11:fail", "12:fail"], 3, 5, 20), "the failures are too old"), ("lockedOut", (["10:fail", "11:fail", "12:fail"], 3, 10, 20), "exactly at the window edge"), ("lockedOut", (["10:fail", "11:fail", "12:fail"], 3, 11, 20), "just inside the window"),
     ("lockedOut", (["10:fail", "11:fail", "50:fail"], 3, 60, 20), "a future failure is ignored"), ("lockedOut", ([], 3, 60, 20), "no events"), ("lockedOut", (["1:fail", "2:fail", "3:fail", "4:fail"], 3, 60, 5), "more than the limit"),
     ("lockedOut", (["1:fail", "2:fail", "3:ok", "4:fail", "5:fail"], 3, 60, 6), "two before and two after a success"), ("lockedOut", (["1:fail", "2:fail", "30:ok"], 2, 60, 20), "a success after now does not reset")],
    starter='''
boolean lockedOut(List<String> events, int maxFailures, int windowSeconds, int now) {
    return false;
}
''', solution=LOCK_SOL,
    wrongs={"success-does-not-reset": LOCK_NO_RESET, "ignores-the-window": LOCK_NO_WINDOW, "needs-more-than-max": LOCK_GT, "counts-the-future": LOCK_FUTURE, "window-edge-off-by-one": LOCK_WINDOW_EDGE},
    hints=["Find where the count starts: just after the last success up to `now`.", "Which comparison excludes a failure exactly `windowSeconds` old?"],
    misconceptions=("MC186",), difficulty=4,
)


def f_login(exists, ok, locked):
    if exists and ok and not locked:
        return "200|ok"
    return "401|Invalid credentials"


LOGIN_SOL = '''
String loginResponse(boolean userExists, boolean passwordOk, boolean locked) {
    if (userExists && passwordOk && !locked) {
        return "200|ok";
    }
    return "401|Invalid credentials";
}
'''
LOGIN_LEAK_USER = LOGIN_SOL.replace('    return "401|Invalid credentials";', '    if (!userExists) {\n        return "401|No such user";\n    }\n    return "401|Invalid credentials";')
LOGIN_LEAK_LOCK = LOGIN_SOL.replace('    return "401|Invalid credentials";', '    if (locked) {\n        return "423|Account locked";\n    }\n    return "401|Invalid credentials";')
LOGIN_LOCKED_OK = LOGIN_SOL.replace(" && !locked", "")

ex25.method(
    "write", "j8-l2.5-write-login-response", "A login answer that tells nothing extra", ["o2"], ["J8.09"], ["IMPL", "MIST"],
    "Write `loginResponse(userExists, passwordOk, locked)`. A success is `200|ok` and needs an existing user, the right password and an account that is not locked. **Every** failure, whatever the reason, must be exactly `401|Invalid credentials`, so an attacker learns nothing about which accounts exist or which are locked.",
    [("loginResponse", [("userExists", "boolean"), ("passwordOk", "boolean"), ("locked", "boolean")], "String")], {"loginResponse": f_login},
    [("loginResponse", (True, True, False), "success"), ("loginResponse", (True, False, False), "wrong password"), ("loginResponse", (False, False, False), "no such user")],
    [("loginResponse", (True, True, True), "locked, right password"), ("loginResponse", (True, False, True), "locked, wrong password"), ("loginResponse", (False, True, False), "no user, password flag set"),
     ("loginResponse", (False, False, True), "no user, locked flag set"), ("loginResponse", (False, True, True), "inconsistent flags")],
    starter='''
String loginResponse(boolean userExists, boolean passwordOk, boolean locked) {
    return "";
}
''', solution=LOGIN_SOL,
    wrongs={"reveals-unknown-user": LOGIN_LEAK_USER, "reveals-lockout": LOGIN_LEAK_LOCK, "locked-account-can-log-in": LOGIN_LOCKED_OK},
    hints=["How many different failure messages should there be?", "Can a locked account succeed with the right password?"],
    misconceptions=("MC186",), difficulty=2,
)

ex25.explain(
    "j8-l2.5-explain-lockout", "Lockout and its cost", ["o1", "o2"], ["J8.09"],
    "A team locks an account for 30 minutes after 5 failed logins, counting failures per source IP address, and shows the message 'No account with that email' for unknown users. Explain two weaknesses in what they built, and one cost of lockout itself that the team should plan for.",
    "Counting per IP address lets an attacker rotate through many addresses and still try unlimited passwords against one account; the OWASP guidance says the counter should belong to the account. The specific message tells an attacker which email addresses have accounts (user enumeration); responses must be generic whatever the reason. A cost of lockout is that an attacker can lock out real customers on purpose by failing logins for their account, a denial of service, so the team needs a recovery path (for example a timed unlock or a reset flow) and monitoring.",
    levels={
        2: ("The answer names both weaknesses with the reason, and a cost of lockout.", [
            "Per-IP counting can be beaten with many addresses, so the counter should be per account. 'No account with that email' lets an attacker find which emails are registered, so every failure should look the same. Lockout can itself be abused to lock real users out, so there needs to be a timed unlock or recovery.",
            "The failure count should follow the account, not the IP, or an attacker can spread guesses over many IPs. The message enumerates users; use one generic message. The cost: deliberately failing logins can lock a customer out, so plan recovery and alerts."]),
        1: ("The answer names one weakness or no cost.", [
            "The message gives away which emails exist.",
            "Count per account instead of per IP."]),
        0: ("The answer approves the design.", [
            "It is helpful to tell users exactly what was wrong.",
            "Per IP is the best way to block attackers."]),
    },
)

l8_l2_5 = Lesson("j8-l2.5", "Lockout and generic responses", ["J8.09"], [
    ("o1", "Count failed logins per account and decide when to lock"),
    ("o2", "Give login answers that do not reveal which accounts exist or are locked"),
], ["j8-l2.1", "j8-l1.2"], 35, ["I105"], """## Before you start

You should have read about password storage and know how a login endpoint answers (lessons 8.1.2 and 8.2.1).

## Explanation

A login form lets anyone guess. Two controls limit guessing.

**Account lockout** stops further login attempts for a period after a number of failures. OWASP's guidance says the counter of failed logins should be associated with the account itself, not the source IP address, so that an attacker cannot avoid it by using many addresses. Related controls are login throttling (slowing attempts) and multi-factor authentication.

**Generic responses:** the application must answer in a generic manner whether the user ID or password was wrong, the account does not exist, or the account is locked or disabled. A message that distinguishes these lets an attacker find which accounts exist (**user enumeration**) and which are locked.

Lockout has a cost: an attacker can lock a real customer out deliberately. Plan a recovery path.

## Worked examples

### Example 1: the window.

With a limit of 3 failures in 60 seconds, three failures at seconds 10, 11 and 12 lock the account at second 20, a success at second 12 would have reset the count.

### Example 2: one answer for every failure.

`401|Invalid credentials` for an unknown user, a wrong password and a locked account.

## Where this is used

- Every login endpoint on the internet. The stage project asks you to add lockout and generic responses to an inherited handler.

## Common mistakes

:::mistake{id=MC186}
**Writing helpful login errors.** "No such user" and "Account locked" help an attacker more than a customer. Keep the message the same and help legitimate users through a reset flow.
:::

## Practice

::exercise{id=j8-l2.5-write-lockout}

::exercise{id=j8-l2.5-write-login-response}

::exercise{id=j8-l2.5-explain-lockout}

## Further reading

- **OWASP Authentication Cheat Sheet** `[I105]`.

## How you'll be assessed

- The **write** exercises check lockout and generic answers (*implementation*).
- The **explain** exercise checks that you can critique a design (*explanation*).
""")
print("module 8.2 authored")
