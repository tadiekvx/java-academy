int largest(int a, int b) {
    int best = a;
    if (b > a) {
        best = b;
    }
    return best;
}

void main() {
    IO.println(largest(3, 9)); // should print 9
}
