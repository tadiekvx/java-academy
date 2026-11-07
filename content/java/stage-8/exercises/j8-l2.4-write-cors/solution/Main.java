boolean corsAllowed(String origin, List<String> allowedOrigins) {
    return !origin.isEmpty() && allowedOrigins.contains(origin);
}

void main() {
}
