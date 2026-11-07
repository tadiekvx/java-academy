String build(int n) {
    String text = "";
    for (int i = 0; i < n; i++) {
        if (i > 0) {
            text += ",";
        }
        text += i;
    }
    return text;
}

int run(int n) {
    return build(n).length();
}

void main() {
}
