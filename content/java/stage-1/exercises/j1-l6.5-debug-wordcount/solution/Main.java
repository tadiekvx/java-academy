int countWords(String text) {
    int words = 0;
    boolean inWord = false;
    for (int i = 0; i < text.length(); i++) {
        if (text.charAt(i) == ' ') {
            inWord = false;
        } else if (!inWord) {
            inWord = true;
            words++;
        }
    }
    return words;
}

void main() {
    IO.println(countWords("hello big world")); // should print 3
}
