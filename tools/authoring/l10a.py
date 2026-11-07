"""Stage 10 authoring: module 10.1 (Architecture principles). Expected values come from Python models; the dependency table is computed from this repository."""
import l10common
from l10common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex11 = Exercises("j10-l1.1")
ex12 = Exercises("j10-l1.2")
ex13 = Exercises("j10-l1.3")

REGISTER = {
    "j10-l1.1": ("Layers, dependency direction and coupling", ["J10.01"]),
    "j10-l1.2": ("Ports and adapters", ["J10.02"]),
    "j10-l1.3": ("Monolith or services, and decision records", ["J10.03"]),
}
MISCS = {
    "MC198": (["J10.01"], "I117", "Layers are only folders; a lower layer may freely call back up to a higher one when that is convenient"),
    "MC199": (["J10.02"], "I117", "A port is a framework feature; the domain code needs to know which database or web framework is outside it"),
    "MC200": (["J10.03"], "I118", "Microservices are the modern default, so a new system should start as many small services"),
}
register(REGISTER, MISCS)

# ====================================================================== j10-l1.1
def f_violations(layers, deps):
    idx = {n: i for i, n in enumerate(layers)}
    out = []
    for d in deps:
        a, b = d.split(">")
        if a not in idx or b not in idx or idx[b] < idx[a]:
            out.append(d)
    return out


VIOL_SOL = '''
List<String> layerViolations(List<String> layers, List<String> deps) {
    List<String> bad = new ArrayList<>();
    for (String dep : deps) {
        String[] parts = dep.split(">");
        int from = layers.indexOf(parts[0]);
        int to = layers.indexOf(parts[1]);
        if (from < 0 || to < 0 || to < from) {
            bad.add(dep);
        }
    }
    return bad;
}
'''
VIOL_UPWARD_OK = VIOL_SOL.replace("if (from < 0 || to < 0 || to < from) {", "if (from < 0 || to < 0) {")
VIOL_SAME_BAD = VIOL_SOL.replace("to < from", "to <= from")
VIOL_UNKNOWN_OK = VIOL_SOL.replace("from < 0 || to < 0 || to < from", "to < from && from >= 0 && to >= 0")
VIOL_SORTED = VIOL_SOL.replace("    return bad;", "    Collections.sort(bad);\n    return bad;")
LAYERS = ["controller", "service", "repository"]

ex11.method(
    "write", "j10-l1.1-write-violations", "Which dependencies point the wrong way", ["o1"], ["J10.01"], ["IMPL"],
    "The layers are listed from the top (closest to the user) to the bottom. A layer may depend on itself or on a layer **below** it; a dependency on a layer above it, or on a name that is not a layer, is a violation. Each dependency is `from>to`. Write `layerViolations(layers, deps)` returning the violating dependencies in the order they were given.",
    [("layerViolations", [("layers", "List<String>"), ("deps", "List<String>")], "List<String>")], {"layerViolations": f_violations},
    [("layerViolations", (LAYERS, ["controller>service", "service>repository"]), "a clean design"), ("layerViolations", (LAYERS, ["repository>service"]), "the bottom calls the middle"), ("layerViolations", (LAYERS, []), "no dependencies")],
    [("layerViolations", (LAYERS, ["service>controller", "controller>repository", "repository>controller"]), "two upward calls"), ("layerViolations", (LAYERS, ["service>service"]), "within a layer"),
     ("layerViolations", (LAYERS, ["service>cache"]), "an unknown layer"), ("layerViolations", (LAYERS, ["cache>service"]), "an unknown source"), ("layerViolations", (["a"], ["a>a", "a>b"]), "a single layer"),
     ("layerViolations", (LAYERS, ["service>controller", "repository>service", "controller>service"]), "order is kept")],
    starter='''
List<String> layerViolations(List<String> layers, List<String> deps) {
    return List.of();
}
''', solution=VIOL_SOL,
    wrongs={"upward-calls-allowed": VIOL_UPWARD_OK, "same-layer-forbidden": VIOL_SAME_BAD, "unknown-names-allowed": VIOL_UNKNOWN_OK, "sorted-output": VIOL_SORTED},
    hints=["Compare the positions of the two layers in the list.", "What does `indexOf` return for a name that is not there?"],
    misconceptions=("MC198",), difficulty=2,
)

DEPS = cap("cap_deps.txt")
ex11.explain(
    "j10-l1.1-explain-dependencies", "Reading this platform's structure", ["o2"], ["J10.01"],
    "This table was produced by a script that reads every Java file of this platform's backend and lists, for each top-level package, the other packages its imports mention.\n\n" + fence(DEPS) + "\n\nAnswer: (1) Which package depends on the most others, and what is its job? (2) Which packages depend on nothing else, and why is that a good property? (3) The last line says no package is on a dependency cycle: what would a cycle between `content` and `assessment` cost? (4) Why is it sensible that `api` depends on `assessment` but `assessment` does not depend on `api`?",
    "(1) api depends on five packages (assessment, content, learner, mentor, progress): it is the outer layer that turns HTTP requests into calls to the others. (2) content, execution and learner depend on nothing else in the application, so they can be understood, tested and changed on their own, and many packages build on them. (3) A cycle would make the two packages impossible to understand or test separately and would make a change in one risk breaking the other; neither could be extracted without the other. (4) Dependencies point inwards, from the HTTP layer to the logic it uses. The logic should not know about HTTP, so it can be reused (by the validator, for example) and tested without a web server.",
    levels={
        2: ("The answer reads the table correctly and links each point to coupling, testing and dependency direction.", [
            "(1) api, with five dependencies; it is the entry layer that maps HTTP to the other packages. (2) content, execution and learner depend on no other package, which keeps them independent and easy to test. (3) A content-assessment cycle would couple them so neither could be changed or tested alone. (4) api sits on top and calls down; the logic must not depend on the web layer, so it can be tested and reused without it.",
            "api is the biggest consumer (assessment, content, learner, mentor, progress). content, execution, learner are leaves, so changes there are safe from upward surprises but affect everyone above. A cycle would tangle two packages into one unit. Dependency direction goes from api to the logic, never back."]),
        1: ("The answer reads parts of the table without the reasons.", [
            "api depends on the most packages and content depends on none.",
            "There are no cycles, which is good."]),
        0: ("The answer misreads the table or sees no value in direction.", [
            "assessment depends on api because they work together.",
            "Direction does not matter as long as the code compiles."]),
    },
)

l10_l1_1 = Lesson("j10-l1.1", "Layers, dependency direction and coupling", ["J10.01"], [
    ("o1", "Find the dependencies that point the wrong way in a layered design"),
    ("o2", "Read a real package dependency table and say what it shows about coupling"),
], ["j7-l3.3", "j2-l3.1"], 40, ["I117"], """## Before you start

You should know controller, service and repository layers (Stage 7) and what an interface is (Stage 2).

## Explanation

As a program grows, the question that decides whether it stays changeable is *what depends on what*. A **dependency** exists when one piece of code needs another to compile or run. Two ideas help:

- **Coupling** is how much one part depends on another: the more it knows about the other's details, the harder it is to change either alone. **Cohesion** is how closely the things inside one part belong together.
- **Dependency direction**: in a layered design, upper layers depend on lower ones and never the other way round. The controller calls the service, the service calls the repository; the repository does not call the controller. When a lower layer needs to reach upward, that is a design smell, and the usual remedy is an interface owned by the lower layer and implemented above (next lesson).

A **cycle** (A depends on B and B on A) is the worst case: neither can be understood, tested or moved without the other.

You do not have to guess. Tools, or a short script, can read the imports and show the real dependency graph. The exercise gives you one for this platform's own backend.

## Worked examples

### Example 1: the platform's packages.

The table in the exercise was computed from the repository. `api` depends on five packages; `content`, `execution` and `learner` depend on none of the others; no package is on a cycle.

### Example 2: a violation.

`repository>service` in a controller/service/repository design is upward: the data layer would be calling business logic.

## Where this is used

- Code review, refactoring and splitting a system. Before extracting a module into a service you must know what it depends on and what depends on it.

## Common mistakes

:::mistake{id=MC198}
**Treating layers as folders.** A layer is a rule about who may call whom. If a lower layer calls upward whenever convenient, the layers no longer reduce coupling.
:::

## Practice

::exercise{id=j10-l1.1-write-violations}

::exercise{id=j10-l1.1-explain-dependencies}

## Further reading

- **Hexagonal architecture** `[I117]`, which takes dependency direction as its main rule.

## How you'll be assessed

- The **write** exercise checks that you can find wrong-way dependencies (*implementation*).
- The **explain** exercise checks that you can read a real dependency table (*explanation*).

The table was computed by a short script that reads `import` lines, so it shows direct compile-time dependencies between top-level packages and nothing about run-time calls.
""")

# ====================================================================== j10-l1.2
HEX_PROGRAM = '''
interface Ledger {
    void record(String entry);

    List<String> entries();
}

class InMemoryLedger implements Ledger {
    private final List<String> entries = new ArrayList<>();

    public void record(String entry) {
        entries.add(entry);
    }

    public List<String> entries() {
        return entries;
    }
}

class FailingLedger implements Ledger {
    public void record(String entry) {
        throw new IllegalStateException("ledger down");
    }

    public List<String> entries() {
        return List.of();
    }
}

class TransferService {
    private final Ledger ledger;

    TransferService(Ledger ledger) {
        this.ledger = ledger;
    }

    String transfer(String from, String to, int cents) {
        if (cents <= 0) {
            return "rejected";
        }
        try {
            ledger.record(from + "->" + to + ":" + cents);
            return "ok";
        } catch (IllegalStateException e) {
            return "unavailable";
        }
    }
}

void main() {
    InMemoryLedger memory = new InMemoryLedger();
    TransferService working = new TransferService(memory);
    System.out.println(working.transfer("a", "b", 50));
    System.out.println(working.transfer("a", "b", 0));
    System.out.println("entries=" + memory.entries());
    TransferService broken = new TransferService(new FailingLedger());
    System.out.println(broken.transfer("a", "b", 10));
}
'''
ex12.predict(
    "j10-l1.2-predict-ports", "One service, two adapters", ["o1"], ["J10.02"],
    "`TransferService` knows only the `Ledger` port. The program wires it once to an in-memory adapter and once to an adapter that always fails. Predict the exact output.",
    HEX_PROGRAM, "ok\nrejected\nentries=[a->b:50]\nunavailable\n",
    ["Which transfers reach the ledger at all?", "What does the service do when the adapter throws?"],
    misconceptions=("MC199",), difficulty=1,
)

ex12.explain(
    "j10-l1.2-explain-ports", "Ports and adapters", ["o2"], ["J10.02"],
    "Brightbank's `TransferService` today calls `JdbcLedger` directly, imports `java.sql` and builds SQL. The team wants to test the transfer rules without a database and to be able to replace PostgreSQL later. Describe how you would restructure it using ports and adapters: what the port is, who owns it, what the adapters are, and which way the dependencies then point. Name one thing it costs.",
    "Define a Ledger interface (the port) in the domain/service code, in terms of the domain (record a transfer, list entries), with no java.sql types. The service depends only on that interface. JdbcLedger becomes an adapter that implements the port and lives outside the core; an in-memory adapter serves tests. Dependencies point inward: the adapter depends on the port, the core depends on nothing technical. The service can then be tested with the in-memory or a failing adapter, and PostgreSQL can be replaced by writing another adapter. The cost is extra interfaces and mapping code between domain objects and the technology's data, which is only worth it where the isolation pays.",
    levels={
        2: ("The answer defines the port in domain terms, places ownership with the core, names the adapters, states the dependency direction and a cost.", [
            "The port is a Ledger interface owned by the service, expressed with domain types and no java.sql. JdbcLedger is an adapter implementing it, and tests use an in-memory adapter. The service depends on the interface, the adapter depends on the port, so dependencies point inward and the database can be swapped. The cost is extra interfaces and translation code.",
            "Introduce an interface for what the service needs from storage and make the core depend only on it. The JDBC code moves into an adapter outside the core. Tests plug in a fake. Direction: adapters point to the core, never the reverse. Cost: more types and mapping."]),
        1: ("The answer introduces an interface without ownership, direction or cost.", [
            "Put an interface in front of the repository.",
            "Use dependency injection to pass the ledger."]),
        0: ("The answer keeps the core dependent on the technology.", [
            "Keep calling JdbcLedger directly but add more tests with a real database.",
            "Move the SQL into the controller."]),
    },
)

l10_l1_2 = Lesson("j10-l1.2", "Ports and adapters", ["J10.02"], [
    ("o1", "Follow how one service behaves with different adapters behind the same port"),
    ("o2", "Restructure a service so its rules do not depend on its database"),
], ["j10-l1.1", "j7-l2.1"], 40, ["I117", "I86"], """## Before you start

You should know dependency injection (Stage 7) and the layer dependency rule (lesson 10.1.1).

## Explanation

**Ports and adapters**, also called hexagonal architecture, is a way of arranging a program so that its core does not know what is outside it. Its stated intent is to let an application be driven equally by users, programs, automated tests or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases.

The vocabulary is small. A **port** is an interface the core defines for talking to the outside, in the core's own terms. An **adapter** is technology-specific code that sits on the other side of a port: for something arriving, it converts an event from the outside world (an HTTP request, a test script) into a call on the port; for something leaving, the core sends through a port and the adapter turns it into the signals the receiving technology needs (SQL, a message). The application is ignorant of the nature of the device.

The consequence is the dependency direction from lesson 10.1.1: the adapter depends on the port, and the core depends on nothing technical. This is also what dependency injection (lesson 7.2.1) makes practical: the wiring code chooses the adapter.

## Worked examples

### Example 1: the same service, two adapters.

The exercise program runs `TransferService` against an in-memory ledger and against one that always fails. The service's rules, and its handling of the failure, are the same.

### Example 2: this platform.

The AI mentor sits behind the `MentorModel` interface and `ClaudeMentorModel` is one implementation of it (an adapter), so a test can supply a fake model instead of calling a real one.

## Where this is used

- Anywhere the outside world is slow, costly or unreliable in tests: databases, payment providers, e-mail, clocks.

## Common mistakes

:::mistake{id=MC199}
**Letting the core name its technology.** If the service imports `java.sql` or a web framework type, it has become part of the adapter, and the benefits are gone.
:::

## Practice

::exercise{id=j10-l1.2-predict-ports}

::exercise{id=j10-l1.2-explain-ports}

## Further reading

- **A. Cockburn, Hexagonal architecture** `[I117]`.

## How you'll be assessed

- The **predict** exercise checks that you can follow two adapters (*identifying*).
- The **explain** exercise checks that you can design the restructure (*explanation*).

The example from this platform is the author's reading of its structure, not a claim that it is a textbook hexagon.
""")

# ====================================================================== j10-l1.3
REQUIRED = ["Title", "Status", "Context", "Decision", "Consequences"]


def f_adr(md):
    lines = [l.strip() for l in md.split("\n")]
    out = []
    if not any(l.startswith("# ") for l in lines):
        out.append("Title")
    for sec in REQUIRED[1:]:
        if f"## {sec}" not in lines:
            out.append(sec)
    return out


ADR_SOL = '''
List<String> adrMissing(String markdown) {
    List<String> lines = new ArrayList<>();
    for (String line : markdown.split("\\n", -1)) {
        lines.add(line.strip());
    }
    List<String> missing = new ArrayList<>();
    boolean title = false;
    for (String line : lines) {
        if (line.startsWith("# ")) {
            title = true;
        }
    }
    if (!title) {
        missing.add("Title");
    }
    for (String section : List.of("Status", "Context", "Decision", "Consequences")) {
        if (!lines.contains("## " + section)) {
            missing.add(section);
        }
    }
    return missing;
}
'''
ADR_PREFIX = ADR_SOL.replace('lines.contains("## " + section)', 'lines.stream().anyMatch(l -> l.startsWith("## " + section))')
ADR_ANYWHERE = ADR_SOL.replace('lines.contains("## " + section)', 'markdown.contains(section)')
ADR_H2_TITLE = ADR_SOL.replace('line.startsWith("# ")', 'line.startsWith("#")')
ADR_ORDER = ADR_SOL.replace('List.of("Status", "Context", "Decision", "Consequences")', 'List.of("Consequences", "Decision", "Context", "Status")')
_GOOD = "# Use PostgreSQL\n\n## Status\nAccepted\n\n## Context\nWe need transactions.\n\n## Decision\nPostgreSQL.\n\n## Consequences\nWe run a database server."

ex13.method(
    "write", "j10-l1.3-write-adr", "Does the record have its parts", ["o1"], ["J10.03"], ["IMPL"],
    "A short decision record (ADR) in Markdown has a title line (`# Title`) and the sections `## Status`, `## Context`, `## Decision` and `## Consequences`, each on a line of its own (surrounding spaces ignored). Write `adrMissing(markdown)` returning the names of the parts that are missing, in the order Title, Status, Context, Decision, Consequences. A complete record returns an empty list. `## Title` does not count as a title.",
    [("adrMissing", [("markdown", "String")], "List<String>")], {"adrMissing": f_adr},
    [("adrMissing", (_GOOD,), "a complete record"), ("adrMissing", ("# Use Kafka\n\n## Context\nWe need events.",), "most parts missing"), ("adrMissing", ("",), "nothing at all")],
    [("adrMissing", ("## Title\n## Status\n## Context\n## Decision\n## Consequences",), "a second-level heading is not a title"), ("adrMissing", ("# T\n## Status\n## Context\n## Decision",), "no consequences"),
     ("adrMissing", ("# T\nThe Status of the Decision and its Context and Consequences are discussed here.",), "the words in prose do not count"), ("adrMissing", ("# T\n  ## Status  \n## Context\n## Decision\n## Consequences",), "spaces around a heading are ignored"),
     ("adrMissing", ("# T\n## Statuses\n## Context\n## Decision\n## Consequences",), "a longer heading is not the section"), ("adrMissing", ("# T\n## Consequences\n## Decision\n## Context\n## Status",), "order of sections does not matter")],
    starter='''
List<String> adrMissing(String markdown) {
    return List.of();
}
''', solution=ADR_SOL,
    wrongs={"prefix-matches": ADR_PREFIX, "words-in-prose-count": ADR_ANYWHERE, "any-heading-is-a-title": ADR_H2_TITLE, "wrong-order-of-names": ADR_ORDER},
    hints=["Compare whole trimmed lines, not substrings.", "A title starts with `# ` (one hash and a space)."],
    misconceptions=("MC200",), difficulty=2,
)

ex13.explain(
    "j10-l1.3-explain-decision", "Write the decision down", ["o2"], ["J10.03"],
    "A team of four, with one product and one database, is asked whether to split Brightbank into separate payments, accounts and reporting services. Write the ADR for the decision you would recommend: a title, the status, the context (what forces apply), the decision, and the consequences, good and bad. Use what the readings say about when a monolith is the better start.",
    "A good record recommends a modular monolith for now and says why. Context: four developers, one product, one database, transactions across accounts and payments, no independent scaling or deployment need yet. Decision: keep one deployable application, with clear module boundaries and dependency rules, and revisit if a module needs to scale or deploy on its own. Consequences: good, a single transaction, no network failures between modules, simple deployment and testing; bad, a single deploy unit and shared database, and discipline needed to keep module boundaries from eroding. It should note that services bring a cost (the microservice premium: more to deploy and operate, plus the failures of lesson 10.2) and that systems built as services from scratch have often run into serious trouble.",
    levels={
        2: ("The answer is a complete ADR with context forces, a decision, and both good and bad consequences, grounded in the readings.", [
            "# Keep Brightbank a modular monolith. Status: proposed. Context: four developers, one product and database, payments and accounts must change balances in one transaction. Decision: stay one deployable, with modules and dependency rules; revisit when a part needs independent scaling or deployment. Consequences: simple deployment and real transactions, no network failures between modules; but one deploy unit and the risk of boundaries eroding. Services carry an operating premium, and starting with them has often gone badly.",
            "Title: One application, clear modules. Status: accepted. Context: small team, one database, strong consistency needed between accounts and payments. Decision: no split now. Consequences: easier operation and testing, a single transaction; harder to scale parts separately and boundaries must be enforced by us. Revisit if the team grows or a module needs its own release cycle."]),
        1: ("The answer states a decision without a context or the bad consequences.", [
            "Decision: stay with a monolith because it is simpler.",
            "We should split into services because that is modern."]),
        0: ("The answer gives no reasoned decision.", [
            "Whatever the senior developer prefers.",
            "Do both at once so nobody can complain."]),
    },
)

l10_l1_3 = Lesson("j10-l1.3", "Monolith or services, and decision records", ["J10.03"], [
    ("o1", "Check a decision record for its required parts"),
    ("o2", "Weigh a monolith against services for a given team and write the decision down"),
], ["j10-l1.2"], 35, ["I118", "I136", "I119"], """## Before you start

You should know layers and ports (lessons 10.1.1 and 10.1.2).

## Explanation

**Microservices** are independently deployable services. The common characteristics, as described by Lewis and Fowler, are organisation around business capability, automated deployment, intelligence in the endpoints and decentralised control of languages and data; there is no precise definition.

They are not free. Fowler observes that almost all the cases he had heard of in which a system was built as microservices from scratch ended in serious trouble, and that microservices carry a significant **microservice premium**, the cost of managing a suite of services, which makes them useful only with more complex systems. The conclusion he draws is that you should not start a new project with microservices. A **modular monolith**, one deployable with enforced boundaries between modules, keeps the option open: a module with clear dependencies can be extracted later (lesson 10.1.1 showed how to check).

Whatever you decide, write it down. An **architectural decision** is a justified design choice that addresses an architecturally significant requirement; an **architectural decision record** (ADR) is a short document that keeps the decision, its context and its consequences, so that a new colleague, or you in a year, knows why. A common layout is a title, then Status, Context, Decision and Consequences.

## Worked examples

### Example 1: the record skeleton.

```markdown
# Use PostgreSQL

## Status
Accepted

## Context
We need transactions.

## Decision
PostgreSQL.

## Consequences
We run a database server.
```

### Example 2: this platform.

It is one deployable, with packages that form no cycle (lesson 10.1.1). That is what a modular monolith looks like.

## Where this is used

- Every non-trivial design discussion. The stage project asks you to defend a split in a decision record.

## Common mistakes

:::mistake{id=MC200}
**Starting with many small services because they are fashionable.** The premium is paid from the first day; the benefits arrive only when the system and the team are big enough to need them.
:::

## Practice

::exercise{id=j10-l1.3-write-adr}

::exercise{id=j10-l1.3-explain-decision}

## Further reading

- **Monolith First** `[I118]`.
- **Microservices** `[I136]`.
- **Architectural Decision Records** `[I119]`.

## How you'll be assessed

- The **write** exercise checks the structure of a record (*implementation*).
- The **explain** exercise checks that you can argue and record a decision (*explanation*).

An ADR template is a convention. The section names used here are one common layout, not a standard.
""")
print("module 10.1 authored")
