int total(int[] prices) {
    int sum = 0;
    for (int price : prices) {
        sum += price;
    }
    return sum;
}

String summary(int[] prices) {
    String word = prices.length == 1 ? "item" : "items";
    return prices.length + " " + word + ", total " + total(prices);
}

void main() {
}
