String shout(String message) {
    return message.toUpperCase() + "!";
}

void main() {
    IO.println(shout("hello")); // should print HELLO!
}
