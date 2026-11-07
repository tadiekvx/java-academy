"""Regenerates the Stage 2+ parts of curriculum.yaml from the lesson files that exist."""
import os, re
CUR = "/Users/brandon/Documents/Java/content/java/curriculum.yaml"
BASE = "/Users/brandon/Documents/Java/content/java"

# id, name, prerequisites, required evidence
CONCEPTS = [
 ("J2.01","Classes, fields and constructors",["J1.10","J1.08"],["IMPL","EXPL","DEBUG"]),
 ("J2.02","Instance methods and this",["J2.01"],["IMPL","MIST","MOD"]),
 ("J2.03","Object references and equality",["J2.02"],["MIST","DEBUG","EXPL"]),
 ("J2.04","static members, toString and equals",["J2.03"],["IMPL","MOD","EXPL"]),
 ("J2.05","Encapsulation and invariants",["J2.04"],["IMPL","DEBUG","EXPL"]),
 ("J2.06","Immutability and defensive copies",["J2.05"],["IMPL","DEBUG","EXPL"]),
 ("J2.07","Interfaces and polymorphism",["J2.05"],["IMPL","MIST","EXPL"]),
 ("J2.08","Inheritance and abstract classes",["J2.07"],["IMPL","MIST","MOD"]),
 ("J2.09","Composition over inheritance",["J2.08"],["IMPL","EXPL"]),
 ("J2.10","Records and enums",["J2.06"],["IMPL","MOD","EXPL"]),
 ("J2.11","Sealed types and pattern-matching switch",["J2.10","J2.07"],["IMPL","DEBUG","EXPL"]),
 ("J2.12","Catching exceptions",["J2.05","J1.12"],["IMPL","MIST","DEBUG"]),
 ("J2.13","Custom and checked exceptions",["J2.12"],["IMPL","EXPL"]),
 ("J2.14","Cleanup and where to catch",["J2.13"],["IMPL","EXPL"]),
 ("J3.01","Lists and sets",["J2.14","J1.11"],["IMPL","MIST","EXPL"]),
 ("J3.02","Maps",["J3.01"],["IMPL","DEBUG","EXPL"]),
 ("J3.03","Ordering and safe iteration",["J3.02"],["IMPL","DEBUG","EXPL"]),
 ("J3.04","Generics",["J3.01","J2.07"],["IMPL","EXPL"]),
 ("J3.05","Lambdas and functional interfaces",["J3.04"],["IMPL","MIST","EXPL"]),
 ("J3.06","Stream pipelines",["J3.05"],["IMPL","MOD","DEBUG"]),
 ("J3.07","Optional, and choosing loops or streams",["J3.06"],["IMPL","EXPL"]),
 ("J3.08","Reading and writing files",["J2.14"],["IMPL","DEBUG"]),
 ("J3.09","Parsing text data and handling failures",["J3.08"],["IMPL","EXPL"]),
 ("J3.10","Dates and time zones",["J2.10"],["IMPL","DEBUG","EXPL"]),
 ("J3.11","Money and BigDecimal",["J3.10"],["IMPL","DEBUG","EXPL"]),
 ("J3.12","Strings in depth",["J1.04"],["IMPL","MOD"]),
 ("J4.01","Git: commits, branches and merging",["J3.12"],["EXPL"]),
 ("J4.02","Git: conflicts, remotes and undoing",["J4.01"],["EXPL"]),
 ("J4.03","Maven: project layout and the POM",["J3.12"],["EXPL"]),
 ("J4.04","Maven: lifecycle, dependencies and conflicts",["J4.03"],["EXPL"]),
 ("J4.05","Writing unit tests",["J4.04","J3.12"],["IMPL","EXPL"]),
 ("J4.06","Test quality: edges, exceptions and doubles",["J4.05"],["IMPL","EXPL"]),
 ("J4.07","Logging and debugging",["J2.14"],["DEBUG","EXPL"]),
 ("J4.08","Refactoring under tests",["J4.06"],["IMPL","MOD"]),
 ("J4.09","Code smells and code review",["J4.08"],["EXPL"]),
 ("J5.01","Counting steps and growth rates",["J3.12"],["IMPL","EXPL","MIST"]),
 ("J5.02","Measuring honestly and spotting accidental quadratics",["J5.01"],["IMPL","DEBUG","EXPL"]),
 ("J5.03","Dynamic arrays",["J5.02"],["IMPL","DEBUG","EXPL"]),
 ("J5.04","Linked lists",["J5.03"],["IMPL","MIST","DEBUG"]),
 ("J5.05","Stacks and queues",["J5.04"],["IMPL","EXPL"]),
 ("J5.06","Hash tables",["J5.05"],["IMPL","DEBUG","EXPL"]),
 ("J5.07","Binary search trees",["J5.04"],["IMPL","MIST","DEBUG"]),
 ("J5.08","Heaps and priority queues",["J5.07"],["IMPL","EXPL"]),
 ("J5.09","Recursion",["J5.01"],["IMPL","MIST","DEBUG"]),
 ("J5.10","Binary search and sorting",["J5.09"],["IMPL","DEBUG","EXPL"]),
 ("J5.11","Graphs: representation and traversal",["J5.05","J5.09"],["IMPL","EXPL"]),
 ("J5.12","Shortest paths",["J5.11","J5.08"],["IMPL","EXPL"]),
 ("J5.13","Dynamic programming",["J5.09"],["IMPL","EXPL"]),
 ("J6.01","Tables, keys and relationships",["J3.01"],["IMPL","EXPL","MIST"]),
 ("J6.02","Selecting and filtering with NULL",["J6.01"],["IMPL","DEBUG","MIST"]),
 ("J6.03","Joins, aggregates and subqueries",["J6.02"],["IMPL","DEBUG","EXPL"]),
 ("J6.04","Writing data, indexes and query plans",["J6.03"],["IMPL","EXPL","DEBUG"]),
 ("J6.05","Constraints and referential integrity",["J6.01"],["IMPL","MIST","DEBUG"]),
 ("J6.06","Transactions and ACID",["J6.05"],["IMPL","EXPL","DEBUG"]),
 ("J6.07","Isolation, lost updates and migrations",["J6.06"],["IMPL","EXPL","MIST"]),
 ("J6.08","JDBC connections and PreparedStatement",["J2.14","J3.09"],["IMPL","MIST","DEBUG"]),
 ("J6.09","Mapping rows and repositories",["J6.08","J2.10"],["IMPL","MOD","EXPL"]),
 ("J6.10","JDBC transactions and resource management",["J6.08","J6.06"],["IMPL","DEBUG","EXPL"]),
 ("J6.11","ORM entities and the persistence context",["J6.09"],["EXPL","MIST"]),
 ("J6.12","Lazy loading and the N+1 problem",["J6.11"],["IMPL","DEBUG","EXPL"]),
 ("J6.13","Choosing JDBC, JPA or SQL",["J6.10","J6.12"],["EXPL","MIST"]),
 ("J7.01","HTTP requests and responses",["J6.01"],["EXPL","MIST","IMPL"]),
 ("J7.02","Methods, safety and idempotence",["J7.01"],["IMPL","EXPL","MIST"]),
 ("J7.03","Status codes and problem details",["J7.02"],["IMPL","MIST","DEBUG"]),
 ("J7.04","Resource design and routing",["J7.03"],["IMPL","EXPL","MOD"]),
 ("J7.05","Inversion of control and dependency injection",["J6.09"],["IMPL","EXPL","MIST"]),
 ("J7.06","Beans, scopes and profiles",["J7.05"],["IMPL","EXPL","MIST"]),
 ("J7.07","Auto-configuration and back-off",["J7.06"],["IMPL","EXPL","MIST"]),
 ("J7.08","Controllers and request mapping",["J7.04","J7.06"],["IMPL","EXPL","MIST"]),
 ("J7.09","Validation and error mapping",["J7.08","J7.03"],["IMPL","DEBUG","EXPL"]),
 ("J7.10","Layers, persistence and pagination",["J7.08","J6.09"],["IMPL","EXPL","MOD"]),
 ("J7.11","Unit, slice and integration tests",["J7.10"],["IMPL","EXPL","MIST"]),
 ("J7.12","Testing HTTP behaviour",["J7.11"],["IMPL","DEBUG","EXPL"]),
 ("J8.01","Threat modelling and the OWASP Top 10",["J7.09"],["EXPL","MIST","IMPL"]),
 ("J8.02","Passwords and hashing",["J8.01"],["IMPL","EXPL","MIST"]),
 ("J8.03","Untrusted input: encoding and paths",["J8.01","J6.08"],["IMPL","MIST","DEBUG"]),
 ("J8.04","Secrets and logging",["J8.01"],["IMPL","EXPL","MIST"]),
 ("J8.05","Authentication, sessions and cookies",["J8.02","J7.03"],["IMPL","EXPL","MIST"]),
 ("J8.06","Tokens and JWT",["J8.05"],["IMPL","EXPL","MIST"]),
 ("J8.07","Access control and ownership",["J8.05"],["IMPL","DEBUG","EXPL"]),
 ("J8.08","Spring Security: CSRF and CORS",["J8.05","J7.08"],["IMPL","EXPL","MIST"]),
 ("J8.09","Lockout and generic responses",["J8.05"],["IMPL","EXPL","DEBUG"]),
 ("J9.01","Threads and the cost of sharing",["J5.04"],["IMPL","EXPL","MIST"]),
 ("J9.02","Races",["J9.01"],["IMPL","EXPL","MIST"]),
 ("J9.03","synchronized, locks and atomics",["J9.02"],["IMPL","EXPL","MIST"]),
 ("J9.04","Visibility and the Java Memory Model",["J9.03"],["EXPL","MIST","IMPL"]),
 ("J9.05","Deadlock",["J9.03"],["IMPL","DEBUG","EXPL"]),
 ("J9.06","Executors and futures",["J9.03"],["IMPL","EXPL","MIST"]),
 ("J9.07","Concurrent collections",["J9.06"],["IMPL","EXPL","MIST"]),
 ("J9.08","Virtual threads and scoped values",["J9.06"],["IMPL","EXPL","MIST"]),
 ("J9.09","Memory and garbage collection",["J5.04"],["IMPL","EXPL","MIST"]),
 ("J9.10","JIT compilation and measuring honestly",["J9.09"],["IMPL","EXPL","MIST"]),
 ("J9.11","Profiling and memory leaks",["J9.10"],["IMPL","EXPL","DEBUG"]),
 ("J10.01","Layers, dependency direction and coupling",["J7.10"],["IMPL", "EXPL", "MIST"]),
 ("J10.02","Ports and adapters",["J10.01"],["IMPL", "EXPL", "MIST"]),
 ("J10.03","Monolith or services, and decision records",["J10.02"],["IMPL", "EXPL", "MIST"]),
 ("J10.04","Timeouts, retries and backoff",["J7.03"],["IMPL", "EXPL", "MIST"]),
 ("J10.05","Idempotency keys",["J10.04", "J7.02"],["IMPL", "EXPL", "DEBUG"]),
 ("J10.06","Sagas, outbox and delivery guarantees",["J10.05", "J6.06"],["IMPL", "EXPL", "MIST"]),
 ("J10.07","Circuit breakers and resilience",["J10.04"],["IMPL", "EXPL", "MIST"]),
 ("J11.01","Containers and images",["J4.05"],["EXPL", "MIST", "IMPL"]),
 ("J11.02","Multi-stage builds and image size",["J11.01"],["EXPL", "MIST", "IMPL"]),
 ("J11.03","Compose, configuration and secrets",["J11.02", "J8.04"],["EXPL", "MIST", "IMPL"]),
 ("J11.04","The JVM in containers",["J11.01", "J9.09"],["EXPL", "MIST", "DEBUG"]),
 ("J11.05","Pipelines as code",["J4.05", "J11.02"],["IMPL", "EXPL", "MIST"]),
 ("J11.06","Deployment strategies and rollback",["J11.05"],["IMPL", "EXPL", "MIST"]),
 ("J11.07","Cloud networking and identity",["J8.07", "J11.03"],["IMPL", "EXPL", "MIST"]),
 ("J11.08","Infrastructure as code and cost",["J11.07"],["IMPL", "EXPL", "MIST"]),
 ("J12.01","Structured logs and the three signals",["J8.04", "J10.04"],["IMPL", "EXPL", "MIST"]),
 ("J12.02","SLIs, SLOs and percentiles",["J12.01"],["IMPL", "EXPL", "MIST"]),
 ("J12.03","Tracing",["J12.01"],["IMPL", "EXPL", "MIST"]),
 ("J12.04","Reading an incident",["J12.02", "J9.11"],["DEBUG", "EXPL", "IMPL"]),
 ("J12.05","Safe change: expand and contract, flags",["J6.07", "J11.06"],["IMPL", "EXPL", "MIST"]),
 ("J12.06","Legacy code and technical debt",["J4.07"],["IMPL", "EXPL", "MIST"]),
 ("J12.07","Design reviews and estimates",["J10.03"],["EXPL", "MIST", "IMPL"]),
]
# (stage, module, title)
MODULES = {
 (2,1):"Classes and objects",(2,2):"Encapsulation and invariants",(2,3):"Interfaces, inheritance and polymorphism",
 (2,4):"Modern type features",(2,5):"Errors and exceptions",
 (3,1):"Collections",(3,2):"Generics",(3,3):"Lambdas and streams",(3,4):"Files, text and persistence",(3,5):"Dates, numbers and text",
 (4,1):"Git and collaboration",(4,2):"Build tools: Maven",(4,3):"Automated testing",(4,4):"Debugging, logging and refactoring",
 (5,1):"Complexity and measurement",(5,2):"Core structures",(5,3):"Algorithms",
 (6,1):"Relational thinking and SQL",(6,2):"Transactions and integrity",(6,3):"JDBC",(6,4):"JPA and Hibernate",
 (7,1):"HTTP and REST fundamentals",(7,2):"Spring core",(7,3):"Spring Boot REST APIs",(7,4):"Testing a Spring application",
 (8,1):"Security fundamentals",(8,2):"Authentication and authorisation",(9,1):"Concurrency fundamentals",(9,2):"Modern concurrency",(9,3):"JVM internals and performance",
 (10,1):"Architecture principles",(10,2):"Distributed systems fundamentals",(11,1):"Docker",(11,2):"CI/CD",(11,3):"Cloud engineering",(12,1):"Observability and troubleshooting",(12,2):"Advanced engineering practices",
}
STAGES = {2:"Object-oriented programming",3:"Core library and modern Java",4:"Professional engineering toolchain",5:"Data structures and algorithms",6:"Databases and persistence",7:"Spring and backend development",8:"Authentication and application security",9:"Concurrency, the JVM and performance",10:"Distributed systems and architecture",11:"Containers, deployment and cloud",12:"Production engineering and capstone"}
# lesson id -> (title, concepts)
LESSONS = {}
# misconceptions: id -> (concepts, source, summary)
MISC = {}

import json
STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

def register(lessons, misc):
    """lessons: {id: (title, [concepts])}; misc: {id: ([concepts], source, summary)}. Merged into state.json and
    curriculum.yaml is regenerated from everything registered so far."""
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"lessons": {}, "misc": {}}
    st["lessons"].update({k: list(v) for k, v in lessons.items()})
    st["misc"].update({k: list(v) for k, v in misc.items()})
    json.dump(st, open(STATE, "w"))
    write({k: tuple(v) for k, v in st["lessons"].items()}, {k: tuple(v) for k, v in st["misc"].items()})

def _q(s): return '"' + s.replace('"', '\\"') + '"'

def write(lesson_titles, misc, root=CUR):
    t = open(root).read()
    # strip previously generated parts
    t = re.sub(r'^  - \{id: J(?:[2-9]|1[0-2])\.\d\d,.*\n', '', t, flags=re.M)
    t = re.sub(r'^  - \{id: MC(?:2[7-9]|[3-9]\d|\d{3,}),.*\n', '', t, flags=re.M)
    t = re.sub(r'\n  - number: 2\n.*\Z', '\n', t, flags=re.S)
    con = "".join(f"  - {{id: {i}, name: {_q(n)}, prerequisites: [{', '.join(p)}], required_evidence: [{', '.join(e)}]}}\n" for i,n,p,e in CONCEPTS)
    # concepts block ends before the blank line preceding 'misconceptions:'
    k = t.index('\nmisconceptions:')
    t = t[:k].rstrip('\n') + '\n' + con + t[k:]
    mi = "".join(f"  - {{id: {i}, concepts: [{', '.join(c)}], source: {s}, summary: {_q(m)}}}\n" for i,(c,s,m) in sorted(misc.items(), key=lambda x:int(x[0][2:])))
    k = t.index('\nstages:')
    t = t[:k].rstrip('\n') + '\n' + mi + t[k:]
    out = ""
    for stage in sorted(STAGES):
        mods = {}
        for lid,(title,concepts) in sorted(lesson_titles.items(), key=lambda x:(int(x[0].split('-l')[1].split('.')[0]), int(x[0].split('.')[1]))):
            if not lid.startswith(f"j{stage}-l"): continue
            m = int(lid.split('-l')[1].split('.')[0])
            mods.setdefault(m, []).append((lid,title,concepts))
        if not mods: continue
        out += f"  - number: {stage}\n    title: {_q(STAGES[stage])}\n    modules:\n"
        for m in sorted(mods):
            out += f"      - number: {m}\n        title: {_q(MODULES[(stage,m)])}\n        lessons:\n"
            for lid,title,concepts in mods[m]:
                out += f"          - {{id: {lid}, title: {_q(title)}, concepts: [{', '.join(concepts)}]}}\n"
    t = t.rstrip('\n') + '\n' + out
    open(root, 'w').write(t)
