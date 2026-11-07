String sizeOf(int code) {
    return switch (code) {
        case 1, 2 -> "small";
        case 3 -> "medium";
        case 4, 5, 6 -> "large";
        default -> "unknown";
    };
}

void main() {
    IO.println(sizeOf(2));
    IO.println(sizeOf(5));
    IO.println(sizeOf(0));
    IO.println(sizeOf(3) + "!");
}
