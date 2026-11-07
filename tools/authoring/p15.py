"""Stage 11 project: j11-p1-release-pipeline (B). A model of a release: gates, rolling deploy, smoke test, rollback."""
import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-11"
from proj import project

MAIN = "\nvoid main() {\n    // Optional: try your pipeline here.\n}\n"
SIG = [("release", [("version", "String"), ("outcomes", "List<String>")], "List<String>")]


def outcome(outcomes, key):
    for o in outcomes:
        k, v = o.split("=")
        if k == key:
            return v
    return "ok"


def model(version, outcomes, m=3):
    log = []
    for stage in ["build", "test", "scan", "push"]:
        r = outcome(outcomes, stage)
        log.append(f"{stage}:{r}")
        if r != "ok":
            log += ["stopped", "live=v1"]
            return log
    if m == 1:
        log += ["live=v1"]
        return log
    log.append("deploy:start")
    for b in (1, 2):
        log.append(f"update:batch{b}")
        if outcome(outcomes, f"batch{b}") == "bad":
            log += ["rollback", "live=v1"]
            return log
    log.append("deploy:done")
    if m == 2:
        log.append(f"live={version}")
        return log
    r = outcome(outcomes, "smoke")
    log.append(f"smoke:{r}")
    if r != "ok":
        log += ["rollback", "live=v1"]
        return log
    log.append(f"live={version}")
    return log


def fn1(version, outcomes):
    return model(version, outcomes, 1)


def fn2(version, outcomes):
    return model(version, outcomes, 2)


def fn3(version, outcomes):
    return model(version, outcomes, 3)


FINAL = '''
// A model of a release. "live=v1" is the version running before the release.
// outcomes is a list like "test=fail", "batch2=bad", "smoke=fail"; anything not listed succeeds.

List<String> release(String version, List<String> outcomes) {
    List<String> log = new ArrayList<>();
    for (String stage : List.of("build", "test", "scan", "push")) {
        String result = outcomeOf(outcomes, stage);
        log.add(stage + ":" + result);
        if (!result.equals("ok")) {
            log.add("stopped");
            log.add("live=v1");
            return log;
        }
    }
    log.add("deploy:start");
    for (int batch = 1; batch <= 2; batch++) {
        log.add("update:batch" + batch);
        if (outcomeOf(outcomes, "batch" + batch).equals("bad")) {
            log.add("rollback");
            log.add("live=v1");
            return log;
        }
    }
    log.add("deploy:done");
    String smoke = outcomeOf(outcomes, "smoke");
    log.add("smoke:" + smoke);
    if (!smoke.equals("ok")) {
        log.add("rollback");
        log.add("live=v1");
        return log;
    }
    log.add("live=" + version);
    return log;
}

String outcomeOf(List<String> outcomes, String key) {
    for (String outcome : outcomes) {
        String[] parts = outcome.split("=");
        if (parts[0].equals(key)) {
            return parts[1];
        }
    }
    return "ok";
}
'''
STARTER = '''
// A model of a release. "live=v1" is the version running before the release.
// outcomes is a list like "test=fail", "batch2=bad", "smoke=fail"; anything not listed succeeds.
//
// Milestone 1: the gates build, test, scan, push (stop at the first failure).
// Milestone 2: a rolling deploy in two batches.   Milestone 3: the smoke test and rollback.

List<String> release(String version, List<String> outcomes) {
    return List.of("live=v1");
}

String outcomeOf(List<String> outcomes, String key) {
    for (String outcome : outcomes) {
        String[] parts = outcome.split("=");
        if (parts[0].equals(key)) {
            return parts[1];
        }
    }
    return "ok";
}
'''


def wrong(old, new, src=FINAL):
    assert old in src, old
    return src.replace(old, new, 1)


WRONGS = {
    "m1-keeps-going-after-a-failure": wrong('            log.add("stopped");\n            log.add("live=v1");\n            return log;', '            log.add("stopped");'),
    "m1-gate-order-changed": wrong('List.of("build", "test", "scan", "push")', 'List.of("build", "scan", "test", "push")'),
    "m2-bad-batch-is-ignored": wrong('        if (outcomeOf(outcomes, "batch" + batch).equals("bad")) {\n            log.add("rollback");\n            log.add("live=v1");\n            return log;\n        }\n', ''),
    "m2-deploys-both-batches-at-once": wrong('    for (int batch = 1; batch <= 2; batch++) {\n        log.add("update:batch" + batch);', '    for (int batch = 1; batch <= 1; batch++) {\n        log.add("update:batch" + batch);'),
    "m3-no-smoke-test": wrong('    String smoke = outcomeOf(outcomes, "smoke");\n    log.add("smoke:" + smoke);\n    if (!smoke.equals("ok")) {\n        log.add("rollback");\n        log.add("live=v1");\n        return log;\n    }\n', ''),
    "m3-smoke-failure-keeps-the-new-version": wrong('    if (!smoke.equals("ok")) {\n        log.add("rollback");\n        log.add("live=v1");\n        return log;\n    }', '    if (!smoke.equals("ok")) {\n        log.add("rollback");\n        log.add("live=" + version);\n        return log;\n    }'),
}


def case(name, version, *outs):
    return ("release", (version, list(outs)), name)


M1V = [case("the tests fail", "v2", "test=fail"), case("the build fails", "v2", "build=fail"), case("the scan fails", "v2", "scan=fail")]
M1H = M1V + [case("the push fails", "v2", "push=fail"), case("two gates fail, only the first counts", "v3", "test=fail", "scan=fail"),
             case("a gate outcome with another word", "v2", "scan=warn"), case("a different version", "v10", "build=ok")]
M2V = [case("the second batch is bad", "v2", "batch2=bad"), case("the first batch is bad", "v2", "batch1=bad"), case("both batches are bad", "v2", "batch1=bad", "batch2=bad")]
M2H = M2V + M1H + [case("a gate failure means no deploy at all", "v2", "scan=fail", "batch1=bad"), case("the smoke result is irrelevant after a bad batch", "v2", "batch1=bad", "smoke=fail")]
M3V = [case("the whole release succeeds", "v2"), case("the smoke test fails", "v2", "smoke=fail"), case("the smoke test is ok explicitly", "v2", "smoke=ok")]
M3H = M3V + M2H + [case("smoke fails but batches fine", "v7", "smoke=fail"), case("only the smoke result is odd", "v2", "smoke=unknown"), case("a different version goes live", "v10")]
FNS = {"release": None}


def mk(rows, fn):
    return [("release", args, name) for (_, args, name) in rows], fn


ms = []
for mid, title, text, vis, hid, fn in [
    ("m1", "The gates", """
     A release goes through the gates `build`, `test`, `scan` and `push`, in that order. For each, add `stage:result` to the log (the result is `ok` unless `outcomes` says otherwise, as in `test=fail`). At the first result that is not `ok`, add `stopped` and `live=v1` (the old version stays live) and finish. The checks of this milestone are all releases that fail a gate; what happens when all four pass is the job of the next milestones.
     """, M1V, M1H, fn3),
    ("m2", "A rolling deploy", """
     After the gates pass, add `deploy:start` and update two batches in turn: add `update:batch1`, check `batch1` (the outcome `batch1=bad` means the new version is unhealthy there), then the same for batch 2. A bad batch adds `rollback` and `live=v1` and finishes. If both are healthy add `deploy:done` (milestone 3 adds the smoke test and the final `live=` line). The checks of this milestone are all releases with a bad batch.
     """, M2V, M2H, fn3),
    ("m3", "The smoke test and rollback", """
     After `deploy:done`, run the smoke test: add `smoke:` and its result (`ok` unless `smoke=fail` or another word is given). Only if it is `ok` does the new version go live: add `live=` followed by the new version. If it is not, add `rollback` and `live=v1`. A release that stopped earlier has no smoke test. From this milestone on, every release that passes everything ends with `live=` and the new version.
     """, M3V, M3H, fn3)]:
    ms.append(dict(id=mid, title=title, methods=SIG, fns={"release": fn}, instructions=text, visible=vis, hidden=hid))
RUBRIC = [
    ("Gates", "Later stages run after a failed gate", "Stops at a failure but leaves the wrong version live", "Stops at the first failure with the old version live, in the stated order"),
    ("Rollback", "A failed deploy or smoke test leaves the new version live", "Rolls back in one case only", "Every failure after the deploy starts ends with a rollback and the old version live"),
    ("Smoke test", "No check after the deploy", "A check that cannot fail the release", "A check after `deploy:done` that decides whether the version goes live"),
    ("Design note", "Missing, or repeats the instructions", "Describes the stages without trade-offs", "Maps each stage to a real tool (CI job, rolling update, health check, smoke test) and says what the model leaves out, honestly"),
]
project("j11-p1-release-pipeline", "A release you can undo", "B",
        "Model a release pipeline: quality gates, a rolling deploy with health checks, a smoke test and automatic rollback.",
        """
        You will write the decision logic of a release, the part that a CI/CD pipeline and an orchestrator carry out: run the gates in order, update the service in two batches, smoke-test the result, and go back to the old version whenever something fails after the deploy has started.

        This course had no CI server and no cloud account, so the project models the logic in plain Java; lessons 11.2.1 and 11.2.2 show the real tools. In your design note, say which real tool does each stage and what the model leaves out.
        """, 3, ["j11-l2.1", "j11-l2.2"], ["J11.05", "J11.06"],
        ["The gates run in order and stop at the first failure.", "A bad batch ends the deploy with a rollback.", "A failed smoke test ends with a rollback and the old version live."],
        ["Plain Java only.", "Run all the checks after each milestone."],
        ["Given a failing gate, then the old version stays live.", "Given a bad batch, then the log ends with a rollback.", "Given a failed smoke test, then the new version is not live."],
        ms, RUBRIC,
        "In 150 words or fewer: For each stage of your release (gates, deploy, smoke test, rollback) name the real tool or feature that would do it (for example a CI job with `needs`, an orchestrator's rolling update, a health check) and say one thing this model leaves out that a real release must handle, such as database changes or traffic switching.",
        STARTER + MAIN, FINAL + MAIN, {k: v + MAIN for k, v in WRONGS.items()})
print("P15 written")
