// Write the class Gate here.

class Gate {
    Gate(List<String> log, String name) {
    }
}

String run(String first, String second, boolean fail) {
    List<String> log = new ArrayList<>();
    try (Gate a = new Gate(log, first); Gate b = new Gate(log, second)) {
        log.add("work");
        if (fail) {
            throw new IllegalStateException("boom");
        }
    } catch (IllegalStateException e) {
        log.add("caught");
    }
    return String.join(",", log);
}

void main() {
}
