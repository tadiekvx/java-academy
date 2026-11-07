int shortest(int n, String[] edges, int from, int to) {
    List<List<int[]>> graph = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        graph.add(new ArrayList<>());
    }
    for (String edge : edges) {
        String[] parts = edge.split("[-:]");
        int a = Integer.parseInt(parts[0]);
        int b = Integer.parseInt(parts[1]);
        int w = Integer.parseInt(parts[2]);
        graph.get(a).add(new int[] {b, w});
        graph.get(b).add(new int[] {a, w});
    }
    int[] cost = new int[n];
    Arrays.fill(cost, Integer.MAX_VALUE);
    cost[from] = 0;
    PriorityQueue<int[]> queue = new PriorityQueue<>(Comparator.comparingInt(entry -> entry[1]));
    queue.offer(new int[] {from, 0});
    while (!queue.isEmpty()) {
        int[] current = queue.poll();
        int node = current[0];
        if (current[1] > cost[node]) {
            continue;
        }
        for (int[] edge : graph.get(node)) {
            int next = edge[0];
            int newCost = cost[node] + edge[1];
            if (newCost < cost[next]) {
                cost[next] = newCost;
                queue.offer(new int[] {next, newCost});
            }
        }
    }
    return cost[to];
}

void main() {
}
