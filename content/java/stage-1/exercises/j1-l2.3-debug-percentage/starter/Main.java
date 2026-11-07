double percentage(int correct, int total) {
    return correct / total * 100;
}

void main() {
    IO.println(percentage(3, 4)); // should print 75.0
}
