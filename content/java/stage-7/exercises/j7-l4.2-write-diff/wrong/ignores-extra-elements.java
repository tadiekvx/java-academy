String firstDifference(List<String> expected, List<String> actual) {
    int longest = Math.min(expected.size(), actual.size());
    for (int i = 0; i < longest; i++) {
        String e = i < expected.size() ? expected.get(i) : "<missing>";
        String a = i < actual.size() ? actual.get(i) : "<missing>";
        if (!e.equals(a)) {
            return "index " + i + ": expected " + e + " but was " + a;
        }
    }
    return "same";
}

void main() {
}
