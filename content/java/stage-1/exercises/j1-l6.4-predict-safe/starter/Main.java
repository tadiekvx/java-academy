int safeDivide(int a, int b) {
    if (b == 0) {
        return 0;
    }
    return a / b;
}

char firstLetter(String text) {
    if (text.isEmpty()) {
        return '?';
    }
    return text.charAt(0);
}

void main() {
    IO.println(safeDivide(12, 4));
    IO.println(safeDivide(12, 0));
    IO.println(firstLetter("Java"));
    IO.println(firstLetter(""));
}
