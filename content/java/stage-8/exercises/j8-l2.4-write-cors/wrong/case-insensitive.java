boolean corsAllowed(String origin, List<String> allowedOrigins) {
    return !origin.isEmpty() && allowedOrigins.stream().anyMatch(origin::equalsIgnoreCase);
}

void main() {
}
