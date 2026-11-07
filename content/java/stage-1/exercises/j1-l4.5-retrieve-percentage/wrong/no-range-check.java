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
    while (!isWholeNumber(typed) || typed.length() > 3) {
        typed = IO.readln("Percentage: ").strip();
        if (!isWholeNumber(typed) || typed.length() > 3) {
            IO.println("Please enter a whole number from 0 to 100.");
        }
    }
    IO.println("Percentage accepted: " + Integer.parseInt(typed));
}
