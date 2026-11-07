int firstDigit(String text) {
    for (int i = 0; i < text.length(); i++) {
        if (Character.isDigit(text.charAt(i))) {
            return i;
        }
    }
    return -1;
}

void main() {
    String text = "Room 42B";
    int count = 0;
    for (int i = 0; i < text.length(); i++) {
        if (text.charAt(i) == 'o') {
            count++;
        }
    }
    IO.println(count);
    IO.println(firstDigit(text));
    IO.println(firstDigit("none"));
}
