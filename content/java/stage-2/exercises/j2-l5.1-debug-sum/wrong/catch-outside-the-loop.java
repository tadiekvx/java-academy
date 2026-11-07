int sumValid(String[] parts) {
    int sum = 0;
    try {
        for (String p : parts) sum += Integer.parseInt(p.trim());
    } catch (NumberFormatException e) {
    }
    return sum;
}

void main() {
}
