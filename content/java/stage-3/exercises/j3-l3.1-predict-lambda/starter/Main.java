void main() {
    int base = 10;
    Function<Integer, Integer> addBase = x -> x + base;
    Predicate<String> isEmpty = String::isEmpty;
    BiFunction<Integer, Integer, Integer> mul = (a, b) -> a * b;
    Supplier<String> hello = () -> "hi";

    IO.println(addBase.apply(5));
    IO.println(isEmpty.test(""));
    IO.println(isEmpty.negate().test(""));
    IO.println(mul.apply(3, 4));
    IO.println(hello.get());

    List<String> words = new ArrayList<>(List.of("pear", "fig", "apple"));
    words.sort((a, b) -> a.length() - b.length());
    IO.println(words);
}
