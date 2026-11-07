boolean hasDuplicate(List<Integer> values) {
    for (int i = 0; i < values.size(); i++) {
        for (int j = i + 1; j < values.size(); j++) {
            if (values.get(i).equals(values.get(j))) {
                return true;
            }
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
