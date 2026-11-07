int parkingFee(int minutes) {
    if (minutes <= 30) {
        return 0;
    }
    int over = minutes - 30;
    int hours = (over + 59) / 60;
    return Math.min(hours * 2, 15);
}

void main() {
}
