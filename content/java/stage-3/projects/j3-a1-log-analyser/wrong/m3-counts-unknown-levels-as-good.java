// A line is well formed if it has a timestamp (UTC, ending in Z), a known level and a message.
// Returns null for a line that is not.
record Entry(Instant time, String level) {}

Entry parseLine(String line) {
    String[] parts = line.split(" ", 3);
    if (parts.length < 3) {
        return null;
    }
    try {
        return new Entry(Instant.parse(parts[0]), parts[1]);
    } catch (DateTimeParseException e) {
        return null;
    }
}

// Errors per day in London time, as "2026-07-01=2,2026-07-02=1", sorted by day.
String errorsPerDay(List<String> lines) {
    Map<String, Integer> perDay = new TreeMap<>();
    for (String line : lines) {
        Entry entry = parseLine(line);
        if (entry != null && entry.level().equals("ERROR")) {
            String day = entry.time().atZone(ZoneId.of("Europe/London")).toLocalDate().toString();
            perDay.merge(day, 1, Integer::sum);
        }
    }
    return perDay.entrySet().stream()
            .map(e -> e.getKey() + "=" + e.getValue())
            .collect(Collectors.joining(","));
}

// The level that appears most often; on a tie, the alphabetically first.
String commonestLevel(List<String> lines) {
    Map<String, Integer> counts = new TreeMap<>();
    for (String line : lines) {
        Entry entry = parseLine(line);
        if (entry != null) {
            counts.merge(entry.level(), 1, Integer::sum);
        }
    }
    String best = "";
    int bestCount = 0;
    for (Map.Entry<String, Integer> e : counts.entrySet()) {
        if (e.getValue() > bestCount) {
            best = e.getKey();
            bestCount = e.getValue();
        }
    }
    return best;
}

// How many lines are not well formed.
int badLines(List<String> lines) {
    int bad = 0;
    for (String line : lines) {
        if (parseLine(line) == null) {
            bad++;
        }
    }
    return bad;
}

// ---------------------------------------------------------------------------------------------
// The callers. Don't change them.
// ---------------------------------------------------------------------------------------------

String m2(int n) {
    String[] levels = {"INFO", "WARN", "ERROR", "DEBUG"};
    List<String> lines = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        lines.add(String.format("2026-07-01T%02d:%02d:00Z %s event %d", (i * 7) % 24, (i * 13) % 60, levels[(int) (((long) i * i + i / 3) % 4)], i));
    }
    return commonestLevel(lines);
}

void main() {
    // Optional: try the analyser out here.
}
