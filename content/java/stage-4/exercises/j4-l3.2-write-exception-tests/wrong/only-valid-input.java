interface Parser {
    int parsePercent(String text);
}

class CorrectParser implements Parser {
    public int parsePercent(String text) {
        if (!text.matches("[0-9]+%")) {
            throw new IllegalArgumentException("not a percentage: " + text);
        }
        int value = Integer.parseInt(text.substring(0, text.length() - 1));
        if (value > 100) {
            throw new IllegalArgumentException("over 100: " + text);
        }
        return value;
    }
}

class ParseMutant1 implements Parser {
    public int parsePercent(String text) {
        if (!text.matches("[0-9]+%")) {
            throw new IllegalArgumentException("not a percentage");
        }
        return Integer.parseInt(text.substring(0, text.length() - 1));
    }
}

class ParseMutant2 implements Parser {
    public int parsePercent(String text) {
        if (!text.matches("[0-9]+%")) {
            throw new IllegalArgumentException("not a percentage");
        }
        int value = Integer.parseInt(text.substring(0, text.length() - 1));
        if (value >= 100) {
            throw new IllegalArgumentException("over 100");
        }
        return value;
    }
}

class ParseMutant3 implements Parser {
    public int parsePercent(String text) {
        String digits = text.endsWith("%") ? text.substring(0, text.length() - 1) : text;
        if (!digits.matches("[0-9]+")) {
            throw new IllegalArgumentException("not a number");
        }
        int value = Integer.parseInt(digits);
        if (value > 100) {
            throw new IllegalArgumentException("over 100");
        }
        return value;
    }
}

class ParseMutant4 implements Parser {
    public int parsePercent(String text) {
        if (!text.matches("[0-9]+%")) {
            throw new IllegalStateException("not a percentage");
        }
        int value = Integer.parseInt(text.substring(0, text.length() - 1));
        if (value > 100) {
            throw new IllegalArgumentException("over 100");
        }
        return value;
    }
}

class ParseMutant5 implements Parser {
    public int parsePercent(String text) {
        if (!text.matches("-?[0-9]+%")) {
            throw new IllegalArgumentException("not a percentage");
        }
        int value = Integer.parseInt(text.substring(0, text.length() - 1));
        if (value > 100) {
            throw new IllegalArgumentException("over 100");
        }
        return value;
    }
}

// throwsIAE(p, text) is true only if parsing the text throws an IllegalArgumentException (and nothing else).
boolean throwsIAE(Parser p, String text) {
    try {
        p.parsePercent(text);
        return false;
    } catch (IllegalArgumentException e) {
        return true;
    } catch (RuntimeException e) {
        return false;
    }
}

// returns(p, text, expected) is true if parsing the text gives the expected value.
boolean returns(Parser p, String text, int expected) {
    try {
        return p.parsePercent(text) == expected;
    } catch (RuntimeException e) {
        return false;
    }
}

boolean allPass(Parser p) {
    return returns(p, "0%", 0)
            && returns(p, "42%", 42)
            && returns(p, "100%", 100);
}

String run(String which) {
    Parser p = switch (which) {
        case "mutant1" -> new ParseMutant1();
        case "mutant2" -> new ParseMutant2();
        case "mutant3" -> new ParseMutant3();
        case "mutant4" -> new ParseMutant4();
        case "mutant5" -> new ParseMutant5();
        default -> new CorrectParser();
    };
    return allPass(p) ? "pass" : "fail";
}

void main() {
}
