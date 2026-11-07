int firstWordLength(String text) {
    int space = text.indexOf(" ");
    if (space == -1) {
        return text.length();
    }
    return space;
}

void main() {
    IO.println(firstWordLength("hello world")); // should print 5
}
