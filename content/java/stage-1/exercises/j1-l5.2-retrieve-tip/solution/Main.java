int totalWithTip(int bill, int tipPercent) {
    int tip = bill * tipPercent / 100;
    return bill + tip;
}

void main() {
    IO.println(totalWithTip(2000, 10)); // should print 2200
}
