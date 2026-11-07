String grade(int score) {
    if (score >= 70) {
        return "A";
    } else if (score >= 60) {
        return "B";
    } else if (score >= 50) {
        return "C";
    } else {
        return "Fail";
    }
}

void main() {
    IO.println(grade(95));
}
