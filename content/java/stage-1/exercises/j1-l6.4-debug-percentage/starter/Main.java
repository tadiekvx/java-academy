int percentage(int part, int total) {
    return part * 100 / total;
}

void main() {
    IO.println(percentage(1, 4)); // should print 25
}
