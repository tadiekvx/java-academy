int mostRepeated(List<String> items) {
    Map<String, Integer> counts = new HashMap<>();
    for (String item : items) {
        counts.put(item, counts.get(item) + 1);
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
