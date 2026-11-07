int digitCount(int n) {
    int count = 1;
    while (n >= 10) {
        n = n / 10;
        count++;
    }
    return count;
}

void main() {
    IO.println(digitCount(4071)); // should print 4
}
