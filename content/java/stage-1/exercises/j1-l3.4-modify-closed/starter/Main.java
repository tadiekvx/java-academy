String dayType(int day) {
    return switch (day) {
        case 1, 2, 3, 4, 5 -> "weekday";
        case 6, 7 -> "weekend";
        default -> "unknown";
    };
}

void main() {
    IO.println(dayType(3));
}
