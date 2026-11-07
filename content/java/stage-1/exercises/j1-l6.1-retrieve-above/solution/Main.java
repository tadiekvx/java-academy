int countAbove(int[] values, int limit) {
    int count = 0;
    for (int value : values) {
        if (value > limit) {
            count++;
        }
    }
    return count;
}

void main() {
    IO.println(countAbove(new int[] {4, 8, 15, 16}, 10)); // should print 2
}
