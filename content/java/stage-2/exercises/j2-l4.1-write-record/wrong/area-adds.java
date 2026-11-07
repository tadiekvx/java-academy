record Rect(int w, int h) {
    Rect {
        if (w < 0 || h < 0) {
            throw new IllegalArgumentException("negative size");
        }
    }

    int area() {
        return w + h;
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
