int shortest(int n, String[] edges, int from, int to) {
    List<List<Integer>> graph = new ArrayList<>();
    int[][] w = new int[n][n];
    for (int i = 0; i < n; i++) graph.add(new ArrayList<>());
    for (String edge : edges) {
        String[] p = edge.split("[-:]");
        int a = Integer.parseInt(p[0]), b = Integer.parseInt(p[1]), c = Integer.parseInt(p[2]);
        graph.get(a).add(b);
        graph.get(b).add(a);
        w[a][b] = c;
        w[b][a] = c;
    }
    int[] hops = new int[n];
    Arrays.fill(hops, -1);
    int[] total = new int[n];
    Deque<Integer> queue = new ArrayDeque<>();
    hops[from] = 0;
    queue.offer(from);
    while (!queue.isEmpty()) {
        int node = queue.poll();
        for (int next : graph.get(node)) {
            if (hops[next] == -1) {
                hops[next] = hops[node] + 1;
                total[next] = total[node] + w[node][next];
                queue.offer(next);
            }
        }
    }
    return hops[to] == -1 ? -1 : total[to];
}

void main() {
}
