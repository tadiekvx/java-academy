long sleepersFinished(int count) throws Exception {
    LongAdder done = new LongAdder();
    try (ExecutorService executor = Executors.newFixedThreadPool(10)) {
        for (int i = 0; i < count; i++) {
            executor.submit(() -> {
                Thread.sleep(20);
                done.increment();
                return null;
            });
        }
    }
    return done.sum();
}

void main() {
}
