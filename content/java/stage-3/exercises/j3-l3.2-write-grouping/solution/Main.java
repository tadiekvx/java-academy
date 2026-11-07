String countByLength(List<String> words) {
    Map<Integer, Long> counts = words.stream()
            .collect(Collectors.groupingBy(String::length, TreeMap::new, Collectors.counting()));
    return counts.entrySet().stream()
            .map(e -> e.getKey() + "=" + e.getValue())
            .collect(Collectors.joining(","));
}

void main() {
}
