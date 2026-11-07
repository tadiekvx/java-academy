int positionOf(int[] values, int target) {
    for (int i = 0; i < values.length; i++) {
        if (values[i] == target) {
            return i;
        }
    }
    return -1;
}

void main() {
    IO.println(positionOf(new int[] {40, 17, 23, 17}, 17)); // should print 1
}
