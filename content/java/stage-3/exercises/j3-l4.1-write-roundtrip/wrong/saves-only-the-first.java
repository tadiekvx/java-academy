void save(Path path, List<String> lines) throws IOException {
    if (!lines.isEmpty()) Files.writeString(path, lines.get(0) + "\n");
}

List<String> load(Path path) throws IOException {
    return Files.readAllLines(path);
}

String roundTrip(List<String> lines) throws IOException {
    Path p = Files.createTempFile("academy", ".txt");
    try {
        save(p, lines);
        return String.join("|", load(p));
    } finally {
        Files.deleteIfExists(p);
    }
}

void main() {
}
