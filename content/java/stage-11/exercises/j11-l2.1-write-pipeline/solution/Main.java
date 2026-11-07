List<String> runPipeline(List<String> jobs, List<String> needs, String failing) {
    Map<String, List<String>> deps = new TreeMap<>();
    for (String job : jobs) {
        deps.computeIfAbsent(job, k -> new ArrayList<>());
    }
    for (String edge : needs) {
        String[] p = edge.split(">");
        deps.computeIfAbsent(p[0], k -> new ArrayList<>()).add(p[1]);
        deps.computeIfAbsent(p[1], k -> new ArrayList<>());
    }
    Map<String, String> status = new HashMap<>();
    List<String> out = new ArrayList<>();
    List<String> remaining = new ArrayList<>(deps.keySet());
    while (!remaining.isEmpty()) {
        String next = null;
        for (String job : remaining) {
            if (status.keySet().containsAll(deps.get(job))) {
                next = job;
                break;
            }
        }
        if (next == null) {
            return List.of("cycle");
        }
        boolean blocked = false;
        for (String dep : deps.get(next)) {
            if (!status.get(dep).equals("ok")) {
                blocked = true;
            }
        }
        String result = blocked ? "skipped" : next.equals(failing) ? "failed" : "ok";
        status.put(next, result);
        out.add(result + ":" + next);
        remaining.remove(next);
    }
    return out;
}

void main() {
}
