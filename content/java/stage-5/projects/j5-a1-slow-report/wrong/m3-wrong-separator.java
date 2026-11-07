// The most common category; if two tie, the alphabetically first.
String topCategory(List<String> categories) {
    Map<String, Integer> counts = new TreeMap<>();
    for (String category : categories) {
        counts.merge(category, 1, Integer::sum);
    }
    String best = "";
    int bestCount = 0;
    for (Map.Entry<String, Integer> entry : counts.entrySet()) {
        if (entry.getValue() > bestCount) {
            best = entry.getKey();
            bestCount = entry.getValue();
        }
    }
    return best;
}

// The distinct values, smallest first.
List<Integer> sortedUnique(List<Integer> values) {
    return new ArrayList<>(new TreeSet<>(values));
}

// The ids joined with commas.
String joinIds(List<Integer> ids) {
    StringBuilder text = new StringBuilder();
    for (int i = 0; i < ids.size(); i++) {
        if (i > 0) {
            text.append(", ");
        }
        text.append(ids.get(i));
    }
    return text.toString();
}

// ---------------------------------------------------------------------------------------------
// The report's callers. Don't change them.
// ---------------------------------------------------------------------------------------------

String m1(int n) {
    List<String> categories = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        categories.add(String.format("cat%02d", (int) ((i * 7919L) % 50)));
    }
    return topCategory(categories);
}

String m2(int n) {
    List<Integer> values = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        values.add((int) ((i * 2654435761L) % 100003));
    }
    List<Integer> result = sortedUnique(values);
    return "size=" + result.size() + " first=" + (result.isEmpty() ? 0 : result.get(0)) + " last=" + (result.isEmpty() ? 0 : result.get(result.size() - 1));
}

String m3(int n) {
    List<Integer> ids = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        ids.add(i);
    }
    String joined = joinIds(ids);
    return "length=" + joined.length() + " start=" + joined.substring(0, Math.min(10, joined.length())) + " end=" + (joined.isEmpty() ? "" : joined.substring(Math.max(0, joined.length() - 10)));
}

void main() {
    // Optional: try the report out here.
}
