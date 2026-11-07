int largestDigit(int n) {
    int best = 0;
    while (n > 0) {
        int digit = n % 10;
        if (digit > best) {
            best = digit;
        }
        n = n / 10;
    }
    return best;
}

void main() {
    IO.println(largestDigit(4071)); // should print 7
}
