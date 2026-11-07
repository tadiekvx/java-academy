int sumValid(String[] parts) {
    int sum = 0;
    try {
        for (String p : parts) {
            sum += Integer.parseInt(p.trim());
        }
    } catch (Exception e) {
        return 0;
    }
    return sum;
}

void main() {
}
