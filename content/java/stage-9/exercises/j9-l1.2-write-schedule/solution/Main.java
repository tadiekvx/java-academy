int finalValue(List<String> schedule) {
    int counter = 0;
    Map<String, Integer> seen = new HashMap<>();
    for (String step : schedule) {
        String[] parts = step.split(":");
        if (parts[1].equals("read")) {
            seen.put(parts[0], counter);
        } else {
            counter = seen.getOrDefault(parts[0], 0) + 1;
        }
    }
    return counter;
}

void main() {
}
