List<String> copyFromTargets(List<String> lines) {
    List<String> names = new ArrayList<>();
    for (String line : lines) {
        String[] words = line.trim().split("\\s+");
        if (words.length > 1 && words[0].equals("COPY") && words[1].startsWith("--from=")) {
            names.add(words[1].substring("--from=".length()));
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
