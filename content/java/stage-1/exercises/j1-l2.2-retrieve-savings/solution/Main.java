int savingsAfterMonth(int start) {
    int savings = start;
    savings = savings + 50;
    savings = savings - 12;
    savings = savings * 3;
    return savings;
}

void main() {
    IO.println(savingsAfterMonth(10)); // should print 144
}
