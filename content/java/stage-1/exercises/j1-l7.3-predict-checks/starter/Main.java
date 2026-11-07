int discount(int age) {
    if (age < 12) return 50;
    if (age >= 65) return 30;
    return 0;
}

void check(String name, int expected, int actual) {
    if (expected == actual) {
        IO.println("PASS " + name);
    } else {
        IO.println("FAIL " + name + ": expected " + expected + " but got " + actual);
    }
}

void main() {
    check("child", 50, discount(5));
    check("boundary 12", 50, discount(12));
    check("adult", 0, discount(30));
    check("senior", 30, discount(65));
    check("boundary 64", 30, discount(64));
}
