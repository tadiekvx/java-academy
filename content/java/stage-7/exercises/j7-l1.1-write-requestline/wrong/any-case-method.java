String parseRequestLine(String line) {
    String[] parts = line.split(" ", -1);
    if (parts.length == 3 && !parts[0].isEmpty() && !parts[1].isEmpty() && parts[2].startsWith("HTTP/")) {
        return String.join("|", parts);
    }
    return "invalid";
}

void main() {
}
