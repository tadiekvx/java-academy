long countWithLock(int threads, int perThread) throws InterruptedException {
    Object lock = new Object();
    long[] counter = {0};
    Thread[] workers = new Thread[threads];
    for (int t = 0; t < threads; t++) {
        workers[t] = new Thread(() -> {
            for (int i = 0; i < perThread; i++) {
                synchronized (new Object()) {
                    counter[0]++;
                }
            }
        });
        workers[t].start();
    }
    for (Thread worker : workers) {
        worker.join();
    }
    return counter[0];
}

void main() {
}
