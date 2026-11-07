boolean divisibleBy(int number, int d) {
    return number % d == 0;
}

boolean isLeapYear(int year) {
    return divisibleBy(year, 4);
}

void main() {
}
