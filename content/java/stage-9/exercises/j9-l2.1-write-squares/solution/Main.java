List<Integer> parallelSquares(List<Integer> values, int threads) throws Exception {
    try (ExecutorService pool = Executors.newFixedThreadPool(Math.max(1, threads))) {
        List<Future<Integer>> futures = new ArrayList<>();
        for (int value : values) {
            futures.add(pool.submit(() -> value * value));
        }
        List<Integer> squares = new ArrayList<>();
        for (Future<Integer> future : futures) {
            squares.add(future.get());
        }
        return squares;
    }
}

void main() {
}
