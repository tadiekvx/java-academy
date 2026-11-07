String extractVariables(String template, String path) {
    String[] t = template.split("/", -1);
    String[] p = path.split("/", -1);
    if (t.length != p.length) {
        return "no-match";
    }
    List<String> found = new ArrayList<>();
    for (int i = 0; i < t.length; i++) {
        if (t[i].startsWith("{") && t[i].endsWith("}")) {
            found.add(t[i].substring(1, t[i].length() - 1) + "=" + p[i]);
        } else if (!t[i].equals(p[i])) {
            return "no-match";
        }
    }
    return String.join(",", found);
}

void main() {
}
