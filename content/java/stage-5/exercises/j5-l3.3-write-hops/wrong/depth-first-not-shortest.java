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
    boolean[] seen = new boolean[n];
    int[] best = {-1};
    walk(graph, from, to, 0, seen, best);
    return best[0];
}

void walk(List<List<Integer>> graph, int node, int to, int depth, boolean[] seen, int[] best) {
    seen[node] = true;
    if (node == to) {
        best[0] = depth;
        return;
    }
    for (int next : graph.get(node)) {
        if (!seen[next] && best[0] == -1) {
            walk(graph, next, to, depth + 1, seen, best);
        }
    }
}

void main() {
}
