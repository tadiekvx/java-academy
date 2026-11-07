int pertDays(int optimistic, int likely, int pessimistic) {
    return (optimistic + 4 * likely + pessimistic + 3) / 6;
}

void main() {
}
