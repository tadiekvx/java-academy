String safePath(String base, String userPath) {
    if (userPath.startsWith("/")) {
        return "rejected";
    }
    java.nio.file.Path root = java.nio.file.Path.of(base).normalize();
    java.nio.file.Path resolved = root.resolve(userPath);
    return resolved.startsWith(root) ? resolved.toString() : "rejected";
}

void main() {
}
