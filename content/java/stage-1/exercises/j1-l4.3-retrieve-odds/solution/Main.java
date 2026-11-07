int sumOfOdds(int n) {
    int total = 0;
    for (int i = 1; i <= n; i += 2) {
        total += i;
    }
    return total;
}

void main() {
    IO.println(sumOfOdds(7)); // should print 16
}
