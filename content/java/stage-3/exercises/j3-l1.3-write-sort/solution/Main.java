List<String> sortedByLength(List<String> words) {
    List<String> copy = new ArrayList<>(words);
    copy.sort(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()));
    return copy;
}

void main() {
}
