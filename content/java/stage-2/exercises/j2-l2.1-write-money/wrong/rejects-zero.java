class Money {
    private final int pence;
    Money(int pence) {
        if (pence <= 0) throw new IllegalArgumentException("not positive");
        this.pence = pence;
    }
    int pence() { return pence; }
    Money plus(Money other) { return new Money(pence + other.pence); }
}

String run(int a, int b) {
    try {
        Money total = new Money(a).plus(new Money(b));
        return total.pence() + " pence";
    } catch (IllegalArgumentException e) {
        return "rejected";
    }
}

void main() {
}
