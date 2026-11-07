String checkPhases(List<String> phases) {
    Map<String, List<String>> needs = Map.of(
            "dual-write", List.of("add-new-column"),
            "backfill", List.of("add-new-column"),
            "switch-reads", List.of("backfill", "dual-write"),
            "stop-writing-old", List.of("switch-reads"),
            "drop-old-column", List.of("switch-reads", "stop-writing-old"));
    Set<String> done = new HashSet<>();
    for (String phase : phases) {
        for (String need : needs.getOrDefault(phase, List.of())) {
            if (!done.contains(need)) {
                return "unsafe:" + phase + " needs " + need;
            }
        }
        done.add(phase);
    }
    return "safe";
}

void main() {
}
