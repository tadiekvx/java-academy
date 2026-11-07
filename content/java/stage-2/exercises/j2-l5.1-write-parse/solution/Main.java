int parseOr(String text, int fallback) {
    try {
        return Integer.parseInt(text.trim());
    } catch (NumberFormatException e) {
        return fallback;
    }
}

void main() {
}
