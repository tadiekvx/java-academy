Predicate<String> ruleFor(String rule) {
    return switch (rule) {
        case "long" -> s -> s.length() >= 5;
        case "short" -> s -> s.length() <= 3;
        case "capital" -> s -> !s.isEmpty() && Character.isUpperCase(s.charAt(0));
        default -> s -> !s.isEmpty();
    };
}

List<String> filterBy(List<String> items, String rule) {
    Predicate<String> p = ruleFor(rule);
    List<String> out = new ArrayList<>();
    for (String s : items) {
        if (p.test(s)) {
            out.add(s);
        }
    }
    return out;
}

void main() {
}
