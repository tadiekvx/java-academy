int positionOf(int[] values, int target) {
    int found = -1;
    for (int i = 0; i < values.length; i++) {
        if (values[i] == target) {
            found = i;
        }
    }
    return found;
}

void main() {
}
