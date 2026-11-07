List<List<Integer>> buildGraph(int n, String[] edges) {
    List<List<Integer>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        graph.add(new ArrayList<>());
    }
    for (String edge : edges) {
        String[] parts = edge.split("-");
        int a = Integer.parseInt(parts[0]);
        int b = Integer.parseInt(parts[1]);
        graph.get(a).add(b);
        graph.get(b).add(a);
    }
    return graph;
}

void main() {
    String[] edges = {"0-1", "0-2", "1-3", "2-3", "2-4", "3-5", "4-5"};
    List<List<Integer>> graph = buildGraph(6, edges);
    boolean[] seen = new boolean[6];
    Deque<Integer> queue = new ArrayDeque<>();
    List<Integer> order = new ArrayList<>();
    seen[0] = true;
    queue.offer(0);
    while (!queue.isEmpty()) {
        int node = queue.poll();
        order.add(node);
        for (int next : graph.get(node)) {
            if (!seen[next]) {
                seen[next] = true;
                queue.offer(next);
            }
        }
    }
    IO.println(order);
    IO.println(graph.get(3));
}
