// INHERITED CODE: the account API of the partner company Brightbank has bought, as found.
// Request: "actor METHOD path [body words]". Actor "-" means nobody is signed in.
// Users: ada and grace (customers) and tess (a teller). Accounts 1 (ada), 2 (grace), 3 (ada) start at 1000.
//
// Your job over four changes (see the milestones): add transfers, make them reliable, make the service
// observable, and handle the incident that follows.

List<String> handleAll(List<String> requests) {
    Map<String, String> owners = Map.of("1", "ada", "2", "grace", "3", "ada");
    Map<String, Integer> balance = new TreeMap<>(Map.of("1", 1000, "2", 1000, "3", 1000));
    Set<String> users = Set.of("ada", "grace", "tess");
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        try {
            String[] t = request.split(" ", -1);
            if (t.length < 3) {
                out.add("400|Bad Request");
            } else if (!users.contains(t[0])) {
                out.add("401|Unauthorized");
            } else if (t[2].matches("/accounts/[0-9]{1,9}")) {
                if (!t[1].equals("GET")) {
                    out.add("405|Method Not Allowed");
                } else {
                    String id = String.valueOf(Integer.parseInt(t[2].substring("/accounts/".length())));
                    if (!owners.containsKey(id)) {
                        out.add("404|Not Found");
                    } else if (t[0].equals("tess") || owners.get(id).equals(t[0])) {
                        out.add("200|" + id + ";" + owners.get(id) + ";" + balance.get(id));
                    } else {
                        out.add("403|Forbidden");
                    }
                }
            } else {
                out.add("404|Not Found");
            }
        } catch (Exception e) {
            out.add("500|Internal Server Error");
        }
    }
    return out;
}

List<String> auditLines(List<String> requests) {
    return new ArrayList<>();
}

void main() {
    // Optional: try your handler here.
}
