String owaspFor(String weakness) {
    return switch (weakness) {
        case "missing-ownership-check" -> "A01 Broken Access Control";
        case "sql-built-from-input" -> "A05 Injection";
        case "no-login-lockout" -> "A07 Authentication Failures";
        case "failed-logins-not-logged" -> "A09 Security Logging and Alerting Failures";
        case "vulnerable-dependency" -> "A03 Software Supply Chain Failures";
        default -> "A02 Security Misconfiguration";
    };
}

void main() {
}
