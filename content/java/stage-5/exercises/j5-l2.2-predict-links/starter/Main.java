class Node {
    int value;
    Node next;

    Node(int value, Node next) {
        this.value = value;
        this.next = next;
    }
}

void main() {
    Node c = new Node(3, null);
    Node b = new Node(2, c);
    Node a = new Node(1, b);
    Node head = a;
    IO.println(head.value + " " + head.next.value + " " + head.next.next.value);
    head = head.next;
    Node z = new Node(9, head);
    IO.println(z.next.next.value);
    b.next = null;
    IO.println(z.next.next == null);
    IO.println(a.next.value);
    IO.println(c.value);
}
