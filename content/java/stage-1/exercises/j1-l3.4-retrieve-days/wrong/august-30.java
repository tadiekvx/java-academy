int daysInMonth(int month) {
    return switch (month) {
        case 1, 3, 5, 7, 10, 12 -> 31;
        case 4, 6, 8, 9, 11 -> 30;
        case 2 -> 28;
        default -> 0;
    };
}

void main() {
}
