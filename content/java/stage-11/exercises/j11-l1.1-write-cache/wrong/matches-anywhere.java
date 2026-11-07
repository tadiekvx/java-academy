int cachedLayers(List<String> before, List<String> after) {
    int cached = 0;
    for (String line : after) {
        if (before.contains(line)) {
            cached++;
        }
    }
    return cached;
}

void main() {
}
