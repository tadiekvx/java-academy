static final int TAX_PERCENT = 20;
static final int FREE_DELIVERY_FROM = 5000;
static final int DELIVERY_FEE = 499;

int total(int pence) {
    int taxed = pence * (100 + TAX_PERCENT) / 100;
    if (pence >= FREE_DELIVERY_FROM) {
        return taxed;
    }
    return taxed + DELIVERY_FEE;
}

void main() {
}
