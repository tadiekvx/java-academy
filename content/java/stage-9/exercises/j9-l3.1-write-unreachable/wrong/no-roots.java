List<String> unreachable(List<String> edges, List<String> roots) {
    Map<String, List<String>> graph = new HashMap<>();
    Set<String> objects = new TreeSet<>(roots);
    for (String edge : edges) {
        String[] parts = edge.split(">");
        graph.computeIfAbsent(parts[0], k -> new ArrayList<>()).add(parts[1]);
        objects.add(parts[0]);
        objects.add(parts[1]);
    }
    Set<String> marked = new HashSet<>();
    Deque<String> work = new ArrayDeque<>();
    while (!work.isEmpty()) {
        String next = work.pop();
        if (marked.add(next)) {
            work.addAll(graph.getOrDefault(next, List.of()));
        }
    }
    List<String> garbage = new ArrayList<>();
    for (String object : objects) {
        if (!marked.contains(object)) {
            garbage.add(object);
        }
    }
    return garbage;
}

void main() {
}
