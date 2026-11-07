class MinHeap {
    void add(int value) {
    }

    int poll() {
        return 0;
    }

    int peek() {
        return 0;
    }

    int size() {
        return 0;
    }
}

String run(String[] ops) {
    MinHeap heap = new MinHeap();
    StringBuilder out = new StringBuilder();
    for (String op : ops) {
        if (op.startsWith("add:")) {
            heap.add(Integer.parseInt(op.substring(4)));
        } else {
            try {
                out.append(heap.poll());
            } catch (NoSuchElementException e) {
                out.append("E");
            }
            out.append(" ");
        }
    }
    return out + "size=" + heap.size() + (heap.size() > 0 ? " peek=" + heap.peek() : "");
}

void main() {
}
