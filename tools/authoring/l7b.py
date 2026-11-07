"""Stage 7 authoring: module 7.2 (Spring core). Learners write the wiring by hand; Spring itself cannot run in the runner."""
import re
import l7common
from l7common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex21 = Exercises("j7-l2.1")
ex22 = Exercises("j7-l2.2")
ex23 = Exercises("j7-l2.3")

REGISTER = {
    "j7-l2.1": ("The problem dependency injection solves", ["J7.05"]),
    "j7-l2.2": ("Beans, scopes and profiles", ["J7.06"]),
    "j7-l2.3": ("What auto-configuration does", ["J7.07"]),
}
MISCS = {
    "MC170": (["J7.05"], "I86", "A class should create its own collaborators with new, because that keeps the code simple and easy to test"),
    "MC171": (["J7.06"], "I87", "A Spring singleton bean is the same as the singleton design pattern, so it is safe to keep per-user state in its fields"),
    "MC172": (["J7.07"], "I89", "Auto-configuration is magic that cannot be changed; to customise anything you must edit the framework's configuration"),
}
register(REGISTER, MISCS)

# ====================================================================== j7-l2.1
WIRING_PROGRAM = '''
interface Notifier {
    String send(String message);
}

class EmailNotifier implements Notifier {
    public String send(String message) {
        return "email:" + message;
    }
}

class SmsNotifier implements Notifier {
    public String send(String message) {
        return "sms:" + message;
    }
}

class TransferService {
    private final Notifier notifier;

    TransferService(Notifier notifier) {
        this.notifier = notifier;
    }

    String transfer(int cents) {
        return notifier.send("moved " + cents);
    }
}

class FixedService {
    private final Notifier notifier = new EmailNotifier();

    String transfer(int cents) {
        return notifier.send("moved " + cents);
    }
}

void main() {
    System.out.println(new TransferService(new EmailNotifier()).transfer(500));
    System.out.println(new TransferService(new SmsNotifier()).transfer(500));
    System.out.println(new FixedService().transfer(500));
    List<String> sent = new ArrayList<>();
    TransferService tested = new TransferService(m -> {
        sent.add(m);
        return "recorded";
    });
    System.out.println(tested.transfer(75) + " " + sent);
}
'''
# Derived by hand from the program: constructor injection picks the notifier, FixedService always uses email,
# and the lambda is a test double that records the message instead of sending it.
ex21.predict(
    "j7-l2.1-predict-wiring", "Who chooses the dependency", ["o1"], ["J7.05"],
    "The program wires objects by hand. One service receives its notifier through the constructor, one creates its own. Predict the exact output.",
    WIRING_PROGRAM, "email:moved 500\nsms:moved 500\nemail:moved 500\nrecorded [moved 75]\n",
    ["Which service lets the caller choose what it talks to?", "What does the lambda let a test do that FixedService does not?"],
    misconceptions=("MC170",), difficulty=1,
)


def f_order(edges, target):
    deps = {}
    for e in edges:
        a, b = e.split(">")
        deps.setdefault(a, []).append(b)
    state, out = {}, []

    def visit(n):
        if state.get(n) == 1:
            raise ValueError("cycle")
        if state.get(n) == 2:
            return
        state[n] = 1
        for d in sorted(deps.get(n, [])):
            visit(d)
        state[n] = 2
        out.append(n)

    try:
        visit(target)
    except ValueError:
        return ["cycle"]
    return out


ORDER_SOL = '''
List<String> creationOrder(List<String> edges, String target) {
    Map<String, List<String>> deps = new HashMap<>();
    for (String edge : edges) {
        String[] parts = edge.split(">");
        deps.computeIfAbsent(parts[0], k -> new ArrayList<>()).add(parts[1]);
    }
    List<String> order = new ArrayList<>();
    if (!visit(target, deps, new HashSet<>(), new HashSet<>(), order)) {
        return List.of("cycle");
    }
    return order;
}

boolean visit(String bean, Map<String, List<String>> deps, Set<String> visiting, Set<String> done, List<String> order) {
    if (done.contains(bean)) {
        return true;
    }
    if (!visiting.add(bean)) {
        return false;
    }
    List<String> wanted = new ArrayList<>(deps.getOrDefault(bean, List.of()));
    Collections.sort(wanted);
    for (String dependency : wanted) {
        if (!visit(dependency, deps, visiting, done, order)) {
            return false;
        }
    }
    visiting.remove(bean);
    done.add(bean);
    order.add(bean);
    return true;
}
'''
ORDER_NO_DEDUPE = ORDER_SOL.replace("    if (done.contains(bean)) {\n        return true;\n    }\n", "")
ORDER_UNSORTED = ORDER_SOL.replace("    Collections.sort(wanted);\n", "")
ORDER_DEP_LAST = ORDER_SOL.replace("    List<String> wanted", "    order.add(bean);\n    List<String> wanted").replace("    visiting.remove(bean);\n    done.add(bean);\n    order.add(bean);\n", "    visiting.remove(bean);\n    done.add(bean);\n")
ORDER_NO_CYCLE = ORDER_SOL.replace("    if (!visiting.add(bean)) {\n        return false;\n    }\n", "    visiting.add(bean);\n").replace("    visiting.remove(bean);\n    done.add(bean);", "    done.add(bean);")

ex21.method(
    "write", "j7-l2.1-write-order", "In what order are beans created", ["o2"], ["J7.05"], ["IMPL"],
    "A container must create a bean's dependencies before the bean itself. An edge `A>B` means A depends on B. Write `creationOrder(edges, target)`: the beans to create so that `target` can be built, dependencies first, each bean once, and the dependencies of one bean taken in alphabetical order. If the target's dependencies contain a cycle, return the single element `cycle`.",
    [("creationOrder", [("edges", "List<String>"), ("target", "String")], "List<String>")], {"creationOrder": f_order},
    [("creationOrder", (["controller>service", "service>repository"], "controller"), "a chain"),
     ("creationOrder", (["a>b", "a>c", "b>d", "c>d"], "a"), "a shared dependency is created once"),
     ("creationOrder", (["a>b", "b>a"], "a"), "a cycle")],
    [("creationOrder", ([], "x"), "no dependencies"),
     ("creationOrder", (["app>zeta", "app>alpha"], "app"), "alphabetical order"),
     ("creationOrder", (["x>y", "y>x", "a>b"], "a"), "a cycle that the target does not reach"),
     ("creationOrder", (["a>a"], "a"), "a bean that needs itself"),
     ("creationOrder", (["service>repository", "controller>service"], "repository"), "the leaf only"),
     ("creationOrder", (["a>b", "b>c", "c>b"], "a"), "a cycle below the target"),
     ("creationOrder", (["a>c", "a>b", "c>d", "b>d"], "a"), "diamond, alphabetical")],
    starter='''
List<String> creationOrder(List<String> edges, String target) {
    return List.of();
}
''', solution=ORDER_SOL,
    wrongs={"creates-twice": ORDER_NO_DEDUPE, "unsorted": ORDER_UNSORTED, "dependent-first": ORDER_DEP_LAST, "ignores-cycles": ORDER_NO_CYCLE},
    hints=["Visit each dependency before you add the bean to the result.", "How do you notice that you are already in the middle of creating a bean?"],
    misconceptions=("MC170",), difficulty=4,
)

ex21.explain(
    "j7-l2.1-explain-injection", "Constructor or setter", ["o1", "o2"], ["J7.05"],
    "A teammate writes `TransferService` with a no-argument constructor and a `setNotifier` method, and forgets to call it in one place. Explain what goes wrong, which style Spring's documentation prefers for mandatory dependencies, and what constructor injection makes impossible.",
    "Dependency injection means an object states its dependencies (constructor arguments, factory-method arguments or properties) and the container supplies them. The reference advises constructors for mandatory dependencies and setters for optional ones. With a setter, an object can exist without its notifier and fail later with a NullPointerException; with a constructor, the object cannot be built without it, and the field can be final.",
    levels={
        2: ("The answer describes the failure, names the preferred style and what the constructor guarantees.", [
            "If nobody calls setNotifier, the service exists but its notifier is null and it fails later with a NullPointerException. Spring's documentation recommends constructors for mandatory dependencies and setters for optional ones. With constructor injection the object cannot be created without its notifier, and the field can be final.",
            "The service is half built: it compiles but breaks at runtime when it uses the missing dependency. Use constructor injection for required collaborators, as the Spring reference suggests. Then the dependency is always present and the class is easy to test by passing a fake."]),
        1: ("The answer prefers constructors without saying what goes wrong.", [
            "Constructor injection is better.",
            "Use the constructor because Spring recommends it."]),
        0: ("The answer sees no difference or prefers creating collaborators inside the class.", [
            "Both work the same, it is only style.",
            "The service should just call new EmailNotifier() itself, then nothing can be forgotten."]),
    },
)

l7_l2_1 = Lesson("j7-l2.1", "The problem dependency injection solves", ["J7.05"], [
    ("o1", "Explain what dependency injection is and what a class that creates its own collaborators gives up"),
    ("o2", "Work out the order in which a container must create beans"),
], ["j6-l3.2"], 45, ["I86", "I88"], """## Before you start

You should know interfaces and constructors from Stage 2, and how a repository separated SQL from the rest in Stage 6.

## Explanation

A class that writes `new EmailNotifier()` inside itself has chosen its collaborator for ever. You cannot give it an SMS notifier, and you cannot give a test a fake without editing the class.

**Dependency injection** (DI) turns that around. The Spring reference defines it as a specialised form of **inversion of control** (IoC): an object defines its dependencies only through constructor arguments, factory-method arguments or properties set after construction, and the **container** injects them when it creates the object. Something else decides which implementation to supply.

You can do all of this by hand, as the exercise program does. A container is the same wiring, done for you: it works out which objects depend on which, creates the dependencies first, and passes them in. A cycle (A needs B, B needs A) has no valid creation order and fails.

The reference's rule of thumb: constructors for mandatory dependencies, setters or configuration methods for optional ones. Constructor injection also means the object is never half built.

## Worked examples

### Example 1: wiring by hand.

```java
Notifier notifier = new EmailNotifier();
TransferService service = new TransferService(notifier);
```

### Example 2: a test double.

```java
TransferService tested = new TransferService(m -> "recorded");
```

No framework, no container: DI is a design, and a framework automates it.

## Where this is used

- Every Spring application. The container reads which classes exist and which constructors they have, and builds the graph you just ordered by hand.

## Common mistakes

:::mistake{id=MC170}
**Creating collaborators with `new` inside the class.** It fixes the implementation, so the class cannot be reconfigured or tested with a fake.
:::

## Practice

::exercise{id=j7-l2.1-predict-wiring}

::exercise{id=j7-l2.1-write-order}

::exercise{id=j7-l2.1-explain-injection}

## Further reading

- **Spring Framework reference, the IoC container** `[I86]`.
- **Spring Framework reference, dependency injection** `[I88]`.

## How you'll be assessed

- The **predict** exercise checks that you can see who chooses a dependency (*identifying*).
- The **write** exercise checks that you can order a dependency graph (*implementation*).
- The **explain** exercise checks the case for constructor injection (*explanation*).

No Spring code runs in these exercises. The code is plain Java that models what the container does.
""")

# ====================================================================== j7-l2.2
SCOPE_PROGRAM = '''
class Counter {
    static int created = 0;
    final int id;

    Counter() {
        id = ++created;
    }
}

class Container {
    private final Map<String, Counter> singletons = new HashMap<>();

    Counter singleton(String name) {
        return singletons.computeIfAbsent(name, n -> new Counter());
    }

    Counter prototype(String name) {
        return new Counter();
    }
}

void main() {
    Container container = new Container();
    Counter a = container.singleton("ledger");
    Counter b = container.singleton("ledger");
    Counter p = container.prototype("ledger");
    Counter q = container.prototype("ledger");
    System.out.println("same singleton=" + (a == b));
    System.out.println("same prototype=" + (p == q));
    System.out.println("created=" + Counter.created);
    System.out.println("ids=" + a.id + "," + b.id + "," + p.id + "," + q.id);
}
'''
# Derived by hand: the singleton is built once (id 1) and returned twice; each prototype call builds a new one (ids 2 and 3).
ex22.predict(
    "j7-l2.2-predict-scopes", "One instance or many", ["o1"], ["J7.06"],
    "A hand-written container hands out a bean either as a singleton (one per name) or as a prototype (a new one every time). Predict the exact output.",
    SCOPE_PROGRAM, "same singleton=true\nsame prototype=false\ncreated=3\nids=1,1,2,3\n",
    ["How many objects does the singleton call create, however often it is asked?", "What does the static counter record?"],
    misconceptions=("MC171",), difficulty=1,
)


def f_profile(expr, active):
    act = set(active) if active else {"default"}
    has_and, has_or = " & " in expr, " | " in expr
    if has_and and has_or:
        return "invalid"
    terms = re.split(r" & | \| ", expr)

    def term(t):
        if t.startswith("!"):
            return t[1:] not in act
        return t in act

    res = [term(t) for t in terms]
    return "true" if (all(res) if not has_or else any(res)) else "false"


PROFILE_SOL = '''
String isActive(String expression, List<String> active) {
    Set<String> profiles = active.isEmpty() ? Set.of("default") : new HashSet<>(active);
    boolean and = expression.contains(" & ");
    boolean or = expression.contains(" | ");
    if (and && or) {
        return "invalid";
    }
    boolean result = and || !or;
    for (String term : expression.split(" & | \\\\| ")) {
        boolean matches = term.startsWith("!") ? !profiles.contains(term.substring(1)) : profiles.contains(term);
        result = or ? result || matches : result && matches;
    }
    return result ? "true" : "false";
}
'''
PROFILE_NO_DEFAULT = PROFILE_SOL.replace('active.isEmpty() ? Set.of("default") : new HashSet<>(active)', "new HashSet<>(active)")
PROFILE_NO_NOT = PROFILE_SOL.replace('term.startsWith("!") ? !profiles.contains(term.substring(1)) : profiles.contains(term)', "profiles.contains(term)")
PROFILE_ALWAYS_AND = PROFILE_SOL.replace("boolean result = and || !or;", "boolean result = true;").replace("result = or ? result || matches : result && matches;", "result = result && matches;")
PROFILE_MIXED = PROFILE_SOL.replace("    if (and && or) {\n        return \"invalid\";\n    }\n", "")

ex22.method(
    "write", "j7-l2.2-write-profile", "Is this bean active", ["o2"], ["J7.06"], ["IMPL"],
    "A bean is registered only when its profile expression is true. Write `isActive(expression, active)`. A term is a profile name or `!name` (not active). Terms are joined by ` & ` (all must hold) or by ` | ` (any may hold), never both: mixing them without parentheses is `invalid`. With no profile active, the profile `default` counts as the only active profile. Return `true`, `false` or `invalid`.",
    [("isActive", [("expression", "String"), ("active", "List<String>")], "String")], {"isActive": f_profile},
    [("isActive", ("production", ["production"]), "a plain name that is active"), ("isActive", ("production", ["dev"]), "a name that is not active"), ("isActive", ("!production", ["dev"]), "not")],
    [("isActive", ("default", []), "the default profile with nothing active"), ("isActive", ("production & us-east", ["production", "us-east"]), "and, both active"),
     ("isActive", ("production & us-east", ["production"]), "and, one missing"), ("isActive", ("dev | test", ["test"]), "or"),
     ("isActive", ("dev | test", ["prod"]), "or, neither"), ("isActive", ("a & b | c", ["a"]), "mixing is invalid"),
     ("isActive", ("!default", []), "not default"), ("isActive", ("!dev & !test", ["prod"]), "two nots"),
     ("isActive", ("production", []), "nothing active")],
    starter='''
String isActive(String expression, List<String> active) {
    return "";
}
''', solution=PROFILE_SOL,
    wrongs={"no-default-profile": PROFILE_NO_DEFAULT, "no-negation": PROFILE_NO_NOT, "or-treated-as-and": PROFILE_ALWAYS_AND, "accepts-mixing": PROFILE_MIXED},
    hints=["What is the set of active profiles when the list is empty?", "Decide `and` or `or` once, then combine the terms."],
    misconceptions=("MC171",), difficulty=3,
)

ex22.explain(
    "j7-l2.2-explain-singleton", "State in a singleton", ["o1"], ["J7.06"],
    "A developer adds a field `private User currentUser;` to a `@Service` class and sets it at the start of each request. In testing it works. In production, users sometimes see each other's data. Explain why, using what you know about the default bean scope.",
    "The default scope is singleton: the container creates one instance of the bean and shares it, so every request that uses the service uses the same object and the same field. Concurrent requests overwrite currentUser and read each other's value. A singleton bean should hold no per-request state; pass the user as a method argument or use a request-scoped bean.",
    levels={
        2: ("The answer uses the singleton default, shows the shared field is overwritten, and gives a fix.", [
            "Spring beans are singletons by default, so all requests share one service object and one currentUser field. Two requests at the same time overwrite each other. Keep per-request data in method arguments or locals, or use a request-scoped bean.",
            "The service is created once for the whole container, so the field is shared across all users. Under load one request sets the field and another reads it. The fix is to pass the user in as a parameter instead of storing it."]),
        1: ("The answer says the bean is shared without explaining the overwrite or the fix.", [
            "The service is a singleton so the field is shared.",
            "There is only one instance of the class."]),
        0: ("The answer blames something else.", [
            "The database is returning the wrong user.",
            "Each request gets its own copy of the service, so this cannot happen."]),
    },
)

l7_l2_2 = Lesson("j7-l2.2", "Beans, scopes and profiles", ["J7.06"], [
    ("o1", "Explain the default bean scope and why singleton beans must not hold per-request state"),
    ("o2", "Decide whether a bean is registered, given a profile expression and the active profiles"),
], ["j7-l2.1"], 40, ["I87", "I94", "I90"], """## Before you start

You should know what dependency injection is and what a container does.

## Explanation

A **bean** is an object whose creation and wiring the container manages. Its **scope** decides how many instances exist. The **singleton** scope is the default: one shared instance per container for that bean definition. Spring's singleton is not the Gang of Four singleton pattern: it is one instance per container, not one per class loader. A **prototype** bean is created anew every time it is requested.

Because a singleton is shared, it must not keep per-user or per-request state in its fields. Concurrent requests would overwrite each other.

**Profiles** switch beans on and off per environment. `@Profile` makes a component eligible for registration when the given profiles are active. A profile string can be a name or an expression using `!` (not), `&` (and) and `|` (or); `&` and `|` cannot be mixed without parentheses. When no profile is active, the `default` profile is enabled. In Spring Boot you choose the active profiles with the `spring.profiles.active` property.

## Worked examples

### Example 1: a profile-specific bean.

```java
@Configuration(proxyBeanMethods = false)
@Profile("production")
public class ProductionConfiguration {
    // beans that exist only when the production profile is active
}
```

### Example 2: choosing the profile.

```properties
spring.profiles.active=dev,hsqldb
```

## Where this is used

- Different databases for development and production, a fake payment gateway in tests, extra logging on a staging environment.

## Common mistakes

:::mistake{id=MC171}
**Keeping per-user data in a singleton's fields.** The default scope is shared by every request. Pass data as arguments.
:::

## Practice

::exercise{id=j7-l2.2-predict-scopes}

::exercise{id=j7-l2.2-write-profile}

::exercise{id=j7-l2.2-explain-singleton}

## Further reading

- **Spring Framework reference, bean scopes** `[I87]`.
- **Spring Framework reference, environment abstraction** `[I94]`.
- **Spring Boot reference, profiles** `[I90]`.

## How you'll be assessed

- The **predict** exercise checks that you can follow instance creation (*identifying*).
- The **write** exercise checks profile expressions (*implementation*).
- The **explain** exercise checks the singleton default (*explanation*).

The annotations above are shown for reading and were not run on this platform.
""")

# ====================================================================== j7-l2.3
RULES = [("jdbc", "DataSource"), ("webmvc", "DispatcherServlet"), ("jackson", "ObjectMapper")]


def f_auto(classpath, user_beans):
    return sorted(bean for jar, bean in RULES if jar in classpath and bean not in user_beans)


AUTO_SOL = '''
List<String> autoConfigure(List<String> classpath, List<String> userBeans) {
    String[][] rules = {{"webmvc", "DispatcherServlet"}, {"jackson", "ObjectMapper"}, {"jdbc", "DataSource"}};
    List<String> created = new ArrayList<>();
    for (String[] rule : rules) {
        if (classpath.contains(rule[0]) && !userBeans.contains(rule[1])) {
            created.add(rule[1]);
        }
    }
    Collections.sort(created);
    return created;
}
'''
AUTO_NO_BACKOFF = AUTO_SOL.replace(" && !userBeans.contains(rule[1])", "")
AUTO_ALWAYS = AUTO_SOL.replace("classpath.contains(rule[0]) && ", "")
AUTO_UNSORTED = AUTO_SOL.replace("    Collections.sort(created);\n", "")
AUTO_RETURNS_USER = AUTO_SOL.replace("    Collections.sort(created);\n    return created;", "    created.addAll(userBeans);\n    Collections.sort(created);\n    return created;")

ex23.method(
    "write", "j7-l2.3-write-autoconfig", "A model of auto-configuration", ["o1"], ["J7.07"], ["IMPL"],
    "This is a model, not Spring's real rule set. Auto-configuration adds a bean when its library is on the classpath **and** you have not defined that bean yourself (it backs off). The rules are: `jdbc` gives `DataSource`, `webmvc` gives `DispatcherServlet`, `jackson` gives `ObjectMapper`. Write `autoConfigure(classpath, userBeans)`, the beans the framework adds, in alphabetical order.",
    [("autoConfigure", [("classpath", "List<String>"), ("userBeans", "List<String>")], "List<String>")], {"autoConfigure": f_auto},
    [("autoConfigure", (["jdbc", "webmvc"], []), "two libraries, no beans of your own"), ("autoConfigure", (["jdbc"], ["DataSource"]), "you defined it: backs off"), ("autoConfigure", ([], []), "an empty classpath")],
    [("autoConfigure", (["jackson", "jdbc", "webmvc"], []), "all three"), ("autoConfigure", (["jackson", "jdbc", "webmvc"], ["ObjectMapper"]), "one backs off"),
     ("autoConfigure", (["webmvc"], ["DataSource"]), "your bean is for another library"), ("autoConfigure", (["jackson"], ["ObjectMapper", "DataSource"]), "everything backs off"),
     ("autoConfigure", (["h2"], []), "an unrelated library"), ("autoConfigure", (["webmvc", "jdbc"], ["DispatcherServlet", "DataSource"]), "two back off")],
    starter='''
List<String> autoConfigure(List<String> classpath, List<String> userBeans) {
    return List.of();
}
''', solution=AUTO_SOL,
    wrongs={"never-backs-off": AUTO_NO_BACKOFF, "ignores-classpath": AUTO_ALWAYS, "unsorted": AUTO_UNSORTED, "returns-your-beans": AUTO_RETURNS_USER},
    hints=["Two conditions must both hold for a bean to be added.", "Does the framework return beans you defined yourself?"],
    misconceptions=("MC172",), difficulty=2,
)

ex23.explain(
    "j7-l2.3-explain-startup", "Reading what the framework did", ["o1", "o2"], ["J7.07"],
    "This is an excerpt of the real startup log of this platform's own backend (a Spring Boot application). Say what it tells you the framework did for you without being asked, how you would find out *why* a particular bean exists, and how you would replace one of the beans it created.\n\n" + fence(cap("cap_startup.txt")),
    "The log shows the application context starting, the embedded web server being started on a port, and the active profile. Auto-configuration added these because the libraries are on the classpath. To see which auto-configuration applied and why, start with --debug and read the conditions report. To replace a bean, define your own bean of that type; auto-configuration is non-invasive and backs away.",
    levels={
        2: ("The answer reads the log, names the --debug conditions report, and says defining your own bean replaces the default.", [
            "It started the Spring context and an embedded web server on a port, which it did because the web libraries are on the classpath. Running with --debug prints a conditions report of what matched and why. To replace a bean I define my own of that type and the default backs away.",
            "The framework configured the server and the application without me writing that code: the dependencies on the classpath triggered it. The --debug switch logs a conditions report explaining each decision. Auto-configuration is non-invasive, so my own DataSource bean, for example, replaces the default one."]),
        1: ("The answer reads the log but does not say how to investigate or customise.", [
            "It started a web server and the application.",
            "The log shows the framework starting up with some configuration."]),
        0: ("The answer treats startup as fixed and unchangeable.", [
            "It is Spring's own code, so you cannot change what it does.",
            "The log is just noise and cannot tell you anything."]),
    },
)

l7_l2_3 = Lesson("j7-l2.3", "What auto-configuration does", ["J7.07"], [
    ("o1", "Say when auto-configuration adds a bean and when it backs off"),
    ("o2", "Read a real startup log and find out what the framework configured, and why"),
], ["j7-l2.2"], 40, ["I89", "I93"], """## Before you start

You should know what a bean, a scope and a profile are.

## Explanation

Spring Boot **auto-configuration** configures an application from the jars on its classpath. The reference gives an example: if an in-memory database such as HSQLDB is on the classpath and you have defined no database connection beans, Boot configures an in-memory database for you. It is opt-in, through `@EnableAutoConfiguration` or `@SpringBootApplication` on one of your configuration classes.

It is **non-invasive**. At any point you can define your own configuration to replace part of it: if you add your own `DataSource` bean, the default embedded database support backs away. If you need to know what is being applied, and why, start the application with `--debug`, which logs a **conditions report**. If a class you do not want is applied, you can exclude it with the `exclude` attribute of `@SpringBootApplication`.

So there is no magic to guess at: the rule is "library on the classpath, and you have not defined the bean".

## Worked examples

### Example 1: this platform's own startup.

This is real output from this platform's backend, captured by starting it:

""" + fence(cap("cap_startup.txt")) + """

### Example 2: replacing a default.

```java
@Bean
DataSource dataSource() {
    // your own: the auto-configured one backs away
}
```

## Where this is used

- Every Boot application. When something is configured that you did not write, or is missing that you expected, the classpath and the conditions report are where to look.

## Common mistakes

:::mistake{id=MC172}
**Treating auto-configuration as fixed.** It is a default. Defining your own bean, setting a property, or excluding a class changes it.
:::

## Practice

::exercise{id=j7-l2.3-write-autoconfig}

::exercise{id=j7-l2.3-explain-startup}

## Further reading

- **Spring Boot reference, auto-configuration** `[I89]`.

## How you'll be assessed

- The **write** exercise checks the rule "classpath and no user bean" (*implementation*).
- The **explain** exercise checks that you can read startup output (*explanation*).

The code in the write exercise is a model with three invented rules, not Spring's real rule set.
""")
print("module 7.2 authored")
