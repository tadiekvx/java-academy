String countByLength(List<String> words) {
    Map<Integer, Long> counts = words.stream()
            .collect(Collectors.groupingBy(w -> w.length() % 2, TreeMap::new, Collectors.counting()));
    return counts.entrySet().stream()
            .map(e -> e.getKey() + "=" + e.getValue())
            .collect(Collectors.joining(","));
}

void main() {
}
