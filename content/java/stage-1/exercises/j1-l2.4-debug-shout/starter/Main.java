String shout(String message) {
    message.toUpperCase();
    return message + "!";
}

void main() {
    IO.println(shout("hello")); // should print HELLO!
}
