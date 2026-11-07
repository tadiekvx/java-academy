int finalValue(List<String> schedule) {
    int counter = 0;
    int[] last = {0};
    for (String step : schedule) {
        String[] parts = step.split(":");
        if (parts[1].equals("read")) {
            last[0] = counter;
        } else {
            counter = last[0] + 1;
        }
    }
    return counter;
}

void main() {
}
