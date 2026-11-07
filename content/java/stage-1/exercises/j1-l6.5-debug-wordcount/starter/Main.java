int countWords(String text) {
    int spaces = 0;
    for (int i = 0; i < text.length(); i++) {
        if (text.charAt(i) == ' ') {
            spaces++;
        }
    }
    return spaces + 1;
}

void main() {
    IO.println(countWords("hello big world")); // should print 3
}
