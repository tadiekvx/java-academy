int percentage(int part, int total) {
    if (total == 0) {
        return 0;
    }
    return part * 100 / total;
}

void main() {
    IO.println(percentage(1, 4)); // should print 25
}
