ArrayList<Integer> removeValue(ArrayList<Integer> numbers, int value) {
    numbers.remove(Integer.valueOf(value));
    return numbers;
}

void main() {
    ArrayList<Integer> numbers = new ArrayList<>();
    numbers.add(5);
    numbers.add(10);
    numbers.add(15);
    IO.println(removeValue(numbers, 10)); // should print [5, 15]
}
