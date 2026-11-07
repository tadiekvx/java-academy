class Player {
    String name;
    int score;

    Player(String name, int score) {
        this.name = name;
        this.score = score;
    }
}

int[] bonusTotals(int score) {
    Player player = new Player("Sam", score);
    Player before = player;
    player.score += 10;
    return new int[] {before.score, player.score};
}

void main() {
}
