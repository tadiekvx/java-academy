double percentage(int correct, int total) {
    return correct * 100.0 / total;
}

void main() {
    IO.println(percentage(3, 4)); // should print 75.0
}
