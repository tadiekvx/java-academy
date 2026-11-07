String owaspFor(String weakness) {
    return switch (weakness) {
        case "missing-ownership-check" -> "A07 Authentication Failures";
        case "sql-built-from-input" -> "A05 Injection";
        case "no-login-lockout" -> "A01 Broken Access Control";
        case "failed-logins-not-logged" -> "A09 Security Logging and Alerting Failures";
        case "vulnerable-dependency" -> "A03 Software Supply Chain Failures";
        default -> "unmapped";
    };
}

void main() {
}
