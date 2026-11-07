int parkingFee(int minutes) {
    if (minutes <= 60) return 0;
    return Math.min((minutes - 60 + 59) / 60 * 2, 15);
}

void main() {
}
