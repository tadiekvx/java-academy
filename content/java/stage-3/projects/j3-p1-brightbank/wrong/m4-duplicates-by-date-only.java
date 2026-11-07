class Money {
    static String format(int pence) {
        String sign = pence < 0 ? "-" : "";
        int absolute = Math.abs(pence);
        String padding = absolute % 100 < 10 ? "0" : "";
        return sign + "£" + absolute / 100 + "." + padding + absolute % 100;
    }
}

record Transaction(LocalDate date, String description, int pence) {}

record Parsed(List<Transaction> good, int bad, int duplicates) {}

// One line is "date,description,amount". Returns null for a line that isn't valid.
Transaction parseLine(String raw) {
    String[] parts = raw.split(",", -1);
    if (parts.length != 3) {
        return null;
    }
    String description = parts[1].strip();
    String amountText = parts[2].strip();
    if (description.isEmpty() || !amountText.matches("[+-]?[0-9]+(\\.[0-9]{1,2})?")) {
        return null;
    }
    LocalDate date;
    try {
        date = LocalDate.parse(parts[0].strip());
    } catch (DateTimeParseException e) {
        return null;
    }
    int pence = new BigDecimal(amountText).movePointRight(2).intValueExact();
    return new Transaction(date, description, pence);
}

Parsed parseAll(List<String> lines) {
    Set<Transaction> unique = new LinkedHashSet<>();
    Set<LocalDate> seenDates = new HashSet<>();
    int bad = 0;
    int duplicates = 0;
    for (String raw : lines) {
        String line = raw.strip();
        if (line.isEmpty() || line.equalsIgnoreCase("date,description,amount")) {
            continue;
        }
        Transaction t = parseLine(raw);
        if (t == null) {
            bad++;
        } else if (!seenDates.add(t.date())) {
            duplicates++;
        } else {
            unique.add(t);
        }
    }
    return new Parsed(new ArrayList<>(unique), bad, duplicates);
}

String summary(List<String> lines) {
    Parsed p = parseAll(lines);
    return "ok=" + p.good().size() + " bad=" + p.bad();
}

String monthlyTotals(List<String> lines) {
    Map<String, Integer> totals = new TreeMap<>();
    for (Transaction t : parseAll(lines).good()) {
        String month = String.format("%d-%02d", t.date().getYear(), t.date().getMonthValue());
        totals.merge(month, t.pence(), Integer::sum);
    }
    if (totals.isEmpty()) {
        return "none";
    }
    return totals.entrySet().stream()
            .map(e -> e.getKey() + "=" + String.format("%+d", e.getValue()))
            .collect(Collectors.joining(","));
}

String statement(List<String> lines, String from, String to) {
    LocalDate start = LocalDate.parse(from);
    LocalDate end = LocalDate.parse(to);
    List<Transaction> inside = new ArrayList<>(parseAll(lines).good().stream()
            .filter(t -> !t.date().isBefore(start) && !t.date().isAfter(end))
            .toList());
    inside.sort(Comparator.comparing(Transaction::date).reversed());
    StringBuilder text = new StringBuilder();
    int total = 0;
    for (Transaction t : inside) {
        text.append(t.date()).append(" ").append(t.description()).append(" ").append(Money.format(t.pence())).append("\n");
        total += t.pence();
    }
    return text + "Total: " + Money.format(total);
}

String uniqueSummary(List<String> lines) {
    Parsed p = parseAll(lines);
    return "ok=" + p.good().size() + " bad=" + p.bad() + " dupes=" + p.duplicates();
}

void main() {
    // Optional: try your methods out here.
}
