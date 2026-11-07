int sumValid(String[] parts) {
    int sum = 0;
    for (String p : parts) {
        try {
            sum += Integer.parseInt(p.trim());
        } catch (NumberFormatException e) {
            // skip entries that are not numbers
        }
    }
    return sum;
}

void main() {
}
