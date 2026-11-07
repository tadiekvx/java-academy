List<String> copyFromTargets(List<String> lines) {
    List<String> names = new ArrayList<>();
    for (String line : lines) {
        String[] words = line.trim().split("\\s+");
        if (words.length > 1 && words[0].equalsIgnoreCase("COPY")) {
            names.add(words[1]);
        }
    }
    return names;
}

String finalBaseImage(List<String> lines) {
    String base = "";
    for (String line : lines) {
        String[] words = line.trim().split("\\s+");
        if (words.length > 1 && words[0].equalsIgnoreCase("FROM")) {
            base = words[1];
        }
    }
    return base;
}

void main() {
}
