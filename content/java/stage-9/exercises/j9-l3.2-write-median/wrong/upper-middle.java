long steadyMedian(List<Long> timings, int warmup) {
    if (warmup >= timings.size()) {
        return -1;
    }
    List<Long> rest = new ArrayList<>(timings.subList(warmup, timings.size()));
    Collections.sort(rest);
    int n = rest.size();
    return n % 2 == 1 ? rest.get(n / 2) : rest.get(n / 2);
}

void main() {
}
