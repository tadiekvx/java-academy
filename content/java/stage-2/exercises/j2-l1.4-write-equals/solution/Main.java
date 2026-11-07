class Point {
    int x;
    int y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof Point p)) return false;
        return x == p.x && y == p.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
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
