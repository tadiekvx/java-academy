"""Stage 6 authoring: module 6.4 (JPA and Hibernate): explanation and plain-Java simulation only.

The runner has no JPA provider, so learners cannot run Hibernate. The module assesses the ideas
(persistence context, dirty checking, lazy loading, the N+1 problem, choosing a tool) with
explanations and with small plain-Java simulations whose expected values are derived here.
"""
import math

import l6common
from l6common import Lesson, Exercises, q, register
import build  # noqa: E402

build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-6"
ex41 = Exercises("j6-l4.1")
ex42 = Exercises("j6-l4.2")
ex43 = Exercises("j6-l4.3")

REGISTER = {
    "j6-l4.1": ("Entities and the persistence context", ["J6.11"]),
    "j6-l4.2": ("Lazy loading and the N+1 problem", ["J6.12"]),
    "j6-l4.3": ("Choosing JDBC, JPA or SQL", ["J6.13"]),
}
MISCS = {
    "MC163": (["J6.11"], "I80", "An ORM entity must be saved with an explicit update call after every change"),
    "MC164": (["J6.12"], "I80", "Lazy loading is free because the data is only read when it is used"),
    "MC165": (["J6.13"], "I80", "An ORM should be used for every query, including reports that total many rows"),
}
register(REGISTER, MISCS)


# ====================================================================== j6-l4.1
CONTEXT_PROGRAM = """
import java.util.*;

class Account {
    final int id;
    long cents;

    Account(int id, long cents) {
        this.id = id;
        this.cents = cents;
    }
}

class Context {
    private final Map<Integer, Account> managed = new HashMap<>();
    private final Map<Integer, Long> snapshot = new HashMap<>();
    int selects = 0;
    int updates = 0;

    Account find(int id) {
        Account known = managed.get(id);
        if (known != null) {
            return known;
        }
        selects++;
        Account loaded = new Account(id, 120000);
        managed.put(id, loaded);
        snapshot.put(id, loaded.cents);
        return loaded;
    }

    void flush() {
        for (Account account : managed.values()) {
            if (account.cents != snapshot.get(account.id)) {
                updates++;
                snapshot.put(account.id, account.cents);
            }
        }
    }
}

void main() {
    Context context = new Context();
    Account first = context.find(1);
    Account second = context.find(1);
    System.out.println("same instance=" + (first == second));
    System.out.println("selects=" + context.selects);
    first.cents -= 5000;
    System.out.println("seen through second=" + second.cents);
    context.flush();
    System.out.println("updates after first flush=" + context.updates);
    context.flush();
    System.out.println("updates after second flush=" + context.updates);
    context.find(2);
    context.find(2);
    System.out.println("selects now=" + context.selects);
}
"""

# Derived by hand from the program above: one find(1) loads, the second returns the managed instance;
# 120000 - 5000 = 115000 cents; the first flush sees one changed account, the second sees none;
# find(2) loads once.
CONTEXT_EXPECTED = """same instance=true
selects=1
seen through second=115000
updates after first flush=1
updates after second flush=1
selects now=2
"""

ex41.predict(
    "j6-l4.1-predict-context",
    "What a persistence context does",
    ["o1"],
    ["J6.11"],
    "The program below is a tiny plain-Java model of a persistence context: an identity map plus a snapshot taken when an entity is loaded. Predict the exact output.",
    CONTEXT_PROGRAM,
    CONTEXT_EXPECTED,
    ["How many times is the database read when the same id is found twice?",
     "Why does the second flush find nothing to write?"],
    misconceptions=(),
    difficulty=1,
)

ex41.explain(
    "j6-l4.1-explain-context",
    "What the persistence context is",
    ["o1"],
    ["J6.11"],
    "What does an ORM's persistence context do while a transaction is open, and why does changing a field on a loaded entity not need an explicit save call?",
    "The persistence context is a cache of the entities read or made persistent in one unit of work, with one instance per identifier. Because it remembers what it loaded, it can compare each managed entity with that state when it is flushed and write only the differences (automatic dirty checking).",
    levels={
        2: ("The answer names the cache of managed entities, one instance per identifier, and dirty checking at flush.", [
            "It is a first-level cache for one unit of work: asking for the same id twice gives the same object, and at flush the ORM compares each managed entity with what it loaded and issues an UPDATE for the ones that changed.",
            "The context holds the managed entities. Because it remembers their loaded state, changes are detected and written when the session flushes, so no explicit update call is needed."]),
        1: ("The answer names the cache but not how changes reach the database.", [
            "It is a cache of the entities that were loaded in the current transaction.",
            "It keeps one object per row so the same row is not read twice."]),
        0: ("The answer treats the context as the database or as a long-lived application cache.", [
            "The context is the database itself, so a change is saved the moment the field is set.",
            "It is a cache shared by the whole application that lives until the server restarts."]),
    },
)

ex41.explain(
    "j6-l4.1-explain-entities",
    "Why an entity is not a record",
    ["o2"],
    ["J6.11"],
    "A teammate wants to declare `Account` as a record and annotate it as a JPA entity because records are shorter. Explain what the specification requires of an entity class and why a record does not fit.",
    "Jakarta Persistence requires an entity to be a top-level or static nested class, not an enum, record or interface, with a public or protected no-argument constructor, and not final. An entity also needs mutable state and a stable identity, because the persistence context manages one instance per identifier and changes its fields.",
    levels={
        2: ("The answer cites the specification's rules and ties them to managed, mutable state and identity.", [
            "The specification says an entity may not be a record and needs a no-argument constructor and must not be final. A record is immutable and final, but the ORM needs to create it empty and change fields as it tracks the row.",
            "An entity is managed: the context keeps one instance per id and updates its fields. Records are final and immutable with no no-argument constructor, so the specification excludes them."]),
        1: ("The answer says records are not allowed without the reason.", [
            "Records cannot be entities in Jakarta Persistence.",
            "An entity has to be a normal class, not a record."]),
        0: ("The answer treats the choice as style.", [
            "A record would work fine, it is just shorter and nobody cares.",
            "Entities are plain objects, so records are interchangeable with them."]),
    },
)

l6_l4_1 = Lesson("j6-l4.1", "Entities and the persistence context", ["J6.11"], [
    ("o1", "Explain what the persistence context does: one instance per identifier and automatic dirty checking"),
    ("o2", "Explain what Jakarta Persistence requires of an entity class, and why a record does not qualify"),
], ["j6-l3.2"], 40, ["I79", "I80"], """## Before you start

You should have written a repository by hand with JDBC, and you should know what a record is.

## Explanation

An object/relational mapper (ORM) maps Java classes to relational tables. **Jakarta Persistence** (JPA) is the specification; **Hibernate** is an implementation of it. A class mapped to a table is an **entity**.

The specification sets rules for an entity: it is a top-level class or a static nested class, it is not an enum, a record or an interface, it has a public or protected no-argument constructor, and it is not final.

A **persistence context** is a cache of the entities read in the current unit of work. For every entity instance read, or made persistent, the context holds one instance per identifier, so asking for the same row twice gives the same object and one database read. The Hibernate guide also calls it the first-level cache. Because it remembers what it loaded, it can find the entities you changed when the session is flushed and write the differences. That is **automatic dirty checking**: after you modify an entity you do not call an update method.

## Worked examples

### Example 1: an entity class.

```java
@Entity
public class Account {
    @Id
    private Integer id;
    private long cents;

    protected Account() { }          // required by the specification
}
```

### Example 2: what the context does in the simulation.

The program in the exercise below models the idea in plain Java. Two lookups of the same id read once. A change made through one reference is seen through the other. The first flush finds one changed account and writes it. The second flush finds nothing to write.

## Predict, then run

::exercise{id=j6-l4.1-predict-context}

## Where this is used

- Every Spring Data JPA repository and every Hibernate session sits on a persistence context, so its behaviour explains surprises such as a change being saved without any call.

## Common mistakes

:::mistake{id=MC163}
**Calling an explicit update after every change, or expecting nothing to be saved without one.** Inside a managed unit of work the context finds the change at flush; outside one (a detached entity) a change is not tracked.
:::

## Practice

::exercise{id=j6-l4.1-predict-context}

::exercise{id=j6-l4.1-explain-context}

::exercise{id=j6-l4.1-explain-entities}

## Further reading

- **Jakarta Persistence 3.2 specification** `[I79]` on the requirements for an entity class.
- **A Short Guide to Hibernate 7** `[I80]` on persistence contexts and dirty checking.

## How you'll be assessed

- The **predict** exercise checks that you can follow an identity map and a flush (*identifying*).
- The **explain** exercises check the context and the entity rules (*explanation*).

The platform cannot run Hibernate, so these exercises assess the ideas through a plain-Java model and your own words.
""")


# ====================================================================== j6-l4.2
STRATEGIES = {"lazy": lambda n: 1 + n, "join-fetch": lambda n: 1, "batch-10": lambda n: 1 + math.ceil(n / 10)}


def f_query_count(*args):
    customers, strategy = args
    if strategy not in STRATEGIES:
        return -1
    return STRATEGIES[strategy](customers)


QUERY_COUNT_SOURCE = """
int queryCount(int customers, String strategy) {
    return switch (strategy) {
        case "lazy" -> 1 + customers;
        case "join-fetch" -> 1;
        case "batch-10" -> 1 + (customers + 9) / 10;
        default -> -1;
    };
}
"""

QUERY_COUNT_FORGETS_FIRST = """
int queryCount(int customers, String strategy) {
    return switch (strategy) {
        case "lazy" -> customers;
        case "join-fetch" -> 1;
        case "batch-10" -> 1 + (customers + 9) / 10;
        default -> -1;
    };
}
"""

QUERY_COUNT_FLOOR = """
int queryCount(int customers, String strategy) {
    return switch (strategy) {
        case "lazy" -> 1 + customers;
        case "join-fetch" -> 1;
        case "batch-10" -> 1 + customers / 10;
        default -> -1;
    };
}
"""

QUERY_COUNT_FETCH_PER_ROW = """
int queryCount(int customers, String strategy) {
    return switch (strategy) {
        case "lazy", "join-fetch" -> 1 + customers;
        case "batch-10" -> 1 + (customers + 9) / 10;
        default -> -1;
    };
}
"""

NPLUS_PROGRAM = """
import java.util.*;

class Store {
    int queries = 0;
    final Map<String, List<String>> accountsByCustomer = new LinkedHashMap<>();

    Store() {
        accountsByCustomer.put("Ada Lovelace", List.of("1200.00", "50.00"));
        accountsByCustomer.put("Grace Hopper", List.of("300.50"));
        accountsByCustomer.put("Alan Turing", List.of());
        accountsByCustomer.put("Edsger Dijkstra", List.of("780.25"));
    }

    List<String> loadCustomers() {
        queries++;
        return new ArrayList<>(accountsByCustomer.keySet());
    }

    List<String> loadAccounts(String customer) {
        queries++;
        return accountsByCustomer.get(customer);
    }

    Map<String, List<String>> loadCustomersWithAccounts() {
        queries++;
        return accountsByCustomer;
    }
}

void main() {
    Store lazy = new Store();
    List<String> lazyLines = new ArrayList<>();
    for (String customer : lazy.loadCustomers()) {
        lazyLines.add(customer + " " + lazy.loadAccounts(customer));
    }
    System.out.println("lazy queries=" + lazy.queries);

    Store fetched = new Store();
    List<String> fetchedLines = new ArrayList<>();
    for (var entry : fetched.loadCustomersWithAccounts().entrySet()) {
        fetchedLines.add(entry.getKey() + " " + entry.getValue());
    }
    System.out.println("join fetch queries=" + fetched.queries);
    System.out.println("same report=" + lazyLines.equals(fetchedLines));
}
"""

# Derived by hand: lazy = 1 customer query + one account query for each of the 4 customers = 5;
# the fetch-join version issues one query; both build the same four lines.
NPLUS_EXPECTED = """lazy queries=5
join fetch queries=1
same report=true
"""

ex42.predict(
    "j6-l4.2-predict-nplusone",
    "How many queries",
    ["o1"],
    ["J6.12"],
    "A plain-Java store counts every query it is asked to run. One report loads each customer's accounts lazily, one customer at a time. The other loads customers and accounts together. Predict the exact output.",
    NPLUS_PROGRAM,
    NPLUS_EXPECTED,
    ["How many customers are there, and how many queries does the loop add for each?",
     "Does the second report show different data, or only cost less?"],
    misconceptions=("MC164",),
    difficulty=1,
)

ex42.method(
    "write",
    "j6-l4.2-write-querycount",
    "Counting the queries",
    ["o1", "o2"],
    ["J6.12"],
    ["IMPL"],
    "A report shows the accounts of every customer in a list of `customers` customers. Write `queryCount(customers, strategy)`, the number of queries the report runs. `\"lazy\"` loads the customer list with one query and then each customer's accounts with one query per customer. `\"join-fetch\"` loads everything in one query. `\"batch-10\"` loads the customer list with one query and then the accounts in batches of 10 customers, one query per batch. Any other strategy returns -1.",
    [("queryCount", [("customers", "int"), ("strategy", "String")], "int")],
    {"queryCount": f_query_count},
    [("queryCount", (3, "lazy"), "lazy loading, three customers"),
     ("queryCount", (3, "join-fetch"), "one query for all"),
     ("queryCount", (25, "batch-10"), "batches of ten")],
    [("queryCount", (0, "lazy"), "no customers still costs the first query"),
     ("queryCount", (0, "batch-10"), "no customers, no batches"),
     ("queryCount", (10, "batch-10"), "exactly one full batch"),
     ("queryCount", (11, "batch-10"), "one customer over a full batch"),
     ("queryCount", (1000, "lazy"), "a long list"),
     ("queryCount", (1000, "join-fetch"), "a long list, one query"),
     ("queryCount", (5, "eager"), "an unknown strategy")],
    starter="""
int queryCount(int customers, String strategy) {
    return 0;
}
""",
    solution=QUERY_COUNT_SOURCE,
    wrongs={"forgets-first-query": QUERY_COUNT_FORGETS_FIRST,
            "rounds-batches-down": QUERY_COUNT_FLOOR,
            "fetch-per-row": QUERY_COUNT_FETCH_PER_ROW},
    hints=["Which query loads the list of customers, and does it run for every strategy?",
           "How many batches of 10 do you need for 11 customers?"],
    misconceptions=("MC164",),
    difficulty=2,
)

ex42.explain(
    "j6-l4.2-explain-nplusone",
    "The N+1 problem",
    ["o2"],
    ["J6.12"],
    "A report loads 500 customers and then prints each customer's accounts, and it is slow in production but fast on a developer's laptop with five customers. What is happening, why does the developer not see it, and what would you change?",
    "Lazy loading means an association is fetched from the database the first time it is used. A loop over N customers that touches each customer's accounts runs one query for the list and N more, one per customer: N+1 selects. The cost grows with the data, so it is invisible with five rows. Fetch the associations the unit of work needs up front, usually with a join fetch in the query or an entity graph, or use batch or subselect fetching.",
    levels={
        2: ("The answer names N+1, explains why it grows with the data, and gives a fetching fix.", [
            "Each customer's accounts are lazy, so the loop runs one query for the customers and one more per customer: 501 queries. With five rows that is six queries and nobody notices. Use a join fetch (or an entity graph) so the accounts come in the first query.",
            "This is the N+1 select problem: lazy loading turns one report into 1 + 500 round trips. It only hurts at scale. Fix it by fetching the accounts with the customers (join fetch), or batch them, and check the query count in a test."]),
        1: ("The answer says it is slow because of many queries but gives no cause or no fix.", [
            "It runs too many queries when the data grows.",
            "The ORM is hitting the database a lot, so add a cache."]),
        0: ("The answer blames the wrong thing.", [
            "The server is too small for 500 rows, so it needs more memory.",
            "Lazy loading is faster, so the fix is to make everything lazy."]),
    },
)

l6_l4_2 = Lesson("j6-l4.2", "Lazy loading and the N+1 problem", ["J6.12"], [
    ("o1", "Count the queries a lazy and a join-fetch strategy issue for a list of N parents"),
    ("o2", "Explain the N+1 problem, why it hides in small data, and how fetching strategies remove it"),
], ["j6-l4.1"], 45, ["I80", "I79"], """## Before you start

You should have read the persistence-context lesson and written a join in SQL.

## Explanation

An ORM can load an association **lazily**: the child rows are read from the database the first time the code uses them. The ORM makes this possible with proxies for the unfetched associations. Lazy loading is convenient, because code that never touches the association never pays for it.

The cost appears in loops. A report that loads N customers and then touches each customer's accounts runs one query for the list and one more for each customer: **N+1 selects**. On a developer's machine N is small and the report is fast; in production N is large and every extra query is a round trip to the database.

The Hibernate guide lists the main strategies for avoiding this: **outer join fetching**, where the association is fetched with a left outer join; **batch fetching**, where the association is fetched with a subsequent select using a batch of primary keys; and **subselect fetching**. It advises that you should almost always use outer join fetching, written as a `join fetch` in HQL or as an entity graph, and fetch what a unit of work needs at the start of it.

## Worked examples

### Example 1: the lazy loop.

```java
List<Customer> customers = entityManager.createQuery("from Customer", Customer.class).getResultList();
for (Customer customer : customers) {
    print(customer.getAccounts());      // first use: one more query per customer
}
```

### Example 2: the same data in one query.

```java
List<Customer> customers = entityManager.createQuery(
        "select distinct c from Customer c left join fetch c.accounts", Customer.class).getResultList();
```

The report prints the same lines. Only the number of round trips changes.

## Predict, then run

::exercise{id=j6-l4.2-predict-nplusone}

## Where this is used

- Every list screen backed by a JPA repository: customer lists with their accounts, orders with their lines.
- Tests that assert the number of queries, which is how a team catches N+1 before production.

## Common mistakes

:::mistake{id=MC164}
**Treating lazy loading as free.** Nothing is read until the first use, but each first use is a query, and a loop multiplies it.
:::

## Practice

::exercise{id=j6-l4.2-predict-nplusone}

::exercise{id=j6-l4.2-write-querycount}

::exercise{id=j6-l4.2-explain-nplusone}

## Further reading

- **A Short Guide to Hibernate 7** `[I80]` on association fetching and proxies.
- **Jakarta Persistence 3.2 specification** `[I79]` on entities and the persistence context.

## How you'll be assessed

- The **predict** exercise checks that you can count queries (*identifying*).
- The **write** exercise checks that you can model the cost of each strategy (*implementation*).
- The **explain** exercise checks the cause and the fix (*explanation*).

The platform cannot run Hibernate, so the code here counts queries in a plain-Java model. The fetch-join snippet above is shown for reading only and has not been run on this platform.
""")


# ====================================================================== j6-l4.3
ex43.explain(
    "j6-l4.3-explain-choice",
    "JDBC, JPA or SQL",
    ["o1", "o2"],
    ["J6.13"],
    "A team must decide how a new bank service reads and writes data. Their first feature is a month-end report that sums transactions across all accounts. Their second is a screen that edits one customer and their accounts. For each feature, say whether you would use hand-written SQL through JDBC or an ORM such as JPA, and what each choice costs.",
    "The choice depends on the work. A set-based report that aggregates many rows is clearest and fastest as one SQL statement, whichever API sends it. A screen that loads a small graph of related objects, changes some fields and saves them fits an ORM, because the persistence context tracks the changes. The ORM costs a persistence-context model to learn, risks N+1 selects and generated SQL you must inspect; JDBC costs mapping code and repetition, and gives full control.",
    levels={
        2: ("The answer matches each feature to a tool with a reason, and names a cost of each.", [
            "The report should be one SQL aggregate (JDBC, or a native or JPQL query), because it works on many rows at once and an ORM would load them as objects. The edit screen suits JPA: the entity is loaded, fields changed, and dirty checking writes them. JPA costs N+1 risk and generated SQL to inspect; JDBC costs hand-written mapping.",
            "Use SQL for the month-end report because the database is good at sums over many rows and I control the statement. Use an ORM for editing a customer with its accounts: less mapping code and automatic change tracking, but I must watch the queries it generates and the fetching strategy."]),
        1: ("The answer picks tools but gives no reason or no cost.", [
            "JDBC for the report and JPA for the edit screen.",
            "Use JPA for both because it is the modern way."]),
        0: ("The answer treats the tools as interchangeable or one as always wrong.", [
            "It makes no difference, they all talk to the same database.",
            "ORMs are always bad, so write SQL for everything and never use JPA."]),
    },
)

l6_l4_3 = Lesson("j6-l4.3", "Choosing JDBC, JPA or SQL", ["J6.13"], [
    ("o1", "Say what each of hand-written SQL, JDBC and JPA is good at"),
    ("o2", "Choose a tool for a given piece of work, and name what the choice costs"),
], ["j6-l4.2"], 35, ["I79", "I80", "I75"], """## Before you start

You should have written JDBC code by hand and explained the N+1 problem.

## Explanation

**SQL** is the language of the database. **JDBC** is the Java API that sends SQL to it: you write the statements and map the rows yourself. **JPA** is a specification for mapping classes to tables, with a persistence context that tracks changes; Hibernate implements it.

They are not alternatives at the same level. An ORM sends SQL through JDBC underneath, and an ORM can run a hand-written query. The question is where the work is.

- **Set-based work** (a report that sums many rows, a bulk update) is a statement about tables. Write it as SQL; mapping each row to an object adds cost and no clarity.
- **Object-graph work** (load a customer and their accounts, change some fields, save) is where an ORM saves code: the persistence context finds the changes at flush.

Each choice has a cost. With JDBC you write and maintain the mapping and the repetition, and you control every statement. With an ORM you must learn the persistence context, watch for N+1 selects, and read the SQL it generates. The Hibernate guide itself recommends an explicit, stateless style where accidental lazy fetching would be a problem.

## Worked examples

### Example 1: a report.

```sql
SELECT account_id, SUM(amount) FROM transactions GROUP BY account_id;
```

One statement, one result. Sending it through JDBC, or as a query from JPA, is a detail; loading every transaction as an object first would be the mistake.

### Example 2: an edit screen.

Load the customer, change `city`, commit. With JPA the entity is managed, so the change is written at flush. With JDBC you write the `UPDATE` and keep it in step with the fields.

## Where this is used

- Every Spring service that has both reporting queries and edit screens uses both styles.

## Common mistakes

:::mistake{id=MC165}
**Loading rows as objects to total them in Java.** The database sums many rows in one statement; an ORM that loads every row first turns a report into a memory and N+1 problem.
:::

## Practice

::exercise{id=j6-l4.3-explain-choice}

## Further reading

- **A Short Guide to Hibernate 7** `[I80]` on persistence contexts, stateless sessions and fetching.
- **Jakarta Persistence 3.2 specification** `[I79]` for the standard.
- **Java SE 25 API** `[I75]` on `PreparedStatement`.

## How you'll be assessed

- The **explain** exercise checks that you match the tool to the work and name the cost (*explanation*).

This lesson is judged by an explanation only. No exercise here can show that a choice would work in a real project.
""")

print("module 6.4 authored")
