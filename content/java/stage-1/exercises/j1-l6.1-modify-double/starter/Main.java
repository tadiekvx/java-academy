int[] doubleAll(int[] values) {
    if (values.length > 0) {
        values[0] = values[0] * 2;
    }
    return values;
}

void main() {
    IO.println(Arrays.toString(doubleAll(new int[] {1, 2, 3})));
}
