int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

void main() {
    IO.println(factorial(4)); // should print 24
}
