List<Integer> kSmallest(int[] values, int k) {
    PriorityQueue<Integer> kept = new PriorityQueue<>(Comparator.reverseOrder());
    for (int v : values) {
        kept.offer(v);
        if (kept.size() > k) {
            kept.poll();
        }
    }
    List<Integer> result = new ArrayList<>(kept);
    return result;
}

void main() {
}
