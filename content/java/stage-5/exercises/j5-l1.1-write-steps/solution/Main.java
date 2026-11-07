long triangular(int n) {
    long m = Math.max(n, 0);
    return m * (m + 1) / 2;
}

int halvings(int n) {
    int count = 0;
    while (n > 1) {
        n = n / 2;
        count++;
    }
    return count;
}

int doublings(int n) {
    int count = 0;
    long k = 1;
    while (k < n) {
        k *= 2;
        count++;
    }
    return count;
}

void main() {
}
