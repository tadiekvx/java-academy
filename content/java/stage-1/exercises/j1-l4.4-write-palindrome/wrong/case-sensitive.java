boolean isPalindrome(String word) {
    int last = word.length() - 1;
    for (int i = 0; i < word.length() / 2; i++) {
        if (word.charAt(i) != word.charAt(last - i)) {
            return false;
        }
    }
    return true;
}

void main() {
}
