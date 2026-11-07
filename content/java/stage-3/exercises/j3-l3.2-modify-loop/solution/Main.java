int sumOfSquaresOfEvens(List<Integer> values) {
    return values.stream()
            .filter(v -> v % 2 == 0)
            .mapToInt(v -> v * v)
            .sum();
}

void main() {
}
