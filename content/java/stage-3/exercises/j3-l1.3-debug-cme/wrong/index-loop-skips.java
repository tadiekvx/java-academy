List<Integer> removeNegatives(List<Integer> values) {
    List<Integer> copy = new ArrayList<>(values);
    for (int i = 0; i < copy.size(); i++) {
        if (copy.get(i) < 0) {
            copy.remove(i);
        }
    }
    return copy;
}

void main() {
}
