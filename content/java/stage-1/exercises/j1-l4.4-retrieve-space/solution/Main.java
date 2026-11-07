int firstSpace(String text) {
    for (int i = 0; i < text.length(); i++) {
        if (text.charAt(i) == ' ') {
            return i;
        }
    }
    return -1;
}

void main() {
    IO.println(firstSpace("hello world")); // should print 5
}
