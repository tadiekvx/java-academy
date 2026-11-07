String htmlEscape(String text) {
    StringBuilder out = new StringBuilder();
    for (char c : text.toCharArray()) {
        switch (c) {
            case '&' -> out.append("&amp;");
            case '<' -> out.append("&lt;");
            case '>' -> out.append("&gt;");
            case '"' -> out.append("&quot;");
            case '\'' -> out.append("&#x27;");
            default -> out.append(c);
        }
    }
    return out.toString();
}

void main() {
}
