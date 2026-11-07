List<String> layerViolations(List<String> layers, List<String> deps) {
    List<String> bad = new ArrayList<>();
    for (String dep : deps) {
        String[] parts = dep.split(">");
        int from = layers.indexOf(parts[0]);
        int to = layers.indexOf(parts[1]);
        if (from < 0 || to < 0 || to < from) {
            bad.add(dep);
        }
    }
    return bad;
}

void main() {
}
