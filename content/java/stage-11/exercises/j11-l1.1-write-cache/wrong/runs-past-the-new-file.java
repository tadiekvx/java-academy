int cachedLayers(List<String> before, List<String> after) {
    int cached = 0;
    while (cached < before.size() && before.get(cached).equals(after.get(cached))) {
        cached++;
    }
    return cached;
}

void main() {
}
