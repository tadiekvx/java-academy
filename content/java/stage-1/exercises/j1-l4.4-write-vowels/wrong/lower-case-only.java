int countVowels(String word) {
    int count = 0;
    for (int i = 0; i < word.length(); i++) {
        if ("aeiou".indexOf(word.charAt(i)) != -1) {
            count++;
        }
    }
    return count;
}

void main() {
}
