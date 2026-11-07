record Point(int x, int y) {}

String run(int x1, int y1, int x2, int y2) {
    Point a = new Point(x1, y1);
    Point b = new Point(x2, y2);
    return a.equals(b) + " " + a + " " + a.x();
}

void main() {
}
