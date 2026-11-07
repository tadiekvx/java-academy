boolean isPalindrome(String word) {
    String lower = word.toLowerCase();
    return lower.length() == 0 || lower.charAt(0) == lower.charAt(lower.length() - 1);
}

void main() {
}
