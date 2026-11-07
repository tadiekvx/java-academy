int ticketPrice(int age) {
    if (age <= 12) {
        return 5;
    } else if (age > 65) {
        return 6;
    } else {
        return 10;
    }
}

void main() {
    IO.println(ticketPrice(12)); // should print 10
    IO.println(ticketPrice(65)); // should print 6
}
