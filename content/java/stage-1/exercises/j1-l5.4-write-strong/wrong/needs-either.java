boolean hasDigit(String t) {
    for (int i = 0; i < t.length(); i++) {
        if (Character.isDigit(t.charAt(i))) {
            return true;
        }
    }
    return false;
}

boolean isStrong(String password) {
    return password.length() >= 8 && hasDigit(password);
}

void main() {
}
