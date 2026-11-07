int parkingFee(int minutes) {
    if (minutes <= 30) return 0;
    return Math.min((minutes - 30) / 60 * 2, 15);
}

void main() {
}
