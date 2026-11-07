int fullBoxes(int eggs) {
    return eggs / 6;
}

int looseEggs(int eggs) {
    return eggs % 6;
}

void main() {
    IO.println(fullBoxes(14)); // should print 2
    IO.println(looseEggs(14)); // should print 2
}
