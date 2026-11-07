class Pair<A, B> {
    private final A first;
    private final B second;

    Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }

    A first() {
        return first;
    }

    B second() {
        return second;
    }

    Pair<B, A> swap() {
        return new Pair<>(second, first);
    }
}

String run(String a, int b) {
    Pair<String, Integer> p = new Pair<>(a, b);
    Pair<Integer, String> s = p.swap();
    return s.first() + ":" + s.second();
}

void main() {
}
