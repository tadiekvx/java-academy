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
    int value = -1;
    while (value < 0) {
        String typed = IO.readln("Players (2-6): ").strip();
        if (isWholeNumber(typed) && typed.length() <= 1 && Integer.parseInt(typed) >= 2 && Integer.parseInt(typed) <= 6) {
            value = Integer.parseInt(typed);
        } else {
            IO.println("Please enter a whole number from 2 to 6.");
        }
    }
    IO.println("Players accepted: " + value);
}
