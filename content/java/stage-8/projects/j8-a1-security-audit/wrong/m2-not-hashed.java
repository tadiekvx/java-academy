import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

// The request handler of Brightbank's account API, after the audit.
// Requests: "LOGIN user password" or "actor METHOD path" (actor "-" means nobody is signed in).

List<String> handleAll(List<String> requests) throws Exception {
    Map<String, String[]> users = new HashMap<>();
    users.put("ada", newUser("ada", "secret1", "customer"));
    users.put("grace", newUser("grace", "hunter22", "customer"));
    users.put("tess", newUser("tess", "teller99", "teller"));
    Map<String, String[]> accounts = new HashMap<>();
    accounts.put("1", new String[] {"ada", "120000"});
    accounts.put("2", new String[] {"grace", "30050"});
    Map<String, Integer> failures = new HashMap<>();
    List<String> out = new ArrayList<>();
    for (String request : requests) {
        String[] parts = request.split(" ", 3);
        if (parts[0].equals("LOGIN")) {
            out.add(login(parts.length > 1 ? parts[1] : "", parts.length > 2 ? parts[2] : "", users, failures));
        } else {
            out.add(read(parts, users, accounts));
        }
    }
    return out;
}

String[] newUser(String name, String password, String role) throws Exception {
    return new String[] {pbkdf2(password, name), role};
}

String pbkdf2(String password, String salt) throws Exception {
    PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt.getBytes(StandardCharsets.UTF_8), 1000, 256);
    byte[] key = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
    return HexFormat.of().formatHex(key);
}

String login(String user, String password, Map<String, String[]> users, Map<String, Integer> failures) throws Exception {
    String generic = "401|Invalid credentials";
    String[] known = users.get(user);
    if (known == null) {
        return generic;
    }
    int failed = failures.getOrDefault(user, 0);
    if (failed >= 3) {
        return generic;
    }
    byte[] attempt = pbkdf2(password, user).getBytes(StandardCharsets.UTF_8);
    if (Arrays.equals(attempt, known[0].getBytes(StandardCharsets.UTF_8))) {
        failures.put(user, 0);
        return "200|ok";
    }
    failures.put(user, failed + 1);
    return generic;
}

String read(String[] parts, Map<String, String[]> users, Map<String, String[]> accounts) {
    String actor = parts[0];
    String method = parts.length > 1 ? parts[1] : "";
    String path = parts.length > 2 ? parts[2] : "";
    if (!users.containsKey(actor)) {
        return "401|Unauthorized";
    }
    if (!path.matches("/accounts/[0-9]{1,9}")) {
        return "404|Not Found";
    }
    if (!method.equals("GET")) {
        return "405|Method Not Allowed";
    }
    String id = String.valueOf(Integer.parseInt(path.substring("/accounts/".length())));
    String[] account = accounts.get(id);
    if (account == null) {
        return "404|Not Found";
    }
    if (users.get(actor)[1].equals("teller") || account[0].equals(actor)) {
        return "200|" + id + ";" + account[0] + ";" + account[1];
    }
    return "403|Forbidden";
}

void main() {
    // Optional: try your handler here.
}
