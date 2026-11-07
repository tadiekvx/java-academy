String substitute(String template, List<String> env) {
    Map<String, String> values = new HashMap<>();
    for (String entry : env) {
        int equals = entry.indexOf('=');
        values.put(entry.substring(0, equals), entry.substring(equals + 1));
    }
    java.util.regex.Matcher matcher = java.util.regex.Pattern.compile("\\$\\$|\\$\\{([_a-zA-Z][_a-zA-Z0-9]*)(?:(:-|-)([^}]*))?\\}").matcher(template);
    StringBuilder out = new StringBuilder();
    while (matcher.find()) {
        String replacement;
        if (matcher.group().equals("$$")) {
            replacement = "$$";
        } else {
            String value = values.get(matcher.group(1));
            String operator = matcher.group(2);
            String fallback = matcher.group(3);
            if (":-".equals(operator)) {
                replacement = value == null || value.isEmpty() ? fallback : value;
            } else if ("-".equals(operator)) {
                replacement = value == null ? fallback : value;
            } else {
                replacement = value == null ? "" : value;
            }
        }
        matcher.appendReplacement(out, java.util.regex.Matcher.quoteReplacement(replacement));
    }
    matcher.appendTail(out);
    return out.toString();
}

void main() {
}
