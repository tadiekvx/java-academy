class Box<T> {
    private T value;

    Box(T value) {
        this.value = value;
    }

    T get() {
        return value;
    }

    void set(T value) {
        this.value = value;
    }
}

String run(int n, String s) {
    Box<Integer> a = new Box<>(n);
    Box<String> b = new Box<>(s);
    a.set(a.get() + 1);
    return a.get() + b.get();
}

void main() {
}
