String addPrices(String a, String b) {
    return new BigDecimal(a).add(new BigDecimal(b)).toPlainString();
}

void main() {
}
