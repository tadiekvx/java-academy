int majorVersion(String line) {
    int start = line.indexOf('"') + 1;
    String version = line.substring(start);
    int dot = version.indexOf('.');
    return Integer.parseInt(version.substring(0, dot));
}

void main() {
}
