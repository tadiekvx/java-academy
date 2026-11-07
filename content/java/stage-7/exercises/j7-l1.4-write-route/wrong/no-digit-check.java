String route(String method, String path) {
    String[] p = path.split("/", -1);
    if (p.length < 2 || !p[0].isEmpty() || !p[1].equals("accounts")) {
        return "not-found";
    }
    if (p.length == 2) {
        return switch (method) {
            case "GET" -> "list-accounts";
            case "POST" -> "create-account";
            default -> "method-not-allowed";
        };
    }
    String id = p[2];
    if (p.length == 3) {
        return switch (method) {
            case "GET" -> "get-account:" + id;
            case "DELETE" -> "delete-account:" + id;
            case "PUT" -> "replace-account:" + id;
            default -> "method-not-allowed";
        };
    }
    if (p.length == 4 && p[3].equals("transactions")) {
        return method.equals("GET") ? "list-transactions:" + id : "method-not-allowed";
    }
    return "not-found";
}

void main() {
}
