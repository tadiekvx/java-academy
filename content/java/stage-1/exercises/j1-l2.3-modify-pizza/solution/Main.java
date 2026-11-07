// Each pizza is cut into 6 slices. Returns how many whole pizzas to order
// so that every person can have slicesEach slices.
int pizzasNeeded(int people, int slicesEach) {
    int slices = people * slicesEach;
    return (slices + 5) / 6;
}

void main() {
    IO.println(pizzasNeeded(3, 2)); // 6 slices
    IO.println(pizzasNeeded(5, 2)); // 10 slices
}
