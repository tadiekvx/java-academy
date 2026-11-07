String csrfDecision(String method, boolean tokenPresent, boolean tokenMatches) {
    if (List.of("GET", "HEAD", "OPTIONS", "TRACE").contains(method.toUpperCase())) {
        return "allow";
    }
    return tokenPresent && tokenMatches ? "allow" : "reject";
}

void main() {
}
