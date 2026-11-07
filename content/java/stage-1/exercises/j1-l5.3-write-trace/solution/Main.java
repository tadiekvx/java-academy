int step1(int n) {
    return step2(n + 1);
}

int step2(int n) {
    return step3(n * 2);
}

int step3(int n) {
    return n + 3;
}

void main() {
    IO.println(step1(4)); // should print 13
}
