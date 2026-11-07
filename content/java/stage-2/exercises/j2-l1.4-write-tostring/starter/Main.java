class Point {
    int x;
    int y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // write toString here
}

String show(int x, int y) {
    Point p = new Point(x, y);
    return "P=" + p;
}

void main() {
}
