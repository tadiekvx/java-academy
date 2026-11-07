int firstVowel(String word) {
    for (int i = 0; i < word.length(); i++) {
        if ("aeiou".indexOf(word.charAt(i)) != -1) {
            return i;
        }
    }
    return -1;
}

void main() {
}
