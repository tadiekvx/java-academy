interface Discount {
    int apply(int pence);
}

class NoDiscount implements Discount {
    public int apply(int pence) {
        return pence;
    }
}

class PercentOff implements Discount {
    private final int percent;

    PercentOff(int percent) {
        this.percent = percent;
    }

    public int apply(int pence) {
        return pence - pence * percent / 100;
    }
}

class Order {
    private final int pence;
    private final Discount discount;

    Order(int pence, Discount discount) {
        this.pence = pence;
        this.discount = discount;
    }

    int total() {
        return pence;
    }
}

int total(int pence, String kind) {
    Discount d;
    if (kind.equals("ten")) {
        d = new PercentOff(10);
    } else if (kind.equals("half")) {
        d = new PercentOff(50);
    } else {
        d = new NoDiscount();
    }
    Order order = new Order(pence, d);
    return order.total();
}

void main() {
}
