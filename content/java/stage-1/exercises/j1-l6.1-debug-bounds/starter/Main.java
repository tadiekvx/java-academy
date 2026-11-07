double average(int[] values) {
    int total = 0;
    for (int i = 0; i <= values.length; i++) {
        total += values[i];
    }
    return (double) total / values.length;
}

void main() {
    IO.println(average(new int[] {4, 8, 15, 16})); // should print 10.75
}
