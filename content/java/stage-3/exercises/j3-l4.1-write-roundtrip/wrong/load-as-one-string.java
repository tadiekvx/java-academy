void save(Path path, List<String> lines) throws IOException {
    Files.write(path, lines);
}

List<String> load(Path path) throws IOException {
    return List.of(Files.readString(path));
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
