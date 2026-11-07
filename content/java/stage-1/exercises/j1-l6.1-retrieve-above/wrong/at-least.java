int countAbove(int[] values, int limit) {
    int count = 0;
    for (int value : values) {
        if (value >= limit) {
            count++;
        }
    }
    return count;
}

void main() {
}
