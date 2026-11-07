int fee(int grams, String zone, boolean express) {
    if (zone.equals("LOCAL") && grams > 20000) {
        return 0;
    }
    int f;
    if (zone.equals("LOCAL")) {
        f = grams <= 1000 ? 500 : 500 + ((grams - 1000 + 499) / 500) * 100;
    } else if (zone.equals("ZA")) {
        f = 900 + (grams / 1000) * 150;
    } else {
        f = 2500 + (grams / 1000) * 400;
    }
    if (express) {
        f = f + f / 2;
    }
    return f;
}

void main() {
}
