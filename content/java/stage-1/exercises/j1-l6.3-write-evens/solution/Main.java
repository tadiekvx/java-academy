ArrayList<Integer> evens(ArrayList<Integer> numbers) {
    ArrayList<Integer> result = new ArrayList<>();
    for (int number : numbers) {
        if (number % 2 == 0) {
            result.add(number);
        }
    }
    return result;
}

void main() {
    ArrayList<Integer> numbers = new ArrayList<>();
    numbers.add(1);
    numbers.add(2);
    numbers.add(4);
    IO.println(evens(numbers)); // should print [2, 4]
}
