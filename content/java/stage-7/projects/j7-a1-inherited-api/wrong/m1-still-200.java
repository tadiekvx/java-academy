// The request handler of the accounts API. Each request is "METHOD path body".

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
        if (path.equals("/accounts")) {
            if (method.equals("GET")) {
                out.add("200|" + String.join(",", accounts.keySet().stream().map(String::valueOf).toList()));
            } else if (method.equals("POST")) {
                String[] f = body.split(";", -1);
                if (f.length != 2 || f[0].isBlank() || !f[1].matches("[0-9]{1,9}")) {
                    out.add("400|Bad Request");
                } else {
                    accounts.put(nextId, new String[] {f[0], String.valueOf(Integer.parseInt(f[1]))});
                    out.add("200|/accounts/" + nextId);
                    nextId++;
                }
            } else {
                out.add("405|Method Not Allowed");
            }
        } else if (path.matches("/accounts/[0-9]{1,9}")) {
            int id = Integer.parseInt(path.substring("/accounts/".length()));
            if (!method.equals("GET")) {
                out.add("405|Method Not Allowed");
            } else if (!accounts.containsKey(id)) {
                out.add("404|Not Found");
            } else {
                out.add("200|" + id + ";" + accounts.get(id)[0] + ";" + accounts.get(id)[1]);
            }
        } else {
            out.add("404|Not Found");
        }
    }
    return out;
}

void main() {
    // Optional: try your handler here.
}
