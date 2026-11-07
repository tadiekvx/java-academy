String csrfDecision(String method, boolean tokenPresent, boolean tokenMatches) {
    if (List.of("GET", "HEAD", "OPTIONS", "TRACE").contains(method)) {
        return "allow";
    }
    return tokenPresent ? "allow" : "reject";
}

void main() {
}
