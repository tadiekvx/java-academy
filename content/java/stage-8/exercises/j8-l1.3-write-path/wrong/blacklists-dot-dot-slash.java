String safePath(String base, String userPath) {
    return userPath.contains("../") ? "rejected" : java.nio.file.Path.of(base).resolve(userPath).normalize().toString();
}

void main() {
}
