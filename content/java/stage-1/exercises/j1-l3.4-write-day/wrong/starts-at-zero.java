String dayName(int day) {
    return switch (day) {
        case 0 -> "Monday";
        case 1 -> "Tuesday";
        case 2 -> "Wednesday";
        case 3 -> "Thursday";
        case 4 -> "Friday";
        case 5 -> "Saturday";
        case 6 -> "Sunday";
        default -> "Unknown";
    };
}

void main() {
}
