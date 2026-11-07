class Counter {
    int n;

    Counter inc() {
        n++;
        return this;
    }

    int value() {
        return n;
    }
}

void main() {
    Counter a = new Counter();
    Counter b = new Counter();
    a.inc().inc().inc();
    b.inc().inc();
    a.inc();
    IO.println(a.value() + " " + b.value());
}
