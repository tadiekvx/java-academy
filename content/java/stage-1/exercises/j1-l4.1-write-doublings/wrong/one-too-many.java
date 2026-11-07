int yearsToReach(int start, int target) {
    int money = start;
    int years = 0;
    while (money <= target) {
        money *= 2;
        years++;
    }
    return years;
}

void main() {
}
