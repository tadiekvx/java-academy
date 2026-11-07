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

void main() {
    // Optional: try your pipeline here.
}
