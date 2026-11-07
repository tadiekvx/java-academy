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
    int value = Integer.parseInt(IO.readln("Age (0-120): ").strip());
    IO.println("Age accepted: " + value);
}
