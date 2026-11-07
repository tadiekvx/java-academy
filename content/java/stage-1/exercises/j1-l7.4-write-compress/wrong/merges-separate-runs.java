String compress(String text) {
    String result = "";
    for (char c = 'a'; c <= 'z'; c++) {
        int n = 0;
        for (int i = 0; i < text.length(); i++) if (text.charAt(i) == c) n++;
        if (n > 0) result += c + "" + n;
    }
    return result;
}

void main() {
}
