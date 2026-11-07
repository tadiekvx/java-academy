List<String> rolloutTrace(int replicas, int batch, List<String> health) {
    if (replicas < 1 || batch < 1) {
        return List.of("invalid");
    }
    List<String> trace = new ArrayList<>();
    int batches = (replicas + batch - 1) / batch;
    for (int b = 0; b < batches; b++) {
        int low = b * batch + 1;
        int high = Math.min(replicas, (b + 1) * batch);
        trace.add("update:" + low + "-" + high);
        if (b < health.size() && health.get(b).equals("bad")) {
            trace.add("rollback:1-" + high);
        }
        trace.add("healthy:" + low + "-" + high);
    }
    trace.add("done");
    return trace;
}

void main() {
}
