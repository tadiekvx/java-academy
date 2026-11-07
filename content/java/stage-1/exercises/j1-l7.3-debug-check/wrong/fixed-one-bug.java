String check(String name, int expected, int actual) {
    if (expected == actual) {
        return "PASS " + name;
    }
    return "FAIL " + name + ": expected " + actual + " but got " + expected;
}

void main() {
}
