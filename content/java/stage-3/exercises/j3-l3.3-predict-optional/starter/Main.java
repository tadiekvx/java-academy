void main() {
    Optional<String> some = Optional.of("kiwi");
    Optional<String> none = Optional.empty();
    String missing = null;

    IO.println(some.map(String::toUpperCase).orElse("?"));
    IO.println(none.map(String::toUpperCase).orElse("?"));
    IO.println(none.isPresent());
    IO.println(Optional.ofNullable(missing).isPresent());
    some.ifPresent(s -> IO.println("has " + s));
    none.ifPresent(s -> IO.println("has " + s));
    IO.println(some.map(String::length).orElse(0));
}
