List<String> creationOrder(List<String> edges, String target) {
    Map<String, List<String>> deps = new HashMap<>();
    for (String edge : edges) {
        String[] parts = edge.split(">");
        deps.computeIfAbsent(parts[0], k -> new ArrayList<>()).add(parts[1]);
    }
    List<String> order = new ArrayList<>();
    if (!visit(target, deps, new HashSet<>(), new HashSet<>(), order)) {
        return List.of("cycle");
    }
    return order;
}

boolean visit(String bean, Map<String, List<String>> deps, Set<String> visiting, Set<String> done, List<String> order) {
    if (done.contains(bean)) {
        return true;
    }
    if (!visiting.add(bean)) {
        return false;
    }
    List<String> wanted = new ArrayList<>(deps.getOrDefault(bean, List.of()));
    for (String dependency : wanted) {
        if (!visit(dependency, deps, visiting, done, order)) {
            return false;
        }
    }
    visiting.remove(bean);
    done.add(bean);
    order.add(bean);
    return true;
}

void main() {
}
