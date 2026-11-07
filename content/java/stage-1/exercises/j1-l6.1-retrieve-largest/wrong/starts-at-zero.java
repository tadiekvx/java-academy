int largest(int[] values) {
    int best = 0;
    for (int value : values) {
        if (value > best) {
            best = value;
        }
    }
    return best;
}

void main() {
}
