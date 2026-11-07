int percentile(List<Integer> values, int p) {
    if (values.isEmpty()) {
        return -1;
    }
    List<Integer> sorted = new ArrayList<>(values);
    Collections.sort(sorted);
    int rank = Math.max(1, p * sorted.size() / 100);
    return sorted.get(Math.min(sorted.size(), rank) - 1);
}

void main() {
}
