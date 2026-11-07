boolean iamAllows(List<String> statements, String action, String resource) {
    boolean allowed = false;
    for (String statement : statements) {
        String[] p = statement.split("\\|");
        if (matches(p[1], action) && matches(p[2], resource)) {
            allowed = true;
        }
    }
    return allowed;
}

boolean matches(String pattern, String text) {
    StringBuilder regex = new StringBuilder();
    for (String part : pattern.split("\\*", -1)) {
        if (regex.length() > 0) {
            regex.append(".*");
        }
        regex.append(java.util.regex.Pattern.quote(part));
    }
    if (pattern.startsWith("*") && regex.length() == 0) {
        return true;
    }
    return java.util.regex.Pattern.compile(regex.toString(), java.util.regex.Pattern.DOTALL).matcher(text).matches();
}

void main() {
}
