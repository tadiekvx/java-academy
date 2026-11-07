String counts(String text) {
    Map<String, Integer> counts = new TreeMap<>();
    for (String w : text.strip().split("\\s+")) {
        if (!w.isEmpty()) {
            counts.merge(w, 1, Integer::sum);
        }
    }
    StringBuilder out = new StringBuilder();
    for (Map.Entry<String, Integer> e : counts.entrySet()) {
        if (!out.isEmpty()) out.append(",");
        out.append(e.getKey()).append("=").append(e.getValue());
    }
    return out.toString();
}

void main() {
}
