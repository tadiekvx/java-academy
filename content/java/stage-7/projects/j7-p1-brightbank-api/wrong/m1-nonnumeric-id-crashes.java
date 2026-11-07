// Brightbank's API layer as a plain-Java request handler. Each request is "METHOD path body" (the body may be absent).
// Each response is "status|body". Two accounts exist at the start; money is whole cents.

List<String> handleAll(List<String> requests) {
    Map<Integer, String[]> accounts = new TreeMap<>();
    accounts.put(1, new String[] {"Ada Lovelace", "120000"});
    accounts.put(2, new String[] {"Grace Hopper", "30050"});
    int[] nextId = {3};
    List<String> responses = new ArrayList<>();
    for (String request : requests) {
        responses.add(handle(request, accounts, nextId));
    }
    return responses;
}

String handle(String request, Map<Integer, String[]> accounts, int[] nextId) {
    String[] parts = request.split(" ", 3);
    String method = parts[0];
    String path = parts.length > 1 ? parts[1] : "";
    String body = parts.length > 2 ? parts[2] : "";
    String[] p = path.split("/", -1);
    if (p.length < 2 || !p[0].isEmpty() || !p[1].equals("accounts")) {
        return "404|Not Found";
    }
    if (p.length == 2) {
        return switch (method) {
            case "GET" -> "200|" + String.join(",", accounts.keySet().stream().map(String::valueOf).toList());
            case "POST" -> create(body, accounts, nextId);
            default -> "405|Method Not Allowed";
        };
    }
    int id = Integer.parseInt(p[2]);
    if (p.length == 3) {
        return switch (method) {
            case "GET" -> accounts.containsKey(id) ? "200|" + describe(id, accounts) : "404|Not Found";
            case "DELETE" -> accounts.remove(id) != null ? "204|" : "404|Not Found";
            case "PUT" -> replace(id, body, accounts, nextId);
            default -> "405|Method Not Allowed";
        };
    }
    if (p.length == 4 && p[3].equals("deposit")) {
        return method.equals("POST") ? deposit(id, body, accounts) : "405|Method Not Allowed";
    }
    return "404|Not Found";
}

String[] parseAccount(String body) {
    String[] fields = body.split(";", -1);
    if (fields.length != 2 || fields[0].isBlank() || !fields[1].matches("[0-9]{1,9}")) {
        return null;
    }
    return fields;
}

String describe(int id, Map<Integer, String[]> accounts) {
    return id + ";" + accounts.get(id)[0] + ";" + accounts.get(id)[1];
}

String create(String body, Map<Integer, String[]> accounts, int[] nextId) {
    String[] fields = parseAccount(body);
    if (fields == null) {
        return "400|Bad Request";
    }
    int id = nextId[0]++;
    accounts.put(id, new String[] {fields[0], String.valueOf(Integer.parseInt(fields[1]))});
    return "201|/accounts/" + id;
}

String replace(int id, String body, Map<Integer, String[]> accounts, int[] nextId) {
    String[] fields = parseAccount(body);
    if (fields == null) {
        return "400|Bad Request";
    }
    boolean created = !accounts.containsKey(id);
    accounts.put(id, new String[] {fields[0], String.valueOf(Integer.parseInt(fields[1]))});
    nextId[0] = Math.max(nextId[0], id + 1);
    return (created ? "201|" : "200|") + describe(id, accounts);
}

String deposit(int id, String body, Map<Integer, String[]> accounts) {
    if (!accounts.containsKey(id)) {
        return "404|Not Found";
    }
    if (!body.matches("[0-9]{1,9}") || Integer.parseInt(body) <= 0) {
        return "400|Bad Request";
    }
    long balance = Long.parseLong(accounts.get(id)[1]) + Integer.parseInt(body);
    accounts.get(id)[1] = String.valueOf(balance);
    return "200|" + balance;
}

void main() {
    // Optional: try your handler here.
}
