record Order(int grams, boolean express, String country) {}

String quote(Order order) {
    int cost = order.grams() < 500 ? 300 : 450;
    if (order.express()) {
        cost += 200;
    }
    if (!order.country().equals("UK")) {
        cost += 500;
    }
    return "cost=" + cost;
}

String run(int grams, boolean express, String country) {
    return quote(new Order(grams, express, country));
}

void main() {
}
