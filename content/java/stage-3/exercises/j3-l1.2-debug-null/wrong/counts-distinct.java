int mostRepeated(List<String> items) {
    Map<String, Integer> counts = new HashMap<>();
    for (String item : items) {
        counts.merge(item, 1, Integer::sum);
    }
    return counts.size();
}

void main() {
}
