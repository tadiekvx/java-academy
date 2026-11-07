int secondLargest(int[] values) {
    if (values.length < 2) return -1;
    int[] copy = values.clone();
    java.util.Arrays.sort(copy);
    return copy[copy.length - 2];
}

void main() {
}
