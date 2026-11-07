int stepsAtBedtime(int start) {
    int steps = start;
    steps = steps + 1200;
    steps = steps + 3400;
    steps = steps - 500;
    return steps;
}

void main() {
    IO.println(stepsAtBedtime(10)); // should print 4110
}
