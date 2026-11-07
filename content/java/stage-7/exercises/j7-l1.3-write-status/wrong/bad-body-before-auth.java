int status(String op, boolean authenticated, boolean exists, boolean valid) {
    if (!List.of("GET", "POST", "PUT", "DELETE").contains(op)) {
        return 405;
    }
    if (!authenticated && valid) {
        return 401;
    }
    return switch (op) {
        case "GET" -> exists ? 200 : 404;
        case "DELETE" -> exists ? 204 : 404;
        case "POST" -> !valid ? 400 : exists ? 409 : 201;
        default -> !valid ? 400 : exists ? 200 : 201;
    };
}

void main() {
}
