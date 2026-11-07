int firstSpace(String text) {
    for (int i = 0; i < text.length(); i++) {
        if (text.charAt(i) == ' ') {
            return i;
        } else {
            return -1;
        }
    }
    return -1;
}

void main() {
}
