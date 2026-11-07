interface Pricing {
    int price(int age);
}

class CorrectPricing implements Pricing {
    public int price(int age) {
        if (age < 5) return 0;
        if (age < 18) return 500;
        if (age < 65) return 1000;
        return 700;
    }
}

class AgeMutant1 implements Pricing {
    public int price(int age) {
        if (age <= 5) return 0;
        if (age < 18) return 500;
        if (age < 65) return 1000;
        return 700;
    }
}

class AgeMutant2 implements Pricing {
    public int price(int age) {
        if (age < 5) return 0;
        if (age <= 18) return 500;
        if (age < 65) return 1000;
        return 700;
    }
}

class AgeMutant3 implements Pricing {
    public int price(int age) {
        if (age < 5) return 0;
        if (age < 18) return 500;
        if (age <= 65) return 1000;
        return 700;
    }
}

class AgeMutant4 implements Pricing {
    public int price(int age) {
        if (age < 5) return 0;
        if (age < 18) return 500;
        if (age < 65) return 1000;
        return 600;
    }
}

class AgeMutant5 implements Pricing {
    public int price(int age) {
        if (age < 4) return 0;
        if (age < 18) return 500;
        if (age < 65) return 1000;
        return 700;
    }
}

// check(p, age, expected) is true when the pricing gives the expected price for that age.
boolean check(Pricing p, int age, int expected) {
    return p.price(age) == expected;
}

boolean allPass(Pricing p) {
    return check(p, 4, 0)
            && check(p, 5, 500)
            && check(p, 17, 500)
            && check(p, 18, 1000)
            && check(p, 64, 1000)
            && check(p, 90, 700);
}

String run(String which) {
    Pricing p = switch (which) {
        case "mutant1" -> new AgeMutant1();
        case "mutant2" -> new AgeMutant2();
        case "mutant3" -> new AgeMutant3();
        case "mutant4" -> new AgeMutant4();
        case "mutant5" -> new AgeMutant5();
        default -> new CorrectPricing();
    };
    return allPass(p) ? "pass" : "fail";
}

void main() {
}
