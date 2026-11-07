ArrayList<Integer> evens(ArrayList<Integer> numbers) {
    ArrayList<Integer> result = new ArrayList<>();
    for (int number : numbers) {
        if (number % 2 != 0) {
            result.add(number);
        }
    }
    return result;
}

void main() {
}
