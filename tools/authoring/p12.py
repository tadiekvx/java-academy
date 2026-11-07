"""Stage 8 project: j8-a1-security-audit (C). A plain-Java request handler with seeded vulnerabilities; the Python model is the oracle."""
import re
import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-8"
from proj import project

MAIN = "\nvoid main() {\n    // Optional: try your handler here.\n}\n"
SIG = [("handleAll", [("requests", "List<String>")], "List<String>")]
GENERIC = "401|Invalid credentials"
USERS = {"ada": ("secret1", "customer"), "grace": ("hunter22", "customer"), "tess": ("teller99", "teller")}
ACCTS = {1: ("ada", 120000), 2: ("grace", 30050)}


def model(requests):
    fails, out = {}, []
    for r in requests:
        parts = r.split(" ", 2)
        if parts[0] == "LOGIN":
            user = parts[1] if len(parts) > 1 else ""
            pw = parts[2] if len(parts) > 2 else ""
            if user not in USERS or fails.get(user, 0) >= 3:
                out.append(GENERIC)
            elif USERS[user][0] == pw:
                fails[user] = 0; out.append("200|ok")
            else:
                fails[user] = fails.get(user, 0) + 1; out.append(GENERIC)
            continue
        actor = parts[0]
        method = parts[1] if len(parts) > 1 else ""
        path = parts[2] if len(parts) > 2 else ""
        if actor not in USERS:
            out.append("401|Unauthorized")
        elif not re.fullmatch(r"/accounts/[0-9]{1,9}", path):
            out.append("404|Not Found")
        elif method != "GET":
            out.append("405|Method Not Allowed")
        else:
            i = int(path.split("/")[2])
            if i not in ACCTS:
                out.append("404|Not Found")
            elif USERS[actor][1] == "teller" or ACCTS[i][0] == actor:
                out.append(f"200|{i};{ACCTS[i][0]};{ACCTS[i][1]}")
            else:
                out.append("403|Forbidden")
    return out


FINAL = '''
// The request handler of Brightbank's account API, after the audit.
// Requests: "LOGIN user password" or "actor METHOD path" (actor "-" means nobody is signed in).

List<String> handleAll(List<String> requests) throws Exception {
    Map<String, String[]> users = new HashMap<>();
    users.put("ada", newUser("ada", "secret1", "customer"));
    users.put("grace", newUser("grace", "hunter22", "customer"));
    users.put("tess", newUser("tess", "teller99", "teller"));
    Map<String, String[]> accounts = new HashMap<>();
    accounts.put("1", new String[] {"ada", "120000"});
    accounts.put("2", new String[] {"grace", "30050"});
    Map<String, Integer> failures = new HashMap<>();
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] parts = request.split(" ", 3);
        if (parts[0].equals("LOGIN")) {
            out.add(login(parts.length > 1 ? parts[1] : "", parts.length > 2 ? parts[2] : "", users, failures));
        } else {
            out.add(read(parts, users, accounts));
        }
    }
    return out;
}

String[] newUser(String name, String password, String role) throws Exception {
    return new String[] {pbkdf2(password, name), role};
}

String pbkdf2(String password, String salt) throws Exception {
    PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt.getBytes(StandardCharsets.UTF_8), 1000, 256);
    byte[] key = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
    return HexFormat.of().formatHex(key);
}

String login(String user, String password, Map<String, String[]> users, Map<String, Integer> failures) throws Exception {
    String generic = "401|Invalid credentials";
    String[] known = users.get(user);
    if (known == null) {
        return generic;
    }
    int failed = failures.getOrDefault(user, 0);
    if (failed >= 3) {
        return generic;
    }
    byte[] attempt = pbkdf2(password, user).getBytes(StandardCharsets.UTF_8);
    if (MessageDigest.isEqual(attempt, known[0].getBytes(StandardCharsets.UTF_8))) {
        failures.put(user, 0);
        return "200|ok";
    }
    failures.put(user, failed + 1);
    return generic;
}

String read(String[] parts, Map<String, String[]> users, Map<String, String[]> accounts) {
    String actor = parts[0];
    String method = parts.length > 1 ? parts[1] : "";
    String path = parts.length > 2 ? parts[2] : "";
    if (!users.containsKey(actor)) {
        return "401|Unauthorized";
    }
    if (!path.matches("/accounts/[0-9]{1,9}")) {
        return "404|Not Found";
    }
    if (!method.equals("GET")) {
        return "405|Method Not Allowed";
    }
    String id = String.valueOf(Integer.parseInt(path.substring("/accounts/".length())));
    String[] account = accounts.get(id);
    if (account == null) {
        return "404|Not Found";
    }
    if (users.get(actor)[1].equals("teller") || account[0].equals(actor)) {
        return "200|" + id + ";" + account[0] + ";" + account[1];
    }
    return "403|Forbidden";
}
'''
INHERITED = '''
// INHERITED CODE: the account API's request handler, as found. Passwords are checked as typed.
// Requests: "LOGIN user password" or "actor METHOD path" (actor "-" means nobody is signed in).
// Audit scope: find what is wrong, fix it in two steps, and report what you found in the design note.

List<String> handleAll(List<String> requests) {
    Map<String, String[]> users = new HashMap<>();
    users.put("ada", new String[] {"secret1", "customer"});
    users.put("grace", new String[] {"hunter22", "customer"});
    users.put("tess", new String[] {"teller99", "teller"});
    Map<String, String[]> accounts = new HashMap<>();
    accounts.put("1", new String[] {"ada", "120000"});
    accounts.put("2", new String[] {"grace", "30050"});
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] parts = request.split(" ", 3);
        if (parts[0].equals("LOGIN")) {
            String user = parts.length > 1 ? parts[1] : "";
            String password = parts.length > 2 ? parts[2] : "";
            String[] known = users.get(user);
            if (known == null) {
                out.add("401|No such user");
            } else if (!known[0].equals(password)) {
                out.add("401|Wrong password");
            } else {
                out.add("200|ok");
            }
        } else {
            String method = parts.length > 1 ? parts[1] : "";
            String path = parts.length > 2 ? parts[2] : "";
            if (!path.matches("/accounts/[0-9]{1,9}")) {
                out.add("404|Not Found");
            } else if (!method.equals("GET")) {
                out.add("405|Method Not Allowed");
            } else {
                String id = String.valueOf(Integer.parseInt(path.substring("/accounts/".length())));
                String[] account = accounts.get(id);
                if (account == null) {
                    out.add("404|No account " + id + " in table accounts (SELECT * FROM accounts WHERE id=" + id + ")");
                } else {
                    out.add("200|" + id + ";" + account[0] + ";" + account[1]);
                }
            }
        }
    }
    return out;
}
'''
IMPORTS = "import java.nio.charset.StandardCharsets;\nimport java.security.MessageDigest;\nimport javax.crypto.SecretKeyFactory;\nimport javax.crypto.spec.PBEKeySpec;\n"


def wrong(old, new, src=FINAL):
    assert old in src, old
    return src.replace(old, new, 1)


WRONGS = {
    "m1-anonymous-allowed": wrong('    if (!users.containsKey(actor)) {\n        return "401|Unauthorized";\n    }\n', ""),
    "m1-any-customer-reads-any-account": wrong('users.get(actor)[1].equals("teller") || account[0].equals(actor)', 'users.containsKey(actor)'),
    "m1-verbose-404": wrong('    if (account == null) {\n        return "404|Not Found";', '    if (account == null) {\n        return "404|No account " + id + " in table accounts";'),
    "m1-teller-cannot-read": wrong('users.get(actor)[1].equals("teller") || ', ""),
    "m2-reveals-unknown-user": wrong('    if (known == null) {\n        return generic;', '    if (known == null) {\n        return "401|No such user";'),
    "m2-no-lockout": wrong("    if (failed >= 3) {\n        return generic;\n    }\n", ""),
    "m2-success-keeps-count": wrong('        failures.put(user, 0);\n        return "200|ok";', '        return "200|ok";'),
    "m2-lockout-message-differs": wrong("    if (failed >= 3) {\n        return generic;", '    if (failed >= 3) {\n        return "423|Account locked";'),
    "m2-not-hashed": wrong("MessageDigest.isEqual(attempt, known[0].getBytes(StandardCharsets.UTF_8))", "Arrays.equals(attempt, known[0].getBytes(StandardCharsets.UTF_8))"),
    "m2-locks-after-four": wrong("failed >= 3", "failed >= 4"),
}


def case(name, *reqs):
    return ("handleAll", (list(reqs),), name)


M1V = [case("signed in as the owner", "ada GET /accounts/1"), case("another customer's account", "ada GET /accounts/2"), case("nobody signed in", "- GET /accounts/1")]
M1H = M1V + [
    case("a teller reads any", "tess GET /accounts/1", "tess GET /accounts/2"),
    case("an unknown actor", "mallory GET /accounts/1"),
    case("a missing account gives no detail", "ada GET /accounts/9"),
    case("a malformed path", "ada GET /accounts/abc", "ada GET /accounts/"),
    case("a wrong method", "ada DELETE /accounts/1", "ada POST /accounts/1 x"),
    case("a leading-zero id", "ada GET /accounts/001"),
    case("grace and ada", "grace GET /accounts/2", "grace GET /accounts/1"),
]
M2V = [case("a good login", "LOGIN ada secret1"), case("a wrong password", "LOGIN ada nope"), case("an unknown user", "LOGIN mallory x")]
M2H = M2V + M1H + [
    case("three failures lock the account", "LOGIN ada a", "LOGIN ada b", "LOGIN ada c", "LOGIN ada secret1"),
    case("two failures do not", "LOGIN ada a", "LOGIN ada b", "LOGIN ada secret1"),
    case("a success resets the count", "LOGIN ada a", "LOGIN ada b", "LOGIN ada secret1", "LOGIN ada c", "LOGIN ada d", "LOGIN ada secret1"),
    case("accounts are counted separately", "LOGIN ada a", "LOGIN ada b", "LOGIN ada c", "LOGIN grace hunter22"),
    case("an empty password", "LOGIN ada ", "LOGIN ada"),
    case("a password with spaces", "LOGIN ada secret1 extra"),
    case("a teller logs in", "LOGIN tess teller99"),
    case("unknown users never lock anything", "LOGIN x a", "LOGIN x b", "LOGIN x c", "LOGIN x d"),
]
RUBRIC = [
    ("Findings", "Fewer than three vulnerabilities named, or none with a category", "Names the vulnerabilities but not their OWASP Top 10:2025 categories", "Names every seeded vulnerability, with its OWASP category, evidence from a request, and its impact"),
    ("Remediation", "A fix that only hides the symptom, or breaks an earlier answer", "Fixes the problems but changes unrelated behaviour", "Each fix is the smallest correct change, in two separate steps, with the earlier checks still passing"),
    ("Design choices", "No discussion of trade-offs", "Notes a trade-off without a reason", "Explains the 403/404 choice, why lockout belongs to the account, and what lockout costs"),
    ("Report", "Missing, or only describes the code", "A list of problems without priorities", "A short report a team lead could act on: findings ranked by risk, fixes made, and what is still open"),
]
ms = [
    dict(id="m1", title="Access control", methods=SIG, fns={"handleAll": model}, visible=M1V, hidden=M1H, instructions="""
        Request lines are `actor METHOD path`; the actor `-` means nobody is signed in. Audit `GET /accounts/{id}` and fix it:

        - An actor who is not a known user gets `401|Unauthorized`.
        - A customer may read only an account they own; anyone else gets `403|Forbidden`. A teller may read any account.
        - A missing account answers exactly `404|Not Found`, with no detail about tables or queries.
        - Keep the existing routing: a path that is not `/accounts/{digits}` is a 404, another method on it is a 405.
        """),
    dict(id="m2", title="Login", methods=SIG, fns={"handleAll": model}, visible=M2V, hidden=M2H,
         source_tests=[("passwords are hashed with PBKDF2 and compared with isEqual", ["PBKDF2WithHmacSHA256", "MessageDigest.isEqual"], None)],
         instructions="""
        `LOGIN user password` should follow lessons 8.1.2 and 8.2.5:

        - A success is `200|ok`. **Every** failure (unknown user, wrong password, locked account) is exactly `401|Invalid credentials`.
        - After **three** failed logins in a row for a user, that account is locked: even the right password gets the generic failure. A success before that resets the count. Unknown users are never counted.
        - Stored passwords are not kept as typed. Keep a PBKDF2 hash (`PBKDF2WithHmacSHA256`, 256 bits, 1000 iterations here, the user's name as the salt) and compare hashes with `MessageDigest.isEqual`.
        """),
]
project("j8-a1-security-audit", "Audit the account API", "C",
        "Audit an inherited request handler for security flaws, fix them in two steps, and write the findings up as a short report.",
        """
        You have been asked to review the account API's request handler before it goes near real customers. It works, and it is insecure in several ways that the stage's lessons cover.

        Do what a reviewer would do: read the code, **write down every flaw you can find** with its OWASP Top 10:2025 category before you change anything, then fix them in two steps, running all the checks after each step:

        1. **Access control** for reading an account.
        2. **Login**: generic answers, lockout and hashed passwords.

        Your design note is the audit report.
        """, 4, ["j8-l1.2", "j8-l1.4", "j8-l2.3", "j8-l2.5"], ["J8.01", "J8.02", "J8.07", "J8.09"],
        ["Only authenticated callers read accounts, and customers read only their own.",
         "Login failures all look the same, and three failures in a row lock the account.",
         "Passwords are stored as PBKDF2 hashes."],
        ["Fix one area at a time.", "Run all the checks after every change.", "Do not add libraries: the JDK has what you need."],
        ["Given another customer's account, then 403.",
         "Given three failed logins, then even the right password fails with the generic message.",
         "Given a missing account, then the response reveals nothing about the database."],
        ms, RUBRIC,
        "Write the audit report (200 words or fewer): list each flaw you found, its OWASP Top 10:2025 category, the request that shows it, and its impact; rank them by risk; say what you fixed in each step and what you left open (for example: no transport security, no session handling, lockout that never expires). Explain why you chose 403 for another customer's account rather than 404.",
        INHERITED.replace("List<String> handleAll", "List<String> handleAll") + MAIN, IMPORTS + FINAL + MAIN, {k: IMPORTS + v + MAIN for k, v in WRONGS.items()})
print("P12 written")
