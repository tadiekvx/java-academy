String initialOf(List<String> names, String prefix) {
    return names.stream()
            .filter(n -> n.startsWith(prefix))
            .reduce((a, b) -> b)
            .map(n -> n.substring(0, 1).toUpperCase())
            .orElse("?");
}

void main() {
}
