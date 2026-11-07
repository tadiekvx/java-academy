// The transfer endpoint. Requests: "key from to cents" with an optional last word "crash" (the credit step fails).

List<String> handleAll(List<String> requests) {
    Map<String, Integer> balance = new TreeMap<>(Map.of("a", 1000, "b", 1000, "c", 1000));
    Map<String, String[]> seen = new HashMap<>();
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] p = request.split(" ");
        if ((p.length != 4 && p.length != 5) || (p.length == 5 && !p[4].equals("crash")) || !p[3].matches("[0-9]{1,9}")) {
            out.add("400|Bad Request");
            continue;
        }
        String key = p[0];
        String from = p[1];
        String to = p[2];
        int cents = Integer.parseInt(p[3]);
        String body = from + ">" + to + ":" + cents;
        if (seen.containsKey(key)) {
            String[] first = seen.get(key);
            out.add(first[0].equals(body) ? first[1] : "409|Conflict");
            continue;
        }
        if (!balance.containsKey(from) || !balance.containsKey(to) || from.equals(to) || cents <= 0) {
            out.add("400|Bad Request");
            continue;
        }
        if (balance.get(from) < cents) {
            String response = "422|Insufficient funds";
            seen.put(key, new String[] {body, response});
            out.add(response);
            continue;
        }
        balance.merge(from, -cents, Integer::sum);
        if (p.length == 5) {
            balance.merge(from, cents, Integer::sum);
            out.add("502|Credit failed, debit reversed");
            continue;
        }
        balance.merge(to, cents, Integer::sum);
        String response = "200|a=" + balance.get("a") + ";b=" + balance.get("b") + ";c=" + balance.get("c");
        seen.put(key, new String[] {body, response});
        out.add(response);
    }
    return out;
}

void main() {
    // Optional: try your handler here.
}
