String summary(List<String> words) {
    List<String> list = words.stream().filter(w -> w.length() < 4).toList();
    return list.size() + ":" + String.join("+", list);
}

void main() {
}
