boolean hasDuplicate(List<Integer> values) {
    List<Integer> seen = new ArrayList<>();
    for (Integer v : values) {
        if (seen.contains(v)) {
            return true;
        }
        seen.add(v);
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
