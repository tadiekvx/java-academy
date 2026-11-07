String properties(String method) {
    return switch (method) {
        case "GET", "HEAD", "OPTIONS", "TRACE" -> "safe+idempotent";
        case "PUT", "DELETE" -> "idempotent";
        case "POST", "CONNECT" -> "neither";
        default -> "unknown";
    };
}

void main() {
}
