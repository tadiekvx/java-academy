class Scores {
    private final int[] values;
    Scores(int[] values) { this.values = values.clone(); }
    int[] all() { return values; }
    int max() { int best = values[0]; for (int v : values) if (v > best) best = v; return best; }
}

int run(int[] input) {
    Scores s = new Scores(input);
    input[0] = -999;
    s.all()[0] = 2000;
    return s.max();
}

void main() {
}
