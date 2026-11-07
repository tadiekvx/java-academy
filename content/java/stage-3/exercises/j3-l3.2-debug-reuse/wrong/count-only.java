String summary(List<String> words) {
    long n = words.stream().filter(w -> w.length() < 4).count();
    return n + ":";
}

void main() {
}
