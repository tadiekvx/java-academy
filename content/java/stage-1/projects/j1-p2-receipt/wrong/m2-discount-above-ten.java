String formatMoney(int pence) {
    String sign = pence < 0 ? "-" : "";
    int absolute = Math.abs(pence);
    String padding = absolute % 100 < 10 ? "0" : "";
    return sign + "£" + absolute / 100 + "." + padding + absolute % 100;
}

int lineTotal(int unitPrice, int quantity) {
    int total = unitPrice * quantity;
    if (quantity > 10) {
        total -= total * 10 / 100;
    }
    return total;
}

int subtotal(int[] unitPrices, int[] quantities) {
    int sum = 0;
    for (int i = 0; i < unitPrices.length; i++) {
        sum += lineTotal(unitPrices[i], quantities[i]);
    }
    return sum;
}

String receipt(String[] names, int[] unitPrices, int[] quantities) {
    String text = "";
    for (int i = 0; i < names.length; i++) {
        text += names[i] + " x" + quantities[i] + " " + formatMoney(lineTotal(unitPrices[i], quantities[i])) + "\n";
    }
    int sub = subtotal(unitPrices, quantities);
    int vat = sub * 20 / 100;
    return text + "Subtotal: " + formatMoney(sub) + "\n"
            + "VAT (20%): " + formatMoney(vat) + "\n"
            + "Total: " + formatMoney(sub + vat);
}

void main() {
    String[] names = {"Tea", "Biscuits"};
    int[] prices = {250, 199};
    int[] quantities = {2, 12};
    IO.println(receipt(names, prices, quantities));
}
