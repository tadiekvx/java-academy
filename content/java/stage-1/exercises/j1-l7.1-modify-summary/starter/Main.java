int total(int[] prices) {
    int sum = 0;
    for (int price : prices) {
        sum += price;
    }
    return sum;
}

String summary(int[] prices) {
    return prices.length + " items, total " + total(prices);
}

void main() {
}
