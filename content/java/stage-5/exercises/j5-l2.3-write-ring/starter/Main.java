class RingQueue {
    RingQueue(int capacity) {
    }

    boolean offer(int value) {
        return false;
    }

    int poll() {
        return 0;
    }

    int size() {
        return 0;
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
