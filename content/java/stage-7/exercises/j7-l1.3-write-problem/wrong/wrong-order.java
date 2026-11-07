String problemJson(int status, String title, String detail) {
    return "{\"type\":\"about:blank\",\"status\":" + status + ",\"title\":\"" + escape(title)
            + "\",\"detail\":\"" + escape(detail) + "\"}";
}

String escape(String text) {
    return text.replace("\\", "\\\\").replace("\"", "\\\"");
}

void main() {
}
