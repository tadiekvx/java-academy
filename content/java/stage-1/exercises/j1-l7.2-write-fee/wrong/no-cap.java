int parkingFee(int minutes) {
    if (minutes <= 30) return 0;
    return (minutes - 30 + 59) / 60 * 2;
}

void main() {
}
