int total(String[] items) {
    int sum = 0;
    for (String item : items) {
        sum += Integer.parseInt(item.trim());
    }
    return sum;
}

String report(String[] items) {
    return "total=" + total(items);
}

void main() {
}
