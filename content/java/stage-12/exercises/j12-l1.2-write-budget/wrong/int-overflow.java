long errorBudgetLeft(int sloPermille, long total, long failed) {
    int allowed = (int) (total * (1000 - sloPermille)) / 1000;
    return allowed - failed;
}

void main() {
}
