// INHERITED CODE: the account API's request handler, as found. Passwords are checked as typed.
// Requests: "LOGIN user password" or "actor METHOD path" (actor "-" means nobody is signed in).
// Audit scope: find what is wrong, fix it in two steps, and report what you found in the design note.

List<String> handleAll(List<String> requests) {
    Map<String, String[]> users = new HashMap<>();
    users.put("ada", new String[] {"secret1", "customer"});
    users.put("grace", new String[] {"hunter22", "customer"});
    users.put("tess", new String[] {"teller99", "teller"});
    Map<String, String[]> accounts = new HashMap<>();
    accounts.put("1", new String[] {"ada", "120000"});
    accounts.put("2", new String[] {"grace", "30050"});
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] parts = request.split(" ", 3);
        if (parts[0].equals("LOGIN")) {
            String user = parts.length > 1 ? parts[1] : "";
            String password = parts.length > 2 ? parts[2] : "";
            String[] known = users.get(user);
            if (known == null) {
                out.add("401|No such user");
            } else if (!known[0].equals(password)) {
                out.add("401|Wrong password");
            } else {
                out.add("200|ok");
            }
        } else {
            String method = parts.length > 1 ? parts[1] : "";
            String path = parts.length > 2 ? parts[2] : "";
            if (!path.matches("/accounts/[0-9]{1,9}")) {
                out.add("404|Not Found");
            } else if (!method.equals("GET")) {
                out.add("405|Method Not Allowed");
            } else {
                String id = String.valueOf(Integer.parseInt(path.substring("/accounts/".length())));
                String[] account = accounts.get(id);
                if (account == null) {
                    out.add("404|No account " + id + " in table accounts (SELECT * FROM accounts WHERE id=" + id + ")");
                } else {
                    out.add("200|" + id + ";" + account[0] + ";" + account[1]);
                }
            }
        }
    }
    return out;
}

void main() {
    // Optional: try your handler here.
}
