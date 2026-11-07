"""Stage 8 authoring: module 8.1 (Security fundamentals). Expected values come from Python (hashlib, hmac), not from Java."""
import hashlib
import posixpath
import re
import l8common
from l8common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex11 = Exercises("j8-l1.1")
ex12 = Exercises("j8-l1.2")
ex13 = Exercises("j8-l1.3")
ex14 = Exercises("j8-l1.4")

REGISTER = {
    "j8-l1.1": ("Threat modelling and the OWASP Top 10", ["J8.01"]),
    "j8-l1.2": ("Passwords and hashing", ["J8.02"]),
    "j8-l1.3": ("Untrusted input: encoding and paths", ["J8.03"]),
    "j8-l1.4": ("Secrets and logging", ["J8.04"]),
}
MISCS = {
    "MC178": (["J8.01"], "I95", "Security is a checklist applied at the end; a feature that passes its tests is secure"),
    "MC179": (["J8.02"], "I96", "Hashing a password with SHA-256 is enough, because a hash cannot be reversed"),
    "MC180": (["J8.03"], "I97", "Validating input on the way in makes it safe to put into any output"),
    "MC181": (["J8.04"], "I98", "A secret in a private repository or in a log line is safe because only the team can see it"),
}
register(REGISTER, MISCS)

# ====================================================================== j8-l1.1
def f_rank(threats):
    rows = []
    for t in threats:
        name, lk, im = t.split(":")
        rows.append((-(int(lk) * int(im)), name, int(lk) * int(im)))
    return [f"{n}={s}" for _, n, s in sorted(rows)]


RANK_SOL = '''
List<String> rank(List<String> threats) {
    List<String[]> rows = new ArrayList<>();
    for (String threat : threats) {
        String[] p = threat.split(":");
        rows.add(new String[] {p[0], String.valueOf(Integer.parseInt(p[1]) * Integer.parseInt(p[2]))});
    }
    rows.sort((a, b) -> {
        int byScore = Integer.compare(Integer.parseInt(b[1]), Integer.parseInt(a[1]));
        return byScore != 0 ? byScore : a[0].compareTo(b[0]);
    });
    List<String> out = new ArrayList<>();
    for (String[] row : rows) {
        out.add(row[0] + "=" + row[1]);
    }
    return out;
}
'''
RANK_ASC = RANK_SOL.replace("Integer.compare(Integer.parseInt(b[1]), Integer.parseInt(a[1]))", "Integer.compare(Integer.parseInt(a[1]), Integer.parseInt(b[1]))")
RANK_NO_TIE = RANK_SOL.replace("return byScore != 0 ? byScore : a[0].compareTo(b[0]);", "return byScore;")
RANK_SUM = RANK_SOL.replace("Integer.parseInt(p[1]) * Integer.parseInt(p[2])", "Integer.parseInt(p[1]) + Integer.parseInt(p[2])")

ex11.method(
    "write", "j8-l1.1-write-rank", "Ranking threats", ["o1"], ["J8.01"], ["IMPL"],
    "A simple threat model scores each threat as likelihood times impact, each from 1 to 5. Each threat is `name:likelihood:impact`. Write `rank(threats)` returning `name=score` for each, highest score first, and alphabetical by name when scores are equal. (This is a teaching model; real risk rating needs more than one multiplication.)",
    [("rank", [("threats", "List<String>")], "List<String>")], {"rank": f_rank},
    [("rank", (["forged-transfer:2:5", "weak-password:4:4", "log-leak:3:2"],), "three threats"), ("rank", (["a:1:1"],), "one threat"), ("rank", ([],), "no threats")],
    [("rank", (["b:3:3", "a:3:3", "c:1:9"],), "ties and a high-impact threat"), ("rank", (["x:5:5", "y:5:1", "z:1:5"],), "equal scores"),
     ("rank", (["idor:4:5", "xss:3:4", "sqli:2:5", "dos:3:3"],), "four threats"), ("rank", (["m:5:5", "n:5:5"],), "an exact tie"),
     ("rank", (["p:1:2", "q:2:1", "r:1:1"],), "small scores")],
    starter='''
List<String> rank(List<String> threats) {
    return List.of();
}
''', solution=RANK_SOL,
    wrongs={"lowest-first": RANK_ASC, "ties-unordered": RANK_NO_TIE, "adds-instead-of-multiplies": RANK_SUM},
    hints=["Compute the score as a number, then sort by it.", "What decides the order when two scores are equal?"],
    misconceptions=("MC178",), difficulty=2,
)

OWASP = {
    "missing-ownership-check": "A01 Broken Access Control",
    "sql-built-from-input": "A05 Injection",
    "no-login-lockout": "A07 Authentication Failures",
    "failed-logins-not-logged": "A09 Security Logging and Alerting Failures",
    "vulnerable-dependency": "A03 Software Supply Chain Failures",
}


def f_owasp(weakness):
    return OWASP.get(weakness, "unmapped")


OWASP_SOL = '''
String owaspFor(String weakness) {
    return switch (weakness) {
        case "missing-ownership-check" -> "A01 Broken Access Control";
        case "sql-built-from-input" -> "A05 Injection";
        case "no-login-lockout" -> "A07 Authentication Failures";
        case "failed-logins-not-logged" -> "A09 Security Logging and Alerting Failures";
        case "vulnerable-dependency" -> "A03 Software Supply Chain Failures";
        default -> "unmapped";
    };
}
'''
OWASP_2021 = OWASP_SOL.replace('"A05 Injection"', '"A03 Injection"')
OWASP_SWAP = OWASP_SOL.replace('"A01 Broken Access Control"', '"A07 Authentication Failures"', 1).replace('case "no-login-lockout" -> "A07 Authentication Failures"', 'case "no-login-lockout" -> "A01 Broken Access Control"')
OWASP_DEFAULT = OWASP_SOL.replace('default -> "unmapped";', 'default -> "A02 Security Misconfiguration";')

ex11.method(
    "write", "j8-l1.1-write-owasp", "Finding the category", ["o2"], ["J8.01"], ["IMPL"],
    "Map a weakness to its category in the **OWASP Top 10:2025** (the 2025 list, not older ones). Write `owaspFor(weakness)` returning the category as `A01 Broken Access Control` style text for: `missing-ownership-check` (A01), `sql-built-from-input` (A05), `vulnerable-dependency` (A03), `no-login-lockout` (A07), `failed-logins-not-logged` (A09). Anything else is `unmapped`.",
    [("owaspFor", [("weakness", "String")], "String")], {"owaspFor": f_owasp},
    [("owaspFor", ("missing-ownership-check",), "an access-control gap"), ("owaspFor", ("sql-built-from-input",), "injection"), ("owaspFor", ("something-else",), "not on the list")],
    [("owaspFor", ("no-login-lockout",), "authentication"), ("owaspFor", ("failed-logins-not-logged",), "logging"), ("owaspFor", ("vulnerable-dependency",), "supply chain"),
     ("owaspFor", ("",), "empty"), ("owaspFor", ("MISSING-OWNERSHIP-CHECK",), "exact names only")],
    starter='''
String owaspFor(String weakness) {
    return "";
}
''', solution=OWASP_SOL,
    wrongs={"2021-numbering": OWASP_2021, "swapped-categories": OWASP_SWAP, "guesses-a-default": OWASP_DEFAULT},
    hints=["Use the exact A-numbers and names of the 2025 list.", "What should an unknown weakness return?"],
    misconceptions=("MC178",), difficulty=2,
)

ex11.explain(
    "j8-l1.1-explain-threat-model", "A threat model for a transfer", ["o1"], ["J8.01"],
    "Brightbank lets a signed-in customer transfer money between accounts through `POST /accounts/{id}/transfers`. Build a small threat model: name what is worth protecting, who might attack and from where, and give three concrete threats with the control that would stop each. Link at least two of the threats to a category of the OWASP Top 10:2025.",
    "A threat model names the assets (balances, the ability to move money, credentials), the actors (an outsider, another customer, a malicious insider) and the entry points (the endpoint, the session, the database). Concrete threats could be: another customer transferring from an account they do not own (A01 Broken Access Control, stopped by an ownership check on every request); a forged request made from another site while the customer is signed in (stopped by a CSRF token); guessing a customer's password (A07 Authentication Failures, slowed by lockout and slow password hashing). Each threat is paired with a control.",
    levels={
        2: ("The answer names assets, actors and entry points, and gives three threats each with a specific control and at least two OWASP categories.", [
            "Assets: balances and the right to move money. Actors: an outsider and another customer. Entry point: the transfer endpoint and the session cookie. Threats: (1) customer A transfers from customer B's account by changing the id, A01 Broken Access Control, stopped by checking ownership on every request; (2) a malicious site makes the browser send the POST, stopped by a CSRF token; (3) password guessing, A07 Authentication Failures, stopped by lockout and a slow password hash.",
            "Protect the accounts and the credentials. Attackers: a stranger on the internet and a logged-in customer. Threats and controls: changing the account id in the URL (A01, check that the account belongs to the caller); sending many password guesses (A07, lockout and generic errors); injecting SQL through the amount or note field (A05 Injection, bound parameters)."]),
        1: ("The answer lists threats without controls, or without the actors and assets.", [
            "Someone could steal money by changing the id, or guess passwords.",
            "Threats: injection, broken access control and weak passwords."]),
        0: ("The answer lists generic advice, not threats to this feature.", [
            "Use HTTPS and a firewall and the system will be secure.",
            "There is no threat because the user is signed in."]),
    },
)

l8_l1_1 = Lesson("j8-l1.1", "Threat modelling and the OWASP Top 10", ["J8.01"], [
    ("o1", "Build a small threat model: assets, actors, entry points, threats and controls"),
    ("o2", "Place a weakness in the right OWASP Top 10:2025 category"),
], ["j7-l3.2"], 40, ["I95"], """## Before you start

You should know how an API handles a request (Stage 7) and have seen an injection (Stage 6).

## Explanation

Security work starts by asking what could go wrong, before writing a control. A **threat model** answers four questions about a feature: what is worth protecting (the **assets**), who might attack it (the **actors**), where they can reach it (the **entry points**), and so which **threats** exist and which **controls** stop them. It is a short written exercise, not a tool.

The **OWASP Top 10** is a standard awareness document, a broad consensus about the most critical security risks to web applications. The 2025 edition lists: A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions. Learn the names: reports, tools and colleagues use them as shorthand.

A threat model also lets you rank. A crude but useful way is likelihood times impact; the exercise uses it to show why two threats of equal size need a tie-break rule.

## Worked examples

### Example 1: a transfer endpoint.

Assets: balances, the right to move money. Actors: an outsider; another customer. Entry points: the endpoint, the session cookie. One threat: another customer changes the account id in the URL. Category: A01 Broken Access Control. Control: check ownership on every request.

### Example 2: reading the list.

This course's earlier stages already met three categories: injection (A05, Stage 6), access control (A01) in the REST routing of Stage 7, and supply chain (A03) in the Maven lesson of Stage 4.

## Where this is used

- Design reviews, pull request reviews and audit reports. The project of this stage asks you to write one.

## Common mistakes

:::mistake{id=MC178}
**Treating security as a final checklist.** A feature that passes its functional tests can still let one customer read another's data. Ask what could go wrong while designing.
:::

## Practice

::exercise{id=j8-l1.1-write-rank}

::exercise{id=j8-l1.1-write-owasp}

::exercise{id=j8-l1.1-explain-threat-model}

## Further reading

- **OWASP Top 10:2025** `[I95]`.

## How you'll be assessed

- The **write** exercises check ranking and the 2025 category names (*implementation*).
- The **explain** exercise checks that you can build a small threat model (*explanation*).
""")

# ====================================================================== j8-l1.2
def pbkdf2(pw, salt, iters):
    return hashlib.pbkdf2_hmac("sha256", pw.encode(), bytes.fromhex(salt), iters).hex()


PBK_SOL = '''
String pbkdf2Hex(String password, String saltHex, int iterations) throws Exception {
    byte[] salt = new byte[saltHex.length() / 2];
    for (int i = 0; i < salt.length; i++) {
        salt[i] = (byte) Integer.parseInt(saltHex.substring(2 * i, 2 * i + 2), 16);
    }
    PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, iterations, 256);
    byte[] key = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
    StringBuilder hex = new StringBuilder();
    for (byte b : key) {
        hex.append(String.format("%02x", b));
    }
    return hex.toString();
}
'''
PBK_SHA = PBK_SOL.replace("    PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, iterations, 256);\n    byte[] key = SecretKeyFactory.getInstance(\"PBKDF2WithHmacSHA256\").generateSecret(spec).getEncoded();",
                          "    MessageDigest digest = MessageDigest.getInstance(\"SHA-256\");\n    digest.update(salt);\n    byte[] key = digest.digest(password.getBytes(java.nio.charset.StandardCharsets.UTF_8));")
PBK_ITER = PBK_SOL.replace("salt, iterations, 256", "salt, iterations + 1, 256")
PBK_NOSALT = PBK_SOL.replace("new PBEKeySpec(password.toCharArray(), salt, iterations, 256)", "new PBEKeySpec(password.toCharArray(), new byte[16], iterations, 256)")

ex12.method(
    "write", "j8-l1.2-write-pbkdf2", "A salted, slow hash", ["o1"], ["J8.02"], ["IMPL"],
    "Write `pbkdf2Hex(password, saltHex, iterations)`: the PBKDF2 key, using `PBKDF2WithHmacSHA256` with a 256-bit result, as 64 lowercase hex characters. The salt arrives as hex text. (The checks use few iterations so they run fast; real systems use far more, and a library such as Spring Security's `PasswordEncoder` chooses and stores the parameters for you.)",
    [("pbkdf2Hex", [("password", "String"), ("saltHex", "String"), ("iterations", "int")], "String")], {"pbkdf2Hex": pbkdf2},
    [("pbkdf2Hex", ("correct horse", "000102030405060708090a0b0c0d0e0f", 1000), "a normal password"), ("pbkdf2Hex", ("correct horse", "ffeeddccbbaa99887766554433221100", 1000), "the same password, another salt"),
     ("pbkdf2Hex", ("", "00", 1), "an empty password")],
    [("pbkdf2Hex", ("password", "73616c74", 1), "one iteration"), ("pbkdf2Hex", ("password", "73616c74", 2), "two iterations"), ("pbkdf2Hex", ("pässwörd", "73616c74", 1000), "non-ASCII is UTF-8"),
     ("pbkdf2Hex", ("a much longer passphrase with spaces in it", "0102030405060708", 5000), "a long passphrase"), ("pbkdf2Hex", ("x", "00ff", 10), "salt bytes above 0x7f")],
    starter='''
String pbkdf2Hex(String password, String saltHex, int iterations) throws Exception {
    return "";
}
''', solution=PBK_SOL,
    wrongs={"plain-sha256": PBK_SHA, "wrong-iterations": PBK_ITER, "ignores-the-salt": PBK_NOSALT},
    hints=["`SecretKeyFactory` with the `PBKDF2WithHmacSHA256` algorithm and a `PBEKeySpec`.", "Convert each pair of hex characters to one byte for the salt."],
    misconceptions=("MC179",), difficulty=3,
)


def verify(attempt, salt, iters, expected):
    return "true" if pbkdf2(attempt, salt, iters) == expected else "false"


VERIFY_SOL = PBK_SOL + '''
String verify(String attempt, String saltHex, int iterations, String expectedHex) throws Exception {
    byte[] got = pbkdf2Hex(attempt, saltHex, iterations).getBytes(java.nio.charset.StandardCharsets.UTF_8);
    byte[] want = expectedHex.getBytes(java.nio.charset.StandardCharsets.UTF_8);
    return MessageDigest.isEqual(got, want) ? "true" : "false";
}
'''
VERIFY_EQUALS = VERIFY_SOL.replace("MessageDigest.isEqual(got, want)", "new String(got).equals(new String(want))")
VERIFY_ALWAYS = VERIFY_SOL.replace("return MessageDigest.isEqual(got, want) ? \"true\" : \"false\";", "return \"true\";")
VERIFY_CASE = VERIFY_SOL.replace("expectedHex.getBytes", "expectedHex.toLowerCase().getBytes")
_H = pbkdf2("s3cret!", "0a0b0c0d", 1000)
VSTUB = '''
String pbkdf2Hex(String password, String saltHex, int iterations) throws Exception {
    // Reuse your solution from the previous exercise, or paste it here.
    return "";
}

String verify(String attempt, String saltHex, int iterations, String expectedHex) throws Exception {
    return "false";
}
'''
ex12.method(
    "write", "j8-l1.2-write-verify", "Checking a login attempt", ["o1"], ["J8.02"], ["IMPL"],
    "Write `verify(attempt, saltHex, iterations, expectedHex)` returning `true` or `false`: hash the attempt with `pbkdf2Hex` (provided as a method you must also keep correct) and compare it with the stored hash using `MessageDigest.isEqual`, not `equals`. The stored hash is lower case hex.",
    [("verify", [("attempt", "String"), ("saltHex", "String"), ("iterations", "int"), ("expectedHex", "String")], "String")], {"verify": verify},
    [("verify", ("s3cret!", "0a0b0c0d", 1000, _H), "the right password"), ("verify", ("s3cret?", "0a0b0c0d", 1000, _H), "a wrong password"), ("verify", ("s3cret!", "0a0b0c0e", 1000, _H), "the wrong salt")],
    [("verify", ("S3CRET!", "0a0b0c0d", 1000, _H), "case matters"), ("verify", ("", "0a0b0c0d", 1000, _H), "empty attempt"), ("verify", ("s3cret!", "0a0b0c0d", 999, _H), "the wrong iteration count"),
     ("verify", ("s3cret!", "0a0b0c0d", 1000, _H.upper()), "the stored hash is lower case"), ("verify", ("s3cret!", "0a0b0c0d", 1000, ""), "no stored hash"),
     ("verify", ("s3cret! ", "0a0b0c0d", 1000, _H), "a trailing space")],
    starter=VSTUB, solution=VERIFY_SOL,
    wrongs={"plain-equals": VERIFY_EQUALS, "always-true": VERIFY_ALWAYS, "case-insensitive-hash": VERIFY_CASE},
    hints=["Hash the attempt exactly as you hashed the original.", "Compare as byte arrays with the JDK's digest comparison."],
    source_tests=[("compares with MessageDigest.isEqual", ["MessageDigest.isEqual"], None)],
    misconceptions=("MC179",), difficulty=3,
)

SALT_PROGRAM = '''
String hex(byte[] bytes) {
    StringBuilder out = new StringBuilder();
    for (byte b : bytes) {
        out.append(String.format("%02x", b));
    }
    return out.toString();
}

byte[] pbkdf2(String password, byte[] salt) throws Exception {
    PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 1000, 256);
    return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
}

void main() throws Exception {
    byte[] saltA = {1, 2, 3, 4};
    byte[] saltB = {4, 3, 2, 1};
    String one = hex(pbkdf2("hunter2", saltA));
    String two = hex(pbkdf2("hunter2", saltA));
    String three = hex(pbkdf2("hunter2", saltB));
    String sha = hex(MessageDigest.getInstance("SHA-256").digest("abc".getBytes()));
    System.out.println("same password, same salt equal=" + one.equals(two));
    System.out.println("same password, other salt equal=" + one.equals(three));
    System.out.println("hash length=" + one.length());
    System.out.println("sha-256 of abc starts with " + sha.substring(0, 8));
}
'''
ex12.predict(
    "j8-l1.2-predict-salt", "What a salt changes", ["o2"], ["J8.02"],
    "The program hashes the same password twice with one salt and once with another, and also prints the start of the SHA-256 digest of `abc` (a published test vector). Predict the exact output.",
    "import java.security.*;\nimport javax.crypto.*;\nimport javax.crypto.spec.*;\n" + SALT_PROGRAM,
    "same password, same salt equal=true\nsame password, other salt equal=false\nhash length=64\nsha-256 of abc starts with ba7816bf\n",
    ["Is the hash a function of the password alone?", "How many hex characters is a 256-bit value?"],
    misconceptions=("MC179",), difficulty=2,
)

ex12.explain(
    "j8-l1.2-explain-storage", "How to store a password", ["o2"], ["J8.02"],
    "A colleague proposes storing passwords encrypted with AES, so that support staff can read them back when a customer forgets. Another proposes storing `SHA-256(password)`. Explain what is wrong with each, and what to store instead. Mention what a salt is for.",
    "A password never needs to be read back: the system only needs to check an attempt, so it should store a one-way hash. Encryption is reversible, so anyone with the key (or a copy of the database and the key) gets every password. A plain SHA-256 is one-way but fast, which lets an attacker try huge numbers of guesses, and identical passwords give identical hashes. Store the result of a slow, purpose-built algorithm (Argon2id, bcrypt or PBKDF2) with a unique random salt per password, which defeats precomputed tables and makes equal passwords differ. A library encoder such as Spring Security's PasswordEncoder does this and records the algorithm so it can be upgraded.",
    levels={
        2: ("The answer rejects both, explains reversibility and speed, and names a slow salted hash and the salt's purpose.", [
            "Encryption can be reversed, so a stolen database plus the key reveals every password, and there is no need to read a password back at all. A bare SHA-256 is fast, so an attacker can try billions of guesses, and equal passwords give equal hashes. Store a slow salted hash such as bcrypt, Argon2id or PBKDF2. The unique salt means precomputed tables do not work and two users with the same password get different hashes.",
            "Neither. Support never needs the original password, so store only a one-way hash. SHA-256 alone is too fast to resist guessing. Use a slow algorithm like Argon2id or PBKDF2 with a random salt per user; the salt stops rainbow tables. In Spring I would use the PasswordEncoder."]),
        1: ("The answer rejects one proposal, or names the right algorithm without saying why.", [
            "Encryption is bad because it can be decrypted.",
            "Use bcrypt."]),
        0: ("The answer accepts one of the proposals.", [
            "SHA-256 is fine because a hash cannot be reversed.",
            "Encryption is safest, since only the key holder can read it."]),
    },
)

l8_l1_2 = Lesson("j8-l1.2", "Passwords and hashing", ["J8.02"], [
    ("o1", "Compute a salted PBKDF2 hash and compare an attempt against it safely"),
    ("o2", "Explain why passwords are hashed with a slow salted algorithm, not encrypted or hashed once"),
], ["j8-l1.1"], 45, ["I96", "I103", "I107"], """## Before you start

You should know what a hash function is from the collections lessons (`hashCode`), and what a byte array is.

## Explanation

A system never needs a user's password back. It needs to answer one question: is this attempt the same password? So it stores a **one-way** transformation, a hash, and hashes each attempt the same way to compare. Spring Security's `PasswordEncoder` is exactly this: a one-way transformation to store a password safely, unsuitable where the original value is needed back (such as credentials your application must present to a database).

Not every hash is suitable. The OWASP password storage guidance says to use a slow hashing algorithm such as **Argon2id**, **bcrypt** or **PBKDF2**, and that fast hashes such as SHA-256 are not suitable because they let an attacker make large numbers of guesses. A unique **salt** must be added to each password so that precomputed lookup tables (rainbow tables) do not work and equal passwords produce different hashes.

The JDK provides PBKDF2 as `SecretKeyFactory` with the standard algorithm name `PBKDF2WithHmacSHA256`. In production you rarely call it by hand: `DelegatingPasswordEncoder`, which this platform uses, supports several encodings at once because many applications have older ones, and it records which one was used with each stored value.

When you compare a stored hash with an attempt, compare in a way that does not stop at the first differing byte; `MessageDigest.isEqual` examines all bytes of its first argument (unless the second is null or empty).

## Worked examples

### Example 1: the salt changes the result.

The predict exercise hashes one password with two salts and gets two different 64-character values, and shows that SHA-256 of `abc` begins `ba7816bf`.

### Example 2: this platform's own encoder.

`SecurityConfig` registers `PasswordEncoderFactories.createDelegatingPasswordEncoder()`. No password is ever stored by this application as typed.

## Where this is used

- Every login. A leaked database of slow salted hashes is far less damaging than a leaked table of passwords.

## Common mistakes

:::mistake{id=MC179}
**Hashing a password once with SHA-256 and calling it secure.** It is one-way, but it is fast, so guessing is cheap. Use a slow, salted password hash.
:::

## Practice

::exercise{id=j8-l1.2-predict-salt}

::exercise{id=j8-l1.2-write-pbkdf2}

::exercise{id=j8-l1.2-write-verify}

::exercise{id=j8-l1.2-explain-storage}

## Further reading

- **OWASP Password Storage Cheat Sheet** `[I96]`.
- **Spring Security, password storage** `[I103]`.
- **Java Security Standard Algorithm Names** `[I107]`.

## How you'll be assessed

- The **predict** exercise checks that you can see what a salt does (*identifying*).
- The **write** exercises check hashing and comparison (*implementation*).
- The **explain** exercise checks the case for slow salted hashes (*explanation*).

The exercises use few iterations so they run quickly. They are not a recommendation for real parameters.
""")

# ====================================================================== j8-l1.3
ESC = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#x27;"}


def f_escape(s):
    return "".join(ESC.get(c, c) for c in s)


ESC_SOL = '''
String htmlEscape(String text) {
    StringBuilder out = new StringBuilder();
    for (char c : text.toCharArray()) {
        switch (c) {
            case '&' -> out.append("&amp;");
            case '<' -> out.append("&lt;");
            case '>' -> out.append("&gt;");
            case '"' -> out.append("&quot;");
            case '\\'' -> out.append("&#x27;");
            default -> out.append(c);
        }
    }
    return out.toString();
}
'''
ESC_REPLACE_CHAIN = '''
String htmlEscape(String text) {
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;");
}
'''
ESC_NO_QUOTES = ESC_SOL.replace('''            case '"' -> out.append("&quot;");\n            case '\\'' -> out.append("&#x27;");\n''', "")
ESC_SCRIPT_ONLY = '''
String htmlEscape(String text) {
    return text.replace("<script>", "").replace("</script>", "");
}
'''

ex13.method(
    "write", "j8-l1.3-write-escape", "Output encoding", ["o1"], ["J8.03"], ["IMPL"],
    "Cross-site scripting happens when untrusted text reaches a page as code. Write `htmlEscape(text)` converting `&` to `&amp;`, `<` to `&lt;`, `>` to `&gt;`, `\"` to `&quot;` and `'` to `&#x27;`, as in the OWASP table. Everything else is unchanged. (Each character must be converted once: `&` is handled first or in the same pass, never after the others.)",
    [("htmlEscape", [("text", "String")], "String")], {"htmlEscape": f_escape},
    [("htmlEscape", ("<script>alert(1)</script>",), "a script tag"), ("htmlEscape", ("Tom & Jerry",), "an ampersand"), ("htmlEscape", ("plain text",), "nothing to change")],
    [("htmlEscape", ('say "hi"',), "double quotes"), ("htmlEscape", ("it's",), "an apostrophe"), ("htmlEscape", ("&lt;",), "an already escaped entity is escaped again"),
     ("htmlEscape", ("",), "empty"), ("htmlEscape", ('<a href="x" onclick=\'y\'>',), "attribute injection"), ("htmlEscape", ("a < b && c > d",), "operators")],
    starter='''
String htmlEscape(String text) {
    return text;
}
''', solution=ESC_SOL,
    wrongs={"double-escapes-ampersand": ESC_REPLACE_CHAIN, "forgets-quotes": ESC_NO_QUOTES, "blacklists-script-tags": ESC_SCRIPT_ONLY},
    hints=["Walk the characters once and convert each by the table.", "Why is removing `<script>` not enough?"],
    misconceptions=("MC180",), difficulty=2,
)


def f_safe(base, user):
    if user.startswith("/"):
        return "rejected"
    joined = posixpath.normpath(posixpath.join(base, user))
    return joined if joined == base or joined.startswith(base + "/") else "rejected"


SAFE_SOL = '''
String safePath(String base, String userPath) {
    if (userPath.startsWith("/")) {
        return "rejected";
    }
    java.nio.file.Path root = java.nio.file.Path.of(base).normalize();
    java.nio.file.Path resolved = root.resolve(userPath).normalize();
    return resolved.startsWith(root) ? resolved.toString() : "rejected";
}
'''
SAFE_NO_NORMALIZE = SAFE_SOL.replace("root.resolve(userPath).normalize()", "root.resolve(userPath)")
SAFE_DOTS = '''
String safePath(String base, String userPath) {
    return userPath.contains("../") ? "rejected" : java.nio.file.Path.of(base).resolve(userPath).normalize().toString();
}
'''
SAFE_ABS = SAFE_SOL.replace('    if (userPath.startsWith("/")) {\n        return "rejected";\n    }\n', "")

ex13.method(
    "write", "j8-l1.3-write-path", "Staying inside a directory", ["o2"], ["J8.03"], ["IMPL", "DEBUG"],
    "A download endpoint serves files from a base directory such as `/srv/files`. Write `safePath(base, userPath)` returning the normalised full path, or `rejected` if the user's path is absolute or would leave the base directory (for example by using `..`). A path that stays inside is returned with `.` and `..` segments resolved.",
    [("safePath", [("base", "String"), ("userPath", "String")], "String")], {"safePath": f_safe},
    [("safePath", ("/srv/files", "report.txt"), "a plain file"), ("safePath", ("/srv/files", "../etc/passwd"), "an escape"), ("safePath", ("/srv/files", "a/b.txt"), "a subdirectory")],
    [("safePath", ("/srv/files", "a/../b.txt"), "dots that stay inside"), ("safePath", ("/srv/files", "a/../../x"), "dots that escape"), ("safePath", ("/srv/files", "/etc/passwd"), "an absolute path"),
     ("safePath", ("/srv/files", ".."), "the parent itself"), ("safePath", ("/srv/files", ""), "the base itself"), ("safePath", ("/srv/files", "a/./b"), "single dots"),
     ("safePath", ("/srv/files", "..hidden/x"), "a name that starts with dots"), ("safePath", ("/srv/files", "a/b/../../.."), "escape after going in"),
     ("safePath", ("/srv/files", "/srv/files/a.txt"), "an absolute path that points inside is still refused")],
    starter='''
String safePath(String base, String userPath) {
    return base + "/" + userPath;
}
''', solution=SAFE_SOL,
    wrongs={"no-normalising": SAFE_NO_NORMALIZE, "blacklists-dot-dot-slash": SAFE_DOTS, "allows-absolute": SAFE_ABS},
    hints=["Resolve the path first, then check where it ended up.", "What does `resolve` do with an absolute argument?"],
    misconceptions=("MC180",), difficulty=3,
)

ex13.explain(
    "j8-l1.3-explain-input", "Validate or encode", ["o1"], ["J8.03"],
    "A team validates the 'display name' field with a regex that allows only letters, digits and spaces, and argues that this makes it safe to insert the name into HTML anywhere. Explain why that reasoning is fragile, and what each of output encoding and parameterised queries adds. Use the OWASP wording about what output encoding does.",
    "Validation limits what comes in, but safety depends on where the value goes out: a value is data or code depending on the context (HTML text, an attribute, a URL, SQL). Output encoding converts untrusted input into a safe form so it is displayed as data and not executed as code, and it protects every place the value is used, even if validation changes or is bypassed. Parameterised queries do the same job for SQL by keeping data separate from the statement. Validation is still useful, as a first filter and for business rules, but it is not a substitute.",
    levels={
        2: ("The answer separates validation from encoding, ties safety to the output context and names both encoding and parameterised queries.", [
            "Validation only restricts input today; the safety of the value depends on the context where it is used (HTML, attribute, URL, SQL), and the rules may change later. Output encoding turns untrusted input into a form shown as data instead of run as code, wherever it is used. Parameterised queries keep SQL data out of the statement. Validation helps, but encoding and parameters are the controls.",
            "A regex today does not protect a new page tomorrow that puts the name in a script or attribute. Encode on output for the context, and use bound parameters for SQL, so untrusted data is never interpreted as code. Keep validation as an extra layer."]),
        1: ("The answer names encoding or parameters without explaining the context argument.", [
            "You should encode output as well.",
            "Use parameterised queries for SQL."]),
        0: ("The answer accepts validation as sufficient.", [
            "The regex is enough because it blocks special characters.",
            "If the input is validated it is safe everywhere."]),
    },
)

l8_l1_3 = Lesson("j8-l1.3", "Untrusted input: encoding and paths", ["J8.03"], [
    ("o1", "Encode untrusted text for HTML output"),
    ("o2", "Resolve a user-supplied path and keep it inside a base directory"),
], ["j8-l1.1", "j6-l3.1"], 40, ["I97", "I95"], """## Before you start

You should have met SQL injection and bound parameters (Stage 6) and know what a path is.

## Explanation

Everything a client sends is **untrusted input**: form fields, query strings, headers, cookies, file names. The attack comes when untrusted text reaches an interpreter as code: SQL (Stage 6), HTML in a browser, a file system path, an operating system command.

For HTML, the defence is **output encoding**. OWASP describes its purpose as converting untrusted input into a safe form where it is displayed as data and does not execute as code in the browser. The table for HTML text converts `&` to `&amp;`, `<` to `&lt;`, `>` to `&gt;`, `"` to `&quot;` and `'` to `&#x27;`. The right encoding depends on the context (HTML text, an attribute, JavaScript, CSS, a URL), which is why a framework or library encoder is normally used instead of hand-written code.

For files, a user-supplied name such as `../../etc/passwd` can climb out of the intended directory (**path traversal**). The fix is not a search for `../` in the string. Resolve the path to its final normalised form, then check that the result still lies under the base directory.

These are not new ideas: it is the same rule as bound parameters. Keep data away from the place where code is interpreted.

## Worked examples

### Example 1: an encoded script tag.

`<script>alert(1)</script>` becomes `&lt;script&gt;alert(1)&lt;/script&gt;`, which a browser shows as text.

### Example 2: normalise, then check.

`/srv/files` + `a/../../x` normalises to `/srv/x`, which is outside `/srv/files`, so it is rejected.

## Where this is used

- Any page that shows user content, any upload or download feature. The React front end of this platform encodes text by default, which is one reason injecting HTML takes deliberate effort there.

## Common mistakes

:::mistake{id=MC180}
**Believing input validation makes a value safe everywhere.** Safety depends on the context where the value is used. Encode or parameterise at the point of use.
:::

## Practice

::exercise{id=j8-l1.3-write-escape}

::exercise{id=j8-l1.3-write-path}

::exercise{id=j8-l1.3-explain-input}

## Further reading

- **OWASP Cross Site Scripting Prevention Cheat Sheet** `[I97]`.
- **OWASP Top 10:2025** `[I95]`, A05 Injection.

## How you'll be assessed

- The **write** exercises check encoding and path containment (*implementation*).
- The **explain** exercise checks that you can reason about context (*explanation*).

The claim about this platform's front end is general knowledge about React, not something this course verified.
""")

# ====================================================================== j8-l1.4
SECRET_KEYS = {"password", "token", "secret", "apikey", "authorization"}


def f_redact(line):
    out = []
    for part in line.split(" "):
        if "=" in part:
            k, v = part.split("=", 1)
            out.append(f"{k}=***" if k.lower() in SECRET_KEYS else part)
        else:
            out.append(part)
    return " ".join(out)


REDACT_SOL = '''
String redact(String line) {
    Set<String> secret = Set.of("password", "token", "secret", "apikey", "authorization");
    String[] parts = line.split(" ", -1);
    for (int i = 0; i < parts.length; i++) {
        int equals = parts[i].indexOf('=');
        if (equals > 0 && secret.contains(parts[i].substring(0, equals).toLowerCase())) {
            parts[i] = parts[i].substring(0, equals + 1) + "***";
        }
    }
    return String.join(" ", parts);
}
'''
REDACT_CASE = REDACT_SOL.replace(".toLowerCase()", "")
REDACT_FIRST = REDACT_SOL.replace("            parts[i] = parts[i].substring(0, equals + 1) + \"***\";\n", "            parts[i] = parts[i].substring(0, equals + 1) + \"***\";\n            break;\n")
REDACT_LINE = REDACT_SOL.replace("    String[] parts = line.split(\" \", -1);", "    if (line.toLowerCase().contains(\"password=\")) {\n        return \"***\";\n    }\n    String[] parts = line.split(\" \", -1);")
REDACT_VALUE_ONLY_KEEP = REDACT_SOL.replace('"apikey", "authorization"', '"apikey"')

ex14.method(
    "write", "j8-l1.4-write-redact", "Logging without leaking", ["o1"], ["J8.04"], ["IMPL"],
    "A log line is a list of space-separated words. A word of the form `key=value` whose key is `password`, `token`, `secret`, `apikey` or `authorization` (in any letter case) must have its value replaced by `***`. Every other word is unchanged, and the spacing of the line is preserved. Write `redact(line)`.",
    [("redact", [("line", "String")], "String")], {"redact": f_redact},
    [("redact", ("login user=ada password=hunter2 ok",), "a password"), ("redact", ("GET /accounts/7 status=200",), "nothing secret"), ("redact", ("token=abc123",), "just a token")],
    [("redact", ("PASSWORD=x Token=y",), "any letter case"), ("redact", ("password=a password=b",), "every occurrence"), ("redact", ("note=password reset sent",), "the word password in a value"),
     ("redact", ("apikey=k1 authorization=Bearer",), "two keys"), ("redact", ("",), "empty line"), ("redact", ("user=ada  password=x",), "double space preserved"),
     ("redact", ("passwordhint=blue",), "a different key")],
    starter='''
String redact(String line) {
    return line;
}
''', solution=REDACT_SOL,
    wrongs={"case-sensitive": REDACT_CASE, "first-only": REDACT_FIRST, "drops-the-line": REDACT_LINE, "forgets-authorization": REDACT_VALUE_ONLY_KEEP},
    hints=["Look at one word at a time and split it at the first `=`.", "Should `Password` and `password` be treated the same?"],
    misconceptions=("MC181",), difficulty=3,
)

ex14.explain(
    "j8-l1.4-explain-secrets", "Where a secret lives", ["o2"], ["J8.04"],
    "A developer adds an API key as a string constant in the source file so the code works 'out of the box', and logs the full request, including the `Authorization` header, to help debugging. The repository is private. Explain what is wrong, and where the key and the log line should be handled instead. This platform reads its AI mentor key from an environment variable; say what that achieves.",
    "A private repository is still copied to laptops, backups, forks and CI logs, and the key stays in the history after it is deleted from the file; anyone who can read the code can use the key. Secrets should be kept out of the source and provided at run time (an environment variable, or a secrets manager), and rotated if exposed. Logs are widely readable and kept for a long time, so credentials must be excluded or redacted before they are written. Reading the key from the environment, as this platform does for the mentor, keeps it out of the repository and lets each environment use its own value.",
    levels={
        2: ("The answer explains why source control is the wrong place, proposes run-time configuration and rotation, and says logs must exclude credentials.", [
            "The key would live in version control history, backups and every clone, so private does not mean secret. Keep it out of the code: supply it at run time through an environment variable or a secrets manager, and rotate it if it leaks. Logs are widely readable, so the Authorization header must be redacted before logging. This platform's environment variable means the key is never in the repository and each environment can have its own.",
            "A constant in source is found by anyone with the code and survives in git history. Use configuration from the environment or a vault, rotate after exposure, and do not log credentials such as the Authorization header. The environment variable approach keeps the secret outside the repository."]),
        1: ("The answer says not to hard-code the key without the reasons or the log point.", [
            "Do not hard-code the key, use an environment variable.",
            "Do not log the header."]),
        0: ("The answer accepts the practice.", [
            "It is fine because the repository is private.",
            "Logging everything is the best way to debug."]),
    },
)

l8_l1_4 = Lesson("j8-l1.4", "Secrets and logging", ["J8.04"], [
    ("o1", "Redact secrets from log lines"),
    ("o2", "Say where secrets should and should not live, and what must never be logged"),
], ["j8-l1.1"], 35, ["I98", "I99"], """## Before you start

You should have used logging in Stage 4 and know what an environment variable is.

## Explanation

A **secret** is any value that grants access: a password, an API key, a token, a database connection string, an encryption key. OWASP observes that many organisations have secrets hardcoded in source code or scattered through configuration files, and recommends centralising the storage, provisioning, auditing and rotation of secrets so they do not leak.

Practical rules that follow:

- Keep secrets out of the source and out of version control. Supply them at run time, for example through an environment variable or a secrets manager, so each environment has its own.
- Assume a secret that was ever committed is exposed, and **rotate** it.
- Never write secrets to logs. The OWASP logging guidance lists data to exclude: authentication passwords, database connection strings, encryption keys and other primary secrets, and payment card data. Redact before logging.

Logs are read by many people and systems and are kept for a long time, so a secret in a log is a secret widely shared.

## Worked examples

### Example 1: this platform's mentor key.

When the backend starts without a key, its real log says `No ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN set: the AI mentor is unavailable`. The key comes from the environment, not from the repository.

### Example 2: a redacted line.

`login user=ada password=hunter2 ok` is logged as `login user=ada password=*** ok`.

## Where this is used

- Every deployment and every logging statement. Credentials in logs and repositories are a common cause of real incidents.

## Common mistakes

:::mistake{id=MC181}
**Thinking a secret is safe because the repository or the log is private.** Copies, backups, history and wide access make "private" a weak control.
:::

## Practice

::exercise{id=j8-l1.4-write-redact}

::exercise{id=j8-l1.4-explain-secrets}

## Further reading

- **OWASP Secrets Management Cheat Sheet** `[I99]`.
- **OWASP Logging Cheat Sheet** `[I98]`.

## How you'll be assessed

- The **write** exercise checks redaction (*implementation*).
- The **explain** exercise checks where secrets belong (*explanation*).
""")
print("module 8.1 authored")
