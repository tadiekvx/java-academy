String problemJson(int status, String title, String detail) {
    return "{\"type\":\"about:blank\",\"title\":\"" + title + "\",\"status\":" + status
            + ",\"detail\":\"" + detail + "\"}";
}

String escape(String text) {
    return text.replace("\\", "\\\\").replace("\"", "\\\"");
}

void main() {
}
