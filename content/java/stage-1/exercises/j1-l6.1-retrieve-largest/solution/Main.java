int largest(int[] values) {
    int best = values[0];
    for (int value : values) {
        if (value > best) {
            best = value;
        }
    }
    return best;
}

void main() {
    IO.println(largest(new int[] {4, 8, 15, 16})); // should print 16
}
