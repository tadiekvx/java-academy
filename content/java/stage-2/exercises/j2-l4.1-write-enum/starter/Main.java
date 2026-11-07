enum Size {
    SMALL, MEDIUM, LARGE;

    int ml() {
        return 0;
    }
}

int total(String[] names) {
    int sum = 0;
    for (String n : names) {
        sum += Size.valueOf(n.toUpperCase()).ml();
    }
    return sum;
}

void main() {
}
