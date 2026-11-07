List<String> unreachable(List<String> edges, List<String> roots) {
    Set<String> objects = new TreeSet<>(roots);
    Set<String> referenced = new HashSet<>();
    for (String edge : edges) {
        String[] parts = edge.split(">");
        objects.add(parts[0]);
        objects.add(parts[1]);
        referenced.add(parts[1]);
    }
    List<String> garbage = new ArrayList<>();
    for (String object : objects) {
        if (!referenced.contains(object) && !roots.contains(object)) {
            garbage.add(object);
        }
    }
    return garbage;
}

void main() {
}
