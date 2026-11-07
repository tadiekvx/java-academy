int discounted(int price, int percentOff) {
    int saving = price * percentOff / 100;
    return price - saving;
}

void main() {
    IO.println(discounted(2000, 25)); // should print 1500
}
