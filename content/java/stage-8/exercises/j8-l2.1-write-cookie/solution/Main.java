String describeCookie(String header) {
    String[] parts = header.split("; ");
    String name = parts[0].split("=", 2)[0];
    boolean httpOnly = false;
    boolean secure = false;
    for (int i = 1; i < parts.length; i++) {
        String attribute = parts[i].split("=", 2)[0].toLowerCase();
        if (attribute.equals("httponly")) {
            httpOnly = true;
        }
        if (attribute.equals("secure")) {
            secure = true;
        }
    }
    return "name=" + name + " httpOnly=" + httpOnly + " secure=" + secure;
}

void main() {
}
