String properties(String method) {
    return switch (method) {
        case "GET", "HEAD", "OPTIONS", "TRACE" -> "safe+idempotent";
        case "PUT", "DELETE", "POST" -> "idempotent";
        case "CONNECT" -> "neither";
        default -> "unknown";
    };
}

void main() {
}
