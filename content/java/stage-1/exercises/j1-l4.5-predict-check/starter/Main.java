boolean isWholeNumber(String text) {
    if (text.isEmpty()) {
        return false;
    }
    for (int i = 0; i < text.length(); i++) {
        if (!Character.isDigit(text.charAt(i))) {
            return false;
        }
    }
    return true;
}

void main() {
    IO.println(isWholeNumber("120"));
    IO.println(isWholeNumber("12 0"));
    IO.println(isWholeNumber("-5"));
    IO.println(isWholeNumber(""));
    IO.println(isWholeNumber("007"));
}
