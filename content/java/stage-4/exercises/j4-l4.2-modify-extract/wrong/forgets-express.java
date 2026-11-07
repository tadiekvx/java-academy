int shippingCost(int grams, boolean express, String country) {
    int cost = country.equals("UK") ? domesticCost(grams) : internationalCost(grams);
    return cost;
}

int domesticCost(int grams) {
    if (grams <= 500) {
        return 300;
    }
    if (grams <= 2000) {
        return 450;
    }
    return 450 + extraKilos(grams) * 100;
}

int internationalCost(int grams) {
    if (grams <= 500) {
        return 800;
    }
    if (grams <= 2000) {
        return 1200;
    }
    return 1200 + extraKilos(grams) * 250;
}

int extraKilos(int grams) {
    return (grams - 2000 + 999) / 1000;
}

void main() {
}
