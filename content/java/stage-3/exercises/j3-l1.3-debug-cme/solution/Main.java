List<Integer> removeNegatives(List<Integer> values) {
    List<Integer> copy = new ArrayList<>(values);
    copy.removeIf(v -> v < 0);
    return copy;
}

void main() {
}
