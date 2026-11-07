int countWords(String text) {
    if (text.isEmpty()) {
        return 0;
    }
    int spaces = 0;
    for (int i = 0; i < text.length(); i++) {
        if (text.charAt(i) == ' ') {
            spaces++;
        }
    }
    IO.println("spaces: " + spaces);
    return spaces + 1;
}

void main() {
    IO.println(countWords("hello big world"));
    IO.println(countWords(""));
    IO.println(countWords("one"));
}
