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
        head = (head + 1) % items.length;
        size--;
        return value;
    }

    int size() {
        return size;
    }
}

String run(int capacity, String[] ops) {
    RingQueue q = new RingQueue(capacity);
    StringBuilder out = new StringBuilder();
    for (String op : ops) {
        if (op.startsWith("offer:")) {
            out.append(q.offer(Integer.parseInt(op.substring(6))) ? "T" : "F");
        } else {
            try {
                out.append(q.poll());
            } catch (NoSuchElementException e) {
                out.append("E");
            }
        }
        out.append(" ");
    }
    return out + "size=" + q.size();
}

void main() {
}
