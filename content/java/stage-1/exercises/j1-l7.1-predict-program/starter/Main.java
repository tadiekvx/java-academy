int clamp(int value, int low, int high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
}

int step(int position, int move) {
    return clamp(position + move, 0, 10);
}

void main() {
    int position = 3;
    int[] moves = {5, 4, -9, -4, 2};
    for (int move : moves) {
        position = step(position, move);
        IO.println(position);
    }
}
