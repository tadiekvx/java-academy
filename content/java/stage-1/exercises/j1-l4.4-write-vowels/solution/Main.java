int countVowels(String word) {
    String lower = word.toLowerCase();
    int count = 0;
    for (int i = 0; i < lower.length(); i++) {
        if ("aeiou".indexOf(lower.charAt(i)) != -1) {
            count++;
        }
    }
    return count;
}

void main() {
    IO.println(countVowels("Education")); // should print 5
}
