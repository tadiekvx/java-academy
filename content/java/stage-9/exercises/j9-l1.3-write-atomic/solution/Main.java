long countWithAtomic(int threads, int perThread) throws InterruptedException {
    AtomicLong counter = new AtomicLong();
    Thread[] workers = new Thread[threads];
    for (int t = 0; t < threads; t++) {
        workers[t] = new Thread(() -> {
            for (int i = 0; i < perThread; i++) {
                counter.incrementAndGet();
            }
        });
        workers[t].start();
    }
    for (Thread worker : workers) {
        worker.join();
    }
    return counter.get();
}

void main() {
}
