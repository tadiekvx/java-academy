List<Integer> kSmallest(int[] values, int k) {
    PriorityQueue<Integer> kept = new PriorityQueue<>(Comparator.naturalOrder());
    for (int v : values) {
        kept.offer(v);
        if (kept.size() > k) {
            kept.poll();
        }
    }
    List<Integer> result = new ArrayList<>(kept);
    Collections.sort(result);
    return result;
}

void main() {
}
