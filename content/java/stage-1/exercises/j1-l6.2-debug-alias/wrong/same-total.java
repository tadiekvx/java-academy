int[] bonusTotals(int[] scores) {
    int before = 0;
    for (int score : scores) {
        before += score;
    }
    return new int[] {before, before};
}

void main() {
}
