String parseRequestLine(String line) {
    String[] parts = line.trim().split("\\s+");
    if (parts.length == 3 && parts[0].matches("[A-Z]+") && !parts[1].isEmpty() && parts[2].startsWith("HTTP/")) {
        return String.join("|", parts);
    }
    return "invalid";
}

void main() {
}
