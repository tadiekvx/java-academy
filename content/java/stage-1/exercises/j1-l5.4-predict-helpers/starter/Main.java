boolean divisibleBy(int number, int d) {
    return number % d == 0;
}

String fizz(int n) {
    if (divisibleBy(n, 15)) {
        return "FizzBuzz";
    }
    if (divisibleBy(n, 3)) {
        return "Fizz";
    }
    if (divisibleBy(n, 5)) {
        return "Buzz";
    }
    return "" + n;
}

void main() {
    IO.println(fizz(9));
    IO.println(fizz(10));
    IO.println(fizz(30));
    IO.println(fizz(7));
}
