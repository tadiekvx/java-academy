String initials(String first, String last) {
    return (first.charAt(0) + "." + last.charAt(0) + ".").toUpperCase();
}

void main() {
    IO.println(initials("ada", "Lovelace")); // should print A.L.
}
