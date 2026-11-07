"""Stage 11 authoring: module 11.1 (Docker). Docker output was captured on this machine on 2026-11-07; exercises are plain-Java models."""
import re
import l11common
from l11common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex11 = Exercises("j11-l1.1")
ex12 = Exercises("j11-l1.2")
ex13 = Exercises("j11-l1.3")
ex14 = Exercises("j11-l1.4")

REGISTER = {
    "j11-l1.1": ("Containers, images and layer caching", ["J11.01"]),
    "j11-l1.2": ("Multi-stage builds", ["J11.02"]),
    "j11-l1.3": ("Compose, configuration and secrets", ["J11.03"]),
    "j11-l1.4": ("The JVM in containers", ["J11.04"]),
}
MISCS = {
    "MC205": (["J11.01"], "I126", "A container is a small virtual machine with its own operating system kernel"),
    "MC206": (["J11.02"], "I126", "A smaller image only matters for download speed; what the build leaves in the final image is not a concern"),
    "MC207": (["J11.03"], "I137", "Putting the database password into the image or the Compose file in the repository is fine because it is only for development"),
    "MC208": (["J11.04"], "I129", "Setting a container memory limit makes the JVM size its heap to that limit; an out-of-memory exit always means the heap is too small"),
}
register(REGISTER, MISCS)

HELLO_SINGLE = open(l11common.SCRATCH + "/dock/hello/Dockerfile.single").read().rstrip("\n")
HELLO_MULTI = open(l11common.SCRATCH + "/dock/hello/Dockerfile.multi").read().rstrip("\n")
APP_DOCKERFILE = open(l11common.SCRATCH + "/dock/app/Dockerfile").read().rstrip("\n")
APP_COMPOSE = open(l11common.SCRATCH + "/dock/app/compose.yaml").read().rstrip("\n")

# ====================================================================== j11-l1.1
def f_cached(before, after):
    n = 0
    for a, b in zip(before, after):
        if a != b:
            break
        n += 1
    return n


CACHE_SOL = '''
int cachedLayers(List<String> before, List<String> after) {
    int cached = 0;
    while (cached < before.size() && cached < after.size() && before.get(cached).equals(after.get(cached))) {
        cached++;
    }
    return cached;
}
'''
CACHE_ANYWHERE = '''
int cachedLayers(List<String> before, List<String> after) {
    int cached = 0;
    for (String line : after) {
        if (before.contains(line)) {
            cached++;
        }
    }
    return cached;
}
'''
CACHE_ALL_OR_NOTHING = CACHE_SOL.replace("    return cached;", "    return cached == after.size() ? cached : 0;")
CACHE_ONE_MORE = CACHE_SOL.replace("    return cached;", "    return Math.min(after.size(), cached + 1);")
CACHE_BEFORE_LEN = CACHE_SOL.replace("cached < after.size() && ", "")
SLOW = ["FROM eclipse-temurin:25-jre-alpine", "WORKDIR /app", "COPY app.jar@v1 app.jar", "COPY content@v1 /content", "ENTRYPOINT java -jar app.jar"]

ex11.method(
    "write", "j11-l1.1-write-cache", "How many layers can Docker reuse", ["o1"], ["J11.01"], ["IMPL"],
    "Docker builds an image layer by layer and can reuse a layer from its cache only if its instruction is unchanged **and every earlier layer was reused**. A `COPY` instruction is written here with a version of its files after an `@` (for example `COPY app.jar@v2 app.jar`), so a change in the files changes the instruction. Write `cachedLayers(before, after)`: the number of leading instructions of `after` that can come from the cache of the `before` build.",
    [("cachedLayers", [("before", "List<String>"), ("after", "List<String>")], "int")], {"cachedLayers": f_cached},
    [("cachedLayers", (SLOW, [SLOW[0], SLOW[1], "COPY app.jar@v2 app.jar", SLOW[3], SLOW[4]]), "the application changed"), ("cachedLayers", (SLOW, SLOW), "nothing changed"), ("cachedLayers", (SLOW, ["FROM eclipse-temurin:26-jre-alpine"] + SLOW[1:]), "the base image changed")],
    [("cachedLayers", (SLOW, [SLOW[0], SLOW[1], SLOW[3], "COPY app.jar@v1 app.jar", SLOW[4]]), "the same lines in another order"), ("cachedLayers", (SLOW, SLOW + ["EXPOSE 8080"]), "a line added at the end"), ("cachedLayers", (SLOW + ["EXPOSE 8080"], SLOW), "a line removed from the end"),
     ("cachedLayers", ([], SLOW), "no earlier build"), ("cachedLayers", (SLOW, []), "an empty new file"), ("cachedLayers", (SLOW, [SLOW[0], "WORKDIR /srv"] + SLOW[2:]), "a change in the second line breaks all that follow")],
    starter='''
int cachedLayers(List<String> before, List<String> after) {
    return 0;
}
''', solution=CACHE_SOL,
    wrongs={"matches-anywhere": CACHE_ANYWHERE, "all-or-nothing": CACHE_ALL_OR_NOTHING, "one-too-many": CACHE_ONE_MORE, "runs-past-the-new-file": CACHE_BEFORE_LEN},
    hints=["Stop at the first instruction that differs.", "Do not count a later identical line once an earlier one changed."],
    misconceptions=("MC205",), difficulty=2,
)

ex11.explain(
    "j11-l1.1-explain-dockerfile", "Reading a Dockerfile and its history", ["o2"], ["J11.01"],
    "This is a Dockerfile for a tiny Java program and what Docker reported about the image it built, on this machine.\n\n" + fence(HELLO_SINGLE, "dockerfile") + "\n\n" + fence(cap("cap_docker_images.txt")) + "\n\nExplain: what each instruction in the Dockerfile does; what a *layer* is and what the `docker history` output shows about them; why, in the Compose file's Dockerfile you will meet next, `COPY app.jar` comes before `COPY content` and both come after the base image; and how a container differs from a virtual machine.",
    "FROM chooses the base image, WORKDIR sets the working directory, COPY adds files from the build context, RUN executes a command at build time (here javac), CMD says what runs when a container starts. Each instruction that changes the file system produces a layer, an immutable slice of the image; docker history lists the layers with their sizes (the Java runtime layers are tens or hundreds of megabytes, our own copy is a few kilobytes). Layers are cached, so instructions that change rarely should come first and ones that change often last, so a code change rebuilds only the last layers. A container is a process (or group of processes) isolated from others on the host, sharing the host's operating system kernel and starting from an image; a virtual machine runs a whole guest kernel on emulated hardware, so it is heavier and slower to start.",
    levels={
        2: ("The answer explains the instructions, layers and the history output, the ordering for the cache, and containers versus VMs.", [
            "FROM picks the base, WORKDIR sets the directory, COPY brings in files, RUN runs javac at build time and CMD is what the container runs. Each file-changing instruction makes a layer; docker history shows them, with the JDK layers large and our COPY a few KB. Docker caches layers, so put what changes rarely (base image, dependencies) first and the application last so a code change rebuilds little. A container shares the host kernel and is just isolated processes; a VM boots its own kernel on virtual hardware.",
            "The Dockerfile starts from the JDK image, copies Hello.java, compiles it and sets the start command. The history lists layers by size. Order matters for caching: stable layers first. Containers share the host kernel, VMs do not."]),
        1: ("The answer explains the instructions but not caching or the VM comparison.", [
            "FROM is the base image and RUN compiles the code.",
            "A container is like a lightweight VM."]),
        0: ("The answer treats a container as a virtual machine.", [
            "A container is a small virtual machine with its own operating system.",
            "The order of instructions does not matter."]),
    },
)

l11_l1_1 = Lesson("j11-l1.1", "Containers, images and layer caching", ["J11.01"], [
    ("o1", "Work out how much of a build Docker can reuse from its cache"),
    ("o2", "Read a Dockerfile and an image history, and explain containers against virtual machines"),
], ["j7-l3.3"], 40, ["I126", "I128"], """## Before you start

You should know how a Java program is compiled and run from the command line (Stages 0 and 4) and what a process is.

## Explanation

An **image** is a read-only package of a file system and the information to start a program from it. A **container** is a running instance of an image: a process (or a few) isolated from the others on the host, started from the image. Unlike a **virtual machine**, a container does not boot its own operating system kernel; it shares the host's, which is why it starts in a fraction of a second and costs little.

An image is built from a **Dockerfile**: a list of instructions. The ones you need first:

- `FROM` chooses the base image the build starts from.
- `WORKDIR` sets the working directory for the instructions that follow.
- `COPY` adds files from the build context (the directory you build from).
- `RUN` runs a command at **build** time, and its result becomes part of the image.
- `CMD` or `ENTRYPOINT` says what runs when a **container** starts.

Every instruction that changes the file system produces a **layer**. Docker caches layers: an instruction can be reused if it is unchanged and every layer before it was reused. So order the Dockerfile from the things that change least (the base, the dependencies) to the things that change most (your code). Change one early line and everything after it is rebuilt.

## Worked examples

### Example 1: a real build.

The exercise shows the Dockerfile of a small Java program, and the output of `docker images` and `docker history` for the image built from it on this machine. The layers of the Java runtime are large; the layer holding our own class file is 12 kilobytes.

### Example 2: this platform's own Dockerfile.

""" + fence(APP_DOCKERFILE, "dockerfile") + """

The next lesson builds the platform into an image like this one and runs it.

## Where this is used

- Every modern deployment. A container image is the unit that is built once, tested, and run the same way on a laptop and on a server.

## Common mistakes

:::mistake{id=MC205}
**Thinking a container is a small virtual machine.** It is an isolated process sharing the host's kernel. That is why it is light, and also why it is not a security boundary as strong as a VM.
:::

## Practice

::exercise{id=j11-l1.1-write-cache}

::exercise{id=j11-l1.1-explain-dockerfile}

## Further reading

- **Docker documentation, resource constraints** `[I128]`, on how containers are limited.
- **Docker documentation, multi-stage builds** `[I126]`.

## How you'll be assessed

- The **write** exercise checks the cache rule (*implementation*).
- The **explain** exercise checks that you can read a Dockerfile and its history (*explanation*).

The Docker output in this lesson was produced on one machine on 2026-11-07 with Docker Desktop 4.98 and will differ in detail on yours. The statement that a container shares the host kernel is standard Docker teaching; it was not taken from a recorded source.
""")

# ====================================================================== j11-l1.2
def f_copy_from(lines):
    out = []
    for l in lines:
        m = re.match(r"\s*COPY\s+--from=(\S+)", l, re.I)
        if m:
            out.append(m.group(1))
    return out


def f_final(lines):
    base = ""
    for l in lines:
        m = re.match(r"\s*FROM\s+(\S+)", l, re.I)
        if m:
            base = m.group(1)
    return base


MS_SOL = '''
List<String> copyFromTargets(List<String> lines) {
    List<String> names = new ArrayList<>();
    for (String line : lines) {
        String[] words = line.trim().split("\\\\s+");
        if (words.length > 1 && words[0].equalsIgnoreCase("COPY") && words[1].startsWith("--from=")) {
            names.add(words[1].substring("--from=".length()));
        }
    }
    return names;
}

String finalBaseImage(List<String> lines) {
    String base = "";
    for (String line : lines) {
        String[] words = line.trim().split("\\\\s+");
        if (words.length > 1 && words[0].equalsIgnoreCase("FROM")) {
            base = words[1];
        }
    }
    return base;
}
'''
MS_ANY_COPY = MS_SOL.replace('words[0].equalsIgnoreCase("COPY") && words[1].startsWith("--from=")', 'words[0].equalsIgnoreCase("COPY")').replace("names.add(words[1].substring(\"--from=\".length()));", "names.add(words[1]);")
MS_CASE = MS_SOL.replace('words[0].equalsIgnoreCase("COPY")', 'words[0].equals("COPY")')
MS_FIRST_FROM = MS_SOL.replace('            base = words[1];', '            if (base.isEmpty()) {\n                base = words[1];\n            }')
MS_AS = MS_SOL.replace('            base = words[1];', '            base = words[words.length - 1];')
ML = HELLO_MULTI.split("\n")
ex12.method(
    "write", "j11-l1.2-write-dockerfile", "Reading a multi-stage Dockerfile", ["o1"], ["J11.02"], ["IMPL"],
    "In a multi-stage Dockerfile each `FROM` starts a new stage and the **last** stage is the image you get; `COPY --from=NAME` brings files from an earlier stage. Write two methods over the lines of a Dockerfile: `copyFromTargets(lines)` returns, in order, the stage names or numbers after `COPY --from=`; `finalBaseImage(lines)` returns the image named by the last `FROM` (the first word after `FROM`, so `FROM x AS y` gives `x`). Instruction names are case-insensitive and may be indented.",
    [("copyFromTargets", [("lines", "List<String>")], "List<String>"), ("finalBaseImage", [("lines", "List<String>")], "String")],
    {"copyFromTargets": f_copy_from, "finalBaseImage": f_final},
    [("copyFromTargets", (ML,), "the course's Dockerfile"), ("finalBaseImage", (ML,), "its final image"), ("copyFromTargets", (["FROM a", "COPY x /x"],), "a plain COPY")],
    [("finalBaseImage", (["FROM a AS build", "RUN x"],), "one stage with a name"), ("finalBaseImage", (["from a", "from b AS second", "COPY --from=0 /x /y"],), "lower case"), ("copyFromTargets", (["FROM a", "FROM b", "  copy --from=0 /x /x", "COPY --from=a /y /y"],), "indented and lower case"),
     ("copyFromTargets", ([],), "empty file"), ("finalBaseImage", ([],), "no FROM"), ("copyFromTargets", (["COPY --chown=1:1 x /x"],), "another COPY flag"), ("finalBaseImage", (["# FROM a", "FROM b"],), "a comment is not an instruction")],
    starter='''
List<String> copyFromTargets(List<String> lines) {
    return List.of();
}

String finalBaseImage(List<String> lines) {
    return "";
}
''', solution=MS_SOL,
    wrongs={"every-copy": MS_ANY_COPY, "case-sensitive": MS_CASE, "first-from": MS_FIRST_FROM, "takes-the-alias": MS_AS},
    hints=["Split each line into words; the instruction is the first word.", "Which FROM decides what the final image is based on?"],
    misconceptions=("MC206",), difficulty=3,
)

ex12.explain(
    "j11-l1.2-explain-multistage", "What stays behind", ["o2"], ["J11.02"],
    "Below are the multi-stage Dockerfile, the build steps Docker ran for it (`--progress=plain`, with the step lines only) and the sizes of the single-stage and multi-stage images built from the same source on this machine.\n\n" + fence(HELLO_MULTI, "dockerfile") + "\n\n" + fence(cap("cap_docker_build.txt")) + "\n\n" + fence("$ docker images hello\nREPOSITORY:TAG   SIZE\nhello:multi      304MB\nhello:single     421MB") + "\n\nExplain which stage each build step belongs to, what ended up in the final image and what was left behind, how large the saving was in megabytes and as a percentage of the single-stage image, and what other benefit a smaller image has besides download time.",
    "Steps 5, 7, 10 and 11 belong to the build stage (JDK image, WORKDIR /src, COPY Hello.java, RUN javac) and steps 6, 8 and 12 to the final stage (JRE image, WORKDIR /app, COPY --from=build /out /app). Only the compiled class files are copied into the final image; the JDK image, the compiler and the source are left behind. The multi-stage image is 304 MB against 421 MB, a saving of 117 MB, about 28 percent (117 divided by 421). A smaller image also has a smaller attack surface, because compilers and build tools that are not there cannot be abused, and less to scan and patch.",
    levels={
        2: ("The answer assigns the steps to stages, says what was copied and left behind, computes the saving and names the security or scanning benefit.", [
            "The JDK image, WORKDIR /src, COPY Hello.java and javac are the build stage; the JRE image, WORKDIR /app and COPY --from=build are the final stage. Only the compiled classes go into the final image; the compiler and source stay behind. 421 minus 304 is 117 MB, about 28 percent. A smaller image also has fewer tools an attacker could use and less to scan.",
            "Build stage: steps 5, 7, 10, 11. Final stage: 6, 8, 12. Only /out is copied across. The saving is 117 MB (28%). Fewer packages means a smaller attack surface."]),
        1: ("The answer gets the saving but not the stage assignment, or the benefit.", [
            "The multi-stage image is 117 MB smaller.",
            "It copies only the compiled classes."]),
        0: ("The answer misreads the stages.", [
            "Both images contain the compiler, they are just built differently.",
            "The smaller image is slower to start."]),
    },
)

l11_l1_2 = Lesson("j11-l1.2", "Multi-stage builds", ["J11.02"], [
    ("o1", "Read a multi-stage Dockerfile: its stages, what is copied between them, and the final base image"),
    ("o2", "Explain from real build output and sizes what a multi-stage build leaves out"),
], ["j11-l1.1"], 40, ["I126"], """## Before you start

You should know what a Dockerfile layer is (lesson 11.1.1).

## Explanation

To build a Java program you need a JDK, with a compiler and build tools. To run it you need only a Java runtime. A single-stage Dockerfile that builds and runs in the same image ships all the build tools to production.

A **multi-stage build** fixes that. As the Docker documentation puts it, you use multiple `FROM` statements in your Dockerfile; each begins a new stage of the build, and you can selectively copy artifacts from one stage to another, leaving behind everything you do not want in the final image. The **last stage is the image you get**. Name a stage with `AS name` and bring files in with `COPY --from=name`.

The effect, measured on this machine in the exercise: the same program in 421 MB as a single stage on the JDK image, and 304 MB as a multi-stage build on the JRE image. A smaller image downloads and starts faster, and also exposes less: the compiler and the source are not there to be abused, and there is less to scan for vulnerabilities.

For a Maven project the build stage would run Maven and copy only the jar across.

## Worked examples

### Example 1: the course's Dockerfile.

""" + fence(HELLO_MULTI, "dockerfile") + """

### Example 2: what the build did.

The captured `docker build` output lists the steps: the build stage's `RUN javac`, and the final stage's `COPY --from=build /out /app`.

## Where this is used

- Every container image for a compiled language. Our platform's own image (next lesson) takes a ready-built jar for simplicity; a real pipeline would build the jar in an earlier stage.

## Common mistakes

:::mistake{id=MC206}
**Shipping the build environment.** An image with a compiler, a package manager and the source is bigger, slower to pull and offers an attacker more to use.
:::

## Practice

::exercise{id=j11-l1.2-write-dockerfile}

::exercise{id=j11-l1.2-explain-multistage}

## Further reading

- **Docker documentation, multi-stage builds** `[I126]`.

## How you'll be assessed

- The **write** exercise checks that you can read the structure of a multi-stage Dockerfile (*implementation*).
- The **explain** exercise checks that you can interpret real build output and sizes (*explanation*).

The sizes are what `docker images` reported on this machine (uncompressed). The security benefit is general practice, not a quotation from a recorded source.
""")

# ====================================================================== j11-l1.3
def f_subst(template, env):
    values = {}
    for e in env:
        k, _, v = e.partition("=")
        values[k] = v

    def one(m):
        if m.group(0) == "$$":
            return "$"
        name, op, default = m.group(1), m.group(2), m.group(3)
        v = values.get(name)
        if op == ":-":
            return default if v is None or v == "" else v
        if op == "-":
            return default if v is None else v
        return "" if v is None else v

    return re.sub(r"\$\$|\$\{([_a-zA-Z][_a-zA-Z0-9]*)(?:(:-|-)([^}]*))?\}", one, template)


SUBST_SOL = '''
String substitute(String template, List<String> env) {
    Map<String, String> values = new HashMap<>();
    for (String entry : env) {
        int equals = entry.indexOf('=');
        values.put(entry.substring(0, equals), entry.substring(equals + 1));
    }
    java.util.regex.Matcher matcher = java.util.regex.Pattern.compile("\\\\$\\\\$|\\\\$\\\\{([_a-zA-Z][_a-zA-Z0-9]*)(?:(:-|-)([^}]*))?\\\\}").matcher(template);
    StringBuilder out = new StringBuilder();
    while (matcher.find()) {
        String replacement;
        if (matcher.group().equals("$$")) {
            replacement = "$";
        } else {
            String value = values.get(matcher.group(1));
            String operator = matcher.group(2);
            String fallback = matcher.group(3);
            if (":-".equals(operator)) {
                replacement = value == null || value.isEmpty() ? fallback : value;
            } else if ("-".equals(operator)) {
                replacement = value == null ? fallback : value;
            } else {
                replacement = value == null ? "" : value;
            }
        }
        matcher.appendReplacement(out, java.util.regex.Matcher.quoteReplacement(replacement));
    }
    matcher.appendTail(out);
    return out.toString();
}
'''
SUBST_EMPTY_IS_SET = SUBST_SOL.replace('replacement = value == null || value.isEmpty() ? fallback : value;', 'replacement = value == null ? fallback : value;')
SUBST_UNSET_ONLY_EMPTY = SUBST_SOL.replace('replacement = value == null ? fallback : value;\n            } else {', 'replacement = value == null || value.isEmpty() ? fallback : value;\n            } else {')
SUBST_NO_DOLLAR = SUBST_SOL.replace('replacement = "$";', 'replacement = "$$";')
SUBST_KEEP_MISSING = SUBST_SOL.replace('replacement = value == null ? "" : value;', 'replacement = value == null ? matcher.group() : value;')

ex13.method(
    "write", "j11-l1.3-write-interpolate", "Compose variable substitution", ["o1"], ["J11.03"], ["IMPL"],
    "Compose files use Bash-like substitution. Write `substitute(template, env)`, where `env` is a list of `NAME=value`. `${NAME}` becomes the value, or the empty string if NAME is unset. `${NAME:-fallback}` becomes the fallback if NAME is unset **or empty**. `${NAME-fallback}` becomes the fallback only if NAME is **unset**. `$$` becomes a single `$`. Everything else is copied unchanged.",
    [("substitute", [("template", "String"), ("env", "List<String>")], "String")], {"substitute": f_subst},
    [("substitute", ("password: ${DB_PASSWORD}", ["DB_PASSWORD=s3cret"]), "a set variable"), ("substitute", ("tag: ${TAG:-latest}", []), "a default for an unset variable"), ("substitute", ("price: $$5", []), "a literal dollar")],
    [("substitute", ("a=${X:-d}", ["X="]), "empty counts as unset for :-"), ("substitute", ("a=${X-d}", ["X="]), "empty is set for -"), ("substitute", ("a=${X-d}", []), "unset for -"),
     ("substitute", ("${A}${B}", ["A=1", "B=2"]), "two variables"), ("substitute", ("${MISSING}", []), "unset with no default is empty"), ("substitute", ("x=${Y:-a-b}", []), "a default containing a dash"),
     ("substitute", ("no variables here", ["A=1"]), "nothing to do"), ("substitute", ("url=jdbc:postgresql://${HOST:-db}:${PORT:-5432}/academy", ["HOST=localhost"]), "a connection string")],
    starter='''
String substitute(String template, List<String> env) {
    return template;
}
''', solution=SUBST_SOL,
    wrongs={"empty-counts-as-set": SUBST_EMPTY_IS_SET, "dash-treated-like-colon-dash": SUBST_UNSET_ONLY_EMPTY, "dollar-dollar-unchanged": SUBST_NO_DOLLAR, "keeps-unset-variables": SUBST_KEEP_MISSING},
    hints=["Use one regular expression that matches `$$` or a braced variable.", "`:-` and `-` differ for a variable that is set but empty."],
    misconceptions=("MC207",), difficulty=4,
)

ex13.explain(
    "j11-l1.3-explain-compose", "Reading a Compose file and its run", ["o2"], ["J11.03"],
    "This is a Compose file that runs this platform's backend with a PostgreSQL database, and what Docker reported when it was started on this machine.\n\n" + fence(APP_COMPOSE, "yaml") + "\n\n" + fence(cap("cap_compose.txt")) + "\n\n" + fence(cap("cap_dbport.txt")) + "\n\nExplain: (1) what `depends_on` with `condition: service_healthy` achieves and what would go wrong without it; (2) how the app finds the database (look at the URL host); (3) why the database service has no `ports` entry, and what the last output shows; (4) where the database password comes from, and why that is better than writing it into the Compose file or the image; (5) what the log line 'Loaded 126 lessons and 494 exercises' tells you about the image.",
    "(1) The app starts only after the database's healthcheck reports it healthy; without it the app could start first and fail to connect, or crash and need restarting. (2) By the service name `db`: Compose puts the services on one network where each service is reachable by its name, so the URL is jdbc:postgresql://db:5432/academy. (3) Only the app needs to be reachable from outside; the database is reachable by the app on the internal network but not published to the host, which shrinks the attack surface, and `docker compose port db 5432` printing `:0` confirms nothing is published. (4) It is interpolated from the environment (here an env file) as ${DB_PASSWORD}; keeping the value out of the file and out of the image means it is not committed to version control or baked into every copy of the image, and each environment can supply its own. (5) The content directory was copied into the image: it contains the 126 lessons and 494 exercises, so the image is self-contained.",
    levels={
        2: ("The answer covers all five points correctly with the reasons.", [
            "(1) The app waits until postgres reports healthy; otherwise it could start before the database accepts connections and fail. (2) Through the service name db on the Compose network. (3) Only the app is published; the db is internal, and the :0 output shows no host port is mapped. (4) ${DB_PASSWORD} comes from the environment or env file, so it is not in the repository or the image and can differ per environment. (5) The content is inside the image: 126 lessons and 494 exercises were loaded from it.",
            "Healthcheck gating means app starts after the db is ready. The host name is db, resolved by Compose's network. The db is not published, which reduces exposure; docker compose port shows nothing mapped. The password is interpolated from the environment instead of being hard-coded. The log shows the image carries the whole content."]),
        1: ("The answer covers some points.", [
            "The app uses the db host name and waits for the database.",
            "The password is a variable."]),
        0: ("The answer misreads the file.", [
            "The app connects to localhost:5432.",
            "The password is stored in the image so it can be reused."]),
    },
)

l11_l1_3 = Lesson("j11-l1.3", "Compose, configuration and secrets", ["J11.03"], [
    ("o1", "Apply Compose's variable substitution rules correctly"),
    ("o2", "Read a Compose file and its run: service names, health-gated start, unpublished ports and configuration"),
], ["j11-l1.2", "j8-l1.4"], 45, ["I127", "I137", "I138"], """## Before you start

You should know what an image and a container are (lessons 11.1.1 and 11.1.2) and why secrets stay out of source control (lesson 8.1.4).

## Explanation

An application is rarely one container. **Docker Compose** describes a multi-container application in one file. Its model: a **service** is an abstract concept implemented by running the same container image and configuration one or more times; services communicate through **networks** and keep persistent data in **volumes**.

Three things in a Compose file matter for a Java service with a database.

**Start order.** `depends_on` makes a service start after another. With `condition: service_healthy` it waits until the dependency is *healthy*, as defined by its `healthcheck`, not merely started. Without that, the application can start before the database accepts connections.

**Names and ports.** On the Compose network each service is reachable by its service name, so the application's database URL uses the host `db`. Only services that need to be reached from outside get a `ports:` entry. The database does not: the application reaches it on the internal network, and nothing is published on the host.

**Configuration.** Compose files use Bash-like `${VARIABLE}` interpolation. `${VAR:-default}` gives the default when VAR is unset or empty, `${VAR-default}` only when it is unset, and `$$` produces a literal dollar sign. If a variable cannot be resolved and has no default, Compose warns and substitutes an empty string. Passing the database password as `${DB_PASSWORD}` from an environment file keeps it out of the Compose file and out of the image, which is the Stage 8 rule applied (the demo password in this lesson's run is a throw-away value for a local demonstration).

## Worked examples

### Example 1: the platform's own stack.

The exercise shows the Compose file and its real run: `ps` with the database `healthy` and only the app's port mapped, an HTTP 200 from the smoke test, and the application's startup lines showing that it reached `db` and loaded the content.

### Example 2: the image that results.

""" + fence(cap("cap_app_image.txt")) + """

The image is large because it contains the 84 MB Spring Boot jar, the Java runtime and the course content.

## Where this is used

- Local development stacks, integration tests that need a real database, and small deployments. (Testcontainers, mentioned in Stage 7, automates the same idea from inside a test.)

## Common mistakes

:::mistake{id=MC207}
**Writing the password into the Compose file or the image "because it is just for development".** The file gets committed and the image gets shared. Use a variable and an untracked env file from the start.
:::

## Practice

::exercise{id=j11-l1.3-write-interpolate}

::exercise{id=j11-l1.3-explain-compose}

## Further reading

- **Docker documentation, how Compose works** `[I127]`.
- **Compose file reference, interpolation** `[I137]`.
- **Compose file reference, services (`depends_on`)** `[I138]`.

## How you'll be assessed

- The **write** exercise checks substitution rules (*implementation*).
- The **explain** exercise checks that you can read a real Compose run (*explanation*).

The run was captured on 2026-11-07 on one machine. The statement that services reach each other by service name is standard Compose behaviour, confirmed by this run's successful connection to host `db`, but not quoted from a recorded source.
""")

# ====================================================================== j11-l1.4
def f_exit(code, oom):
    if code == 0:
        return "ok"
    if code == 137 and oom:
        return "kernel-oom-kill"
    if code == 137:
        return "killed-by-signal"
    return "application-error"


EXIT_SOL = '''
String classifyExit(int exitCode, boolean oomKilled) {
    if (exitCode == 0) {
        return "ok";
    }
    if (exitCode == 137) {
        return oomKilled ? "kernel-oom-kill" : "killed-by-signal";
    }
    return "application-error";
}
'''
EXIT_137_ALWAYS_OOM = EXIT_SOL.replace('return oomKilled ? "kernel-oom-kill" : "killed-by-signal";', 'return "kernel-oom-kill";')
EXIT_FLAG_ONLY = EXIT_SOL.replace("    if (exitCode == 137) {", "    if (oomKilled) {")
EXIT_ONE_IS_OOM = EXIT_SOL.replace('    return "application-error";', '    return exitCode == 1 ? "kernel-oom-kill" : "application-error";')
EXIT_ZERO_FLAG = EXIT_SOL.replace('    if (exitCode == 0) {\n        return "ok";\n    }', '    if (exitCode == 0 && !oomKilled) {\n        return "ok";\n    }')

ex14.method(
    "write", "j11-l1.4-write-exit", "Why did the container stop", ["o1"], ["J11.04"], ["IMPL", "DEBUG"],
    "`docker inspect` reports a container's exit code and whether the kernel's out-of-memory killer stopped it (`OOMKilled`). Write `classifyExit(exitCode, oomKilled)`: `ok` for exit code 0; for 137 (the process was killed with signal 9) `kernel-oom-kill` if `oomKilled` is true, otherwise `killed-by-signal`; any other code is `application-error`.",
    [("classifyExit", [("exitCode", "int"), ("oomKilled", "boolean")], "String")], {"classifyExit": f_exit},
    [("classifyExit", (0, False), "a normal exit"), ("classifyExit", (137, True), "the kernel killed it for memory"), ("classifyExit", (1, False), "the application failed")],
    [("classifyExit", (137, False), "killed by something else, for example docker kill"), ("classifyExit", (143, False), "terminated, signal 15"), ("classifyExit", (1, True), "the flag with another code"),
     ("classifyExit", (0, True), "exit code zero"), ("classifyExit", (2, False), "another application error"), ("classifyExit", (255, False), "the highest code")],
    starter='''
String classifyExit(int exitCode, boolean oomKilled) {
    return "";
}
''', solution=EXIT_SOL,
    wrongs={"every-137-is-memory": EXIT_137_ALWAYS_OOM, "trusts-the-flag-only": EXIT_FLAG_ONLY, "one-means-memory": EXIT_ONE_IS_OOM, "flag-overrides-success": EXIT_ZERO_FLAG},
    hints=["Exit code 137 alone does not say why the process got the signal.", "Check for success first."],
    misconceptions=("MC208",), difficulty=2,
)

ex14.explain(
    "j11-l1.4-explain-memory", "Two ways to run out of memory", ["o2"], ["J11.04"],
    "These are real results from this machine. First, the heap the JVM chose in containers with different memory limits. Second, the same program (`Hog`, which holds `N` megabytes of arrays) run in a container limited to 128 MB, once with the default heap and once with `-Xmx1g`.\n\n" + fence(cap("cap_jvm_flags.txt")) + "\n\n" + fence(cap("cap_oom.txt")) + "\n\nExplain: (1) what the first output shows about how the JVM sees a container's limit; (2) why the first run ended with an exception and exit code 1 while the second ended with exit code 137 and `OOMKilled=true`, and who stopped each; (3) which failure is easier to diagnose and why; (4) what you would set for a service that needs about 300 MB of heap, and what else uses memory in the container besides the heap.",
    "(1) The JVM reads the container limit and sizes its default heap from it: 126 MB for a 256 MB limit, 256 MB for a 1 GB limit, 61 MB for 128 MB, so the heap is only part of the limit (about half for small containers and a quarter for the larger one here). (2) With the default heap (61 MB) the JVM itself ran out of heap and threw OutOfMemoryError: Java heap space, exit code 1, and the JVM chose to stop. With -Xmx1g the JVM believed it could use 989 MB, kept allocating, and the process exceeded the container's 128 MB, so the kernel's out-of-memory killer ended it with SIGKILL (137, OOMKilled=true) with no Java exception and no heap dump. (3) The first, because the JVM prints an exception with a stack trace and can write a heap dump; the second leaves only the exit code and OOMKilled flag. (4) Set the container limit above the heap with room for the rest: metaspace, thread stacks, code cache, native and direct buffers; for a 300 MB heap a limit of, say, 512 MB or more, with -XX:MaxRAMPercentage or -Xmx chosen so the heap stays below the limit, then verify under load.",
    levels={
        2: ("The answer reads the heap sizes, distinguishes the two failures and who killed each, notes the diagnosability and gives a sizing rule with non-heap memory.", [
            "(1) The JVM sees the limit and picks a heap of 61 MB for 128 MB, 126 MB for 256 MB and 256 MB for 1 GB, so the heap is a fraction of the limit. (2) The first run threw OutOfMemoryError: Java heap space, exit 1, the JVM stopped itself. In the second -Xmx1g let the heap grow past the 128 MB container, so the kernel OOM killer sent SIGKILL: 137 and OOMKilled=true. (3) The first is easier: stack trace and possible heap dump; the second only shows an exit code. (4) For a 300 MB heap give the container well over that (for example 512 MB or 1 GB), because metaspace, thread stacks, code cache and native buffers also count, and set the heap flag below the limit, then test.",
            "The JVM is container-aware: it sized its heap from the limit. Default heap OOM is a Java exception (exit 1). Forcing -Xmx1g in a 128 MB container let the process outgrow the limit so the kernel killed it (137, OOMKilled). The Java one is easier to debug. For 300 MB heap, set limit higher than heap plus off-heap memory."]),
        1: ("The answer distinguishes the two failures without the sizing rule.", [
            "One was a Java OutOfMemoryError and the other was killed by the kernel.",
            "The heap should be smaller than the container limit."]),
        0: ("The answer treats both as the same or the limit as the heap.", [
            "Both mean the heap is too small, so just raise -Xmx.",
            "The container limit is the heap size."]),
    },
)

l11_l1_4 = Lesson("j11-l1.4", "The JVM in containers", ["J11.04"], [
    ("o1", "Tell a kernel out-of-memory kill from a Java heap error from a container's exit information"),
    ("o2", "Explain how the JVM sizes its heap in a container and how to budget the container's memory"),
], ["j11-l1.1", "j9-l3.1"], 40, ["I128", "I129"], """## Before you start

You should know what the heap is (lesson 9.3.1) and what a container memory limit is (lesson 11.1.1).

## Explanation

By default a container has no resource constraints and can use as much of a resource as the host's scheduler allows. Docker can enforce **hard memory limits**: `--memory` (or `-m`) sets the maximum memory the container can use. If a process exceeds a hard limit the kernel's **out-of-memory killer** stops it.

A modern JVM reads the container's limit and sizes its default heap from it. The `java` command documents `-XX:MaxRAMPercentage`, the maximum heap as a percentage of the available memory (25 percent by default), and `-XX:MinRAMPercentage` for small heaps, which it defines as approximately 125 MB. The real numbers measured on this machine (exercise): a 256 MB container got a 126 MB heap, a 1 GB container a 256 MB heap, a 128 MB container a 61 MB heap. So the heap is only a **part** of the container's memory, and the rest is needed too: metaspace (class metadata), thread stacks, the code cache and native or direct buffers.

That gives two different failures, both captured in the exercise:

- **A Java heap `OutOfMemoryError`.** The JVM ran out of its own heap. You get an exception, a stack trace and, if configured, a heap dump. The exit code is 1.
- **A kernel OOM kill.** The process as a whole outgrew the container. There is no Java exception, because the kernel simply kills the process. The exit code is 137 (128 plus signal 9) and `docker inspect` shows `OOMKilled=true`.

Fix by budgeting: set the container limit comfortably above the heap, set the heap (`-Xmx` or `-XX:MaxRAMPercentage`) below the limit, and test under load.

## Worked examples

### Example 1: what the JVM chose.

Run `java -XX:+PrintFlagsFinal -version` in a container with a limit and read `MaxHeapSize`.

### Example 2: the two exits.

A program holding 300 MB: with the default heap it dies with an OutOfMemoryError (exit 1); with `-Xmx1g` in a 128 MB container it is killed (137, OOMKilled).

## Where this is used

- Every Java service in Kubernetes or any container platform: pods restarting with exit code 137 are a classic.

## Common mistakes

:::mistake{id=MC208}
**Raising `-Xmx` to fix an exit code 137.** The process was killed because it outgrew the container. A larger heap makes that more likely. Look at `OOMKilled`, then budget the whole container.
:::

## Practice

::exercise{id=j11-l1.4-write-exit}

::exercise{id=j11-l1.4-explain-memory}

## Further reading

- **Docker documentation, resource constraints** `[I128]`.
- **The `java` command (Java SE 25)** `[I129]`.

## How you'll be assessed

- The **write** exercise checks that you can classify an exit (*implementation, debugging*).
- The **explain** exercise checks that you can read the memory results and budget a container (*explanation*).

The heap sizes are what this JDK (25.0.5) chose on this machine in Docker Desktop's virtual machine; other versions and platforms may choose differently. The description of metaspace, stacks and the code cache as other users of memory is standard JVM knowledge and is not quoted from a recorded source.
""")
print("module 11.1 authored")
