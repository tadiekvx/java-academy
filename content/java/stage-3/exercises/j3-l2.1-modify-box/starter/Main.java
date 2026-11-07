class IntBox {
    private int value;
    IntBox(int value) { this.value = value; }
    int get() { return value; }
    void set(int value) { this.value = value; }
}

class StringBox {
    private String value;
    StringBox(String value) { this.value = value; }
    String get() { return value; }
    void set(String value) { this.value = value; }
}

String run(int n, String s) {
    Box<Integer> a = new Box<>(n);
    Box<String> b = new Box<>(s);
    a.set(a.get() + 1);
    return a.get() + b.get();
}

void main() {
}
