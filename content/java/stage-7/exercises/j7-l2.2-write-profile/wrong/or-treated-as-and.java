String isActive(String expression, List<String> active) {
    Set<String> profiles = active.isEmpty() ? Set.of("default") : new HashSet<>(active);
    boolean and = expression.contains(" & ");
    boolean or = expression.contains(" | ");
    if (and && or) {
        return "invalid";
    }
    boolean result = true;
    for (String term : expression.split(" & | \\| ")) {
        boolean matches = term.startsWith("!") ? !profiles.contains(term.substring(1)) : profiles.contains(term);
        result = result && matches;
    }
    return result ? "true" : "false";
}

void main() {
}
