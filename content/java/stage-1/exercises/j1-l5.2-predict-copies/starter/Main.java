int bump(int n) {
    n = n + 10;
    return n;
}

void main() {
    int score = 5;
    int other = bump(score);
    IO.println(score);
    IO.println(other);
    score = bump(score);
    IO.println(score);
    IO.println(bump(bump(0)));
}
