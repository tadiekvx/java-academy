enum Size {
    SMALL(250), MEDIUM(330), LARGE(500);

    private final int ml;

    Size(int ml) {
        this.ml = ml;
    }

    int ml() {
        return ml * 2;
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
