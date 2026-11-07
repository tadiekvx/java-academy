class Point {
    int x;
    int y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
}

void main() {
    Point p = new Point(1, 2);
    Point q = new Point(1, 2);
    Point r = p;
    IO.println(p == q);
    IO.println(p.equals(q));
    IO.println(p.equals(r));
    IO.println(p.x == q.x);
}
