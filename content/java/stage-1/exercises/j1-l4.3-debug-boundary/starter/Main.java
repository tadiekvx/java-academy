int countSpaces(String message) {
    int count = 0;
    for (int i = 1; i < message.length(); i++) {
        if (message.charAt(i) == ' ') {
            count++;
        }
    }
    return count;
}

void main() {
    IO.println(countSpaces(" hello")); // should print 1
}
