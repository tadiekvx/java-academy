class RingQueue {
    private final int[] items;
    private int head;
    private int size;

    RingQueue(int capacity) {
        items = new int[capacity];
    }

    boolean offer(int value) {
        if (size == items.length) {
            return false;
        }
        items[(head + size) % items.length] = value;
        size++;
        return true;
    }

    int poll() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        int value = items[head];
        head = head + 1;
        size--;
        return value;
    }

    int size() {
        return size;
    }
}

void main() {
}
