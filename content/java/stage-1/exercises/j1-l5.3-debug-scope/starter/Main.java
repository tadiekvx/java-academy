int largest(int a, int b) {
    if (a > b) {
        int best = a;
    } else {
        int best = b;
    }
    return best;
}

void main() {
    IO.println(largest(3, 9)); // should print 9
}
