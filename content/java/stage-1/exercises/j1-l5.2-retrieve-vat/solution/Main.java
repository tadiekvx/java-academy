int withTax(int net, int rate) {
    int tax = net * rate / 100;
    return net + tax;
}

void main() {
    IO.println(withTax(1000, 20)); // should print 1200
}
