// A model of a release. "live=v1" is the version running before the release.
// outcomes is a list like "test=fail", "batch2=bad", "smoke=fail"; anything not listed succeeds.

List<String> release(String version, List<String> outcomes) {
    List<String> log = new ArrayList<>();
    for (String stage : List.of("build", "scan", "test", "push")) {
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

void main() {
    // Optional: try your pipeline here.
}
