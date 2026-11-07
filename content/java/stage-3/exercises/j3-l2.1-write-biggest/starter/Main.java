<T> T biggest(List<T> items) {
    return items.get(0);
}

String run(List<String> words, List<Integer> numbers) {
    return biggest(words) + "," + biggest(numbers);
}

void main() {
}
