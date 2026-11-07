class SimpleLog {
    private final int threshold;

    SimpleLog(String threshold) {
        this.threshold = rank(threshold);
    }

    private static int rank(String level) {
        return switch (level) {
            case "DEBUG" -> 0;
            case "INFO" -> 1;
            case "WARN" -> 2;
            case "ERROR" -> 3;
            default -> throw new IllegalArgumentException("unknown level: " + level);
        };
    }

    String log(String level, String message) {
        if (rank(level) > threshold) {
            return "[" + level + "] " + message;
        }
        return "";
    }
}

String run(String threshold, String[] entries) {
    try {
        SimpleLog log = new SimpleLog(threshold);
        List<String> lines = new ArrayList<>();
        for (String entry : entries) {
            String[] parts = entry.split(":", 2);
            String line = log.log(parts[0], parts[1]);
            if (!line.isEmpty()) {
                lines.add(line);
            }
        }
        return String.join("|", lines);
    } catch (IllegalArgumentException e) {
        return "unknown level";
    }
}

void main() {
}
