List<Integer> pageOf(List<Integer> items, int page, int size) {
    if (page < 1 || size < 1) {
        return List.of();
    }
    long from = (long) (page - 1) * size;
    if (from >= items.size()) {
        return List.of();
    }
    return items.subList((int) from, (int) Math.min(items.size(), from + size));
}

int totalPages(int total, int size) {
    if (size < 1 || total < 0) {
        return 0;
    }
    return (total + size - 1) / size;
}

void main() {
}
