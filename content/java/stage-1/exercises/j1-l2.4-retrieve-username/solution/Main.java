String username(String first, String last) {
    return (first.charAt(0) + last).toLowerCase();
}

void main() {
    IO.println(username("Grace", "Hopper")); // should print ghopper
}
