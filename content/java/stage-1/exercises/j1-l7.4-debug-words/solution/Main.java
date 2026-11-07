int countWords(String text) {
    int count = 0;
    boolean inWord = false;
    for (int i = 0; i < text.length(); i++) {
        if (text.charAt(i) == ' ') {
            inWord = false;
        } else if (!inWord) {
            inWord = true;
            count++;
        }
    }
    return count;
}

void main() {
}
