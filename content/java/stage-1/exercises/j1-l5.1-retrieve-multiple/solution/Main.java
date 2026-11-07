boolean isMultipleOf(int n, int k) {
    return n % k == 0;
}

void main() {
    IO.println(isMultipleOf(12, 4)); // should print true
}
