int spread(int[] values) {
    int smallest = values[0];
    int largest = values[0];
    for (int value : values) {
        if (value < smallest) {
            smallest = value;
        }
        if (value > largest) {
            largest = value;
        }
    }
    return largest - smallest;
}

void main() {
    IO.println(spread(new int[] {4, 8, 15, 16})); // should print 12
}
