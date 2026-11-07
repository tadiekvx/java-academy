class Point {
    int x;
    int y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // write equals and hashCode here
}

String compare(int x1, int y1, int x2, int y2) {
    Point a = new Point(x1, y1);
    Point b = new Point(x2, y2);
    boolean equal = a.equals(b);
    boolean hashRule = !equal || a.hashCode() == b.hashCode();
    return equal + "," + hashRule;
}

void main() {
}
