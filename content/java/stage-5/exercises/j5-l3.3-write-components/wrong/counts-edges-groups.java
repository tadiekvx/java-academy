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

void dfs(List<List<Integer>> graph, int node, boolean[] visited) {
    visited[node] = true;
    for (int next : graph.get(node)) {
        if (!visited[next]) {
            dfs(graph, next, visited);
        }
    }
}

int components(int n, String[] edges) {
    List<List<Integer>> graph = buildGraph(n, edges);
    boolean[] visited = new boolean[n];
    int count = 0;
    for (int node = 0; node < n; node++) {
        if (!visited[node]) {
            dfs(graph, node, visited);
            count += 2;
        }
    }
    return count;
}

void main() {
}
