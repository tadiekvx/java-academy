String summary(int[] prices) {
    String word = prices.length == 1 ? "item" : "items";
    return prices.length + " " + word;
}

void main() {
}
