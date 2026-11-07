String build(int n) {
    StringBuilder text = new StringBuilder();
    for (int i = 0; i < n; i++) {
        if (i > 0) {
            text.append(",");
        }
        text.append(i);
    }
    return text.toString();
}

int run(int n) {
    return build(n).length();
}

void main() {
}
