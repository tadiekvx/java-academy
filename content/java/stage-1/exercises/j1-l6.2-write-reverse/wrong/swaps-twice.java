int[] reversed(int[] values) {
    int[] copy = Arrays.copyOf(values, values.length);
    for (int i = 0; i < copy.length; i++) {
        int other = copy.length - 1 - i;
        int saved = copy[i];
        copy[i] = copy[other];
        copy[other] = saved;
    }
    return copy;
}

void main() {
}
