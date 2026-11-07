int hoursPart(int totalSeconds) {
    return totalSeconds / 3600;
}

int minutesPart(int totalSeconds) {
    return totalSeconds % 3600 / 60;
}

int secondsPart(int totalSeconds) {
    return totalSeconds % 60;
}

String describe(int totalSeconds) {
    return hoursPart(totalSeconds) + "h " + minutesPart(totalSeconds) + "m " + secondsPart(totalSeconds) + "s";
}

void main() {
    IO.println(describe(7509)); // should print 2h 5m 9s
}
