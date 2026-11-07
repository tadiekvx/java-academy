List<String> plan(List<String> desired, List<String> current) {
    Map<String, String> want = new TreeMap<>();
    Map<String, String> have = new TreeMap<>();
    for (String item : desired) {
        want.put(item.substring(0, item.indexOf('=')), item.substring(item.indexOf('=') + 1));
    }
    for (String item : current) {
        have.put(item.substring(0, item.indexOf('=')), item.substring(item.indexOf('=') + 1));
    }
    Set<String> names = new TreeSet<>(want.keySet());
    names.addAll(have.keySet());
    List<String> changes = new ArrayList<>();
    for (String name : names) {
        if (want.containsKey(name) && !have.containsKey(name)) {
            changes.add("+ " + name);
        } else if (have.containsKey(name) && !want.containsKey(name)) {
            changes.add("- " + name);
        } else if (true) {
            changes.add("~ " + name);
        }
    }
    return changes;
}

void main() {
}
