class Counter {
    static int created = 0;
    final int id;

    Counter() {
        id = ++created;
    }
}

class Container {
    private final Map<String, Counter> singletons = new HashMap<>();

    Counter singleton(String name) {
        return singletons.computeIfAbsent(name, n -> new Counter());
    }

    Counter prototype(String name) {
        return new Counter();
    }
}

void main() {
    Container container = new Container();
    Counter a = container.singleton("ledger");
    Counter b = container.singleton("ledger");
    Counter p = container.prototype("ledger");
    Counter q = container.prototype("ledger");
    System.out.println("same singleton=" + (a == b));
    System.out.println("same prototype=" + (p == q));
    System.out.println("created=" + Counter.created);
    System.out.println("ids=" + a.id + "," + b.id + "," + p.id + "," + q.id);
}
