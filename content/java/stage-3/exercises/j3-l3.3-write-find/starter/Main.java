Optional<String> findLong(List<String> names, int min) {
    return Optional.empty();
}

String firstLong(List<String> names, int min) {
    return findLong(names, min).orElse("none");
}

void main() {
}
