int wholeHours(int totalMinutes) {
    return totalMinutes / 60;
}

int leftoverMinutes(int totalMinutes) {
    return totalMinutes % 60;
}

void main() {
    IO.println(wholeHours(135));      // should print 2
    IO.println(leftoverMinutes(135)); // should print 15
}
