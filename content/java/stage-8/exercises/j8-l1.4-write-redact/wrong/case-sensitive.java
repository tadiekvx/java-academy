String redact(String line) {
    Set<String> secret = Set.of("password", "token", "secret", "apikey", "authorization");
    String[] parts = line.split(" ", -1);
    for (int i = 0; i < parts.length; i++) {
        int equals = parts[i].indexOf('=');
        if (equals > 0 && secret.contains(parts[i].substring(0, equals))) {
            parts[i] = parts[i].substring(0, equals + 1) + "***";
        }
    }
    return String.join(" ", parts);
}

void main() {
}
