int[] stats(int[] values) {
    int smallest = values[0];
    int largest = values[0];
    int sum = 0;
    for (int i = 1; i < values.length; i++) {
        int value = values[i];
        if (value < smallest) {
            smallest = value;
        }
        if (value > largest) {
            largest = value;
        }
        sum += value;
    }
    return new int[] {smallest, largest, sum};
}

void main() {
}
