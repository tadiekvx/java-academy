int[] reversed(int[] values) {
    int[] copy = Arrays.copyOf(values, values.length);
    for (int i = 0; i < copy.length / 2; i++) {
        int other = copy.length - 1 - i;
        int saved = copy[i];
        copy[i] = copy[other];
        copy[other] = saved;
    }
    return copy;
}

void main() {
    IO.println(Arrays.toString(reversed(new int[] {1, 2, 3}))); // should print [3, 2, 1]
}
