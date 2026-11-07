long sleepersFinished(int count) throws Exception {
    LongAdder done = new LongAdder();
    ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
    {
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
