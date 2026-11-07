int halvings(int n) {
    int count = 0;
    while (n > 1) {
        n = n / 2;
        count++;
    }
    return count;
}

void main() {
    IO.println(halvings(8)); // should print 3
}
