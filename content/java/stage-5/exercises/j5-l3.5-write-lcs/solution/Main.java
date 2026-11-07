int lcs(String a, String b) {
    int[][] len = new int[a.length() + 1][b.length() + 1];
    for (int i = 1; i <= a.length(); i++) {
        for (int j = 1; j <= b.length(); j++) {
            if (a.charAt(i - 1) == b.charAt(j - 1)) {
                len[i][j] = len[i - 1][j - 1] + 1;
            } else {
                len[i][j] = Math.max(len[i - 1][j], len[i][j - 1]);
            }
        }
    }
    return len[a.length()][b.length()];
}

void main() {
}
