sealed interface Shape permits Circle, Square, Triangle {}

record Circle(int r) implements Shape {}
record Square(int side) implements Shape {}
record Triangle(int base, int height) implements Shape {}

String describe(Shape s) {
    return switch (s) {
        case Circle c -> "circle r=" + c.r();
        case Square q -> "square side=" + q.side();
    };
}

String run(String kind, int a, int b) {
    Shape s;
    if (kind.equals("circle")) {
        s = new Circle(a);
    } else if (kind.equals("square")) {
        s = new Square(a);
    } else {
        s = new Triangle(a, b);
    }
    return describe(s);
}

void main() {
}
