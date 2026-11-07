String summary(List<String> words) {
    Stream<String> shortWords = words.stream().filter(w -> w.length() < 4);
    long count = shortWords.count();
    List<String> list = shortWords.toList();
    return count + ":" + String.join("+", list);
}

void main() {
}
