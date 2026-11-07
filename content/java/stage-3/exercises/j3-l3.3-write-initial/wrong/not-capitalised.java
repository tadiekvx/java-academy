String initialOf(List<String> names, String prefix) {
    return names.stream()
            .filter(n -> n.startsWith(prefix))
            .findFirst()
            .map(n -> n.substring(0, 1))
            .orElse("?");
}

void main() {
}
