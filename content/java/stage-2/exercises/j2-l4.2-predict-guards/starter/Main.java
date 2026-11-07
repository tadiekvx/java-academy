sealed interface Shape permits Circle, Square {}

record Circle(int r) implements Shape {}
record Square(int side) implements Shape {}

String size(Shape s) {
    return switch (s) {
        case Circle c when c.r() > 10 -> "big circle";
        case Circle c -> "circle";
        case Square q when q.side() > 10 -> "big square";
        case Square q -> "square";
    };
}

void main() {
    IO.println(size(new Circle(3)));
    IO.println(size(new Circle(30)));
    IO.println(size(new Square(30)));
    IO.println(size(new Square(10)));
}
