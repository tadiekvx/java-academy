String letterType(char letter) {
    return switch (letter) {
        case 'a', 'e', 'i', 'o', 'u' -> "vowel";
        default -> "consonant";
    };
}

void main() {
    IO.println(letterType('a')); // should print vowel
}
