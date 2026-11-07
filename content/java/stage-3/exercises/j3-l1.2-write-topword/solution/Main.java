String topWord(String text) {
    Map<String, Integer> counts = new TreeMap<>();
    for (String w : text.toLowerCase().strip().split("\\s+")) {
        if (!w.isEmpty()) {
            counts.merge(w, 1, Integer::sum);
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

void main() {
}
