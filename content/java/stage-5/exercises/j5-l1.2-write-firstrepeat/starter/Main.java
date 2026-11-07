int firstRepeat(List<Integer> values) {
    return -1;
}

String run(int n, int repeatAt) {
    List<Integer> values = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        values.add(i * 2);
    }
    if (repeatAt >= 1 && repeatAt < n) {
        values.set(repeatAt, 0);
        if (repeatAt + 1 < n) {
            values.set(repeatAt + 1, 2);
        }
    }
    return String.valueOf(firstRepeat(values));
}

void main() {
}
