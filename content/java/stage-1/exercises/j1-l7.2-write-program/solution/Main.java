int parkingFee(int minutes) {
    if (minutes <= 30) {
        return 0;
    }
    int hours = (minutes - 30 + 59) / 60;
    return Math.min(hours * 2, 15);
}

void main() {
    int minutes = Integer.parseInt(IO.readln("Minutes parked: ").trim());
    IO.println("Fee: " + parkingFee(minutes));
}
