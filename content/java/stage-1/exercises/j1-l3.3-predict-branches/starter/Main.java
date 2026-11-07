String size(int litres) {
    if (litres >= 100) {
        return "large";
    } else if (litres >= 10) {
        return "medium";
    } else {
        return "small";
    }
}

void main() {
    IO.println(size(250));
    IO.println(size(10));
    IO.println(size(9));
    if (size(50).equals("medium")) {
        IO.println("fits");
    } else {
        IO.println("doesn't fit");
    }
}
