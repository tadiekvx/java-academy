# Stage 6 plan: Databases and persistence

Status: proposal, 2026-11-06. Written before any Stage 6 lesson. It decides what the
platform can grade honestly, and records the one platform change needed.

## 1. What the platform can grade, and what it cannot

The learner's code runs as one compact source file in a separate JVM with no database
server and an empty environment. PostgreSQL runs only for the platform itself.

| Topic | Can be graded? | How |
|---|---|---|
| SQL (`SELECT`, joins, grouping, subqueries, writes) | **Yes, if the JVM gets an embedded database** | Learner's SQL runs against an in-memory H2 database created by the exercise driver; the driver returns rows as strings or numbers |
| JDBC (`PreparedStatement`, row mapping, repositories) | **Yes, with the same change** | The learner writes Java that opens an H2 connection and queries it; the driver sets up fixtures and calls the learner's method |
| Transactions (commit, rollback, constraint failures) | **Yes, single-threaded** | Two connections used in sequence; deterministic |
| Lost update / isolation | **Partly** | A deterministic two-connection interleaving can be reproduced; real concurrent isolation is explanation-only (Stage 9 covers concurrency) |
| Indexes and `EXPLAIN` | **Read, not tuned** | Real PostgreSQL 18 output is captured for the lesson; learners read plans and explain them. Query-plan choices are not graded automatically |
| Flyway migrations | **No** | The platform's own real migrations are read; migration execution is explanation-only |
| JPA / Hibernate | **No runtime** | Assessed by code reading, explanation, and plain-Java simulations of lazy loading and N+1 query counts. Nothing claims to run Hibernate |
| PostgreSQL administration | **No** | Real `psql` output is captured; no learner connects to a server |

**Why H2 and not PostgreSQL:** the runner is one JVM; there is no database per learner.
H2 2.4.240 is pure Java, starts in memory inside that JVM, and supports the standard SQL
this stage teaches (keys, joins, aggregates, constraints, transactions, `EXPLAIN`).
The lessons state that PostgreSQL 18 is the platform's production database, that the
examples were run there, and where H2's dialect differs. PostgreSQL-specific output is
labelled as such and never presented as H2 output.

## 2. The platform change (needs the owner's decision)

1. Add `com.h2database:h2` (version managed by Spring Boot 4.1.2: 2.4.240) as a runtime
   dependency of the backend.
2. In `LocalJvmRunner`, add the H2 jar from the platform's class path to the compile and
   run class paths of learner programs. Nothing else about execution changes. The runner
   remains **not a sandbox**, and the lesson content says an in-memory database is not a
   security boundary.
3. Add a regression test that compiles and runs a small JDBC program through the runner
   and checks its rows, so a future class-path change cannot silently break Stage 6.

Alternatives considered:

- **Explanation-only stage.** No platform change, but the stage could not assess the
  central skill (writing SQL and JDBC) at all. Rejected as too weak.
- **SQLite JDBC.** Also a single jar, but H2 has stronger standard-SQL support
  (constraints, `GROUP BY`, transactions, `EXPLAIN`) and is the database Spring Boot's
  own test support documents. H2 also runs in PostgreSQL compatibility mode.
- **Use the platform's PostgreSQL.** Rejected: learner code would share the platform's
  data, credentials would have to be exposed, and a test could damage real records.

If the owner declines the change, Stage 6 becomes explanation- and code-reading-only
(like the Git and Maven lessons in Stage 4), and the stage states that plainly.

## 3. Modules and lessons (13 lessons)

The master plan lists 24 lesson topics. As with Stages 2–5, closely related topics are
combined; nothing central is dropped. The omissions are stated in the docs.

### 6.1 Relational thinking and SQL (4 lessons)
1. `j6-l1.1` Tables, keys and relationships — entities, primary and foreign keys,
   one-to-many, many-to-many via a join table, a first normal form argument.
2. `j6-l1.2` Querying with `SELECT`, `WHERE` and `NULL` — projection, filtering,
   ordering, `NULL` and three-valued logic, `IS NULL`.
3. `j6-l1.3` Joins and aggregates — inner and left joins, `GROUP BY`, `HAVING`,
   aggregate traps (`COUNT(*)` vs `COUNT(column)`, grouping before filtering).
4. `j6-l1.4` Writing data, indexes and query plans — `INSERT`/`UPDATE`/`DELETE`,
   `RETURNING`, unique and check constraints at work, what an index does, reading a real
   PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)` plan.

### 6.2 Transactions and integrity (3 lessons)
5. `j6-l2.1` Constraints that keep data honest — `NOT NULL`, `UNIQUE`, `CHECK`,
   foreign keys and referential actions; why the database, not only Java, enforces them.
6. `j6-l2.2` Transactions: all or nothing — `BEGIN`/`COMMIT`/`ROLLBACK`, ACID with
   concrete bank examples, atomic transfers, constraint failures mid-transaction.
7. `j6-l2.3` Isolation, lost updates and migrations — read committed and the anomalies
   it allows, a deterministic lost-update reproduction, `SELECT ... FOR UPDATE` and
   optimistic version columns; Flyway's role, read from the platform's real migrations.

### 6.3 JDBC (3 lessons)
8. `j6-l3.1` Connections and `PreparedStatement` — `DriverManager`, try-with-resources,
   parameters, SQL injection demonstrated and fixed, batch updates.
9. `j6-l3.2` Mapping rows and repositories — `ResultSet` to records, generated keys,
   repository boundaries, keeping SQL out of the domain model.
10. `j6-l3.3` Transactions and resource management in JDBC — auto-commit off,
    commit/rollback in the right places, closing in the right order, a leak reproduced
    and fixed.

### 6.4 JPA and Hibernate (3 lessons, explanation and simulation only)
11. `j6-l4.1` Entities, relationships and the persistence context — what an ORM maps,
    the identity map and dirty checking, why `@Entity` classes are not records.
12. `j6-l4.2` Lazy loading and the N+1 problem — a plain-Java simulation counts queries;
    learners predict, measure and fix the count. Clearly labelled as a simulation of the
    behaviour, not Hibernate itself.
13. `j6-l4.3` Choosing JDBC, JPA or something else — trade-offs, when SQL is clearer,
    when an ORM earns its cost; a design-justification explanation.

## 4. Projects

- **`j6-p1-brightbank` (Category B).** Brightbank v6: schema, constraints, a JDBC
  repository in one file against H2. Milestones: create schema; open an account; deposit
  and withdraw with a constraint; atomic transfer; statement with a join; a change
  request adds a date filter and a monthly summary. Requirements and acceptance criteria
  only.
- **`j6-a1-inherited-ledger` (Category C).** An inherited JDBC ledger with seeded
  defects: SQL injection, a join that duplicates rows, a read-modify-write lost update,
  a connection leak on the error path, and a query-per-row loop. Bug reports, a change
  request, and review questions. Every defect is reproducible against H2 and has a test
  that fails before the fix and passes after it.

## 5. Evidence and honesty

- Every SQL/JDBC exercise's expected values are computed independently in Python from
  the fixture data, not by running the Java reference.
- Every lesson that quotes PostgreSQL output will quote output captured from the
  project's PostgreSQL 18 on port 5433, with the command that produced it.
- JPA claims are read from the Jakarta Persistence specification and the Hibernate
  documentation; the lessons say what was read and that Hibernate was not run.
- No learner has used any of this. No person has reviewed it. The mentor is not tested
  against a real model and does not support projects.
