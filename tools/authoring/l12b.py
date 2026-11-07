"""Stage 12 authoring: module 12.2 (Advanced engineering practices). Plain-Java models; expectations from Python."""
import zlib
import l12common
from l12common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex21 = Exercises("j12-l2.1")
ex22 = Exercises("j12-l2.2")
ex23 = Exercises("j12-l2.3")

REGISTER = {
    "j12-l2.1": ("Safe change: expand and contract, and flags", ["J12.05"]),
    "j12-l2.2": ("Legacy code and technical debt", ["J12.06"]),
    "j12-l2.3": ("Design reviews and estimates", ["J12.07"]),
}
MISCS = {
    "MC218": (["J12.05"], "I133", "Renaming a database column is one safe step: change the column and deploy the code together"),
    "MC219": (["J12.06"], "I135", "To work safely on legacy code, first clean it up; tests can come later"),
    "MC220": (["J12.07"], "I136", "An estimate is a promise of one number, and a design review is a check that the author is right"),
}
register(REGISTER, MISCS)

# ====================================================================== j12-l2.1
RULES = {
    "dual-write": ["add-new-column"],
    "backfill": ["add-new-column"],
    "switch-reads": ["backfill", "dual-write"],
    "stop-writing-old": ["switch-reads"],
    "drop-old-column": ["switch-reads", "stop-writing-old"],
}


def f_phases(phases):
    done = set()
    for p in phases:
        for need in RULES.get(p, []):
            if need not in done:
                return f"unsafe:{p} needs {need}"
        done.add(p)
    return "safe"


PH_SOL = '''
String checkPhases(List<String> phases) {
    Map<String, List<String>> needs = Map.of(
            "dual-write", List.of("add-new-column"),
            "backfill", List.of("add-new-column"),
            "switch-reads", List.of("backfill", "dual-write"),
            "stop-writing-old", List.of("switch-reads"),
            "drop-old-column", List.of("switch-reads", "stop-writing-old"));
    Set<String> done = new HashSet<>();
    for (String phase : phases) {
        for (String need : needs.getOrDefault(phase, List.of())) {
            if (!done.contains(need)) {
                return "unsafe:" + phase + " needs " + need;
            }
        }
        done.add(phase);
    }
    return "safe";
}
'''
PH_NO_DROP_RULE = PH_SOL.replace('"drop-old-column", List.of("switch-reads", "stop-writing-old"));', '"drop-old-column", List.of("switch-reads"));')
PH_FIRST_ONLY = PH_SOL.replace('"switch-reads", List.of("backfill", "dual-write"),', '"switch-reads", List.of("backfill"),')
PH_LAST_WINS = PH_SOL.replace("        done.add(phase);\n", "        done.clear();\n        done.add(phase);\n")
PH_NO_ADD = PH_SOL.replace('"dual-write", List.of("add-new-column"),\n            "backfill", List.of("add-new-column"),', '"dual-write", List.of(),\n            "backfill", List.of(),')
GOOD = ["add-new-column", "dual-write", "backfill", "switch-reads", "stop-writing-old", "drop-old-column"]

ex21.method(
    "write", "j12-l2.1-write-phases", "Is the migration order safe", ["o1"], ["J12.05"], ["IMPL"],
    "Renaming a column without downtime uses the expand-migrate-contract (parallel change) pattern in several releases. The phases and what each needs before it: `dual-write` and `backfill` need `add-new-column`; `switch-reads` needs `backfill` and `dual-write`; `stop-writing-old` needs `switch-reads`; `drop-old-column` needs `switch-reads` and `stop-writing-old`; `add-new-column` needs nothing. Write `checkPhases(phases)` returning `safe`, or for the **first** phase whose needs are not all done earlier in the list, `unsafe:PHASE needs NEED` naming the first missing need in the order listed above. Unknown phases need nothing.",
    [("checkPhases", [("phases", "List<String>")], "String")], {"checkPhases": f_phases},
    [("checkPhases", (GOOD,), "the full safe order"), ("checkPhases", (["add-new-column", "drop-old-column"],), "dropping too early"), ("checkPhases", (["switch-reads"],), "switching before anything is ready")],
    [("checkPhases", (["add-new-column", "backfill", "switch-reads"],), "switching reads before dual write"), ("checkPhases", (["add-new-column", "dual-write", "backfill", "switch-reads", "drop-old-column"],), "dropping before the old writes stop"),
     ("checkPhases", (["add-new-column", "backfill", "dual-write", "switch-reads", "stop-writing-old", "drop-old-column"],), "backfill and dual write in either order"), ("checkPhases", ([],), "nothing at all"),
     ("checkPhases", (["dual-write"],), "writing to a column that does not exist"), ("checkPhases", (["add-new-column", "mystery", "dual-write"],), "an unknown phase"), ("checkPhases", (["add-new-column", "dual-write", "backfill", "stop-writing-old"],), "stopping writes before the switch")],
    starter='''
String checkPhases(List<String> phases) {
    return "safe";
}
''', solution=PH_SOL,
    wrongs={"drop-needs-too-little": PH_NO_DROP_RULE, "switch-needs-too-little": PH_FIRST_ONLY, "forgets-earlier-phases": PH_LAST_WINS, "ignores-add-column": PH_NO_ADD},
    hints=["Remember which phases you have already seen.", "Report the first problem you meet, reading left to right."],
    misconceptions=("MC218",), difficulty=3,
)


def f_flag(user, flag, percent):
    return zlib.crc32(f"{flag}:{user}".encode()) % 100 < percent


FLAG_SOL = '''
boolean inRollout(String user, String flag, int percent) {
    java.util.zip.CRC32 crc = new java.util.zip.CRC32();
    crc.update((flag + ":" + user).getBytes(java.nio.charset.StandardCharsets.UTF_8));
    return crc.getValue() % 100 < percent;
}
'''
FLAG_RANDOM = '''
boolean inRollout(String user, String flag, int percent) {
    return Math.random() * 100 < percent;
}
'''
FLAG_NO_FLAG = FLAG_SOL.replace('(flag + ":" + user)', '(user)')
FLAG_LE = FLAG_SOL.replace("< percent", "<= percent")
FLAG_HASHCODE = FLAG_SOL.replace("    java.util.zip.CRC32 crc = new java.util.zip.CRC32();\n    crc.update((flag + \":\" + user).getBytes(java.nio.charset.StandardCharsets.UTF_8));\n    return crc.getValue() % 100 < percent;", "    return Math.floorMod((flag + \":\" + user).hashCode(), 100) < percent;")
USERS = [f"user{i}" for i in range(40)]

ex21.method(
    "write", "j12-l2.1-write-rollout", "A stable percentage rollout", ["o2"], ["J12.05"], ["IMPL"],
    "A feature flag turned on for a percentage of users must give the **same** answer for the same user every time, and different flags must pick different users. Write `inRollout(user, flag, percent)`: compute the CRC-32 checksum (`java.util.zip.CRC32`) of the UTF-8 bytes of `flag + \":\" + user`, take it modulo 100, and return true if that is **below** `percent`. (0 is nobody, 100 is everybody.)",
    [("inRollout", [("user", "String"), ("flag", "String"), ("percent", "int")], "boolean")], {"inRollout": f_flag},
    [("inRollout", ("ada", "new-ui", 50), "a user and a flag"), ("inRollout", ("ada", "new-ui", 0), "nobody"), ("inRollout", ("ada", "new-ui", 100), "everybody")],
    [("inRollout", (u, "new-ui", 30), f"{u} at 30 percent") for u in USERS[:7]] + [("inRollout", ("grace", "other-flag", 50), "another flag"), ("inRollout", ("", "f", 50), "empty user"), ("inRollout", ("user0", "new-ui", 9), "a user exactly on the boundary is not in"), ("inRollout", ("user0", "new-ui", 10), "one percent more brings them in")],
    starter='''
boolean inRollout(String user, String flag, int percent) {
    return false;
}
''', solution=FLAG_SOL,
    wrongs={"random": FLAG_RANDOM, "ignores-the-flag": FLAG_NO_FLAG, "at-most": FLAG_LE, "java-hashcode": FLAG_HASHCODE},
    hints=["The same input must always give the same output, so do not use randomness.", "`<` against the percentage, not `<=`."],
    misconceptions=("MC218",), difficulty=3,
)

ex21.explain(
    "j12-l2.1-explain-safe-change", "Two ways to change safely", ["o2"], ["J12.05"],
    "The accounts table has a `balance_text` column that must become a numeric `balance_cents` column, with the service running all the time and several instances deployed one after another. Describe the phases you would use (expand, migrate, contract) and which release does what; explain why a single release that renames the column breaks the rolling update of lesson 11.2.2; and explain how a feature flag helps with the switch of reads and what it costs.",
    "Expand: add the new nullable balance_cents column (old code ignores it). Migrate: release code that writes both columns (dual write), backfill the old rows, then release code that reads the new column, switching back is possible while the old column is still written. Contract: stop writing the old column, then drop it in a later release. A single rename breaks the rolling update because during the rollout old and new instances run together and share the database: whichever version does not know the new name fails. A flag lets you switch reads for a percentage of users and switch back instantly without a deploy, so the risky step is small and reversible; the cost is complexity: every flag adds branches to test, and old flags must be removed once the change is done.",
    levels={
        2: ("The answer gives the phases with releases, explains the coexisting versions problem, and states the flag benefit and cost.", [
            "Release 1: add balance_cents (expand). Release 2: dual-write both columns and backfill old rows (migrate). Release 3: read from balance_cents, possibly behind a flag. Release 4: stop writing the old column. Release 5: drop it (contract). A one-step rename fails because during a rolling update old and new versions run at once against one database, and one of them will not know the column. A flag allows switching reads gradually and back without a deploy, but adds branches that must be tested and later removed.",
            "Add the new column first, then write to both and backfill, then switch reads, then stop writing the old one, and only then drop it. Rename in one go breaks the mixed-version period. A flag makes the read switch reversible but is extra complexity to clean up."]),
        1: ("The answer lists some phases or the flag point, not both with the reason.", [
            "Add the new column, copy the data, then drop the old one.",
            "Use a feature flag."]),
        0: ("The answer renames in one step.", [
            "Rename the column and deploy at night.",
            "Take the service down while changing it."]),
    },
)

l12_l2_1 = Lesson("j12-l2.1", "Safe change: expand and contract, and flags", ["J12.05"], [
    ("o1", "Check that a multi-release migration is in a safe order"),
    ("o2", "Plan a zero-downtime schema change and explain how a feature flag helps and costs"),
], ["j6-l2.3", "j11-l2.2"], 45, ["I133", "I134"], """## Before you start

You should know database migrations (lesson 6.2.3) and rolling updates (lesson 11.2.2).

## Explanation

In a system that is always running, you cannot change the shape of the data and the code that uses it in one instant. During a rolling update the old and the new version both run, against the same database. A change that only one version understands breaks the other.

**Parallel change**, also called **expand and contract**, is the pattern for backward-incompatible changes. It breaks the change into three phases: **expand** (add the new thing beside the old one), **migrate** (move the users of the old thing, and the data, to the new one), **contract** (remove the old thing). Each step is small and each release works with the one before it, so any step can be rolled back.

For renaming a database column that means: add the new column; write to both and backfill the old rows; switch reads to the new column; stop writing the old one; and only then drop it.

A **feature toggle** (flag) lets you change system behaviour without changing code, which suits the risky step, switching reads: turn it on for 5 percent of users, watch the metrics, widen it, or turn it off at once. The article on toggles also warns that they fall into different categories that should be treated differently, and that toggles introduce complexity: each flag is another path to test, and a flag that outlives its purpose is debt. A percentage rollout must be **stable**: the same user must always land on the same side, which is why it is computed from a hash of the user and the flag, not from a random number.

## Worked examples

### Example 1: the safe order.

`add-new-column, dual-write, backfill, switch-reads, stop-writing-old, drop-old-column`. Dropping the old column right after adding the new one is unsafe because the data was never moved.

### Example 2: a stable bucket.

CRC-32 of `new-ui:ada`, modulo 100, gives the same number on every machine and in every release, so user `ada` is in or out of the 30 percent for good.

## Where this is used

- Every schema change on a live system, and every gradual release.

## Common mistakes

:::mistake{id=MC218}
**Renaming a column in one release.** Whatever version does not know the new name fails during the rollout. Expand, migrate, then contract.
:::

## Practice

::exercise{id=j12-l2.1-write-phases}

::exercise{id=j12-l2.1-write-rollout}

::exercise{id=j12-l2.1-explain-safe-change}

## Further reading

- **Parallel Change** `[I133]`.
- **Feature Toggles** `[I134]`.

## How you'll be assessed

- The **write** exercises check the order of phases and a stable rollout (*implementation*).
- The **explain** exercise checks that you can plan the change (*explanation*).

The phase names for the column rename are the author's application of the pattern, not a quotation. The use of a CRC for bucketing is one common technique, not the only one.
""")

# ====================================================================== j12-l2.2
def legacy_fee(grams, zone, express):
    if zone == "LOCAL":
        f = 500 if grams <= 1000 else 500 + ((grams - 1000 + 499) // 500) * 100
    elif zone == "ZA":
        f = 900 + (grams // 1000) * 150
    else:
        f = 2500 + (grams // 1000) * 400
    if express:
        f = f + f // 2
    return f


def new_fee(grams, zone, express):
    if zone == "LOCAL" and grams >= 20000:
        return 0
    return legacy_fee(grams, zone, express)


LEGACY = '''
int fee(int grams, String zone, boolean express) {
    int f;
    if (zone.equals("LOCAL")) {
        f = grams <= 1000 ? 500 : 500 + ((grams - 1000 + 499) / 500) * 100;
    } else if (zone.equals("ZA")) {
        f = 900 + (grams / 1000) * 150;
    } else {
        f = 2500 + (grams / 1000) * 400;
    }
    if (express) {
        f = f + f / 2;
    }
    return f;
}
'''
FEE_SOL = LEGACY.replace("    int f;\n", "    if (zone.equals(\"LOCAL\") && grams >= 20000) {\n        return 0;\n    }\n    int f;\n")
FEE_ALL_ZONES = FEE_SOL.replace('zone.equals("LOCAL") && grams >= 20000', "grams >= 20000")
FEE_BOUNDARY = FEE_SOL.replace("grams >= 20000", "grams > 20000")
FEE_EXPRESS_COSTS = FEE_SOL.replace("        return 0;\n    }\n    int f;", "        return express ? 150 : 0;\n    }\n    int f;")
FEE_FIXED_QUIRK = FEE_SOL.replace("f = 900 + (grams / 1000) * 150;", "f = 900 + ((grams + 999) / 1000) * 150;")
FEE_FIXED_ROUNDING = FEE_SOL.replace("f = f + f / 2;", "f = (int) Math.round(f * 1.5);")

ex22.method(
    "modify", "j12-l2.2-modify-fee", "Add a rule without breaking the quirks", ["o1"], ["J12.06"], ["MOD"],
    "`fee` calculates a shipping fee in cents, and it has quirks that customers' invoices depend on (the `ZA` zone ignores a part of a kilogram, an express fee uses integer arithmetic, and so on). Change nothing about those results. Add one rule: a parcel for the `LOCAL` zone of **20000 grams or more** is free (fee 0, and express does not change that). All other results must stay exactly as they are, even where you think they are wrong. Pin the old behaviour down first (a characterization test), then make the change.",
    [("fee", [("grams", "int"), ("zone", "String"), ("express", "boolean")], "int")], {"fee": new_fee},
    [("fee", (500, "LOCAL", False), "a small local parcel"), ("fee", (20000, "LOCAL", False), "exactly 20 kg is free"), ("fee", (1999, "ZA", False), "the ZA quirk")],
    [("fee", (1000, "LOCAL", False), "the local base"), ("fee", (1001, "LOCAL", True), "just over the base, express"), ("fee", (19999, "LOCAL", False), "just under free"), ("fee", (30000, "LOCAL", True), "free even with express"),
     ("fee", (30000, "ZA", False), "heavy parcels in other zones still cost"), ("fee", (2500, "ZA", True), "ZA with express, integer arithmetic"), ("fee", (999, "EU", False), "another zone"), ("fee", (4200, "EU", True), "another zone with express"),
     ("fee", (20000, "LOCAL", True), "free at the limit with express")],
    starter=LEGACY, solution=FEE_SOL,
    wrongs={"free-in-every-zone": FEE_ALL_ZONES, "off-by-one-at-20kg": FEE_BOUNDARY, "express-charged-on-free": FEE_EXPRESS_COSTS, "fixed-the-za-quirk": FEE_FIXED_QUIRK},
    hints=["Add the new rule before the existing calculation.", "Do not tidy the quirks: the invoices depend on them."],
    misconceptions=("MC219",), difficulty=3,
)

ex22.explain(
    "j12-l2.2-explain-debt", "Managing debt on purpose", ["o2"], ["J12.06"],
    "Your team has these items: (a) a 400-line method nobody understands but that rarely changes; (b) a billing module changed every week that has no tests; (c) a library two major versions behind with a known vulnerability; (d) inconsistent naming across the code. Explain what characterization tests are and why they come first when changing legacy code, rank the four items for the next quarter with reasons, and say how you would keep the list from being forgotten.",
    "A characterization test records what the code actually does (starting from a hypothesis and checking it), so that a change can be made safely even when nobody knows what the code is supposed to do; they come first because refactoring or extending without a safety net can silently change behaviour. Ranking by risk and cost of delay: (c) first, a known vulnerability is a security risk that grows; (b) next, because it changes weekly without tests, so its risk is exercised all the time and tests will pay back fast; (a) can wait since it rarely changes, add characterization tests only when it must change; (d) is the cheapest and lowest value, fix it opportunistically when touching code. Keep a visible, prioritised list (in the issue tracker or in ADRs) with an owner and a review date, reserve a fixed share of each iteration for debt, and record debt knowingly taken on, with the reason, when it is taken.",
    levels={
        2: ("The answer defines characterization tests and why first, ranks all four with risk reasoning, and gives a way to keep the debt visible.", [
            "A characterization test records what the code currently does, so I can change it without knowing the intent and see if I altered behaviour; it comes first because a refactor without that net can silently break things. Ranking: the vulnerable library (security risk), then billing (changed weekly, no tests), then the 400-line method (leave it until it must change), then naming (opportunistic). Keep a prioritised list in the tracker with owners, and give each iteration a fixed share for debt.",
            "Characterization tests pin current behaviour and make later change safe. Order: (c), (b), (a), (d), because of risk and change frequency. Track it visibly and review it regularly."]),
        1: ("The answer ranks without reasons or defines the tests without the ranking.", [
            "Fix the vulnerable library first.",
            "Characterization tests test what the code does."]),
        0: ("The answer proposes rewriting everything or ignoring debt.", [
            "Rewrite the whole system from scratch.",
            "Debt does not matter if the code works."]),
    },
)

l12_l2_2 = Lesson("j12-l2.2", "Legacy code and technical debt", ["J12.06"], [
    ("o1", "Add a rule to legacy code without changing any existing result"),
    ("o2", "Explain characterization tests and prioritise technical debt with reasons"),
], ["j4-l4.1", "j12-l2.1"], 45, ["I135"], """## Before you start

You should know unit tests and refactoring (Stage 4).

## Explanation

**Legacy code** is code that is valuable and hard to change: usually because it has no tests, so nobody can say what changing it would break. The temptation is to tidy it first. That is the risky order.

Feathers' technique is the **characterization test**: when you do not know whether the code is correct, write tests that record what it actually does. You start from a hypothesis (for plain text, I guess the output equals the input), run it, and let the result correct you. The tests describe the present behaviour, quirks and all. Only then do you change the code, and the tests tell you at once if you altered something you did not mean to.

The exercise does exactly that. `fee` has quirks that invoices depend on. Your task is to add one rule and change nothing else, so the quirks must stay: the hidden tests include cases that "fix" them and fail you if you do.

**Technical debt** is the accumulated cost of shortcuts and of code left to age. It is not all equal. To prioritise, ask how risky it is (a known vulnerability), how often the code changes (the more it changes, the more a lack of tests costs), and how cheap it is to fix. Make it visible: a prioritised list, owners, a share of each iteration reserved for it, and a note of debt taken on knowingly and why.

## Worked examples

### Example 1: pinning down a quirk.

The `ZA` zone computes `900 + (grams / 1000) * 150` with integer division, so 1999 grams costs the same as 1000. A characterization test records `fee(1999, "ZA", false) == 1050`.

### Example 2: the change.

Add the free-shipping rule at the top and leave every other line alone.

## Where this is used

- Every codebase older than a year. Most professional work is changing code that somebody else wrote.

## Common mistakes

:::mistake{id=MC219}
**Cleaning up legacy code before pinning its behaviour.** Each tidy-up may change a result that someone depends on. Characterize first, then change.
:::

## Practice

::exercise{id=j12-l2.2-modify-fee}

::exercise{id=j12-l2.2-explain-debt}

## Further reading

- **M. Feathers, Characterization Testing** `[I135]`.

## How you'll be assessed

- The **modify** exercise checks that you change only what was asked (*modification*).
- The **explain** exercise checks your reasoning about debt (*explanation*).

The ranking method in the debt exercise (risk, change frequency, cost) is common practice, not a quotation.
""")

# ====================================================================== j12-l2.3
def f_pert(o, m, p):
    return (o + 4 * m + p + 3) // 6


PERT_SOL = '''
int pertDays(int optimistic, int likely, int pessimistic) {
    return (optimistic + 4 * likely + pessimistic + 3) / 6;
}
'''
PERT_AVG = '''
int pertDays(int optimistic, int likely, int pessimistic) {
    return (optimistic + likely + pessimistic) / 3;
}
'''
PERT_FLOOR = PERT_SOL.replace("+ 3) / 6", ") / 6")
PERT_LIKELY = '''
int pertDays(int optimistic, int likely, int pessimistic) {
    return likely;
}
'''
PERT_WRONG_WEIGHT = PERT_SOL.replace("4 * likely", "2 * likely")

ex23.method(
    "write", "j12-l2.3-write-estimate", "A range, not a promise", ["o1"], ["J12.07"], ["IMPL"],
    "A three-point estimate gives optimistic, most-likely and pessimistic durations in days. One common way to combine them (the PERT formula) is `(optimistic + 4 * likely + pessimistic) / 6`. Write `pertDays(optimistic, likely, pessimistic)` returning that value **rounded to the nearest whole day, halves up** (use integer arithmetic).",
    [("pertDays", [("optimistic", "int"), ("likely", "int"), ("pessimistic", "int")], "int")], {"pertDays": f_pert},
    [("pertDays", (2, 4, 12), "a feature"), ("pertDays", (5, 5, 5), "no uncertainty"), ("pertDays", (1, 2, 3), "symmetrical")],
    [("pertDays", (1, 1, 10), "a long tail"), ("pertDays", (3, 6, 9), "rounding half up"), ("pertDays", (0, 0, 0), "nothing"), ("pertDays", (1, 3, 20), "a very pessimistic case"), ("pertDays", (10, 12, 14), "a narrow range"), ("pertDays", (2, 3, 4), "exactly three"), ("pertDays", (4, 5, 11), "fractional result")],
    starter='''
int pertDays(int optimistic, int likely, int pessimistic) {
    return 0;
}
''', solution=PERT_SOL,
    wrongs={"plain-average": PERT_AVG, "rounds-down": PERT_FLOOR, "ignores-the-range": PERT_LIKELY, "wrong-weight": PERT_WRONG_WEIGHT},
    hints=["Add 3 before dividing by 6 to round half up.", "The likely value counts four times."],
    misconceptions=("MC220",), difficulty=2,
)

ex23.explain(
    "j12-l2.3-explain-review", "Review a design", ["o2"], ["J12.07"],
    "A colleague's design document proposes: 'Split accounts and payments into two microservices now, each with its own database. The payments service will call accounts synchronously for every payment. We estimate it takes three weeks.' Write the review you would give. Include: two questions about the design, with the failure scenario each is probing (use Stage 10); one thing you would ask to be decided in an ADR; what is missing from the estimate; and how you would phrase the review so that it is useful and kind.",
    "Questions: (1) A payment needs the accounts service. When accounts is slow or down, what happens to payments (timeouts, retries, cascading failure, breaker or fallback), and how is a payment made exactly once if the call is retried (idempotency key)? (2) With two databases there is no single transaction for debit and credit: how is a failure between the two steps handled (saga with compensation, outbox) and what does the customer see? ADR: whether to split at all for a small team with one product (a modular monolith is the alternative), with the context and consequences recorded. Estimate: a single number with no range or assumptions; it omits the operating costs (deployment pipelines for two services, monitoring, data migration, testing failure paths) and uncertainty; ask for optimistic, likely and pessimistic values and the assumptions. Tone: review the design, not the person; say what is good, ask questions rather than issue verdicts, give reasons, and separate must-fix from suggestions.",
    levels={
        2: ("The answer asks two substantive distributed-systems questions, calls for an ADR on the split, criticises the estimate and gives a constructive tone.", [
            "Questions: what happens to payments when accounts is slow or down (timeouts, breaker, fallback), and how is a retried payment kept exactly-once with an idempotency key? How do you handle a failure between debit and credit across two databases (saga, outbox)? Please record in an ADR why we split rather than keep a modular monolith. The estimate is one number with no range or assumptions, and leaves out pipelines, monitoring, data migration and failure testing; give three points. I would start with what is good in the plan, ask questions rather than demand changes, and mark which points must be settled before starting.",
            "Probe failure: synchronous coupling and cascades; no shared transaction. Ask for an ADR on splitting versus a monolith. The estimate needs a range and its assumptions and the cost of running two services. Be specific and respectful, review the design not the author."]),
        1: ("The answer has some questions or the estimate point but not both.", [
            "Microservices are too complicated for the team.",
            "Three weeks is too short."]),
        0: ("The answer accepts the proposal or attacks the author.", [
            "Looks good to me, ship it.",
            "This design is amateur and the author should know better."]),
    },
)

ex23.explain(
    "j12-l2.3-explain-estimate", "Saying how long it will take", ["o2"], ["J12.07"],
    "Your manager asks 'how long will the transfer-limits feature take?' You have an estimate of 2 days optimistic, 5 likely and 14 pessimistic. Compute the three-point (PERT) figure by hand, and then write the answer you would give your manager in three or four sentences: what you say, what assumptions you state, what could change it, and when you will update them.",
    "(2 + 4 times 5 + 14) divided by 6 = 36 / 6 = 6 days. A good answer gives the range, not just the number: about 6 days expected, most likely 5, and it could take up to 14 if the unknowns go badly. It states the assumptions (the limits rules are already agreed, the existing transfer code can be extended without refactoring, review and testing are included) and names the biggest risks (unclear rules, the legacy fee code, dependency on another team). It commits to an update at a specific point, for example after the first two days when the unknowns have shrunk, and says what would trigger an earlier warning. It avoids both a single confident date and a refusal to answer.",
    levels={
        2: ("The answer computes 6 days and communicates a range with assumptions, risks and an update point.", [
            "(2 + 4*5 + 14)/6 = 6 days. I would say: expect about 6 working days, likely 5, but up to 14 if the rules turn out unclear or the old fee code needs refactoring. This assumes the limits are agreed and that testing is included. I will update you after two days, and sooner if the rules change.",
            "6 days by the formula. Tell the manager: about a week, range 2 to 14, depends on the rules being settled and on the legacy code. Review again after the first spike."]),
        1: ("The answer computes the number or communicates a range, not both.", [
            "It will take 6 days.",
            "It could be anywhere from 2 to 14 days."]),
        0: ("The answer refuses or gives false certainty.", [
            "Exactly 5 days, I promise.",
            "It is impossible to estimate software."]),
    },
)

l12_l2_3 = Lesson("j12-l2.3", "Design reviews and estimates", ["J12.07"], [
    ("o1", "Combine three-point estimates"),
    ("o2", "Review a design and communicate an estimate honestly"),
], ["j10-l1.3", "j12-l2.2"], 40, ["I136", "I119"], """## Before you start

You should have read about decision records and trade-offs (module 10.1) and distributed failures (module 10.2).

## Explanation

Two of a senior engineer's regular jobs are not coding: reviewing designs and saying how long things will take.

**A design review** examines a proposal before it is built, when changing it is cheapest. A useful review asks questions that probe failure and cost, not just correctness: what happens when this dependency is down; how is a retried request made safe; where is the single transaction when there are two databases; what does this cost to operate. It asks for the decision to be written down (an ADR) when it is architecturally significant. And it is written about the design, not the person: say what is good, ask questions rather than issue verdicts, give reasons, and separate what must be settled from what is a suggestion.

**Estimating** is predicting something uncertain. A single number hides the uncertainty and invites a promise. A **range** is more honest and more useful. The three-point estimate takes an optimistic, a most-likely and a pessimistic figure; one common weighted combination, the PERT formula, is `(optimistic + 4 × likely + pessimistic) / 6`. Whatever the method, state the **assumptions** (what must be true), name the **risks** that would move the figure, and say **when you will update** it. An estimate is a forecast that is revised as unknowns become known, not a commitment made once.

## Worked examples

### Example 1: a figure.

2, 5 and 14 days give (2 + 20 + 14) / 6 = 6 days.

### Example 2: a microservice proposal.

The review questions come straight from module 10.2: slow dependency, retries, no shared transaction.

## Where this is used

- Every planning meeting and every pull request that proposes a structural change. The capstone asks you to defend decisions in writing.

## Common mistakes

:::mistake{id=MC220}
**Giving one number as a promise, or using a review to prove the author wrong.** Give a range with assumptions, and review to improve the design.
:::

## Practice

::exercise{id=j12-l2.3-write-estimate}

::exercise{id=j12-l2.3-explain-review}

::exercise{id=j12-l2.3-explain-estimate}

## Further reading

- **Microservices (Lewis and Fowler)** `[I136]`.
- **Architectural Decision Records** `[I119]`.

## How you'll be assessed

- The **write** exercise checks the estimate formula (*implementation*).
- The **explain** exercises check the quality of a review and an estimate (*explanation*).

The PERT formula and the advice on reviews and estimates are standard practice and were not taken from a recorded source. The two readings above cover the design questions, not the estimating method.
""")
print("module 12.2 authored")
