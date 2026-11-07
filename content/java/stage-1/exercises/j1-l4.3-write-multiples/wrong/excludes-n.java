int sumOfMultiples(int n, int k) {
    int total = 0;
    for (int m = k; m < n; m += k) {
        total += m;
    }
    return total;
}

void main() {
}
