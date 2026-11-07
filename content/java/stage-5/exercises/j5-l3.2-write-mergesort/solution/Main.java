int[] mergeSort(int[] values) {
    if (values.length <= 1) {
        return values;
    }
    int mid = values.length / 2;
    int[] left = mergeSort(Arrays.copyOfRange(values, 0, mid));
    int[] right = mergeSort(Arrays.copyOfRange(values, mid, values.length));
    int[] merged = new int[values.length];
    int i = 0;
    int j = 0;
    int k = 0;
    while (i < left.length && j < right.length) {
        merged[k++] = left[i] <= right[j] ? left[i++] : right[j++];
    }
    while (i < left.length) {
        merged[k++] = left[i++];
    }
    while (j < right.length) {
        merged[k++] = right[j++];
    }
    return merged;
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
