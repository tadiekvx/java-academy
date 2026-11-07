List<Long> backoffDelays(int attempts, long baseMs, long capMs) {
    List<Long> delays = new ArrayList<>();
    for (int i = 0; i < attempts; i++) {
        delays.add(Math.min(capMs, baseMs * (1 << i)));
    }
    return delays;
}

void main() {
}
