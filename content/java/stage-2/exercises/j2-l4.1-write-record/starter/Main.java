record Rect(int w, int h) {
    int area() {
        return 0;
    }
}

String run(int w, int h) {
    try {
        Rect r = new Rect(w, h);
        return r + " area=" + r.area();
    } catch (IllegalArgumentException e) {
        return "rejected";
    }
}

void main() {
}
