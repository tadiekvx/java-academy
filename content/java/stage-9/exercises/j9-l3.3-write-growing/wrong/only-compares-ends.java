List<String> growingClasses(List<String> snapshots) {
    List<Map<String, Integer>> parsed = new ArrayList<>();
    for (String snapshot : snapshots) {
        Map<String, Integer> counts = new HashMap<>();
        for (String part : snapshot.split(",")) {
            if (!part.isEmpty()) {
                String[] pair = part.split("=");
                counts.put(pair[0], Integer.parseInt(pair[1]));
            }
        }
        parsed.add(counts);
    }
    List<String> growing = new ArrayList<>();
    if (parsed.size() < 2) {
        return growing;
    }
    for (String name : parsed.get(0).keySet()) {
        boolean always = true;
        for (int i = 0; i + 1 < parsed.size() && always; i += parsed.size() - 1) {
            Integer now = parsed.get(i).get(name);
            Integer next = parsed.get(i + 1).get(name);
            always = now != null && next != null && now < next;
        }
        if (always) {
            growing.add(name);
        }
    }
    Collections.sort(growing);
    return growing;
}

void main() {
}
