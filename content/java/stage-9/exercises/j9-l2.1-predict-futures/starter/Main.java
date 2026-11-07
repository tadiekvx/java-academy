void main() {
    CompletableFuture<Integer> a = CompletableFuture.supplyAsync(() -> 20);
    CompletableFuture<Integer> b = CompletableFuture.supplyAsync(() -> 22);
    int total = a.thenCombine(b, Integer::sum).thenApply(x -> x * 2).join();
    System.out.println("total=" + total);
    String outcome = CompletableFuture.<String>supplyAsync(() -> {
        throw new IllegalStateException("boom");
    }).exceptionally(e -> "recovered:" + e.getClass().getSimpleName()).join();
    System.out.println(outcome);
    System.out.println("done=" + a.isDone() + "," + b.isDone());
}
