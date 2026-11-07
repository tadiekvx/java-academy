class IntList {
    private int[] data = new int[4];
    private int size;

    void add(int value) {
        if (size == data.length) {
            data = Arrays.copyOf(data, data.length + 4);
        }
        data[size] = value;
        size++;
    }

    int get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException("index " + index + ", size " + size);
        }
        return data[index];
    }

    int size() {
        return size;
    }

    int capacity() {
        return data.length;
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
