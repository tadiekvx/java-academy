"""Stage 11 authoring: module 11.3 (Cloud engineering). Vendor-neutral models; AWS documentation is the single provider reference. No cloud account was used."""
import ipaddress
import re
import l11common
from l11common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex31 = Exercises("j11-l3.1")
ex32 = Exercises("j11-l3.2")

REGISTER = {
    "j11-l3.1": ("Cloud networking and identity", ["J11.07"]),
    "j11-l3.2": ("Infrastructure as code and cost", ["J11.08"]),
}
MISCS = {
    "MC211": (["J11.07"], "I132", "Opening a port to 0.0.0.0/0 is fine while testing because nobody knows the address"),
    "MC212": (["J11.07"], "I131", "A service account with broad permissions is simpler and just as safe, because only our code uses it"),
    "MC213": (["J11.08"], "I131", "Cloud resources cost nothing until traffic arrives, so leaving them running is free"),
}
register(REGISTER, MISCS)

# ====================================================================== j11-l3.1
def f_sg(rules, proto, port, ip):
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    for r in rules:
        p, ports, cidr = r.split(":")
        if p != proto:
            continue
        lo, _, hi = ports.partition("-")
        lo, hi = int(lo), int(hi or lo)
        if lo <= port <= hi and addr in ipaddress.ip_network(cidr, strict=False):
            return True
    return False


SG_SOL = '''
boolean sgAllows(List<String> rules, String protocol, int port, String ip) {
    long address = toInt(ip);
    if (address < 0) {
        return false;
    }
    for (String rule : rules) {
        String[] p = rule.split(":");
        if (!p[0].equals(protocol)) {
            continue;
        }
        String[] range = p[1].split("-");
        int low = Integer.parseInt(range[0]);
        int high = Integer.parseInt(range[range.length - 1]);
        String[] cidr = p[2].split("/");
        int bits = Integer.parseInt(cidr[1]);
        long mask = bits == 0 ? 0 : (0xFFFFFFFFL << (32 - bits)) & 0xFFFFFFFFL;
        if (port >= low && port <= high && (address & mask) == (toInt(cidr[0]) & mask)) {
            return true;
        }
    }
    return false;
}

long toInt(String ip) {
    String[] parts = ip.split("\\\\.");
    if (parts.length != 4) {
        return -1;
    }
    long value = 0;
    for (String part : parts) {
        int octet;
        try {
            octet = Integer.parseInt(part);
        } catch (NumberFormatException e) {
            return -1;
        }
        if (octet < 0 || octet > 255) {
            return -1;
        }
        value = value * 256 + octet;
    }
    return value;
}
'''
SG_NO_PROTO = SG_SOL.replace("        if (!p[0].equals(protocol)) {\n            continue;\n        }\n", "")
SG_EXCLUSIVE_HIGH = SG_SOL.replace("port <= high", "port < high")
SG_NO_MASK = SG_SOL.replace("(address & mask) == (toInt(cidr[0]) & mask)", "address == toInt(cidr[0])")
SG_ZERO_MASK = SG_SOL.replace("long mask = bits == 0 ? 0 : (0xFFFFFFFFL << (32 - bits)) & 0xFFFFFFFFL;", "long mask = (long) (-1 << (32 - bits)) & 0xFFFFFFFFL;")
RULES = ["tcp:443:0.0.0.0/0", "tcp:5432:10.0.0.0/16", "tcp:8000-8100:192.168.1.0/24"]

ex31.method(
    "write", "j11-l3.1-write-sg", "Does the firewall let it in", ["o1"], ["J11.07"], ["IMPL"],
    "A security group lets in only the traffic that one of its allow rules permits (everything else is denied). A rule is `protocol:port:cidr` or `protocol:low-high:cidr` (IPv4). Write `sgAllows(rules, protocol, port, ip)`: true if some rule has the same protocol, a port range containing `port` (both ends included) and a CIDR block containing `ip`. An `ip` that is not a valid IPv4 address is refused.",
    [("sgAllows", [("rules", "List<String>"), ("protocol", "String"), ("port", "int"), ("ip", "String")], "boolean")], {"sgAllows": f_sg},
    [("sgAllows", (RULES, "tcp", 443, "203.0.113.9"), "https from anywhere"), ("sgAllows", (RULES, "tcp", 5432, "10.0.7.1"), "the database from inside"), ("sgAllows", (RULES, "tcp", 5432, "203.0.113.9"), "the database from outside")],
    [("sgAllows", (RULES, "udp", 443, "203.0.113.9"), "another protocol"), ("sgAllows", (RULES, "tcp", 8000, "192.168.1.200"), "the first port of a range"), ("sgAllows", (RULES, "tcp", 8100, "192.168.1.1"), "the last port of a range"),
     ("sgAllows", (RULES, "tcp", 8101, "192.168.1.1"), "one past the range"), ("sgAllows", (RULES, "tcp", 8050, "192.168.2.1"), "the wrong block"), ("sgAllows", (RULES, "tcp", 443, "not-an-ip"), "an invalid address"),
     ("sgAllows", ([], "tcp", 443, "1.2.3.4"), "no rules"), ("sgAllows", (["tcp:22:203.0.113.5/32"], "tcp", 22, "203.0.113.5"), "a single address"), ("sgAllows", (["tcp:22:203.0.113.5/32"], "tcp", 22, "203.0.113.6"), "the next address")],
    starter='''
boolean sgAllows(List<String> rules, String protocol, int port, String ip) {
    return false;
}
''', solution=SG_SOL,
    wrongs={"ignores-protocol": SG_NO_PROTO, "range-excludes-the-end": SG_EXCLUSIVE_HIGH, "exact-address-only": SG_NO_MASK, "slash-zero-breaks": SG_ZERO_MASK},
    hints=["Turn each IPv4 address into a number and compare under the CIDR mask.", "What is the mask for /0?"],
    misconceptions=("MC211",), difficulty=4,
)


def glob(pattern, text):
    return re.fullmatch(".*".join(re.escape(p) for p in pattern.split("*")), text, re.S) is not None


def f_iam(statements, action, resource):
    allowed = False
    for s in statements:
        effect, act, res = s.split("|")
        if glob(act, action) and glob(res, resource):
            if effect == "Deny":
                return False
            allowed = True
    return allowed


IAM_SOL = '''
boolean iamAllows(List<String> statements, String action, String resource) {
    boolean allowed = false;
    for (String statement : statements) {
        String[] p = statement.split("\\\\|");
        if (matches(p[1], action) && matches(p[2], resource)) {
            if (p[0].equals("Deny")) {
                return false;
            }
            allowed = true;
        }
    }
    return allowed;
}

boolean matches(String pattern, String text) {
    StringBuilder regex = new StringBuilder();
    for (String part : pattern.split("\\\\*", -1)) {
        if (regex.length() > 0) {
            regex.append(".*");
        }
        regex.append(java.util.regex.Pattern.quote(part));
    }
    if (pattern.startsWith("*") && regex.length() == 0) {
        return true;
    }
    return java.util.regex.Pattern.compile(regex.toString(), java.util.regex.Pattern.DOTALL).matcher(text).matches();
}
'''
IAM_ALLOW_WINS = IAM_SOL.replace('            if (p[0].equals("Deny")) {\n                return false;\n            }\n            allowed = true;', '            allowed = true;')
IAM_LAST_WINS = IAM_SOL.replace('            if (p[0].equals("Deny")) {\n                return false;\n            }\n            allowed = true;', '            allowed = !p[0].equals("Deny");')
IAM_DEFAULT_ALLOW = IAM_SOL.replace("    boolean allowed = false;", "    boolean allowed = statements.isEmpty();")
IAM_PREFIX = IAM_SOL.replace("matcher(text).matches()", "matcher(text).lookingAt()")

ST = ["Allow|s3:Get*|reports/*", "Allow|s3:Put*|reports/*", "Deny|s3:*|reports/secret/*"]
ex31.method(
    "write", "j11-l3.1-write-iam", "May this identity do that", ["o2"], ["J11.07"], ["IMPL"],
    "Identity policies list statements `Effect|action-pattern|resource-pattern` (Effect is `Allow` or `Deny`). In a pattern `*` matches any run of characters, including none; everything else must match exactly and in full. A request is allowed only if some `Allow` statement matches both the action and the resource, and **no** matching `Deny` exists: an explicit deny overrides any allow, and with no matching allow the answer is no. Write `iamAllows(statements, action, resource)`.",
    [("iamAllows", [("statements", "List<String>"), ("action", "String"), ("resource", "String")], "boolean")], {"iamAllows": f_iam},
    [("iamAllows", (ST, "s3:GetObject", "reports/2026.csv"), "an allowed read"), ("iamAllows", (ST, "s3:GetObject", "reports/secret/key.txt"), "an explicit deny wins"), ("iamAllows", (ST, "s3:DeleteObject", "reports/2026.csv"), "nothing allows it")],
    [("iamAllows", (ST, "s3:PutObject", "reports/new.csv"), "an allowed write"), ("iamAllows", (ST, "s3:GetObject", "other/x"), "the wrong resource"), ("iamAllows", ([], "s3:GetObject", "reports/x"), "no statements means no"),
     ("iamAllows", (["Allow|*|*"], "ec2:Start", "anything"), "allow everything"), ("iamAllows", (["Allow|*|*", "Deny|ec2:*|*"], "ec2:Start", "i-1"), "a deny narrows an allow-all"), ("iamAllows", (["Deny|s3:*|reports/secret/*", "Allow|s3:*|reports/*"], "s3:GetObject", "reports/secret/a"), "order does not matter"),
     ("iamAllows", (["Allow|s3:Get*|reports"], "s3:GetObject", "reports/x"), "a pattern must match in full"), ("iamAllows", (["Allow|s3:GetObject|a.b"], "s3:GetObject", "axb"), "a dot is not a wildcard")],
    starter='''
boolean iamAllows(List<String> statements, String action, String resource) {
    return false;
}
''', solution=IAM_SOL,
    wrongs={"allow-beats-deny": IAM_ALLOW_WINS, "last-statement-wins": IAM_LAST_WINS, "empty-policy-allows": IAM_DEFAULT_ALLOW, "prefix-matches": IAM_PREFIX},
    hints=["Keep going through all the statements: a later deny can still cancel an earlier allow.", "Quote the literal parts of a pattern before building a regular expression."],
    misconceptions=("MC212",), difficulty=4,
)

ex31.explain(
    "j11-l3.1-explain-least-privilege", "Open ports and broad roles", ["o2"], ["J11.07"],
    "A new Brightbank environment is built with: a database security group that allows `tcp:5432` from `0.0.0.0/0` 'so we can connect from home'; the application running with an identity that is allowed `*` on `*`; and one shared set of credentials for the whole team. Say what is wrong with each, name the OWASP Top 10:2025 category that fits the broad role, and describe how you would fix each. Use the guidance 'least privilege' and 'deny by default' from Stage 8.",
    "Allowing 5432 from 0.0.0.0/0 lets anyone on the internet try to reach the database; the guidance is to restrict access to the sources that need it and not to open ranges wider than needed, so allow it only from the application's security group or a known address or VPN. An identity allowed everything on everything gives any bug or stolen credential full control (A01 Broken Access Control); apply least privilege, granting only the specific actions on the specific resources the application needs, and rely on an explicit deny for the dangerous ones. Shared credentials cannot be traced to a person or revoked for one; give each person and each service its own identity, with short-lived credentials where possible, and keep secrets in a secret store (Stage 8).",
    levels={
        2: ("The answer identifies all three problems, names A01, and gives specific fixes in line with least privilege and deny by default.", [
            "5432 open to the whole internet should be restricted to the application's security group or a VPN address. An identity with * on * breaks least privilege; a bug or stolen key owns everything, which is A01 Broken Access Control. Grant only the needed actions on the needed resources, deny the rest by default. Shared credentials cannot be traced or revoked individually, so give each person and service their own identity and keep secrets in a secret store.",
            "Open database port: allow only the app and a known address. Allow-all role: least privilege, A01. Shared credentials: separate identities, revocable, short-lived. All of it follows deny by default."]),
        1: ("The answer spots some problems without the fixes or the category.", [
            "The database should not be open to everyone.",
            "The role has too many permissions."]),
        0: ("The answer accepts the set-up as convenient.", [
            "It is only a test environment so it does not matter.",
            "Nobody knows the address so the open port is safe."]),
    },
)

l11_l3_1 = Lesson("j11-l3.1", "Cloud networking and identity", ["J11.07"], [
    ("o1", "Evaluate security-group rules and identity-policy statements by hand"),
    ("o2", "Review an environment for open ports, broad roles and shared credentials"),
], ["j11-l1.3", "j8-l2.3"], 45, ["I131", "I132", "I104"], """## Before you start

You should know least privilege and deny by default (lesson 8.2.3) and what a container stack looks like (module 11.1).

## Explanation

In the cloud you do not buy servers, you rent building blocks: virtual machines or containers, managed databases, networks and storage, created through an API. Two kinds of settings decide who can reach and use them, and they are where most cloud security incidents begin.

**Network rules.** In AWS, a security group acts as a virtual firewall for an instance: the only traffic that reaches the instance is the traffic allowed by the security group's rules. A rule specifies a source or destination, a port range and a protocol. If a rule for SSH is not there, you cannot connect with SSH. The AWS guidance for rules is to authorise specific address ranges and not to open large port ranges: `0.0.0.0/0` lets anyone, from any address, use that protocol and port. A database should be reachable only from the application tier.

**Identity.** Every request is made by an identity (a person, or a service's role) and evaluated against policies. In AWS's policy evaluation, an explicit deny in a policy overrides an allow. Combined with the Stage 8 rules of least privilege and deny by default, the design is: grant each identity only the specific actions on the specific resources it needs; everything else is refused.

Why AWS? The course is vendor-neutral, but one concrete provider is needed for exact wording. The same ideas exist, under other names, in every cloud. No cloud account was used to make these lessons; the exercises model the evaluation rules, and the lessons quote the provider's documentation for them.

## Worked examples

### Example 1: a rule set.

`tcp:443:0.0.0.0/0, tcp:5432:10.0.0.0/16`: HTTPS from anywhere is allowed; the database port only from inside 10.0.0.0/16.

### Example 2: a policy with a deny.

`Allow s3:Get* on reports/*` plus `Deny s3:* on reports/secret/*`: reading `reports/2026.csv` works, reading `reports/secret/key.txt` does not, though the allow matches it.

## Where this is used

- Every cloud environment review. A frequent audit finding is a database or admin port open to the world, or a role allowed everything.

## Common mistakes

:::mistake{id=MC211}
**Opening to everyone "temporarily".** Scanners find open ports within minutes, and temporary rules are forgotten. Restrict the source from the start.
:::

## Practice

::exercise{id=j11-l3.1-write-sg}

::exercise{id=j11-l3.1-write-iam}

::exercise{id=j11-l3.1-explain-least-privilege}

## Further reading

- **AWS, security groups** `[I132]`.
- **AWS, policy evaluation logic** `[I131]`.
- **OWASP Authorization Cheat Sheet** `[I104]`.

## How you'll be assessed

- The **write** exercises check rule evaluation (*implementation*).
- The **explain** exercise checks a review of an environment (*explanation*).

The exercises are simplified models: real policies have conditions, more kinds of policy and more rules of evaluation than the single explicit-deny rule used here. The remark that scanners find open ports within minutes is general experience, not a recorded source.
""")

# ====================================================================== j11-l3.2
def f_plan(desired, current):
    d = dict(x.split("=", 1) for x in desired)
    c = dict(x.split("=", 1) for x in current)
    out = []
    for name in sorted(set(d) | set(c)):
        if name in d and name not in c:
            out.append("+ " + name)
        elif name in c and name not in d:
            out.append("- " + name)
        elif d[name] != c[name]:
            out.append("~ " + name)
    return out


PLAN_SOL = '''
List<String> plan(List<String> desired, List<String> current) {
    Map<String, String> want = new TreeMap<>();
    Map<String, String> have = new TreeMap<>();
    for (String item : desired) {
        want.put(item.substring(0, item.indexOf('=')), item.substring(item.indexOf('=') + 1));
    }
    for (String item : current) {
        have.put(item.substring(0, item.indexOf('=')), item.substring(item.indexOf('=') + 1));
    }
    Set<String> names = new TreeSet<>(want.keySet());
    names.addAll(have.keySet());
    List<String> changes = new ArrayList<>();
    for (String name : names) {
        if (want.containsKey(name) && !have.containsKey(name)) {
            changes.add("+ " + name);
        } else if (have.containsKey(name) && !want.containsKey(name)) {
            changes.add("- " + name);
        } else if (!want.get(name).equals(have.get(name))) {
            changes.add("~ " + name);
        }
    }
    return changes;
}
'''
PLAN_NO_CHANGES = PLAN_SOL.replace('        } else if (!want.get(name).equals(have.get(name))) {\n            changes.add("~ " + name);\n        }', '        }')
PLAN_NO_DESTROY = PLAN_SOL.replace('        } else if (have.containsKey(name) && !want.containsKey(name)) {\n            changes.add("- " + name);', '        } else if (have.containsKey(name) && !want.containsKey(name)) {')
PLAN_UNSORTED = PLAN_SOL.replace("Set<String> names = new TreeSet<>(want.keySet());", "Set<String> names = new LinkedHashSet<>(want.keySet());").replace("Map<String, String> want = new TreeMap<>();", "Map<String, String> want = new LinkedHashMap<>();")
PLAN_REPLACE_ALL = PLAN_SOL.replace("!want.get(name).equals(have.get(name))", "true")
ex32.method(
    "write", "j11-l3.2-write-plan", "What would change", ["o1"], ["J11.08"], ["IMPL"],
    "Infrastructure as code describes the **desired** state of resources in files; a tool compares it with the **current** state and prints a plan. Resources are `name=configuration`. Write `plan(desired, current)` returning the changes sorted by name: `+ name` to create (in desired only), `- name` to destroy (in current only), `~ name` to change (in both, configuration differs). Resources that are the same produce nothing.",
    [("plan", [("desired", "List<String>"), ("current", "List<String>")], "List<String>")], {"plan": f_plan},
    [("plan", (["web=2cpu", "db=large"], ["web=2cpu", "db=small"]), "one change"), ("plan", (["web=2cpu"], []), "a new environment"), ("plan", ([], ["web=2cpu"]), "everything removed")],
    [("plan", (["a=1", "b=2"], ["a=1", "b=2"]), "nothing to do"), ("plan", (["c=1", "a=1"], ["b=1", "a=2"]), "create, destroy and change, sorted"), ("plan", ([], []), "empty"),
     ("plan", (["x=a=b"], ["x=a=c"]), "an equals sign inside the configuration"), ("plan", (["z=1", "y=1", "x=1"], []), "creates are sorted"), ("plan", (["a=1"], ["a=1", "b=1", "c=1"]), "two destroyed")],
    starter='''
List<String> plan(List<String> desired, List<String> current) {
    return List.of();
}
''', solution=PLAN_SOL,
    wrongs={"ignores-changes": PLAN_NO_CHANGES, "never-destroys": PLAN_NO_DESTROY, "unsorted": PLAN_UNSORTED, "changes-everything": PLAN_REPLACE_ALL},
    hints=["Split each item at the first equals sign.", "Walk the names of both sets in sorted order."],
    misconceptions=("MC213",), difficulty=3,
)


def f_cost(items, hours):
    return sum(int(i.split(":")[1]) * int(i.split(":")[2]) * hours for i in items)


COST_SOL = '''
long estimateCents(List<String> items, int hoursPerMonth) {
    long total = 0;
    for (String item : items) {
        String[] p = item.split(":");
        total += Long.parseLong(p[1]) * Long.parseLong(p[2]) * hoursPerMonth;
    }
    return total;
}
'''
COST_INT = COST_SOL.replace("long total = 0;", "int total = 0;")
COST_IGNORE_COUNT = COST_SOL.replace(" * Long.parseLong(p[2])", "")
COST_ONE_HOUR = COST_SOL.replace(" * hoursPerMonth", "")
ex32.method(
    "write", "j11-l3.2-write-cost", "A monthly estimate", ["o1"], ["J11.08"], ["IMPL"],
    "Each resource is `name:centsPerHour:instances`. Write `estimateCents(items, hoursPerMonth)`: the total cost in cents for a month, the sum of `centsPerHour * instances * hoursPerMonth` over the items, as a `long`. (The prices in the checks are invented for practice and are not any provider's prices.)",
    [("estimateCents", [("items", "List<String>"), ("hoursPerMonth", "int")], "long")], {"estimateCents": f_cost},
    [("estimateCents", (["app:12:2", "db:40:1"], 730), "an app and a database"), ("estimateCents", ([], 730), "no resources"), ("estimateCents", (["app:12:2"], 0), "switched off all month")],
    [("estimateCents", (["big:2000000:300"], 730), "the total needs a long"), ("estimateCents", (["a:1:1", "b:2:3", "c:3:2"], 100), "three resources"), ("estimateCents", (["spot:5:10"], 200), "part of the month"),
     ("estimateCents", (["x:0:5"], 730), "free resources"), ("estimateCents", (["app:12:4", "app2:12:4"], 730), "two similar services")],
    starter='''
long estimateCents(List<String> items, int hoursPerMonth) {
    return 0;
}
''', solution=COST_SOL,
    wrongs={"int-overflow": COST_INT, "forgets-instances": COST_IGNORE_COUNT, "forgets-hours": COST_ONE_HOUR},
    hints=["Multiply as long values.", "Hours are per month, not per day."],
    misconceptions=("MC213",), difficulty=2,
)

ex32.explain(
    "j11-l3.2-explain-iac", "Why describe it in files", ["o2"], ["J11.08"],
    "A teammate builds the staging environment by clicking in a cloud console and keeps a wiki page of the steps. Explain the problems with that approach and what changes with infrastructure as code (a reviewed file, a plan, repeatable apply), including what a plan lets a reviewer see before anything changes. Then explain three cost habits for a small team: what to do about resources left running, always-on versus on-demand, and who should be able to see the bill.",
    "Console clicks cannot be reviewed, repeated, compared or rolled back; the wiki goes out of date and environments drift apart. Infrastructure as code describes the environment in files that are version-controlled and reviewed like code; a tool compares the desired state with the real one and prints a plan (what will be created, changed or destroyed), so a reviewer sees the effect, such as an accidental destroy of a database, before anything happens, and the same files recreate the environment on demand. Cost habits: switch off or delete what is not in use (a forgotten environment keeps costing money every hour), prefer on-demand or scaled-down capacity for non-production, tag resources and set budgets and alerts, and make the cost visible to the team that causes it.",
    levels={
        2: ("The answer gives the problems of manual set-up, the benefits including the plan, and three cost habits.", [
            "Clicking cannot be reviewed or repeated and the wiki drifts, so staging and production differ. As code, the environment is in version control and reviewed, and a plan shows creates, changes and destroys before applying, for example catching a database being destroyed; the same files rebuild the environment. Cost: delete or stop idle environments, scale non-production down or on demand, and set budgets and alerts that the team can see.",
            "Manual steps are not reproducible or reviewable. With IaC you review the diff and the plan and can recreate anything. For cost: do not leave test stacks running, size non-prod small, and give the team the billing view with alerts."]),
        1: ("The answer lists benefits without the plan or without the cost habits.", [
            "Infrastructure as code is repeatable.",
            "Turn things off when not used."]),
        0: ("The answer prefers manual set-up or ignores cost.", [
            "The console is quicker, the wiki is good enough.",
            "Cloud costs only matter for big companies."]),
    },
)

l11_l3_2 = Lesson("j11-l3.2", "Infrastructure as code and cost", ["J11.08"], [
    ("o1", "Compute a plan from desired and current state, and a monthly cost estimate"),
    ("o2", "Argue for infrastructure as code and describe cost habits for a small team"),
], ["j11-l3.1"], 35, ["I131", "I132"], """## Before you start

You should have read about security groups and policies (lesson 11.3.1).

## Explanation

Cloud resources can be created by clicking in a console, but that cannot be reviewed, repeated or undone, and the notes describing it go stale. **Infrastructure as code** (IaC) describes the environment in files that live in version control. A tool compares the **desired** state in the files with the **current** state of the real environment and prints a **plan**: which resources will be created, changed or destroyed. A person reviews the plan, then applies it. The same files recreate the environment elsewhere, which is how staging stays close to production.

The value of the plan is that it makes the effect of a change visible before it happens: a one-line edit that would destroy and recreate the database shows up as a destroy.

**Cost** needs the same discipline. Cloud services are billed by use, often by the hour, so resources left running cost money whether or not anyone uses them. Habits that matter to a small team: delete or stop what is not in use, run non-production small or on demand, tag resources by owner and purpose, set budgets with alerts, and let the team see the bill. A rough estimate (price per hour times instances times hours) before building is worth doing.

This course used no cloud account and no IaC tool. The exercises model the diff and the estimate, and the pricing numbers in them are invented.

## Worked examples

### Example 1: a plan.

Desired `web=2cpu, db=large`, current `web=2cpu, db=small`: `~ db`.

### Example 2: an estimate.

`app:12:2` and `db:40:1` for 730 hours: (12 times 2 plus 40) times 730 = 46 720 cents (invented prices).

## Where this is used

- Every team that runs more than one environment. The stage project models a release pipeline rather than infrastructure, because no cloud account is available to this course.

## Common mistakes

:::mistake{id=MC213}
**Leaving test resources running because "nobody is using them".** Billing is by time, not by traffic.
:::

## Practice

::exercise{id=j11-l3.2-write-plan}

::exercise{id=j11-l3.2-write-cost}

::exercise{id=j11-l3.2-explain-iac}

## Further reading

- **AWS, policy evaluation logic** `[I131]` and **security groups** `[I132]`, for what such files typically configure.

## How you'll be assessed

- The **write** exercises check the plan and the estimate (*implementation*).
- The **explain** exercise checks the case for IaC and cost habits (*explanation*).

The description of plans and cost habits is general industry practice and is not quoted from a recorded source.
""")
print("module 11.3 authored")
