String letterType(char letter) {
    return switch (letter) {
        case 'a', 'e', 'i', 'o' -> "vowel";
        default -> "consonant";
    };
}

void main() {
}
