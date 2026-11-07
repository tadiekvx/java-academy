interface Shape {
    int area();
}

class Rect implements Shape {
    private final int width;
    private final int height;

    Rect(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public int area() {
        return width + height;
    }
}

class Square implements Shape {
    private final int side;

    Square(int side) {
        this.side = side;
    }

    public int area() {
        return side * side;
    }
}

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
