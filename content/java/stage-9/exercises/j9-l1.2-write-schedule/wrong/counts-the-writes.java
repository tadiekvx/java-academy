int finalValue(List<String> schedule) {
    int writes = 0;
    for (String step : schedule) {
        if (step.endsWith(":write")) {
            writes++;
        }
    }
    return writes;
}

void main() {
}
