boolean hasDuplicate(List<Integer> values) {
    Set<Integer> seen = new HashSet<>();
    for (Integer v : values) {
        if (!seen.add(v)) {
            return true;
        }
    }
    return false;
}

String run(int n, boolean duplicate) {
    List<Integer> values = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        values.add(i);
    }
    if (duplicate && n > 0) {
        values.add(0);
    }
    return String.valueOf(hasDuplicate(values));
}

void main() {
}
