int shippingCost(int grams, boolean express, String country) {
    int cost;
    if (country.equals("UK")) {
        if (grams <= 500) {
            cost = 300;
        } else if (grams <= 2000) {
            cost = 450;
        } else {
            cost = 450 + ((grams - 2000 + 999) / 1000) * 100;
        }
    } else {
        if (grams <= 500) {
            cost = 800;
        } else if (grams <= 2000) {
            cost = 1200;
        } else {
            cost = 1200 + ((grams - 2000 + 999) / 1000) * 250;
        }
    }
    if (express) {
        cost = cost * 2;
    }
    return cost;
}

void main() {
}
