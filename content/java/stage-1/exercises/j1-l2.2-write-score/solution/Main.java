int finalScore(int start) {
    int score = start;
    score = score + 15;
    score = score - 4;
    score = score * 2;
    return score;
}

void main() {
    IO.println(finalScore(10)); // should print 42
}
