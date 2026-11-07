List<String> processTransfers(List<String> requests) {
    Map<String, Integer> balance = new TreeMap<>(Map.of("a", 1000, "b", 1000, "c", 1000));
    Map<String, String[]> seen = new HashMap<>();
    List<String> results = new ArrayList<>();
    for (String request : requests) {
        String[] p = request.split(":");
        String key = p[0];
        String body = p[1] + ">" + p[2] + ":" + Integer.parseInt(p[3]);
        int cents = Integer.parseInt(p[3]);
        if (seen.containsKey(key)) {
            String[] old = seen.get(key);
            results.add(old[0].equals(body) ? "dup:" + old[1] : "conflict");
            continue;
        }
        if (!balance.containsKey(p[1]) || !balance.containsKey(p[2]) || p[1].equals(p[2]) || cents <= 0) {
            seen.put(key, new String[] {body, "invalid"});
            results.add("invalid");
            continue;
        }
        if (balance.get(p[1]) < cents) {
            seen.put(key, new String[] {body, "rejected"});
            results.add("rejected");
            continue;
        }
        balance.merge(p[1], -cents, Integer::sum);
        balance.merge(p[2], cents, Integer::sum);
        seen.put(key, new String[] {body, "applied"});
        results.add("applied");
    }
    results.add("a=" + balance.get("a") + ";b=" + balance.get("b") + ";c=" + balance.get("c"));
    return results;
}

void main() {
}
