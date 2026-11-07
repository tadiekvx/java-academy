int readPort(String text) {
    return Integer.parseInt(text);
}

String describePort(String text) {
    try {
        return "port " + readPort(text);
    } catch (ConfigException e) {
        return e.getMessage() + " <- " + e.getCause().getClass().getSimpleName();
    }
}

void main() {
}
