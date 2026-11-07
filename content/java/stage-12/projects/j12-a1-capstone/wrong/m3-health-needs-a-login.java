// Brightbank's API handler. Request: "actor METHOD path [body words]". Actor "-" means nobody is signed in.
// Users: ada and grace (customers) and tess (a teller). Accounts 1 (ada), 2 (grace), 3 (ada) start at 1000.

List<String> handleAll(List<String> requests) {
    Map<String, String> owners = new HashMap<>(Map.of("1", "ada", "2", "grace", "3", "ada"));
    Map<String, Integer> balance = new TreeMap<>(Map.of("1", 1000, "2", 1000, "3", 1000));
    Set<String> users = Set.of("ada", "grace", "tess");
    Map<String, String[]> seen = new HashMap<>();
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        out.add(handle(request, owners, balance, users, seen));
    }
    return out;
}

String handle(String request, Map<String, String> owners, Map<String, Integer> balance, Set<String> users, Map<String, String[]> seen) {
    String[] t = request.split(" ", -1);
    if (t.length < 3) {
        return "400|Bad Request";
    }
    String actor = t[0];
    String method = t[1];
    String path = t[2];
    if (!users.contains(actor)) {
        return "401|Unauthorized";
    }
    if (path.equals("/health")) {
        return method.equals("GET") ? "200|ok" : "405|Method Not Allowed";
    }
    if (path.matches("/accounts/[0-9]{1,9}")) {
        if (!method.equals("GET")) {
            return "405|Method Not Allowed";
        }
        String id = String.valueOf(Integer.parseInt(path.substring("/accounts/".length())));
        if (!owners.containsKey(id)) {
            return "404|Not Found";
        }
        if (actor.equals("tess") || owners.get(id).equals(actor)) {
            return "200|" + id + ";" + owners.get(id) + ";" + balance.get(id);
        }
        return "403|Forbidden";
    }
    if (path.equals("/transfers")) {
        if (!method.equals("POST")) {
            return "405|Method Not Allowed";
        }
        return transfer(actor, Arrays.copyOfRange(t, 3, t.length), owners, balance, seen);
    }
    return "404|Not Found";
}

String transfer(String actor, String[] b, Map<String, String> owners, Map<String, Integer> balance, Map<String, String[]> seen) {
    if ((b.length != 4 && b.length != 5) || (b.length == 5 && !b[4].equals("crash")) || !b[3].matches("[0-9]{1,9}")) {
        return "400|Bad Request";
    }
    String key = b[0];
    String from = b[1];
    String to = b[2];
    int cents = Integer.parseInt(b[3]);
    String body = from + ">" + to + ":" + cents;
    if (seen.containsKey(key)) {
        String[] first = seen.get(key);
        return first[0].equals(body) ? first[1] : "409|Conflict";
    }
    if (!balance.containsKey(from) || !balance.containsKey(to) || from.equals(to) || cents <= 0) {
        return "400|Bad Request";
    }
    if (!actor.equals("tess") && !owners.get(from).equals(actor)) {
        return "403|Forbidden";
    }
    if (balance.get(from) < cents) {
        String response = "422|Insufficient funds";
        seen.put(key, new String[] {body, response});
        return response;
    }
    if (b.length == 5) {
        return "502|Credit failed, debit reversed";
    }
    balance.merge(from, -cents, Integer::sum);
    balance.merge(to, cents, Integer::sum);
    List<String> parts = new ArrayList<>();
    for (Map.Entry<String, Integer> entry : balance.entrySet()) {
        parts.add(entry.getKey() + ":" + entry.getValue());
    }
    String response = "200|" + String.join(";", parts);
    seen.put(key, new String[] {body, response});
    return response;
}

List<String> auditLines(List<String> requests) {
    List<String> responses = handleAll(requests);
    List<String> lines = new ArrayList<>();
    for (int i = 0; i < requests.size(); i++) {
        String[] t = requests.get(i).split(" ", -1);
        String actor = t.length > 0 ? t[0] : "";
        String method = t.length > 1 ? t[1] : "";
        String path = t.length > 2 ? t[2] : "";
        String status = responses.get(i).substring(0, responses.get(i).indexOf('|'));
        lines.add("{\"actor\":" + quote(actor) + ",\"method\":" + quote(method) + ",\"path\":" + quote(path) + ",\"status\":" + status + "}");
    }
    return lines;
}

String quote(String text) {
    return "\"" + text.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
}

void main() {
    // Optional: try your handler here.
}
