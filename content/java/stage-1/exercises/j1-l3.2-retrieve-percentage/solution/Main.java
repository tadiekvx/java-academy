boolean isValidPercentage(int value) {
    return value >= 0 && value <= 100;
}

void main() {
    IO.println(isValidPercentage(50)); // should print true
}
