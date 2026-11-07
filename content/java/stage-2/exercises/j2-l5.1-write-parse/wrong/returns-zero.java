int parseOr(String text, int fallback) {
    try { return Integer.parseInt(text.trim()); } catch (NumberFormatException e) { return 0; }
}

void main() {
}
