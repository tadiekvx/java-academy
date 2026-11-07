boolean isCorrect(String answer) {
    String cleaned = answer.strip().toLowerCase();
    return cleaned.equals("paris");
}

void main() {
    IO.println(isCorrect("Paris")); // should print true
}
