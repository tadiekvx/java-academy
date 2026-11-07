String summarise(List<String> lines) {
    Map<String, Integer> totals = new TreeMap<>();
    int bad = 0;
    for (String raw : lines) {
        String line = raw.strip();
        if (line.isEmpty() || line.equalsIgnoreCase("category,amount")) {
            continue;
        }
        String[] parts = line.split(",", -1);
        if (parts.length != 2) {
            bad++;
            continue;
        }
        String category = parts[0].strip();
        String amount = parts[1].strip();
        if (category.isEmpty() || !amount.matches("-?[0-9]+")) {
            bad++;
            continue;
        }
        totals.merge(category, Integer.parseInt(amount), Integer::sum);
    }
    StringBuilder out = new StringBuilder();
    for (Map.Entry<String, Integer> e : totals.entrySet()) {
        if (!out.isEmpty()) out.append(",");
        out.append(e.getKey()).append("=").append(e.getValue());
    }
    return (out.isEmpty() ? "none" : out) + " | bad=" + bad;
}

void main() {
}
