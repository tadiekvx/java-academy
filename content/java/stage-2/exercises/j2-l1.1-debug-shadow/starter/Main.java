class Point {
    int x;
    int y;

    Point(int x, int y) {
        x = x;
        y = y;
    }
}

int sumOf(int a, int b) {
    Point p = new Point(a, b);
    return p.x + p.y;
}

void main() {
}
