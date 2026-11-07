Optional<String> findLong(List<String> names, int min) {
    return names.stream()
            .filter(n -> n.length() > min)
            .findFirst();
}

void main() {
}
