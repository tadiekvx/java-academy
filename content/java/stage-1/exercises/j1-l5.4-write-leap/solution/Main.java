boolean divisibleBy(int number, int d) {
    return number % d == 0;
}

boolean isLeapYear(int year) {
    if (divisibleBy(year, 400)) {
        return true;
    }
    if (divisibleBy(year, 100)) {
        return false;
    }
    return divisibleBy(year, 4);
}

void main() {
    IO.println(isLeapYear(2024)); // should print true
}
