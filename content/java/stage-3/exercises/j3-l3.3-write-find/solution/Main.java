Optional<String> findLong(List<String> names, int min) {
    return names.stream()
            .filter(n -> n.length() >= min)
            .findFirst();
}

String firstLong(List<String> names, int min) {
    return findLong(names, min).orElse("none");
}

void main() {
}
