int total(int pence) {
    int taxed = pence * 120 / 100;
    if (pence >= 5000) {
        return taxed;
    }
    return taxed + 499;
}

void main() {
}
