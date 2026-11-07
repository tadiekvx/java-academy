String safePath(String base, String userPath) {
    java.nio.file.Path root = java.nio.file.Path.of(base).normalize();
    java.nio.file.Path resolved = root.resolve(userPath).normalize();
    return resolved.startsWith(root) ? resolved.toString() : "rejected";
}

void main() {
}
