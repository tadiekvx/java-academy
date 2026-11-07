boolean lockedOut(List<String> events, int maxFailures, int windowSeconds, int now) {
    int start = 0;
    for (int i = 0; i < events.size(); i++) {
        String[] e = events.get(i).split(":");
        if (e[1].equals("ok") && Integer.parseInt(e[0]) <= now) {
            start = i + 1;
        }
    }
    int failures = 0;
    for (int i = start; i < events.size(); i++) {
        String[] e = events.get(i).split(":");
        int t = Integer.parseInt(e[0]);
        if (e[1].equals("fail") && t > now - windowSeconds && t <= now) {
            failures++;
        }
    }
    return failures >= maxFailures;
}

void main() {
}
