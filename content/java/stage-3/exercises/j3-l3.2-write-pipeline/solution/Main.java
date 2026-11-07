List<String> longUpper(List<String> words, int minLength) {
    return words.stream()
            .filter(w -> w.length() >= minLength)
            .map(String::toUpperCase)
            .sorted()
            .toList();
}

void main() {
}
