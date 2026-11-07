int sumOfSquaresOfEvens(List<Integer> values) {
    int total = 0;
    for (int v : values) {
        if (v % 2 == 0) {
            total += v * v;
        }
    }
    return total;
}

void main() {
}
