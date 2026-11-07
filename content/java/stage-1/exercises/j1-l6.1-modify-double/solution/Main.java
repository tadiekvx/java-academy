int[] doubleAll(int[] values) {
    for (int i = 0; i < values.length; i++) {
        values[i] = values[i] * 2;
    }
    return values;
}

void main() {
    IO.println(Arrays.toString(doubleAll(new int[] {1, 2, 3})));
}
