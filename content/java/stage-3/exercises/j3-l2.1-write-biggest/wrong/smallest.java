<T extends Comparable<T>> T biggest(List<T> items) {
    T best = items.get(0);
    for (T item : items) {
        if (item.compareTo(best) < 0) {
            best = item;
        }
    }
    return best;
}

String run(List<String> words, List<Integer> numbers) {
    return biggest(words) + "," + biggest(numbers);
}

void main() {
}
