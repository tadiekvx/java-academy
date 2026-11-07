int firstVowel(String word) {
    String lower = word.toLowerCase();
    for (int i = 0; i < lower.length(); i++) {
        if ("aeiou".indexOf(lower.charAt(i)) != -1) {
            return i;
        }
    }
    return -1;
}

void main() {
    IO.println(firstVowel("Banana")); // should print 1
}
