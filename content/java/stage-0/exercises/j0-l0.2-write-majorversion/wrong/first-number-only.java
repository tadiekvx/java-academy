int majorVersion(String line) {
    int start = line.indexOf('"') + 1;
    int end = line.indexOf('"', start);
    String version = line.substring(start, end);
    int digits = 0;
    while (digits < version.length() && Character.isDigit(version.charAt(digits))) {
        digits++;
    }
    return Integer.parseInt(version.substring(0, digits));
}

void main() {
}
