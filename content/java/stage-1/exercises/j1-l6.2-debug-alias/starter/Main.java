int[] bonusTotals(int[] scores) {
    int[] boosted = scores;
    for (int i = 0; i < boosted.length; i++) {
        boosted[i] = boosted[i] + 10;
    }
    int before = 0;
    for (int score : scores) {
        before += score;
    }
    int after = 0;
    for (int score : boosted) {
        after += score;
    }
    return new int[] {before, after};
}

void main() {
    IO.println(Arrays.toString(bonusTotals(new int[] {1, 2, 3}))); // should print [6, 36]
}
