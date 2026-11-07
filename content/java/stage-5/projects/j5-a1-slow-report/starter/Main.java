// INHERITED slow report. It is correct. The ticket says it must run in under 2 seconds on a month's data.
// Find where the time goes, and fix it without changing any answer.

// INHERITED CODE: it gives the right answers, and it is far too slow on a real month's data.

// Most common category; if two tie, the alphabetically first.
String topCategory(List<String> categories) {
    String best = "";
    int bestCount = 0;
    for (String category : categories) {
        int count = Collections.frequency(categories, category);
        if (count > bestCount || (count == bestCount && category.compareTo(best) < 0)) {
            best = category;
            bestCount = count;
        }
    }
    return best;
}

// The distinct values, smallest first.
List<Integer> sortedUnique(List<Integer> values) {
    List<Integer> result = new ArrayList<>();
    for (Integer value : values) {
        if (result.contains(value)) {
            continue;
        }
        int position = 0;
        while (position < result.size() && result.get(position) < value) {
            position++;
        }
        result.add(position, value);
    }
    return result;
}

// The ids joined with commas.
String joinIds(List<Integer> ids) {
    String text = "";
    for (int i = 0; i < ids.size(); i++) {
        if (i > 0) {
            text += ",";
        }
        text += ids.get(i);
    }
    return text;
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
