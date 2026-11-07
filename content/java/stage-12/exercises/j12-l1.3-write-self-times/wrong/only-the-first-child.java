List<String> selfTimes(List<String> spans) {
    Map<String, Integer> duration = new LinkedHashMap<>();
    Map<String, Integer> childTotal = new HashMap<>();
    for (String span : spans) {
        String[] p = span.split(":");
        int length = Integer.parseInt(p[3]) - Integer.parseInt(p[2]);
        duration.put(p[0], length);
        childTotal.putIfAbsent(p[1], length);
    }
    List<String> out = new ArrayList<>();
    for (Map.Entry<String, Integer> entry : duration.entrySet()) {
        out.add(entry.getKey() + "=" + (entry.getValue() - childTotal.getOrDefault(entry.getKey(), 0)));
    }
    return out;
}

void main() {
}
