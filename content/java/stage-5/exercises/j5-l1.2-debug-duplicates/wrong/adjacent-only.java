boolean hasDuplicate(List<Integer> values) {
    for (int i = 0; i + 1 < values.size(); i++) {
        if (values.get(i).equals(values.get(i + 1))) {
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
