String total(List<String> prices, int vatPercent) {
    BigDecimal sum = BigDecimal.ZERO;
    for (String price : prices) {
        sum = sum.add(new BigDecimal(price));
    }
    BigDecimal withVat = sum.multiply(BigDecimal.valueOf(100)).divide(BigDecimal.valueOf(100));
    return withVat.setScale(2, RoundingMode.HALF_UP).toPlainString();
}

void main() {
}
