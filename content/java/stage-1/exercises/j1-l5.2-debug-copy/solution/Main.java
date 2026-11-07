int applyDiscount(int price) {
    int reduced = price - price / 10;
    return reduced;
}

void main() {
    IO.println(applyDiscount(2000)); // should print 1800
}
