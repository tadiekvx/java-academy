class IntLinkedList {
    void addFirst(int value) {
    }

    void addLast(int value) {
    }

    void removeFirst() {
    }

    void reverse() {
    }

    int size() {
        return 0;
    }

    @Override
    public String toString() {
        return "[]";
    }
}

String run(String[] ops) {
    IntLinkedList list = new IntLinkedList();
    for (String op : ops) {
        if (op.startsWith("first:")) {
            list.addFirst(Integer.parseInt(op.substring(6)));
        } else if (op.startsWith("last:")) {
            list.addLast(Integer.parseInt(op.substring(5)));
        } else if (op.equals("removeFirst")) {
            list.removeFirst();
        } else if (op.equals("reverse")) {
            list.reverse();
        }
    }
    return list + " size=" + list.size();
}

void main() {
}
