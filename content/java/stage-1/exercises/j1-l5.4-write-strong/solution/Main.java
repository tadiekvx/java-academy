boolean hasDigit(String text) {
    for (int i = 0; i < text.length(); i++) {
        if (Character.isDigit(text.charAt(i))) {
            return true;
        }
    }
    return false;
}

boolean hasCapital(String text) {
    for (int i = 0; i < text.length(); i++) {
        if (Character.isUpperCase(text.charAt(i))) {
            return true;
        }
    }
    return false;
}

boolean isStrong(String password) {
    return password.length() >= 8 && hasDigit(password) && hasCapital(password);
}

void main() {
    IO.println(isStrong("Tr0ub4dor")); // should print true
}
