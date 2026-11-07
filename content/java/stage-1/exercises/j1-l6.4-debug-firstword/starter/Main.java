int firstWordLength(String text) {
    int space = text.indexOf(" ");
    return text.substring(0, space).length();
}

void main() {
    IO.println(firstWordLength("hello world")); // should print 5
}
