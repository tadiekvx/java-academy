int lcs(String a, String b) {
    return go(a, b, 0, 0);
}

int go(String a, String b, int i, int j) {
    if (i == a.length() || j == b.length()) {
        return 0;
    }
    if (a.charAt(i) == b.charAt(j)) {
        return 1 + go(a, b, i + 1, j + 1);
    }
    return Math.max(go(a, b, i + 1, j), go(a, b, i, j + 1));
}

void main() {
}
