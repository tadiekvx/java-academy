// INHERITED CODE: the shipping calculator for the shop. Costs are in pence.
// Ticket 482: "Customers in the US are being charged the UK (domestic) price."

int shippingCost(int grams, boolean express, String country) {
    int cost;
    if (country.startsWith("U")) {
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
