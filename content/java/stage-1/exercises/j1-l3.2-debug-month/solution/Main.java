boolean isValidMonth(int month) {
    return month >= 1 && month <= 12;
}

void main() {
    IO.println(isValidMonth(1)); // should print true
}
