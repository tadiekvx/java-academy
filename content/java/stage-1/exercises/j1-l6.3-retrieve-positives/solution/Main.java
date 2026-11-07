ArrayList<Integer> positives(ArrayList<Integer> numbers) {
    ArrayList<Integer> result = new ArrayList<>();
    for (int number : numbers) {
        if (number > 0) {
            result.add(number);
        }
    }
    return result;
}

void main() {
}
