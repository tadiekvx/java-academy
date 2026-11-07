int linear(int n) {
    int c = 0;
    for (int i = 0; i < n; i++) {
        c++;
    }
    return c;
}

int nested(int n) {
    int c = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            c++;
        }
    }
    return c;
}

int triangle(int n) {
    int c = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            c++;
        }
    }
    return c;
}

int halving(int n) {
    int c = 0;
    while (n > 1) {
        n = n / 2;
        c++;
    }
    return c;
}

void main() {
    IO.println(linear(16));
    IO.println(nested(16));
    IO.println(triangle(16));
    IO.println(halving(16));
    IO.println(halving(1000));
    IO.println(halving(1));
}
