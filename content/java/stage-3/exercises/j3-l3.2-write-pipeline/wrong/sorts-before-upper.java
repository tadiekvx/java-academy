List<String> longUpper(List<String> words, int minLength) {
    return words.stream()
            .filter(w -> w.length() >= minLength)
            .sorted()
            .map(String::toUpperCase)
            .toList();
}

void main() {
}
