int[] mergeSort(int[] values) {
    return values.clone();
}

String run(int n) {
    int[] values = new int[n];
    for (int i = 0; i < n; i++) {
        values[i] = (int) ((i * 2654435761L) % 1000003);
    }
    int[] sorted = mergeSort(values);
    boolean ok = sorted.length == n;
    long sum = 0;
    for (int i = 0; i < sorted.length; i++) {
        sum += sorted[i];
        if (i > 0 && sorted[i - 1] > sorted[i]) {
            ok = false;
        }
    }
    return "sorted=" + ok + " sum=" + sum + " first=" + (n > 0 ? sorted[0] : 0) + " last=" + (n > 0 ? sorted[sorted.length - 1] : 0);
}

void main() {
}
