class Counter {
    int count;

    void increment() {
        count++;
    }

    void add(int amount) {
        count += amount;
    }

    void reset() {
        count = 0;
    }

    int value() {
        return count;
    }
}

int run(String[] ops) {
    Counter c = new Counter();
    for (String op : ops) {
        if (op.equals("inc")) {
            c.increment();
        } else if (op.equals("reset")) {
            c.reset();
        } else if (op.startsWith("add:")) {
            c.add(Integer.parseInt(op.substring(4)));
        }
    }
    return c.value();
}

void main() {
}
