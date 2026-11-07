String wordCounts(List<String> words, int threads) throws InterruptedException {
    ConcurrentHashMap<String, Integer> counts = new ConcurrentHashMap<>();
    int parts = Math.max(1, threads);
    Thread[] workers = new Thread[parts];
    for (int w = 0; w < parts; w++) {
        final int id = w;
        workers[w] = new Thread(() -> {
            for (int i = id; i < words.size(); i += parts + parts) {
                counts.merge(words.get(i), 1, Integer::sum);
            }
        });
        workers[w].start();
    }
    for (Thread worker : workers) {
        worker.join();
    }
    List<String> parts2 = new ArrayList<>();
    for (String word : new TreeSet<>(counts.keySet())) {
        parts2.add(word + "=" + counts.get(word));
    }
    return String.join(",", parts2);
}

void main() {
}
