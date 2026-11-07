interface Discount {
    int apply(int pence, boolean member);
}

class Correct implements Discount {
    public int apply(int pence, boolean member) {
        int percent = (pence >= 10000 ? 10 : 0) + (member ? 2 : 0);
        return pence - pence * percent / 100;
    }
}

class Mutant1 implements Discount {
    public int apply(int pence, boolean member) {
        int percent = (pence > 10000 ? 10 : 0) + (member ? 2 : 0);
        return pence - pence * percent / 100;
    }
}

class Mutant2 implements Discount {
    public int apply(int pence, boolean member) {
        int percent = pence >= 10000 ? 10 + (member ? 2 : 0) : 0;
        return pence - pence * percent / 100;
    }
}

class Mutant3 implements Discount {
    public int apply(int pence, boolean member) {
        int percent = (pence >= 10000 ? 10 : 0) + (member ? 3 : 0);
        return pence - pence * percent / 100;
    }
}

class Mutant4 implements Discount {
    public int apply(int pence, boolean member) {
        int percent = (pence >= 10000 ? 11 : 0) + (member ? 2 : 0);
        return pence - pence * percent / 100;
    }
}

class Mutant5 implements Discount {
    public int apply(int pence, boolean member) {
        int percent = (pence >= 10000 ? 10 : 0) + (member ? 2 : 0);
        return pence - (pence * percent + 99) / 100;
    }
}

class Mutant6 implements Discount {
    public int apply(int pence, boolean member) {
        int percent = pence >= 10000 ? 10 : 0;
        return pence - pence * percent / 100;
    }
}

// check(d, pence, member, expected) is true when the discount code gives the expected price.
boolean check(Discount d, int pence, boolean member, int expected) {
    return d.apply(pence, member) == expected;
}

boolean allPass(Discount d) {
    return check(d, 5000, false, 5000)
            && check(d, 9999, false, 9999)
            && check(d, 10000, false, 9000)
            && check(d, 20000, false, 18000)
            && check(d, 5000, true, 4900)
            && check(d, 20000, true, 17600)
            && check(d, 101, true, 99);
}

String run(String which) {
    Discount d = switch (which) {
        case "mutant1" -> new Mutant1();
        case "mutant2" -> new Mutant2();
        case "mutant3" -> new Mutant3();
        case "mutant4" -> new Mutant4();
        case "mutant5" -> new Mutant5();
        case "mutant6" -> new Mutant6();
        default -> new Correct();
    };
    return allPass(d) ? "pass" : "fail";
}

void main() {
}
