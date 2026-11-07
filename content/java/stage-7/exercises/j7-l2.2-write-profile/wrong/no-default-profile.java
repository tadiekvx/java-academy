String isActive(String expression, List<String> active) {
    Set<String> profiles = new HashSet<>(active);
    boolean and = expression.contains(" & ");
    boolean or = expression.contains(" | ");
    if (and && or) {
        return "invalid";
    }
    boolean result = and || !or;
    for (String term : expression.split(" & | \\| ")) {
        boolean matches = term.startsWith("!") ? !profiles.contains(term.substring(1)) : profiles.contains(term);
        result = or ? result || matches : result && matches;
    }
    return result ? "true" : "false";
}

void main() {
}
