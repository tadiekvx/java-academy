String grade(int score) {
    if (score >= 70) {
        return "A";
    } else if (score >= 60) {
        return "B";
    } else if (score >= 50) {
        return "C";
    } else if (score >= 90) {
        return "A*";
    } else {
        return "Fail";
    }
}

void main() {
}
