int parseOr(String text, int fallback) {
    try { return Integer.parseInt(text); } catch (NumberFormatException e) { return fallback; }
}

void main() {
}
