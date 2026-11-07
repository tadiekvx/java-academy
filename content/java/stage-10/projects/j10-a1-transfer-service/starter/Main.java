// INHERITED CODE: the transfer endpoint, as found. Requests: "key from to cents" with an optional last word
// "crash", which makes the credit step of that attempt fail (the second service is down).
// Ticket 1001: "Customers are charged twice when their phone retries a transfer."
// Ticket 1002: "When the credit fails the money has gone from the sender and arrived nowhere."

List<String> handleAll(List<String> requests) {
    Map<String, Integer> balance = new TreeMap<>(Map.of("a", 1000, "b", 1000, "c", 1000));
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] p = request.split(" ");
        if ((p.length != 4 && p.length != 5) || (p.length == 5 && !p[4].equals("crash")) || !p[3].matches("[0-9]{1,9}")) {
            out.add("400|Bad Request");
            continue;
        }
        String from = p[1];
        String to = p[2];
        int cents = Integer.parseInt(p[3]);
        if (!balance.containsKey(from) || !balance.containsKey(to) || from.equals(to) || cents <= 0) {
            out.add("400|Bad Request");
            continue;
        }
        if (balance.get(from) < cents) {
            out.add("422|Insufficient funds");
            continue;
        }
        balance.merge(from, -cents, Integer::sum);
        if (p.length == 5) {
            out.add("500|Internal Server Error");
            continue;
        }
        balance.merge(to, cents, Integer::sum);
        out.add("200|a=" + balance.get("a") + ";b=" + balance.get("b") + ";c=" + balance.get("c"));
    }
    return out;
}

void main() {
    // Optional: try your handler here.
}
