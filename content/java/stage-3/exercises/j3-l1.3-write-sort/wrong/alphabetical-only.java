List<String> sortedByLength(List<String> words) {
    List<String> copy = new ArrayList<>(words);
    copy.sort(Comparator.naturalOrder());
    return copy;
}

void main() {
}
