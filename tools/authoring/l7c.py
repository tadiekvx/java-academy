"""Stage 7 authoring: module 7.3 (Spring Boot REST APIs). Real controller code from this repository is used for reading."""
import re
import l7common
from l7common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex31 = Exercises("j7-l3.1")
ex32 = Exercises("j7-l3.2")
ex33 = Exercises("j7-l3.3")

REGISTER = {
    "j7-l3.1": ("Controllers and request mapping", ["J7.08"]),
    "j7-l3.2": ("Validation and error mapping", ["J7.09"]),
    "j7-l3.3": ("Layers, persistence and pagination", ["J7.10"]),
}
MISCS = {
    "MC173": (["J7.08"], "I91", "A controller method must build the whole HTTP response itself, including converting objects to JSON"),
    "MC174": (["J7.09"], "I92", "Validating in the controller with if statements is the same as declaring constraints, so there is nothing to gain from a framework"),
    "MC175": (["J7.10"], "I91", "Pages are numbered from 1 everywhere, and a page request beyond the data is an error"),
}
register(REGISTER, MISCS)

# ====================================================================== j7-l3.1
def f_vars(template, path):
    t, p = template.split("/"), path.split("/")
    if len(t) != len(p):
        return "no-match"
    found = []
    for a, b in zip(t, p):
        if a.startswith("{") and a.endswith("}"):
            if b == "":
                return "no-match"
            found.append(f"{a[1:-1]}={b}")
        elif a != b:
            return "no-match"
    return ",".join(found)


VARS_SOL = '''
String extractVariables(String template, String path) {
    String[] t = template.split("/", -1);
    String[] p = path.split("/", -1);
    if (t.length != p.length) {
        return "no-match";
    }
    List<String> found = new ArrayList<>();
    for (int i = 0; i < t.length; i++) {
        if (t[i].startsWith("{") && t[i].endsWith("}")) {
            if (p[i].isEmpty()) {
                return "no-match";
            }
            found.add(t[i].substring(1, t[i].length() - 1) + "=" + p[i]);
        } else if (!t[i].equals(p[i])) {
            return "no-match";
        }
    }
    return String.join(",", found);
}
'''
VARS_NO_LENGTH = VARS_SOL.replace('    if (t.length != p.length) {\n        return "no-match";\n    }\n', "").replace("i < t.length", "i < Math.min(t.length, p.length)")
VARS_NO_LITERAL = VARS_SOL.replace('        } else if (!t[i].equals(p[i])) {\n            return "no-match";\n        }', "        }")
VARS_EMPTY_OK = VARS_SOL.replace("            if (p[i].isEmpty()) {\n                return \"no-match\";\n            }\n", "")

ex31.method(
    "write", "j7-l3.1-write-variables", "Path variables", ["o1"], ["J7.08"], ["IMPL"],
    "A mapping like `@GetMapping(\"/accounts/{id}/transactions/{tid}\")` is a template. Write `extractVariables(template, path)`. A path matches when it has the same number of `/`-separated segments, every fixed segment is equal, and every `{name}` segment is non-empty. Return the variables in order as `name=value` joined by commas (an empty string if the template has none), or `no-match`.",
    [("extractVariables", [("template", "String"), ("path", "String")], "String")], {"extractVariables": f_vars},
    [("extractVariables", ("/accounts/{id}", "/accounts/7"), "one variable"),
     ("extractVariables", ("/accounts/{id}/transactions/{tid}", "/accounts/7/transactions/12"), "two variables"),
     ("extractVariables", ("/accounts/{id}", "/customers/7"), "a fixed segment differs")],
    [("extractVariables", ("/accounts", "/accounts"), "no variables"), ("extractVariables", ("/accounts/{id}", "/accounts/"), "an empty variable"),
     ("extractVariables", ("/accounts/{id}", "/accounts/7/transactions"), "too many segments"), ("extractVariables", ("/accounts/{id}/transactions", "/accounts/7"), "too few segments"),
     ("extractVariables", ("/{kind}/{id}", "/accounts/abc"), "variables anywhere"), ("extractVariables", ("/accounts/{id}", "/accounts/a%20b"), "the value is kept as sent")],
    starter='''
String extractVariables(String template, String path) {
    return "no-match";
}
''', solution=VARS_SOL,
    wrongs={"ignores-length": VARS_NO_LENGTH, "ignores-fixed-segments": VARS_NO_LITERAL, "accepts-empty-variable": VARS_EMPTY_OK},
    hints=["Compare the two lists of segments one position at a time.", "What should happen when the counts differ?"],
    misconceptions=("MC173",), difficulty=3,
)

CONTROLLER_CODE = '''@RestController
@RequestMapping("/api")
class CurriculumController {

    private final ContentAccess access;

    CurriculumController(ContentAccess access) {
        this.access = access;
    }

    @GetMapping("/lessons/{id}")
    LessonView lesson(@PathVariable String id) {
        Lesson lesson = access.lesson(id);
        // ... builds and returns a LessonView record
    }
}'''
ex31.explain(
    "j7-l3.1-explain-controller", "Reading a real controller", ["o2"], ["J7.08"],
    "This is a shortened copy of a real controller from this platform's backend.\n\n" + fence(CONTROLLER_CODE, "java") + "\n\nSay which request it handles, where `id` comes from, what happens to the `LessonView` the method returns, and where the `ContentAccess` argument comes from.",
    "It handles GET /api/lessons/{id}: the class-level @RequestMapping adds the /api prefix and @GetMapping the rest. @PathVariable binds the {id} segment of the URL to the parameter. @RestController includes @ResponseBody, so the returned LessonView is written to the response body (as JSON) rather than resolved as a view name. The ContentAccess is passed to the constructor by the container, which is dependency injection.",
    levels={
        2: ("The answer covers the route, the path variable, @ResponseBody behaviour and the injected constructor argument.", [
            "GET /api/lessons/{id}: /api from the class, /lessons/{id} from the method. @PathVariable gives id the value from the URL. Because it is a @RestController, the returned LessonView is serialised straight into the response body, not looked up as a template. Spring supplies the ContentAccess through the constructor.",
            "It answers GET requests for /api/lessons/something. The something is passed in as id by @PathVariable. @RestController means the return value is the response body (JSON). The container builds the controller and injects ContentAccess, since the constructor needs it."]),
        1: ("The answer gets the route right but not the return value or the constructor.", [
            "It handles GET /api/lessons/ with an id.",
            "It looks up a lesson by id and returns it."]),
        0: ("The answer misreads the code.", [
            "It handles every request to the server.",
            "The controller creates the ContentAccess itself."]),
    },
)

l7_l3_1 = Lesson("j7-l3.1", "Controllers and request mapping", ["J7.08"], [
    ("o1", "Match a request path against a template and extract the path variables"),
    ("o2", "Read a Spring controller: route, path variable, response body and injected dependencies"),
], ["j7-l1.4", "j7-l2.2"], 40, ["I91", "I86"], """## Before you start

You should be able to route a method and path (lesson 7.1.4) and know that the container injects constructor arguments (lesson 7.2.1).

## Explanation

A **controller** is a class whose methods handle HTTP requests. In Spring MVC you declare the routing with annotations: `@RequestMapping` on the class gives a prefix, and `@GetMapping`, `@PostMapping`, `@PutMapping` and `@DeleteMapping` on a method give the method and the rest of the path. A `{name}` segment in the path is a **path variable**, and `@PathVariable` binds it to a method parameter.

`@RestController` is a composed annotation meta-annotated with `@Controller` and `@ResponseBody`. Every method inherits `@ResponseBody`, so what it returns is written directly to the response body, converted by the message converters (JSON for a Java record), instead of being resolved as the name of a view.

A controller is a bean. Its constructor arguments are injected by the container.

## Worked examples

### Example 1: a real controller from this repository.

```java
@GetMapping("/lessons/{id}")
LessonView lesson(@PathVariable String id) { ... }
```

This is the method that served the lesson text you are reading. Its route is the table you wrote in lesson 7.1.4, written as an annotation.

### Example 2: the same route, one more segment.

`@GetMapping("/accounts/{id}/transactions/{tid}")` binds `id` and `tid`. The exercise implements the matching rule.

## Where this is used

- Every Spring REST API. Controllers should be thin: read the request, call a service, return the result.

## Common mistakes

:::mistake{id=MC173}
**Building the response by hand.** With `@RestController` you return an object and the framework writes the body and the content type.
:::

## Practice

::exercise{id=j7-l3.1-write-variables}

::exercise{id=j7-l3.1-explain-controller}

## Further reading

- **Spring Framework reference, annotated controllers** `[I91]`.

## How you'll be assessed

- The **write** exercise checks that you can match a template (*implementation*).
- The **explain** exercise checks that you can read a real controller (*explanation*).

The platform cannot run Spring controllers. The annotations here are read, not run.
""")

# ====================================================================== j7-l3.2
def f_validate(owner, currency, opening):
    out = []
    if owner.strip() == "":
        out.append("owner: must not be blank")
    if not re.fullmatch(r"[A-Z]{3}", currency):
        out.append("currency: must be a 3-letter code")
    if opening < 0:
        out.append("openingCents: must not be negative")
    return out


VALIDATE_SOL = '''
List<String> validate(String owner, String currency, int openingCents) {
    List<String> problems = new ArrayList<>();
    if (owner.isBlank()) {
        problems.add("owner: must not be blank");
    }
    if (!currency.matches("[A-Z]{3}")) {
        problems.add("currency: must be a 3-letter code");
    }
    if (openingCents < 0) {
        problems.add("openingCents: must not be negative");
    }
    return problems;
}
'''
VALIDATE_STOPS = VALIDATE_SOL.replace('        problems.add("owner: must not be blank");', '        problems.add("owner: must not be blank");\n        return problems;')
VALIDATE_EMPTY_OWNER = VALIDATE_SOL.replace("owner.isBlank()", "owner.isEmpty()")
VALIDATE_LOWER = VALIDATE_SOL.replace('"[A-Z]{3}"', '"[A-Za-z]{3}"')
VALIDATE_ZERO = VALIDATE_SOL.replace("openingCents < 0", "openingCents <= 0")

ex32.method(
    "write", "j7-l3.2-write-validate", "Declared constraints, written by hand", ["o1"], ["J7.09"], ["IMPL"],
    "Bean Validation lets you declare constraints on a request object; here you write the checks by hand to see what they do. Write `validate(owner, currency, openingCents)` returning every violation, in this field order: `owner: must not be blank` (blank means empty or only spaces), `currency: must be a 3-letter code` (exactly three capital letters), `openingCents: must not be negative`. A valid request returns an empty list. Report all violations, not just the first.",
    [("validate", [("owner", "String"), ("currency", "String"), ("openingCents", "int")], "List<String>")], {"validate": f_validate},
    [("validate", ("Ada", "ZAR", 1000), "a valid request"), ("validate", ("", "ZAR", 1000), "no owner"), ("validate", ("Ada", "zar", -1), "two problems")],
    [("validate", ("   ", "ZAR", 0), "only spaces, zero is allowed"), ("validate", ("Ada", "ZA", 5), "too short"), ("validate", ("Ada", "ZARR", 5), "too long"),
     ("validate", ("Ada", "Z4R", 5), "a digit"), ("validate", ("", "", -5), "everything is wrong"), ("validate", ("Grace", "USD", 0), "zero opening is valid"),
     ("validate", ("Ada", "ZAR", -2147483648), "the smallest int")],
    starter='''
List<String> validate(String owner, String currency, int openingCents) {
    return List.of();
}
''', solution=VALIDATE_SOL,
    wrongs={"stops-at-first": VALIDATE_STOPS, "empty-but-not-blank": VALIDATE_EMPTY_OWNER, "lower-case-allowed": VALIDATE_LOWER, "zero-rejected": VALIDATE_ZERO},
    hints=["Check every field, and add a message for each failure.", "What is the difference between empty and blank?"],
    misconceptions=("MC174",), difficulty=2,
)


def f_to_status(name):
    return {
        "IllegalArgumentException": "400|Bad Request",
        "EmailTakenException": "409|Conflict",
        "MentorUnavailableException": "503|Service Unavailable",
        "AuthenticationException": "401|Unauthorized",
    }.get(name, "500|Internal Server Error")


STATUS_MAP_SOL = '''
String toStatus(String exception) {
    return switch (exception) {
        case "IllegalArgumentException" -> "400|Bad Request";
        case "EmailTakenException" -> "409|Conflict";
        case "MentorUnavailableException" -> "503|Service Unavailable";
        case "AuthenticationException" -> "401|Unauthorized";
        default -> "500|Internal Server Error";
    };
}
'''
STATUS_MAP_ALL_400 = STATUS_MAP_SOL.replace('case "EmailTakenException" -> "409|Conflict";', 'case "EmailTakenException" -> "400|Bad Request";')
STATUS_MAP_DEFAULT_400 = STATUS_MAP_SOL.replace('default -> "500|Internal Server Error";', 'default -> "400|Bad Request";')
STATUS_MAP_LEAK = STATUS_MAP_SOL.replace('default -> "500|Internal Server Error";', 'default -> "500|" + exception;')

ex32.method(
    "write", "j7-l3.2-write-errors", "Exceptions to statuses", ["o2"], ["J7.09"], ["IMPL", "DEBUG"],
    "This platform's `ApiErrors` class maps exceptions to responses with `@ExceptionHandler` methods. Write the same table as `toStatus(exception)`, taking a simple class name and returning `status|title`: `IllegalArgumentException` is `400|Bad Request`, `EmailTakenException` is `409|Conflict`, `MentorUnavailableException` is `503|Service Unavailable`, `AuthenticationException` is `401|Unauthorized`, and any other name is `500|Internal Server Error` (never the exception's name).",
    [("toStatus", [("exception", "String")], "String")], {"toStatus": f_to_status},
    [("toStatus", ("IllegalArgumentException",), "bad input"), ("toStatus", ("EmailTakenException",), "a conflict"), ("toStatus", ("NullPointerException",), "a bug")],
    [("toStatus", ("MentorUnavailableException",), "a dependency is down"), ("toStatus", ("AuthenticationException",), "login failed"), ("toStatus", ("SQLException",), "unexpected: no details"),
     ("toStatus", ("",), "empty"), ("toStatus", ("illegalargumentexception",), "names are exact"), ("toStatus", ("OutOfMemoryError",), "an error, not an exception")],
    starter='''
String toStatus(String exception) {
    return "";
}
''', solution=STATUS_MAP_SOL,
    wrongs={"conflict-as-400": STATUS_MAP_ALL_400, "default-as-client-error": STATUS_MAP_DEFAULT_400, "leaks-the-name": STATUS_MAP_LEAK},
    hints=["A conflict is not a malformed request.", "What should an unexpected exception tell the client?"],
    misconceptions=("MC174",), difficulty=2,
)

ADVICE_CODE = '''@RestControllerAdvice
class ApiErrors {

    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    Map<String, String> badRequest(IllegalArgumentException e) {
        return Map.of("error", e.getMessage());
    }

    @ExceptionHandler(AccountService.EmailTakenException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    Map<String, String> emailTaken(AccountService.EmailTakenException e) {
        return Map.of("error", e.getMessage());
    }
}'''
ex32.explain(
    "j7-l3.2-explain-advice", "Critique an error handler", ["o2"], ["J7.09"],
    "This is a shortened copy of the real error handler of this platform.\n\n" + fence(ADVICE_CODE, "java") + "\n\nExplain what `@RestControllerAdvice` and `@ExceptionHandler` do for the controllers. Then compare the response body with RFC 9457 problem details, and name one risk of putting `e.getMessage()` in the body.",
    "A @RestControllerAdvice class applies to all controllers, and each @ExceptionHandler method turns one exception type into a response, with @ResponseStatus setting the status, so controllers can just throw. The body here is {\"error\": message}, which is not the standard application/problem+json shape (type, title, status, detail). A risk of e.getMessage() is that an exception message written for developers can leak internal details, or be unhelpful to the client.",
    levels={
        2: ("The answer explains the advice and handlers, compares the body with RFC 9457 and names the message risk.", [
            "The advice class is shared by all controllers: when one throws IllegalArgumentException the handler turns it into a 400 with a body. The body is {\"error\": ...} rather than a problem detail with type, title, status and detail. Putting e.getMessage() in the body can leak internals or confuse the client, because the message was written for developers.",
            "@RestControllerAdvice makes the handlers apply everywhere and @ExceptionHandler picks the exception; @ResponseStatus sets 400 or 409. It is a custom error shape, not application/problem+json with the standard members. The risk is that messages from deeper code may expose implementation details."]),
        1: ("The answer explains the handlers without the comparison or the risk.", [
            "It maps exceptions to HTTP statuses for all controllers.",
            "When a controller throws an exception it returns a 400 or a 409."]),
        0: ("The answer misunderstands where the handler applies.", [
            "It only works for one controller method.",
            "The handler is called by the client to report errors."]),
    },
)

l7_l3_2 = Lesson("j7-l3.2", "Validation and error mapping", ["J7.09"], [
    ("o1", "Check a request object and report every violation, as declared constraints would"),
    ("o2", "Map exceptions to statuses in one place, without leaking internals"),
], ["j7-l3.1", "j7-l1.3"], 45, ["I92", "I91", "I85"], """## Before you start

You should know the status codes (lesson 7.1.3) and how a controller maps a request (lesson 7.3.1).

## Explanation

Request data is untrusted, so a controller must reject bad input with a 400 and a message the client can act on, rather than failing later with a 500. **Bean Validation** gives a common way to do this: you annotate properties of a request object with declarative constraints, and the runtime enforces them. There are built-in constraints, and you can write your own. In a controller you ask for the check with `@Valid` on the request body parameter. (Method validation on other beans relies on `@Validated` and AOP proxies.)

The exercise writes the same checks by hand so you can see exactly what a constraint does. Note that it reports **all** violations, not just the first, which is what makes an API pleasant to use.

**Error mapping** keeps controllers clean. Instead of building error responses in every method, controllers throw, and one class turns exceptions into responses: `@RestControllerAdvice` applies to all controllers, and each `@ExceptionHandler` method handles one exception type. The status should be truthful (lesson 7.1.3), the body useful to the client (RFC 9457 defines a standard shape), and an unexpected exception should become a generic 500 that does not reveal its name, message or stack.

## Worked examples

### Example 1: this platform's own error handler.

The real class maps `IllegalArgumentException` to 400, an email already taken to 409 and an unavailable mentor to 503. The exercise asks you to rebuild its table.

### Example 2: a request object with constraints (read only).

```java
record OpenAccount(@NotBlank String owner, @Pattern(regexp = "[A-Z]{3}") String currency, @Min(0) int openingCents) {}
```

## Where this is used

- Every API that accepts input. The same declarations also feed generated API documentation.

## Common mistakes

:::mistake{id=MC174}
**Treating validation as a few `if` statements in each controller.** Declared constraints are shared, tested once and reported consistently; scattered checks drift apart.
:::

## Practice

::exercise{id=j7-l3.2-write-validate}

::exercise{id=j7-l3.2-write-errors}

::exercise{id=j7-l3.2-explain-advice}

## Further reading

- **Spring Framework reference, Bean Validation** `[I92]`.
- **RFC 9457, Problem Details for HTTP APIs** `[I85]`.

## How you'll be assessed

- The **write** exercises check validation and error mapping (*implementation*).
- The **explain** exercise checks that you can critique a real handler (*explanation*).

The annotation example is shown for reading and has not been run on this platform.
""")

# ====================================================================== j7-l3.3
def f_page(items, page, size):
    if page < 0 or size < 1:
        return []
    return items[page * size:(page + 1) * size]


def f_pages(total, size):
    if size < 1 or total < 0:
        return 0
    return -(-total // size)


PAGE_SOL = '''
List<Integer> pageOf(List<Integer> items, int page, int size) {
    if (page < 0 || size < 1) {
        return List.of();
    }
    long from = (long) page * size;
    if (from >= items.size()) {
        return List.of();
    }
    return items.subList((int) from, (int) Math.min(items.size(), from + size));
}

int totalPages(int total, int size) {
    if (size < 1 || total < 0) {
        return 0;
    }
    return (total + size - 1) / size;
}
'''
PAGE_ONE_BASED = PAGE_SOL.replace("long from = (long) page * size;", "long from = (long) (page - 1) * size;").replace("page < 0", "page < 1")
PAGE_THROWS = PAGE_SOL.replace("    if (from >= items.size()) {\n        return List.of();\n    }\n", "")
PAGE_OVERFLOW = PAGE_SOL.replace("long from = (long) page * size;", "int from = page * size;").replace("(int) from", "from").replace("(int) Math.min(items.size(), from + size)", "Math.min(items.size(), from + size)")
PAGES_FLOOR = PAGE_SOL.replace("(total + size - 1) / size", "total / size")

ex33.method(
    "write", "j7-l3.3-write-page", "Pages of results", ["o1"], ["J7.10"], ["IMPL"],
    "A list endpoint returns one page at a time. Pages are numbered from 0. Write `pageOf(items, page, size)`: the items on that page, in order, or an empty list for a negative page, a size below 1, or a page past the end. Also write `totalPages(total, size)`: how many pages `total` items need, 0 for a size below 1 or a negative total.",
    [("pageOf", [("items", "List<Integer>"), ("page", "int"), ("size", "int")], "List<Integer>"), ("totalPages", [("total", "int"), ("size", "int")], "int")],
    {"pageOf": f_page, "totalPages": f_pages},
    [("pageOf", ([1, 2, 3, 4, 5, 6, 7], 0, 3), "first page"), ("pageOf", ([1, 2, 3, 4, 5, 6, 7], 2, 3), "a short last page"), ("totalPages", (7, 3), "pages for 7 items")],
    [("pageOf", ([1, 2, 3, 4, 5, 6], 1, 3), "an exact last page"), ("pageOf", ([1, 2, 3], 5, 3), "past the end"), ("pageOf", ([1, 2, 3], -1, 3), "negative page"),
     ("pageOf", ([1, 2, 3], 0, 0), "size zero"), ("pageOf", ([], 0, 10), "no items"), ("pageOf", ([1, 2, 3], 1, 2147483647), "a huge size"),
     ("pageOf", ([1, 2, 3], 2147483647, 2), "a huge page number"), ("totalPages", (6, 3), "an exact fit"), ("totalPages", (0, 5), "no items"),
     ("totalPages", (5, 0), "size zero"), ("totalPages", (1, 100), "one item")],
    starter='''
List<Integer> pageOf(List<Integer> items, int page, int size) {
    return List.of();
}

int totalPages(int total, int size) {
    return 0;
}
''', solution=PAGE_SOL,
    wrongs={"one-based": PAGE_ONE_BASED, "past-the-end-crashes": PAGE_THROWS, "int-overflow": PAGE_OVERFLOW, "pages-round-down": PAGES_FLOOR},
    hints=["Page 0 starts at item 0. Where does page `p` start?", "What happens to `page * size` for a very large page?"],
    misconceptions=("MC175",), difficulty=3,
)

ex33.explain(
    "j7-l3.3-explain-layers", "Where does each concern live", ["o2"], ["J7.10"],
    "A team has put request parsing, a SQL query and a balance rule all inside one controller method. Explain how you would split it into controller, service and repository, and say which layer should own the transaction, the validation of the request, the business rule and the SQL.",
    "The controller handles HTTP: it reads the request, triggers validation, calls the service and returns the result or lets an exception become a response. The service holds the business rule and defines the transaction boundary, so several repository calls commit or roll back together (as in Stage 6). The repository owns the SQL and nothing else. Each layer can then be tested separately and the SQL can change without touching the HTTP code.",
    levels={
        2: ("The answer assigns request handling, rule, transaction and SQL to the right layers, with a benefit.", [
            "The controller parses the request, validates it and calls the service. The service applies the balance rule and owns the transaction, so its repository calls commit together. The repository holds the SQL. This way each layer can be tested alone and the SQL can change without changing the HTTP code.",
            "Controller: HTTP in and out, plus validation of the body. Service: the business rule and the transaction around several repository calls. Repository: only queries. Then I can test the rule with a fake repository."]),
        1: ("The answer names the layers without assigning the concerns.", [
            "Split it into controller, service and repository.",
            "Put the SQL in a repository and keep the controller small."]),
        0: ("The answer keeps the concerns together.", [
            "One method is simpler, splitting only adds files.",
            "Put the SQL in the controller so it is close to the request."]),
    },
)

l7_l3_3 = Lesson("j7-l3.3", "Layers, persistence and pagination", ["J7.10"], [
    ("o1", "Return one page of a list, with correct edge cases"),
    ("o2", "Assign request handling, business rules, transactions and SQL to controller, service and repository"),
], ["j7-l3.2", "j6-l3.3"], 40, ["I91"], """## Before you start

You should know how a repository wraps SQL (Stage 6) and how a controller handles a request (lesson 7.3.1).

## Explanation

A Spring application is usually split in layers. The **controller** speaks HTTP. The **service** holds the business rules and is where a **transaction** starts and ends, so that several repository calls commit or roll back together (the same all-or-nothing idea as Stage 6). The **repository** owns the queries. A layer only talks to the one below it.

An endpoint that returns a list should not return the whole table. **Pagination** returns one page at a time. A page is described by a page number and a size; this course numbers pages from 0 (the first page is page 0), and says so in the API documentation, because other APIs choose 1. A request for a page past the end is not an error: it is simply an empty page. Compute positions with care: `page * size` can overflow an `int` for large values.

## Worked examples

### Example 1: one page.

For items `1..7` with size 3: page 0 is `1,2,3`, page 1 is `4,5,6`, page 2 is `7`, page 3 is empty, and there are 3 pages.

### Example 2: layers in this repository.

`CurriculumController` calls a content-access object rather than reading files itself, and `ApiErrors` turns exceptions into responses. Each class has one job.

## Where this is used

- Every list endpoint. Without a page size limit, one request can read the whole table.

## Common mistakes

:::mistake{id=MC175}
**Assuming pages start at 1, or that a page past the end is an error.** Agree the convention in the API documentation; a common choice for a page past the end is an empty list.
:::

## Practice

::exercise{id=j7-l3.3-write-page}

::exercise{id=j7-l3.3-explain-layers}

## Further reading

- **Spring Framework reference, annotated controllers** `[I91]`.

## How you'll be assessed

- The **write** exercise checks paging arithmetic (*implementation*).
- The **explain** exercise checks the division into layers (*explanation*).
""")
print("module 7.3 authored")
