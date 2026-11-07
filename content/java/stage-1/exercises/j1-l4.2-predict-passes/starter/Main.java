void main() {
    int a = 0;
    int count = 0;
    while (a < 10) {
        a += 4;
        count++;
    }
    IO.println(count);

    int n = 64;
    int halvings = 0;
    while (n > 1) {
        n = n / 2;
        halvings++;
    }
    IO.println(halvings);
}
