int total(int[] values) {
    int sum = 0;
    for (int value : values) {
        sum += value;
    }
    return sum;
}

void main() {
    IO.println(total(new int[] {4, 8, 15, 16})); // should print 43
}
