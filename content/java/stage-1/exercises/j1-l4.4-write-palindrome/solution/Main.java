boolean isPalindrome(String word) {
    String lower = word.toLowerCase();
    int last = lower.length() - 1;
    for (int i = 0; i < lower.length() / 2; i++) {
        if (lower.charAt(i) != lower.charAt(last - i)) {
            return false;
        }
    }
    return true;
}

void main() {
    IO.println(isPalindrome("level")); // should print true
}
