boolean isCorrect(String answer) {
    String cleaned = answer.strip().toLowerCase();
    return cleaned == "paris";
}

void main() {
    IO.println(isCorrect("Paris")); // should print true
}
