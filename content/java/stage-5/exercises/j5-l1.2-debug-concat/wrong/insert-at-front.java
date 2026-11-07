String build(int n) {
    StringBuilder text = new StringBuilder();
    for (int i = n - 1; i >= 0; i--) {
        text.insert(0, i);
        if (i < n - 1) {
            text.insert(String.valueOf(i).length(), ",");
        }
    }
    return text.toString();
}

int run(int n) {
    return build(n).length();
}

void main() {
}
