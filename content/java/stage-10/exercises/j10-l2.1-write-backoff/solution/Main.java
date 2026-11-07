List<Long> backoffDelays(int attempts, long baseMs, long capMs) {
    List<Long> delays = new ArrayList<>();
    long delay = Math.min(capMs, baseMs);
    for (int i = 0; i < attempts; i++) {
        delays.add(delay);
        delay = Math.min(capMs, delay * 2);
    }
    return delays;
}

void main() {
}
