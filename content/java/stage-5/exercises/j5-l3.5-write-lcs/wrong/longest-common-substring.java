int lcs(String a, String b) {
    int best = 0;
    for (int i = 0; i < a.length(); i++) {
        for (int j = 0; j < b.length(); j++) {
            int k = 0;
            while (i + k < a.length() && j + k < b.length() && a.charAt(i + k) == b.charAt(j + k)) {
                k++;
            }
            best = Math.max(best, k);
        }
    }
    return best;
}

void main() {
}
