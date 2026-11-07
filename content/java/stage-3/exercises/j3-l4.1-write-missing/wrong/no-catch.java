String firstLineOr(Path path, String fallback) throws IOException {
    List<String> lines = Files.readAllLines(path);
    return lines.isEmpty() ? fallback : lines.get(0);
}

String readFirst(String content, boolean fileExists, String fallback) throws IOException {
    Path p = Files.createTempFile("academy", ".txt");
    Files.deleteIfExists(p);
    try {
        if (fileExists) {
            Files.writeString(p, content);
        }
        return firstLineOr(p, fallback);
    } finally {
        Files.deleteIfExists(p);
    }
}

void main() {
}
