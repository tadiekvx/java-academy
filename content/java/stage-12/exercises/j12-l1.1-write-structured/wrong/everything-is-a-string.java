String structuredLog(String level, String message, List<String> fields) {
    StringBuilder out = new StringBuilder("{\"level\":" + quote(level) + ",\"message\":" + quote(message));
    for (String field : fields) {
        int equals = field.indexOf('=');
        String key = field.substring(0, equals);
        String value = field.substring(equals + 1);
        out.append(",").append(quote(key)).append(":").append(quote(value));
    }
    return out.append("}").toString();
}

String quote(String text) {
    return "\"" + text.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
}

void main() {
}
