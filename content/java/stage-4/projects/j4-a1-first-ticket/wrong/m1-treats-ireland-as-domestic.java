// The shipping calculator for the shop. Costs are in pence.

int shippingCost(int grams, boolean express, String country) {
    if (grams <= 0) {
        throw new IllegalArgumentException("weight must be positive: " + grams);
    }
    if (country.isEmpty()) {
        throw new IllegalArgumentException("a country is required");
    }
    int cost = (country.equals("UK") || country.equals("IE")) ? domesticCost(grams) : internationalCost(grams);
    return express ? cost * 2 : cost;
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

// Whole kilograms (rounded up) beyond the first 2 kg.
int extraKilos(int grams) {
    return (grams - 2000 + 999) / 1000;
}

// ---------------------------------------------------------------------------------------------
// The callers of the calculator. Don't change them.
// ---------------------------------------------------------------------------------------------

String quote(int grams, boolean express, String country) {
    try {
        return "cost=" + shippingCost(grams, express, country);
    } catch (IllegalArgumentException e) {
        return "rejected";
    }
}

void main() {
    // Optional: try the calculator out here.
}
