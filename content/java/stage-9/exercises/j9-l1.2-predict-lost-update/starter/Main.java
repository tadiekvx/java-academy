void main() throws Exception {
    int[] counter = {0};
    CountDownLatch bothHaveRead = new CountDownLatch(2);
    Runnable increment = () -> {
        int seen = counter[0];
        bothHaveRead.countDown();
        try {
            bothHaveRead.await();
        } catch (InterruptedException e) {
            return;
        }
        counter[0] = seen + 1;
    };
    Thread a = new Thread(increment);
    Thread b = new Thread(increment);
    a.start();
    b.start();
    a.join();
    b.join();
    System.out.println("two increments, counter=" + counter[0]);
}
