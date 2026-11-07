void main() {
    for (int i = 0; i < 4; i++) {
        IO.print(i);
    }
    IO.println();
    for (int i = 5; i > 0; i -= 2) {
        IO.print(i);
    }
    IO.println();
    int count = 0;
    for (int i = 1; i <= 10; i += 4) {
        count++;
    }
    IO.println(count);
}
