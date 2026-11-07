class IntLinkedList {
    private Node head;
    private int size;

    private static class Node {
        int value;
        Node next;

        Node(int value) {
            this.value = value;
        }
    }

    void addFirst(int value) {
        Node node = new Node(value);
        node.next = head;
        head = node;
        size++;
    }

    void addLast(int value) {
        Node node = new Node(value);
        if (head == null) {
            head = node;
        } else {
            Node current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = node;
        }
        size++;
    }

    void removeFirst() {
        if (head != null) {
            head = head.next;
            size--;
        }
    }

    void reverse() {
        Node previous = null;
        Node current = head;
        while (current != null) {
            current.next = previous;
            previous = current;
            current = current.next;
        }
        head = previous;
    }

    int size() {
        return size;
    }

    @Override
    public String toString() {
        StringBuilder text = new StringBuilder("[");
        for (Node current = head; current != null; current = current.next) {
            if (current != head) {
                text.append(", ");
            }
            text.append(current.value);
        }
        return text.append("]").toString();
    }
}

void main() {
}
