int percentile(List<Integer> values, int p) {
    if (values.isEmpty()) {
        return -1;
    }
    long sum = 0;
    for (int v : values) {
        sum += v;
    }
    return (int) (sum / values.size());
}

void main() {
}
