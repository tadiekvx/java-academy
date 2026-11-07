long errorBudgetLeft(int sloPermille, long total, long failed) {
    long allowed = total * (1000 - sloPermille) / 1000;
    return allowed - failed;
}

void main() {
}
