String grade(int score) {
    if (score >= 50) {
        return "C";
    } else if (score >= 60) {
        return "B";
    } else if (score >= 70) {
        return "A";
    } else {
        return "Fail";
    }
}

void main() {
    IO.println(grade(92)); // should print A
}
