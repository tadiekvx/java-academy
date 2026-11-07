int daysInMonth(int month) {
    return switch (month) {
        case 1, 3, 5, 7, 8, 10, 12 -> 31;
        case 4, 6, 9, 11 -> 30;
        case 2 -> 28;
        default -> 0;
    };
}

void main() {
    IO.println(daysInMonth(2)); // should print 28
}
