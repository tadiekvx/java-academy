List<String> sortedByLength(List<String> words) {
    List<String> copy = new ArrayList<>(words);
    copy.sort(Comparator.comparing(String::length));
    return copy;
}

void main() {
}
