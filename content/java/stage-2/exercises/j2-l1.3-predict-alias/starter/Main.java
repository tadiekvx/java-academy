class Player {
    String name;
    int score;

    Player(String name) {
        this.name = name;
    }
}

void main() {
    Player a = new Player("Sam");
    Player b = a;
    b.score = 50;
    Player c = new Player("Sam");
    IO.println(a.score);
    IO.println(c.score);
    IO.println(a == b);
    IO.println(a == c);
}
