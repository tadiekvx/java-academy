class ConfigException extends RuntimeException {
    ConfigException(String message, Throwable cause) {
        super(message, cause);
    }
}

int readPort(String text) {
    try {
        return Integer.parseInt(text);
    } catch (NumberFormatException e) {
        throw new ConfigException("bad port", e);
    }
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
