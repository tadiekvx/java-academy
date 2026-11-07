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
    int day = 0;
    while (day == 0) {
        String typed = IO.readln("Day (1-31): ").strip();
        if (isWholeNumber(typed) && typed.length() <= 3 && Integer.parseInt(typed) >= 1) {
            day = Integer.parseInt(typed);
        } else {
            IO.println("Please enter a whole number from 1 to 31.");
        }
    }
    IO.println("Day accepted: " + day);
}
