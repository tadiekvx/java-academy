long estimateCents(List<String> items, int hoursPerMonth) {
    int total = 0;
    for (String item : items) {
        String[] p = item.split(":");
        total += Long.parseLong(p[1]) * Long.parseLong(p[2]) * hoursPerMonth;
    }
    return total;
}

void main() {
}
