class Gate implements AutoCloseable {
    private final List<String> log;
    private final String name;

    Gate(List<String> log, String name) {
        this.log = log;
        this.name = name;
        log.add("open " + name);
    }

    @Override
    public void close() {
        log.add("closed " + name);
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
