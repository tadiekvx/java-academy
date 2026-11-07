List<Integer> parallelSquares(List<Integer> values, int threads) throws Exception {
    List<Integer> squares = new ArrayList<>();
    for (int value : values) {
        squares.add(value * value);
    }
    return squares;
}

void main() {
}
