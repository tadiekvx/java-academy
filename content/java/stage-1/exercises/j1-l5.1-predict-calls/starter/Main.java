int triple(int n) {
    return n * 3;
}

String label(int n) {
    return "Item " + n;
}

void main() {
    IO.println(triple(4));
    IO.println(triple(triple(2)));
    IO.println(label(triple(1)));
    int x = triple(5) - triple(2);
    IO.println(x);
}
