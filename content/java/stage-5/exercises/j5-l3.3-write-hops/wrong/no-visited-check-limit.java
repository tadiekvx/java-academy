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

int hops(int n, String[] edges, int from, int to) {
    List<List<Integer>> graph = buildGraph(n, edges);
    int[] distance = new int[n];
    Arrays.fill(distance, -1);
    Deque<Integer> queue = new ArrayDeque<>();
    distance[from] = 0;
    queue.offer(from);
    if (from == to) return 1;
    while (!queue.isEmpty()) {
        int node = queue.poll();
        for (int next : graph.get(node)) {
            if (distance[next] == -1 || distance[next] > distance[node] + 1) {
                distance[next] = distance[node] + 1;
                if (next != from) queue.offer(next);
            }
        }
    }
    return distance[to];
}

void main() {
}
