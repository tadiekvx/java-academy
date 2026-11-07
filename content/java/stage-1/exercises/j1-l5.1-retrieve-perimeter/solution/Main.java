int perimeter(int width, int height) {
    return 2 * (width + height);
}

void main() {
    IO.println(perimeter(3, 5)); // should print 16
}
