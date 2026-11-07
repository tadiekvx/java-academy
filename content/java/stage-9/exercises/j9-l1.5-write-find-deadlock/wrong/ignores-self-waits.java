List<String> findDeadlock(List<String> waits) {
    Map<String, Set<String>> graph = new HashMap<>();
    Set<String> nodes = new TreeSet<>();
    for (String edge : waits) {
        String[] parts = edge.split(">");
        graph.computeIfAbsent(parts[0], k -> new HashSet<>()).add(parts[1]);
        nodes.add(parts[0]);
        nodes.add(parts[1]);
    }
    List<String> stuck = new ArrayList<>();
    for (String start : nodes) {
        Set<String> seen = new HashSet<>();
        Deque<String> stack = new ArrayDeque<>(graph.getOrDefault(start, Set.of()));
        stack.remove(start);
        boolean cycle = false;
        while (!stack.isEmpty() && !cycle) {
            String next = stack.pop();
            if (next.equals(start)) {
                cycle = true;
            } else if (seen.add(next)) {
                stack.addAll(graph.getOrDefault(next, Set.of()));
            }
        }
        if (cycle) {
            stuck.add(start);
        }
    }
    return stuck;
}

void main() {
}
