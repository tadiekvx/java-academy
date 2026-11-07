"""Stage 7 authoring: module 7.4 (Testing a Spring application). Real tests from this repository are used for reading."""
import l7common
from l7common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex41 = Exercises("j7-l4.1")
ex42 = Exercises("j7-l4.2")

REGISTER = {
    "j7-l4.1": ("Unit, slice and integration tests", ["J7.11"]),
    "j7-l4.2": ("Testing HTTP behaviour", ["J7.12"]),
}
MISCS = {
    "MC176": (["J7.11"], "I93", "Every Spring test should start the whole application context, because that is the only realistic test"),
    "MC177": (["J7.12"], "I93", "A test with mocked collaborators proves the whole feature works"),
}
register(REGISTER, MISCS)


def f_classify(http, db, whole):
    if whole or (http and db):
        return "integration"
    if http or db:
        return "slice"
    return "unit"


CLASSIFY_SOL = '''
String classify(boolean usesHttp, boolean usesDatabase, boolean needsWholeContext) {
    if (needsWholeContext || (usesHttp && usesDatabase)) {
        return "integration";
    }
    if (usesHttp || usesDatabase) {
        return "slice";
    }
    return "unit";
}
'''
CLASSIFY_NO_WHOLE = CLASSIFY_SOL.replace("needsWholeContext || ", "")
CLASSIFY_BOTH_SLICE = CLASSIFY_SOL.replace(" || (usesHttp && usesDatabase)", "")
CLASSIFY_HTTP_ONLY_UNIT = CLASSIFY_SOL.replace("if (usesHttp || usesDatabase) {", "if (usesDatabase) {")

ex41.method(
    "write", "j7-l4.1-write-classify", "Which kind of test", ["o1"], ["J7.11"], ["IMPL"],
    "This is a rule of thumb, not a Spring rule. Write `classify(usesHttp, usesDatabase, needsWholeContext)` returning the cheapest kind of test that will do. `integration` if the test needs the whole application context, or both the web layer and the database. `slice` if it needs only the web layer or only the database. Otherwise `unit`.",
    [("classify", [("usesHttp", "boolean"), ("usesDatabase", "boolean"), ("needsWholeContext", "boolean")], "String")], {"classify": f_classify},
    [("classify", (False, False, False), "a pure rule"), ("classify", (True, False, False), "a controller's mapping"), ("classify", (True, True, False), "a request that writes a row")],
    [("classify", (False, True, False), "a repository query"), ("classify", (False, False, True), "security and configuration together"), ("classify", (True, False, True), "whole context"),
     ("classify", (True, True, True), "everything"), ("classify", (False, True, True), "database plus whole context")],
    starter='''
String classify(boolean usesHttp, boolean usesDatabase, boolean needsWholeContext) {
    return "";
}
''', solution=CLASSIFY_SOL,
    wrongs={"ignores-whole-context": CLASSIFY_NO_WHOLE, "http-plus-db-is-slice": CLASSIFY_BOTH_SLICE, "http-only-is-unit": CLASSIFY_HTTP_ONLY_UNIT},
    hints=["Which conditions force the most expensive kind?", "A web-layer test with no database is which kind?"],
    misconceptions=("MC176",), difficulty=2,
)

TEST_CODE = '''@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class ProjectFlowTest {

    @LocalServerPort
    int port;

    private ApiClient client;

    @BeforeEach
    void setUp() {
        client = new ApiClient(port);
    }

    @Test
    void listsAllProjectsWithTheirCategories() throws Exception {
        String body = client.get("/api/projects").body();

        assertThat(body)
                .contains("\\"id\\":\\"j1-p1-finance\\"").contains("\\"category\\":\\"A\\"");
    }
}'''
ex41.explain(
    "j7-l4.1-explain-levels", "Reading a real test", ["o2"], ["J7.11"],
    "This is a shortened copy of a real test from this platform.\n\n" + fence(TEST_CODE, "java") + "\n\nWhat kind of test is it (unit, slice or integration)? What does `RANDOM_PORT` do? What does this test give you that a test of the controller class on its own would not, and what does it cost?",
    "It is an integration test: @SpringBootTest builds the application context and, with RANDOM_PORT, starts an embedded server on a random port, so the test makes real HTTP requests through the whole stack (routing, serialisation, security, the real beans). A unit test of the controller class would not exercise the mapping, JSON conversion or filters. The cost is slower tests that need more setup, and failures that point at the whole stack rather than one class.",
    levels={
        2: ("The answer classifies it, explains RANDOM_PORT, and names both the gain and the cost.", [
            "An integration test. @SpringBootTest loads the whole context and RANDOM_PORT starts a real embedded server on a free port, so the request goes over HTTP through routing, JSON and security. A plain controller test would miss those. It is slower and a failure could be anywhere in the stack.",
            "It is an integration test of the running application. RANDOM_PORT means a real server on a random free port, so there are no port clashes between test runs. It proves the pieces work together, but it is slower than a unit test and harder to diagnose."]),
        1: ("The answer classifies it or explains the port but not both the gain and the cost.", [
            "It is an integration test that starts the app.",
            "RANDOM_PORT starts the server on a random port."]),
        0: ("The answer calls it a unit test or misreads the annotation.", [
            "It is a unit test because it has one test method.",
            "RANDOM_PORT makes the test data random."]),
    },
)

l7_l4_1 = Lesson("j7-l4.1", "Unit, slice and integration tests", ["J7.11"], [
    ("o1", "Choose the cheapest kind of test that can catch a given problem"),
    ("o2", "Read a real Spring Boot integration test and say what it proves and costs"),
], ["j7-l3.3"], 40, ["I93"], """## Before you start

You should have written unit tests in Stage 4 and know the controller, service and repository layers.

## Explanation

Tests come in sizes. A **unit test** exercises one class with its collaborators replaced by fakes: it is fast and pinpoints a failure. An **integration test** starts the application and exercises the pieces together. In between are **slice tests**, which load only a part of the configuration.

The Spring Boot reference explains why slices exist: auto-configuration works well for applications, but can be a little too much for tests, so it often helps to load only the parts of the configuration that are required to test a slice of the application. For example, `@WebMvcTest` focuses on the web layer without starting a complete application context.

`@SpringBootTest` creates the application context through `SpringApplication`. With `webEnvironment = RANDOM_PORT` it starts an embedded server on a random port and gives you a real web environment, so requests go over real HTTP; the default mock environment is used with `@AutoConfigureMockMvc` instead.

The rule of thumb is to use the cheapest test that can catch the problem: a business rule needs a unit test, a mapping needs a web slice, and the wiring between layers needs a few integration tests.

## Worked examples

### Example 1: a real integration test of this platform.

`ProjectFlowTest` in this repository is annotated `@SpringBootTest(webEnvironment = RANDOM_PORT)`. It starts the real backend and calls the project API through HTTP.

### Example 2: a unit test with a fake (plain Java).

```java
TransferService tested = new TransferService(m -> "recorded");
```

No container is needed. This is the benefit of constructor injection from lesson 7.2.1.

## Where this is used

- Every Spring project's test suite: many unit tests, some slices, few integration tests.

## Common mistakes

:::mistake{id=MC176}
**Starting the whole context for every test.** It is slow and makes failures hard to locate. Use the cheapest test that can catch the problem.
:::

## Practice

::exercise{id=j7-l4.1-write-classify}

::exercise{id=j7-l4.1-explain-levels}

## Further reading

- **Spring Boot reference, testing Spring Boot applications** `[I93]`.

## How you'll be assessed

- The **write** exercise checks that you can choose a test size (*implementation*).
- The **explain** exercise checks that you can read a real test (*explanation*).

The platform cannot run Spring tests. The test above is real code from this repository, and the lesson cites what its annotations do from the reference.
""")


def f_diff(expected, actual):
    for i in range(max(len(expected), len(actual))):
        e = expected[i] if i < len(expected) else "<missing>"
        a = actual[i] if i < len(actual) else "<missing>"
        if e != a:
            return f"index {i}: expected {e} but was {a}"
    return "same"


DIFF_SOL = '''
String firstDifference(List<String> expected, List<String> actual) {
    int longest = Math.max(expected.size(), actual.size());
    for (int i = 0; i < longest; i++) {
        String e = i < expected.size() ? expected.get(i) : "<missing>";
        String a = i < actual.size() ? actual.get(i) : "<missing>";
        if (!e.equals(a)) {
            return "index " + i + ": expected " + e + " but was " + a;
        }
    }
    return "same";
}
'''
DIFF_SHORTEST = DIFF_SOL.replace("Math.max(expected.size(), actual.size())", "Math.min(expected.size(), actual.size())")
DIFF_LAST = DIFF_SOL.replace('            return "index " + i + ": expected " + e + " but was " + a;\n', '            return "index " + (i + 1) + ": expected " + e + " but was " + a;\n')
DIFF_SWAPPED = DIFF_SOL.replace('"index " + i + ": expected " + e + " but was " + a', '"index " + i + ": expected " + a + " but was " + e')

ex42.method(
    "write", "j7-l4.2-write-diff", "A useful assertion message", ["o1"], ["J7.12"], ["IMPL"],
    "A good failing test says where it went wrong. Write `firstDifference(expected, actual)`: `same` if the lists are equal, otherwise `index N: expected X but was Y` for the first position (from 0) where they differ. A list that ends early shows `<missing>` in its place.",
    [("firstDifference", [("expected", "List<String>"), ("actual", "List<String>")], "String")], {"firstDifference": f_diff},
    [("firstDifference", (["a", "b"], ["a", "b"]), "equal lists"), ("firstDifference", (["a", "b", "c"], ["a", "x", "c"]), "a changed element"), ("firstDifference", (["a", "b"], ["a"]), "the actual list is short")],
    [("firstDifference", (["a"], ["a", "b"]), "the actual list is long"), ("firstDifference", ([], []), "both empty"), ("firstDifference", ([], ["a"]), "expected is empty"),
     ("firstDifference", (["a", "b"], ["b", "a"]), "order matters"), ("firstDifference", (["200", "OK"], ["404", "OK"]), "the first position"),
     ("firstDifference", (["x", "y", "z"], ["x", "y", "z", "w"]), "an extra element")],
    starter='''
String firstDifference(List<String> expected, List<String> actual) {
    return "";
}
''', solution=DIFF_SOL,
    wrongs={"ignores-extra-elements": DIFF_SHORTEST, "one-based-index": DIFF_LAST, "swapped-message": DIFF_SWAPPED},
    hints=["Loop to the length of the longer list.", "What should be reported for a position one list does not have?"],
    misconceptions=("MC177",), difficulty=2,
)

ex42.explain(
    "j7-l4.2-explain-mocks", "When a mock misleads", ["o2"], ["J7.12"],
    "A test replaces the account repository with a mock (for example with `@MockitoBean`) that returns a canned account, and checks that `GET /accounts/7` returns 200 with that account. The feature later breaks in production because the real query has a typo, and the test stays green. Explain why, and say what you would add. Also say why testing against a real database is valuable and what, on this machine, stops you from using Testcontainers.",
    "A mock replaces the real collaborator, so the test proves only that the controller and service work with the canned answer; the real query is never run. To catch a broken query you need a test against a real database, such as an integration test or a repository slice test. Testcontainers would give a real PostgreSQL in a container, but this machine has no Docker installed, so it cannot be used here; the platform's own tests use the project's database or an in-memory one instead.",
    levels={
        2: ("The answer explains what the mock hides, adds a real-database test, and states the Docker limit.", [
            "The mock returns what the test told it to, so the query is never executed and its typo is invisible. I would add a test that runs the real repository against a real database. Testcontainers would give a real PostgreSQL, but Docker is not installed on this machine, so I would use the project's own database or an in-memory one here.",
            "Mocks isolate the layer, but they also hide the layer they replace. A repository test or integration test against an actual database would have caught the typo. Testcontainers needs Docker, which this machine does not have, so it is not an option here."]),
        1: ("The answer explains the mock but gives no remedy or ignores the environment.", [
            "The mock hides the real query, so the test passed anyway.",
            "Add an integration test with a real database."]),
        0: ("The answer trusts the mock or blames the framework.", [
            "The test passed, so the feature must work.",
            "Spring is not reliable with mocks."]),
    },
)

l7_l4_2 = Lesson("j7-l4.2", "Testing HTTP behaviour", ["J7.12"], [
    ("o1", "Write assertion messages that show where a response differs"),
    ("o2", "Explain when a mocked collaborator hides a defect that a real one would show"),
], ["j7-l4.1"], 40, ["I93"], """## Before you start

You should know the three test sizes from the last lesson.

## Explanation

An HTTP test sends a request and checks the **status**, the **headers** that matter and the **body**. You can do that in two ways. With a mock web environment (`@AutoConfigureMockMvc`), the request is dispatched inside the same process without a network connection, which is fast. With `RANDOM_PORT`, a real embedded server listens on a random port and the test makes a real HTTP call, which exercises more.

A test double such as one created with `@MockitoBean` (Spring Framework's annotation for defining a Mockito mock inside the application context) is useful to simulate failures that are hard to trigger. But a mock only returns what you tell it to, so the test proves nothing about the collaborator it replaced. Use mocks to isolate, and keep tests that run the real thing for the parts that matter, such as queries.

A failing test should say where it differs: which position, what was expected and what happened. That is the habit the exercise trains.

**What this lesson does not cover:** Testcontainers, the usual way to run a real PostgreSQL in a test, needs Docker, which is not installed on the machine this course was built on. The idea is the same as using the project's own database in an integration test.

## Worked examples

### Example 1: assert the whole response.

```java
String body = client.get("/api/projects").body();
assertThat(body).contains("\\"category\\":\\"A\\"");
```

(from this repository's `ProjectFlowTest`).

### Example 2: a message that locates the problem.

`index 1: expected 404 but was 200` tells you more than `lists differ`.

## Where this is used

- API regression tests, contract checks between a front end and a back end, and bug reports that include a failing test.

## Common mistakes

:::mistake{id=MC177}
**Believing a test with mocked collaborators proves the feature works.** It proves the code under test works with the mock's answers.
:::

## Practice

::exercise{id=j7-l4.2-write-diff}

::exercise{id=j7-l4.2-explain-mocks}

## Further reading

- **Spring Boot reference, testing Spring Boot applications** `[I93]`.

## How you'll be assessed

- The **write** exercise checks that you can report a difference usefully (*implementation*).
- The **explain** exercise checks that you can judge what a mock hides (*explanation*).
""")
print("module 7.4 authored")
