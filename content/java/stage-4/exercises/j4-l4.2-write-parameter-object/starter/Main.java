String quote(int grams, boolean express, String country) {
    int cost = grams <= 500 ? 300 : 450;
    if (express) {
        cost += 200;
    }
    if (!country.equals("UK")) {
        cost += 500;
    }
    return "cost=" + cost;
}

String run(int grams, boolean express, String country) {
    return quote(new Order(grams, express, country));
}

void main() {
}
