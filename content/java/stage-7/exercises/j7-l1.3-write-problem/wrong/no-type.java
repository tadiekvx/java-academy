String problemJson(int status, String title, String detail) {
    return "{\"title\":\"" + escape(title) + "\",\"status\":" + status
            + ",\"detail\":\"" + escape(detail) + "\"}";
}

String escape(String text) {
    return text.replace("\\", "\\\\").replace("\"", "\\\"");
}

void main() {
}
