int mostRepeated(List<String> items) {
    Map<String, Integer> counts = new HashMap<>();
    for (String item : items) {
        counts.merge(item, 1, Integer::sum);
    }
    int best = 0;
    for (int n : counts.values()) {
        if (n > best) {
            best = n;
        }
    }
    return best;
}

void main() {
}
