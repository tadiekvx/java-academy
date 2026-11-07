// INHERITED CODE: the log analyser. A line looks like:  2026-07-01T23:30:00Z ERROR disk full
// The time is always UTC (the Z). The operations team works in London time.

// Errors per day, as "2026-07-01=2,2026-07-02=1", sorted by day.
String errorsPerDay(List<String> lines) {
    Map<String, Integer> perDay = new TreeMap<>();
    for (String line : lines) {
        String[] parts = line.split(" ", 3);
        if (parts[1].equals("ERROR")) {
            String day = parts[0].substring(0, 10);
            perDay.merge(day, 1, Integer::sum);
        }
    }
    return perDay.entrySet().stream()
            .map(e -> e.getKey() + "=" + e.getValue())
            .collect(Collectors.joining(","));
}

// The level that appears most often; on a tie, the alphabetically first.
String commonestLevel(List<String> lines) {
    List<String> levels = new ArrayList<>();
    for (String line : lines) {
        levels.add(line.split(" ", 3)[1]);
    }
    String best = "";
    int bestCount = 0;
    for (String level : levels) {
        int count = Collections.frequency(levels, level);
        if (count > bestCount || (count == bestCount && level.compareTo(best) < 0)) {
            best = level;
            bestCount = count;
        }
    }
    return best;
}

// How many lines are not well formed.
int badLines(List<String> lines) {
    return 0;
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
