void countdown(int n) {
    if (n == 0) {
        IO.println("liftoff");
        return;
    }
    IO.println("down " + n);
    countdown(n - 1);
    IO.println("up " + n);
}

int sumDigits(int n) {
    if (n == 0) {
        return 0;
    }
    return n % 10 + sumDigits(n / 10);
}

int fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

void main() {
    countdown(3);
    IO.println(sumDigits(9875));
    IO.println(fib(10));
}
