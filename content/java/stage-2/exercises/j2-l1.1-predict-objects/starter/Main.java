class Box {
    int size;
    String label;
    boolean open;

    Box(int size) {
        this.size = size;
    }
}

void main() {
    Box a = new Box(5);
    Box b = new Box(5);
    b.size = 9;
    IO.println(a.size);
    IO.println(b.size);
    IO.println(a.label);
    IO.println(a.open);
}
