int inner(int n) {
    n = n + 1;
    IO.println("inner " + n);
    return n * 2;
}

int outer(int n) {
    IO.println("outer " + n);
    int result = inner(n + 10);
    IO.println("back " + n);
    return result;
}

void main() {
    IO.println(outer(1));
}
