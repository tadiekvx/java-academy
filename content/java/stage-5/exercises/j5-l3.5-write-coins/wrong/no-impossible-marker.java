int minCoins(int[] coins, int amount) {
    int[] best = new int[amount + 1];
    best[0] = 0;
    for (int a = 1; a <= amount; a++) {
        for (int coin : coins) {
            if (coin <= a && best[a - coin] != Integer.MAX_VALUE) {
                best[a] = Math.min(best[a], best[a - coin] + 1);
            }
        }
    }
    return best[amount] == Integer.MAX_VALUE ? -1 : best[amount];
}

void main() {
}
