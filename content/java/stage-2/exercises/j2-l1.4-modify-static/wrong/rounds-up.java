class Shop {
    static final int TAX_PERCENT = 20;
    static int priceWithTax(int pence) {
        return (pence * (100 + TAX_PERCENT) + 99) / 100;
    }
}

int total(int pence) {
    return Shop.priceWithTax(pence);
}

void main() {
}
