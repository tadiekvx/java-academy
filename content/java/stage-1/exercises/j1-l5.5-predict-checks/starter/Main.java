int middle(int a, int b, int c) {
    if (a > b) {
        return a;
    }
    return b;
}

void check(String name, int expected, int actual) {
    if (expected == actual) {
        IO.println("PASS " + name);
    } else {
        IO.println("FAIL " + name + ": expected " + expected + " but got " + actual);
    }
}

void main() {
    check("ascending", 5, middle(1, 5, 9));
    check("descending", 5, middle(9, 5, 1));
    check("middle first", 5, middle(5, 1, 9));
}
