int majorVersion(String line) {
    int start = line.indexOf('"') + 1;
    int end = line.indexOf('"', start);
    String version = line.substring(start, end);
    if (version.startsWith("1.")) {
        version = version.substring(2);
    }
    int digits = 0;
    while (digits < version.length() && Character.isDigit(version.charAt(digits))) {
        digits++;
    }
    return Integer.parseInt(version.substring(0, digits));
}

void main() {
    IO.println(majorVersion("openjdk version \"25.0.5\" 2026-10-24")); // should print 25
}
