int cachedLayers(List<String> before, List<String> after) {
    int cached = 0;
    while (cached < before.size() && cached < after.size() && before.get(cached).equals(after.get(cached))) {
        cached++;
    }
    return cached == after.size() ? cached : 0;
}

void main() {
}
