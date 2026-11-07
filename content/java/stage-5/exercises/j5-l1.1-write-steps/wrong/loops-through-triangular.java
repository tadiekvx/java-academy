long triangular(int n) {
    long count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i; j < n; j++) {
            count++;
        }
    }
    return count;
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
