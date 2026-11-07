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
    String typed = "";
    while (!isWholeNumber(typed) || typed.length() > 1) {
        typed = IO.readln("Players (2-6): ").strip();
        if (!isWholeNumber(typed) || typed.length() > 1) {
            IO.println("Please enter a whole number from 2 to 6.");
        }
    }
    IO.println("Players accepted: " + Integer.parseInt(typed));
}
