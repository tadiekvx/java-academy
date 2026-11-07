List<String> adrMissing(String markdown) {
    List<String> lines = new ArrayList<>();
    for (String line : markdown.split("\n", -1)) {
        lines.add(line.strip());
    }
    List<String> missing = new ArrayList<>();
    boolean title = false;
    for (String line : lines) {
        if (line.startsWith("# ")) {
            title = true;
        }
    }
    if (!title) {
        missing.add("Title");
    }
    for (String section : List.of("Status", "Context", "Decision", "Consequences")) {
        if (!lines.contains("## " + section)) {
            missing.add(section);
        }
    }
    return missing;
}

void main() {
}
