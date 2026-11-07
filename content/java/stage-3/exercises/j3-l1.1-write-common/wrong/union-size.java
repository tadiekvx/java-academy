int commonCount(List<String> a, List<String> b) {
    Set<String> all = new HashSet<>(a);
    all.addAll(b);
    return all.size();
}

void main() {
}
