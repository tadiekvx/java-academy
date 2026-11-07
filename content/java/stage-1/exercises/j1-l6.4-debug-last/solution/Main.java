int lastElement(int[] values) {
    if (values.length == 0) {
        return -1;
    }
    return values[values.length - 1];
}

void main() {
    IO.println(lastElement(new int[] {4, 8, 15})); // should print 15
}
