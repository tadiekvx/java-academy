String properties(String method) {
    return switch (method) {
        case "GET", "HEAD", "OPTIONS", "TRACE" -> "safe+idempotent";
        case "PUT" -> "idempotent";
        case "POST", "CONNECT", "DELETE" -> "neither";
        default -> "unknown";
    };
}

void main() {
}
