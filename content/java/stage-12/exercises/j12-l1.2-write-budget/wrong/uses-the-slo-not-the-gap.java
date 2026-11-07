long errorBudgetLeft(int sloPermille, long total, long failed) {
    long allowed = total * sloPermille / 1000;
    return allowed - failed;
}

void main() {
}
