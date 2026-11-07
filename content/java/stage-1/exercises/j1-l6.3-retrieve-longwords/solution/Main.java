ArrayList<String> longWords(ArrayList<String> words, int minLength) {
    ArrayList<String> result = new ArrayList<>();
    for (String word : words) {
        if (word.length() > minLength) {
            result.add(word);
        }
    }
    return result;
}

void main() {
}
