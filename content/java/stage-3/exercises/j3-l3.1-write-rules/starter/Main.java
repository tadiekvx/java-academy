Predicate<String> ruleFor(String rule) {
    return s -> true;
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
