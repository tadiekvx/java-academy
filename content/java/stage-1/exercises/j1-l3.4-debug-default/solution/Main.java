String medal(int place) {
    return switch (place) {
        case 1 -> "gold";
        case 2 -> "silver";
        case 3 -> "bronze";
        default -> "none";
    };
}

void main() {
    IO.println(medal(4)); // should print none
}
