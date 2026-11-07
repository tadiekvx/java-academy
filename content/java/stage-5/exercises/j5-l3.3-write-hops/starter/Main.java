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
    return -1;
}

void main() {
}
