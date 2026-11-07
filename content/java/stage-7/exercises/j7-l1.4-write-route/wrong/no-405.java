String route(String method, String path) {
    String[] p = path.split("/", -1);
    if (p.length < 2 || !p[0].isEmpty() || !p[1].equals("accounts")) {
        return "not-found";
    }
    if (p.length == 2) {
        return switch (method) {
            case "GET" -> "list-accounts";
            case "POST" -> "create-account";
            default -> "not-found";
        };
    }
    if (!p[2].matches("[0-9]+")) {
        return "not-found";
    }
    String id = p[2];
    if (p.length == 3) {
        return switch (method) {
            case "GET" -> "get-account:" + id;
            case "DELETE" -> "delete-account:" + id;
            case "PUT" -> "replace-account:" + id;
            default -> "not-found";
        };
    }
    if (p.length == 4 && p[3].equals("transactions")) {
        return method.equals("GET") ? "list-transactions:" + id : "not-found";
    }
    return "not-found";
}

void main() {
}
