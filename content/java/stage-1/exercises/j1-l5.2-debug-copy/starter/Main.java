int applyDiscount(int price) {
    int reduced = price - price / 10;
    return price;
}

void main() {
    IO.println(applyDiscount(2000)); // should print 1800
}
