int fullWeeks(int days) {
    return days / 7;
}

int extraDays(int days) {
    return days % 7;
}

void main() {
    IO.println(fullWeeks(10)); // should print 1
    IO.println(extraDays(10)); // should print 3
}
