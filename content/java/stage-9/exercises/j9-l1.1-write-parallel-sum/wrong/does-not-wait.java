long parallelSum(int[] data, int threads) throws InterruptedException {
    int parts = Math.max(1, threads);
    long[] partial = new long[parts];
    Thread[] workers = new Thread[parts];
    int chunk = (data.length + parts - 1) / parts;
    for (int w = 0; w < parts; w++) {
        final int id = w;
        workers[w] = new Thread(() -> {
            long sum = 0;
            for (int i = id * chunk; i < Math.min(data.length, (id + 1) * chunk); i++) {
                sum += data[i];
            }
            partial[id] = sum;
        });
        workers[w].start();
    }
    long total = 0;
    for (int w = 0; w < parts; w++) {
        total += partial[w];
    }
    return total;
}

void main() {
}
