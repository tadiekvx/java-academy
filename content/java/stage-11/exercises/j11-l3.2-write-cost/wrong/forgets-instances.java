long estimateCents(List<String> items, int hoursPerMonth) {
    long total = 0;
    for (String item : items) {
        String[] p = item.split(":");
        total += Long.parseLong(p[1]) * hoursPerMonth;
    }
    return total;
}

void main() {
}
