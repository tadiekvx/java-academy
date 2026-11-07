long steadyMedian(List<Long> timings, int warmup) {
    if (warmup >= timings.size()) {
        return -1;
    }
    List<Long> rest = new ArrayList<>(timings.subList(warmup, timings.size()));
    Collections.sort(rest);
    int n = rest.size();
    long sum = 0;
    for (long t : rest) {
        sum += t;
    }
    return sum / n;
}

void main() {
}
