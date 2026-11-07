interface Shape {
    int area();
}

// Write the classes Rect and Square here.

int totalArea(String[] specs) {
    int total = 0;
    for (String spec : specs) {
        String[] parts = spec.split(":");
        Shape s;
        if (parts[0].equals("rect")) {
            String[] d = parts[1].split("x");
            s = new Rect(Integer.parseInt(d[0]), Integer.parseInt(d[1]));
        } else {
            s = new Square(Integer.parseInt(parts[1]));
        }
        total += s.area();
    }
    return total;
}

void main() {
}
