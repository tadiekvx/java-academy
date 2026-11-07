double pricePerItem(int totalPence, int items) {
    return (double) totalPence / items;
}

void main() {
    IO.println(pricePerItem(99, 2)); // should print 49.5
}
