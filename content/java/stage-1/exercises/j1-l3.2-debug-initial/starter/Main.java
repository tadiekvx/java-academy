boolean startsWithA(String word) {
    return word.length() > 0 & word.charAt(0) == 'A';
}

void main() {
    IO.println(startsWithA("")); // should print false
}
