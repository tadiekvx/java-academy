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
        String typed = IO.readln("Percentage: ").strip();
        if (isWholeNumber(typed) && typed.length() <= 3 && Integer.parseInt(typed) >= 0 && Integer.parseInt(typed) <= 100) {
            value = Integer.parseInt(typed);
        } else {
            IO.println("Please enter a whole number from 0 to 100.");
        }
    }
    IO.println("Percentage accepted: " + value);
}
