int firstVowel(String word) {
    String lower = word.toLowerCase();
    int found = -1;
    for (int i = 0; i < lower.length(); i++) {
        if ("aeiou".indexOf(lower.charAt(i)) != -1) {
            found = i;
        }
    }
    return found;
}

void main() {
    IO.println(firstVowel("Banana")); // should print 1
}
