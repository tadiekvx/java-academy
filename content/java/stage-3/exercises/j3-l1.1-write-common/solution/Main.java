int commonCount(List<String> a, List<String> b) {
    Set<String> common = new HashSet<>(a);
    common.retainAll(new HashSet<>(b));
    return common.size();
}

void main() {
}
