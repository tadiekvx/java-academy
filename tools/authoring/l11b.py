"""Stage 11 authoring: module 11.2 (CI/CD). Not runnable on this platform; exercises model the logic."""
import l11common
from l11common import Lesson, Exercises, q, register, cap, fence
import build  # noqa: E402

ex21 = Exercises("j11-l2.1")
ex22 = Exercises("j11-l2.2")

REGISTER = {
    "j11-l2.1": ("Pipelines as code", ["J11.05"]),
    "j11-l2.2": ("Deployment strategies and rollback", ["J11.06"]),
}
MISCS = {
    "MC209": (["J11.05"], "I130", "A pipeline is a list of scripts that all run whether or not an earlier one failed"),
    "MC210": (["J11.06"], "I130", "A deployment that passed its tests cannot fail in production, so rollback is only for emergencies"),
}
register(REGISTER, MISCS)

WORKFLOW = '''name: ci
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "25"
      - run: mvn -B -f backend/pom.xml test

  image:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t academy:${{ github.sha }} .
'''


def f_pipeline(jobs, needs, failing):
    deps = {j: [] for j in jobs}
    for e in needs:
        a, b = e.split(">")
        deps.setdefault(a, []).append(b)
        deps.setdefault(b, [])
    status, out = {}, []
    remaining = sorted(deps)
    while remaining:
        ready = [j for j in remaining if all(d in status for d in deps[j])]
        if not ready:
            return ["cycle"]
        j = ready[0]
        if any(status[d] != "ok" for d in deps[j]):
            status[j] = "skipped"
        else:
            status[j] = "failed" if j == failing else "ok"
        out.append(f"{status[j]}:{j}")
        remaining.remove(j)
    return out


PIPE_SOL = '''
List<String> runPipeline(List<String> jobs, List<String> needs, String failing) {
    Map<String, List<String>> deps = new TreeMap<>();
    for (String job : jobs) {
        deps.computeIfAbsent(job, k -> new ArrayList<>());
    }
    for (String edge : needs) {
        String[] p = edge.split(">");
        deps.computeIfAbsent(p[0], k -> new ArrayList<>()).add(p[1]);
        deps.computeIfAbsent(p[1], k -> new ArrayList<>());
    }
    Map<String, String> status = new HashMap<>();
    List<String> out = new ArrayList<>();
    List<String> remaining = new ArrayList<>(deps.keySet());
    while (!remaining.isEmpty()) {
        String next = null;
        for (String job : remaining) {
            if (status.keySet().containsAll(deps.get(job))) {
                next = job;
                break;
            }
        }
        if (next == null) {
            return List.of("cycle");
        }
        boolean blocked = false;
        for (String dep : deps.get(next)) {
            if (!status.get(dep).equals("ok")) {
                blocked = true;
            }
        }
        String result = blocked ? "skipped" : next.equals(failing) ? "failed" : "ok";
        status.put(next, result);
        out.add(result + ":" + next);
        remaining.remove(next);
    }
    return out;
}
'''
PIPE_RUNS_ANYWAY = PIPE_SOL.replace('String result = blocked ? "skipped" : next.equals(failing) ? "failed" : "ok";', 'String result = next.equals(failing) ? "failed" : "ok";')
PIPE_ONLY_DIRECT = PIPE_SOL.replace('if (!status.get(dep).equals("ok")) {', 'if (status.get(dep).equals("failed")) {')
PIPE_NO_CYCLE = PIPE_SOL.replace('            return List.of("cycle");', '            return out;')
PIPE_NO_ORDER = PIPE_SOL.replace("        for (String job : remaining) {\n            if (status.keySet().containsAll(deps.get(job))) {\n                next = job;\n                break;\n            }\n        }", "        next = remaining.get(remaining.size() - 1);")
JOBS = ["build", "test", "scan", "package", "deploy"]
NEEDS = ["test>build", "scan>build", "package>test", "package>scan", "deploy>package"]

ex21.method(
    "write", "j11-l2.1-write-pipeline", "Which jobs run", ["o1"], ["J11.05"], ["IMPL"],
    "A pipeline is a set of jobs; `A>B` means job A `needs` job B (it runs only after B, and only if B succeeded). Jobs run one at a time here. At each step run the alphabetically first job whose needs have all been decided. A job whose needs did not all succeed is `skipped`; otherwise it runs and is `failed` if it is the job named `failing` (use an empty string for none), or `ok`. Write `runPipeline(jobs, needs, failing)` returning one `status:job` entry per job in the order they were decided. If no job can be decided because of a cycle, return `[\"cycle\"]`.",
    [("runPipeline", [("jobs", "List<String>"), ("needs", "List<String>"), ("failing", "String")], "List<String>")], {"runPipeline": f_pipeline},
    [("runPipeline", (JOBS, NEEDS, ""), "everything passes"), ("runPipeline", (JOBS, NEEDS, "test"), "the tests fail"), ("runPipeline", (["a", "b"], ["a>b", "b>a"], ""), "a cycle")],
    [("runPipeline", (JOBS, NEEDS, "build"), "the first job fails"), ("runPipeline", (JOBS, NEEDS, "scan"), "the scan fails, the tests still run"), ("runPipeline", (JOBS, NEEDS, "deploy"), "the last job fails"),
     ("runPipeline", ([], [], ""), "no jobs"), ("runPipeline", (["only"], [], "only"), "a single failing job"), ("runPipeline", (["b", "a"], [], ""), "independent jobs run in name order"),
     ("runPipeline", (JOBS, NEEDS, "package"), "packaging fails"), ("runPipeline", (["x", "y", "z"], ["z>y", "y>x"], "x"), "a chain with its root failing")],
    starter='''
List<String> runPipeline(List<String> jobs, List<String> needs, String failing) {
    return List.of();
}
''', solution=PIPE_SOL,
    wrongs={"runs-dependants-anyway": PIPE_RUNS_ANYWAY, "skips-only-direct-dependants": PIPE_ONLY_DIRECT, "ignores-cycles": PIPE_NO_CYCLE, "ignores-needs": PIPE_NO_ORDER},
    hints=["A job is ready when every job it needs has a status.", "A skipped job also blocks the jobs that need it."],
    misconceptions=("MC209",), difficulty=4,
)

ex21.explain(
    "j11-l2.1-explain-workflow", "Reading a workflow", ["o2"], ["J11.05"],
    "This is a GitHub Actions workflow file for this repository. It was written for the course and has **not** been run.\n\n" + fence(WORKFLOW, "yaml") + "\n\nExplain: when it runs; what the two jobs do; what `needs: test` means and what happens to the `image` job if a test fails; why a pipeline like this is stored in the repository next to the code; and name two things a team would add before relying on it for releases.",
    "The workflow runs on every push and pull request. The test job checks out the code, installs Java 25 (Temurin) and runs the backend's Maven tests; the image job checks out the code and builds a Docker image tagged with the commit hash. `needs: test` makes the image job wait for the test job and run only if it succeeded, so a failed test means no image is built. Keeping the pipeline in the repository (pipeline as code) versions it with the code, lets it be reviewed like code, and makes the build reproducible for anyone. Before relying on it for releases a team would add things such as a vulnerability scan of the image, publishing the image to a registry, caching dependencies, pinning action versions, a deployment step with a smoke test, and secrets handled through the platform's secret store.",
    levels={
        2: ("The answer describes the trigger, both jobs, the `needs` behaviour, the pipeline-as-code benefit and two sensible additions.", [
            "It runs on every push and pull request. test checks out, sets up Java 25 and runs mvn test; image checks out and builds a Docker image tagged with the commit SHA. needs: test means image waits and is skipped if tests fail. Having it in the repo means it is versioned and reviewed with the code. Before releases I would add an image scan and push to a registry, and probably a deploy plus smoke test.",
            "Triggers: push and PR. Jobs: tests, then an image build gated by needs. If a test fails the image job does not run. As code it is reviewed and reproducible. To add: scanning, registry publishing, caching, pinned versions."]),
        1: ("The answer describes the jobs without the dependency or the additions.", [
            "It runs the tests and builds an image.",
            "It runs on push."]),
        0: ("The answer misreads the workflow.", [
            "The image job runs at the same time as the test job whatever the result.",
            "It deploys to production."]),
    },
)

l11_l2_1 = Lesson("j11-l2.1", "Pipelines as code", ["J11.05"], [
    ("o1", "Work out which jobs of a pipeline run, fail or are skipped"),
    ("o2", "Read a CI workflow file and say what it does and what it still lacks"),
], ["j11-l1.2", "j4-l3.2"], 40, ["I130"], """## Before you start

You should know Maven builds and unit tests (Stage 4) and Docker images (module 11.1).

## Explanation

Continuous integration (CI) means that every change is built and tested automatically. A **pipeline** is the automated sequence of steps: build, test, scan, package, publish, deploy. Modern CI systems describe the pipeline in a file that lives in the repository, **pipeline as code**, so it is versioned with the code, reviewed in pull requests and reproducible.

In GitHub Actions a **workflow** is made of **jobs**, each running in a runner environment given by `runs-on`. Jobs run in parallel unless one declares `needs`: `jobs.<job_id>.needs` makes a job wait for the named jobs, and it runs only if they succeeded. That one keyword is what turns a list of jobs into a pipeline with quality gates: a failing test job means the image job never runs, and the next jobs that need the image are skipped in turn.

A pipeline is only as good as its gates. A useful one builds from a clean checkout, runs the tests, scans, builds an image once and promotes that same image through environments, and stops at the first failing gate.

## Worked examples

### Example 1: a workflow.

The exercise shows a two-job workflow for this repository, written for the course and **not executed** (the platform has no CI server and no repository host to run it on).

### Example 2: skipping.

With `test>build, scan>build, package>test, package>scan, deploy>package` and `test` failing, the run is `ok:build, ok:scan, failed:test, skipped:package, skipped:deploy`.

## Where this is used

- Every professional project. The Stage 4 `mvn test` you ran by hand is what the first job automates.

## Common mistakes

:::mistake{id=MC209}
**Treating the pipeline as independent scripts.** Jobs depend on each other. A failed gate must stop everything that needs it.
:::

## Practice

::exercise{id=j11-l2.1-write-pipeline}

::exercise{id=j11-l2.1-explain-workflow}

## Further reading

- **GitHub Docs, workflow syntax for GitHub Actions** `[I130]`.

## How you'll be assessed

- The **write** exercise checks gating logic (*implementation*).
- The **explain** exercise checks that you can read a workflow (*explanation*).

The workflow shown was not run. The versions of the actions it uses (`checkout`, `setup-java`) were not checked against their current releases, so verify them before use.
""")

# ====================================================================== j11-l2.2
def f_rollout(replicas, batch, health):
    if replicas < 1 or batch < 1:
        return ["invalid"]
    out = []
    batches = -(-replicas // batch)
    for b in range(batches):
        lo, hi = b * batch + 1, min(replicas, (b + 1) * batch)
        out.append(f"update:{lo}-{hi}")
        if b < len(health) and health[b] == "bad":
            out.append(f"rollback:1-{hi}")
            return out
        out.append(f"healthy:{lo}-{hi}")
    out.append("done")
    return out


ROLL_SOL = '''
List<String> rolloutTrace(int replicas, int batch, List<String> health) {
    if (replicas < 1 || batch < 1) {
        return List.of("invalid");
    }
    List<String> trace = new ArrayList<>();
    int batches = (replicas + batch - 1) / batch;
    for (int b = 0; b < batches; b++) {
        int low = b * batch + 1;
        int high = Math.min(replicas, (b + 1) * batch);
        trace.add("update:" + low + "-" + high);
        if (b < health.size() && health.get(b).equals("bad")) {
            trace.add("rollback:1-" + high);
            return trace;
        }
        trace.add("healthy:" + low + "-" + high);
    }
    trace.add("done");
    return trace;
}
'''
ROLL_BATCH_ONLY = ROLL_SOL.replace('trace.add("rollback:1-" + high);', 'trace.add("rollback:" + low + "-" + high);')
ROLL_KEEPS_GOING = ROLL_SOL.replace('            return trace;\n        }\n        trace.add("healthy', '        }\n        trace.add("healthy')
ROLL_FLOOR = ROLL_SOL.replace("(replicas + batch - 1) / batch", "replicas / batch")
ROLL_NO_VALIDATE = ROLL_SOL.replace('    if (replicas < 1 || batch < 1) {\n        return List.of("invalid");\n    }\n', "")
ROLL_BAD_IS_OK = ROLL_SOL.replace('health.get(b).equals("bad")', 'health.get(b).equals("worse")')

ex22.method(
    "write", "j11-l2.2-write-rollout", "A rolling update with health checks", ["o1"], ["J11.06"], ["IMPL"],
    "A rolling update replaces `replicas` copies of a service with a new version, `batch` at a time, numbered from 1. For each batch the trace has `update:LOW-HIGH`; then the batch is checked: `health` lists the result of each batch (`ok` or `bad`; batches beyond the list are `ok`). A healthy batch adds `healthy:LOW-HIGH`. A **bad** batch stops the rollout and rolls back **everything updated so far**, adding `rollback:1-HIGH`. If all batches are healthy, finish with `done`. If `replicas` or `batch` is below 1, return just `invalid`. Write `rolloutTrace(replicas, batch, health)`.",
    [("rolloutTrace", [("replicas", "int"), ("batch", "int"), ("health", "List<String>")], "List<String>")], {"rolloutTrace": f_rollout},
    [("rolloutTrace", (4, 2, []), "two batches, all fine"), ("rolloutTrace", (4, 2, ["ok", "bad"]), "the second batch is bad"), ("rolloutTrace", (0, 1, []), "nothing to update")],
    [("rolloutTrace", (5, 2, []), "a short last batch"), ("rolloutTrace", (5, 2, ["bad"]), "the first batch is bad"), ("rolloutTrace", (6, 6, []), "all at once"),
     ("rolloutTrace", (6, 1, ["ok", "ok", "bad", "ok"]), "one at a time, the third is bad"), ("rolloutTrace", (3, 0, []), "a batch size of zero"), ("rolloutTrace", (7, 3, ["ok", "ok", "ok"]), "three batches"),
     ("rolloutTrace", (2, 5, ["bad"]), "the batch is larger than the fleet")],
    starter='''
List<String> rolloutTrace(int replicas, int batch, List<String> health) {
    return List.of();
}
''', solution=ROLL_SOL,
    wrongs={"rolls-back-only-the-bad-batch": ROLL_BATCH_ONLY, "carries-on-after-a-bad-batch": ROLL_KEEPS_GOING, "drops-the-short-batch": ROLL_FLOOR, "no-validation": ROLL_NO_VALIDATE, "never-sees-bad": ROLL_BAD_IS_OK},
    hints=["Round the number of batches up.", "On a bad batch, stop immediately."],
    misconceptions=("MC210",), difficulty=3,
)

ex22.explain(
    "j11-l2.2-explain-strategies", "Choosing how to release", ["o2"], ["J11.06"],
    "Brightbank's payments service must be released several times a week without downtime, and a bad release must be undone in minutes. Compare a rolling update with a blue/green deployment for it: how each works, what each costs, what happens to database changes, and how the smoke test and rollback fit in. Say which you would choose for a team of four and why.",
    "A rolling update replaces instances in batches, checking health between batches; it needs no extra environment, but old and new versions run side by side during the rollout, so they must both work with the same database and API. A blue/green deployment runs the new version as a full second environment next to the current one, tests it (a smoke test) and then switches traffic over at once, so rollback is switching back; it costs a second full environment for the duration and still needs database changes that both versions tolerate. In both cases the database change should be backward compatible (expand and contract, Stage 12), a smoke test should check the new version before it takes real traffic or right after the first batch, and rollback should be automatic when the check fails. For a small team a rolling update is usually the simpler and cheaper choice, provided the versions can coexist.",
    levels={
        2: ("The answer describes both strategies with cost and database compatibility, places the smoke test and rollback, and makes a reasoned choice.", [
            "Rolling replaces instances in batches with health checks, cheap but old and new versions coexist for a while. Blue/green builds a second full environment, smoke-tests it, then switches traffic; rollback is switching back, but it costs a second environment. Both need backward-compatible database changes. The smoke test gates the switch or the next batch and a failure triggers rollback. For four people I would pick a rolling update, as long as the versions can coexist.",
            "Rolling: batches, health-checked, no extra environment, mixed versions. Blue/green: full parallel environment, instant switch and switch-back, double cost. Schema changes must work for both versions either way. Smoke test then automatic rollback. I would choose rolling for simplicity."]),
        1: ("The answer describes the strategies without the database point or the choice.", [
            "Rolling updates replace a few at a time; blue/green switches all at once.",
            "Blue/green is safer."]),
        0: ("The answer ignores rollback or compatibility.", [
            "Stop the service, deploy and start it again at night.",
            "Release without checking, tests passed already."]),
    },
)

l11_l2_2 = Lesson("j11-l2.2", "Deployment strategies and rollback", ["J11.06"], [
    ("o1", "Trace a rolling update with health checks and a rollback"),
    ("o2", "Compare rolling and blue/green releases and fit smoke tests and rollback into them"),
], ["j11-l2.1"], 40, ["I130"], """## Before you start

You should know what a pipeline does (lesson 11.2.1).

## Explanation

Passing the tests does not prove that a release works in production: the real configuration, data and traffic differ. So deployment itself needs a safe strategy, with a way back.

A **rolling update** replaces the running instances a batch at a time. After each batch it checks health; if the new version is unhealthy, it stops and rolls back what it changed. It needs no spare environment, but for a while old and new versions run together, so both must work with the same database and the same clients.

A **blue/green deployment** runs the new version (green) as a complete second environment alongside the current one (blue). You test green (a **smoke test**: a few quick requests proving the essentials work), then switch the traffic. Rollback is switching back. It costs a second environment while it lasts.

Whatever the strategy: make the database change **backward compatible** so the old version still works (the expand-and-contract technique of Stage 12), put a **smoke test** after the deploy, and make **rollback** automatic when it fails and fast to do by hand. The smoke test of the Compose run in lesson 11.1.3 (an HTTP 200 from `/api/curriculum`) is the smallest example.

## Worked examples

### Example 1: a rolling update of four replicas in batches of two.

`update:1-2, healthy:1-2, update:3-4, healthy:3-4, done`. If the second batch is bad: `update:3-4, rollback:1-4`, which returns all four to the old version.

### Example 2: rollback is part of the design.

If you cannot say how to go back, you do not yet have a deployment strategy.

## Where this is used

- Every production system. Orchestrators such as Kubernetes implement rolling updates and health checks for you; this course models the logic.

## Common mistakes

:::mistake{id=MC210}
**Treating rollback as an emergency procedure written when it is needed.** Design it and rehearse it. A schema change that cannot be undone defeats it.
:::

## Practice

::exercise{id=j11-l2.2-write-rollout}

::exercise{id=j11-l2.2-explain-strategies}

## Further reading

- **GitHub Docs, workflow syntax** `[I130]` for how a pipeline gates a deployment job.

## How you'll be assessed

- The **write** exercise checks the rollout logic (*implementation*).
- The **explain** exercise checks the comparison and the choice (*explanation*).

The descriptions of rolling and blue/green deployment are standard industry practice and are not quoted from a recorded source; no orchestrator was run for this course.
""")
print("module 11.2 authored")
