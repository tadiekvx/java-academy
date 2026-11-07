void main() throws Exception {
    int[] partial = new int[3];
    Thread[] workers = new Thread[3];
    for (int w = 0; w < 3; w++) {
        final int id = w;
        workers[w] = new Thread(() -> {
            int last = id == 2 ? 100 : (id + 1) * 33;
            int sum = 0;
            for (int n = id * 33 + 1; n <= last; n++) {
                sum += n;
            }
            partial[id] = sum;
        });
        workers[w].start();
    }
    for (Thread worker : workers) {
        worker.join();
    }
    System.out.println("partials=" + Arrays.toString(partial));
    System.out.println("total=" + (partial[0] + partial[1] + partial[2]));
}
