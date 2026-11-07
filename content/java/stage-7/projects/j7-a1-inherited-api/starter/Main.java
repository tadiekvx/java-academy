// INHERITED CODE: the request handler of an older accounts API. Each request is "METHOD path body".
// Ticket 701: "Creating an account answers 200. Clients expect 201."
// Ticket 702: "Asking for an account that does not exist crashes with a 500."

List<String> handleAll(List<String> requests) {
    Map<Integer, String[]> accounts = new TreeMap<>();
    accounts.put(1, new String[] {"Ada Lovelace", "120000"});
    accounts.put(2, new String[] {"Grace Hopper", "30050"});
    int nextId = 3;
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] parts = request.split(" ", 3);
        String method = parts[0];
        String path = parts[1];
        String body = parts.length > 2 ? parts[2] : "";
        try {
            if (path.equals("/accounts") && method.equals("GET")) {
                out.add("200|" + String.join(",", accounts.keySet().stream().map(String::valueOf).toList()));
            } else if (path.equals("/accounts") && method.equals("POST")) {
                String[] f = body.split(";", -1);
                if (f.length != 2 || f[0].isBlank() || !f[1].matches("[0-9]{1,9}")) {
                    out.add("400|Bad Request");
                } else {
                    accounts.put(nextId, new String[] {f[0], String.valueOf(Integer.parseInt(f[1]))});
                    out.add("200|/accounts/" + nextId);
                    nextId++;
                }
            } else if (path.startsWith("/accounts/") && method.equals("GET")) {
                int id = Integer.parseInt(path.substring("/accounts/".length()));
                String[] a = accounts.get(id);
                out.add("200|" + id + ";" + a[0] + ";" + a[1]);
            } else {
                out.add("404|Not Found");
            }
        } catch (Exception e) {
            out.add("500|Internal Server Error");
        }
    }
    return out;
}

void main() {
    // Optional: try your handler here.
}
