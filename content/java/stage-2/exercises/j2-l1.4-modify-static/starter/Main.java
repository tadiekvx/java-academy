class Shop {
    int priceWithTax(int pence) {
        return pence * (100 + 20) / 100;
    }
}

int total(int pence) {
    return Shop.priceWithTax(pence);
}

void main() {
}
