List<Integer> removeNegatives(List<Integer> values) {
    List<Integer> copy = new ArrayList<>(values);
    for (Integer v : copy) {
        if (v < 0) {
            copy.remove(v);
        }
    }
    return copy;
}

void main() {
}
