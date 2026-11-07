class Pair<A, B> {
    Pair(A first, B second) {
    }

    A first() {
        return null;
    }

    B second() {
        return null;
    }

    Pair<B, A> swap() {
        return new Pair<>(null, null);
    }
}

String run(String a, int b) {
    Pair<String, Integer> p = new Pair<>(a, b);
    Pair<Integer, String> s = p.swap();
    return s.first() + ":" + s.second();
}

void main() {
}
