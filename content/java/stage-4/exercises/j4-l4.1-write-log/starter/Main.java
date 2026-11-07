class SimpleLog {
    SimpleLog(String threshold) {
    }

    String log(String level, String message) {
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
