List<String> validate(String owner, String currency, int openingCents) {
    List<String> problems = new ArrayList<>();
    if (owner.isBlank()) {
        problems.add("owner: must not be blank");
    }
    if (!currency.matches("[A-Za-z]{3}")) {
        problems.add("currency: must be a 3-letter code");
    }
    if (openingCents < 0) {
        problems.add("openingCents: must not be negative");
    }
    return problems;
}

void main() {
}
