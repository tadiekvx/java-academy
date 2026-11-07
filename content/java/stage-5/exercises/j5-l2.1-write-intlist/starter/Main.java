class IntList {
    void add(int value) {
    }

    int get(int index) {
        return 0;
    }

    int size() {
        return 0;
    }

    int capacity() {
        return 0;
    }
}

String run(int n) {
    IntList list = new IntList();
    for (int i = 0; i < n; i++) {
        list.add(i);
    }
    long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += list.get(i);
    }
    boolean badIndex;
    try {
        list.get(n);
        badIndex = false;
    } catch (IndexOutOfBoundsException e) {
        badIndex = true;
    }
    return "size=" + list.size() + " capacity=" + list.capacity() + " sum=" + sum + " badIndex=" + badIndex;
}

void main() {
}
