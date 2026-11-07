String shorten(String text, int limit) {
    if (text.length() <= limit) {
        return text;
    }
    return text.substring(0, limit);
}

void main() {
    IO.println(shorten("hello world", 5)); // should print hello
}
