boolean corsAllowed(String origin, List<String> allowedOrigins) {
    return !origin.isEmpty() && allowedOrigins.stream().anyMatch(origin::startsWith);
}

void main() {
}
